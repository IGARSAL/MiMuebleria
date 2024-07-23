from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from tienda.models import Producto, ReporteVentas
from .models import Pedido, LineaPedido
from carro.carro import Carro
from django.views.generic import ListView
from tienda.models import CategoriaProd
from django.shortcuts import render
from django.http import JsonResponse
from decimal import Decimal, ROUND_HALF_UP 

class ProcesarPedido(LoginRequiredMixin, View):
    login_url = '/adminApp/login'

    def post(self, request, *args, **kwargs):
        carro = Carro(request)
        pedido = Pedido.objects.create(user=request.user)
        lineas_pedido = []
        total_pedido = 0


        for key, value in carro.carro.items():
            print(f"Procesando producto con id {key}")  # Debugging
            print(f"Valor en carrito: {value}")  # Debugging

            cantidad = int(value["stock"])
            precio = float(value["precio"])
            total_linea = cantidad * precio
            total_pedido += total_linea

            try:
                producto = Producto.objects.get(id=key)
                print(f"Producto encontrado: {producto.nomProduct} con stock {producto.stock}")  # Debugging
                if producto.stock < cantidad:
                    messages.error(request, f"No existen suficientes productos en almacen para {producto.nomProduct}")
                    return redirect("home")

                producto.stock -= cantidad
                producto.ventas_totales += cantidad
                producto.save()
                print(f"Producto {producto.nomProduct} actualizado: stock {producto.stock}, ventas_totales {producto.ventas_totales}")  # Debugging

                lineas_pedido.append(LineaPedido(
                    producto=producto,
                    cantidadVendida=cantidad,
                    total_pedido=total_linea,
                    pedido=pedido,
                ))

                ReporteVentas.objects.create(
                    producto=producto,
                    usuario=request.user,
                    cantidad=cantidad,
                    total_venta=total_linea,
                )

            except Producto.DoesNotExist:
                messages.error(request, f"El producto con id {key} no existe.")
                return redirect("home")

        print("Guardando líneas de pedido...")  # Debugging
        if lineas_pedido:
            LineaPedido.objects.bulk_create(lineas_pedido)
            print("Líneas de pedido guardadas.")  # Debugging
        else:
            print("No hay líneas de pedido para guardar.")  # Debugging

        pedido.total_pedido = total_pedido
        pedido.save()
        print(f"Pedido guardado con total: {pedido.total_pedido}")  # Debugging

        # Vaciar el carrito después de procesar el pedido
        carro.vaciar_carro()
        # Redirigir al usuario a una página de confirmación o similar
        messages.success(request, "Pedido procesado exitosamente.")
        return redirect('confirmacion_pedido', pedido_id=pedido.id)
      
       
class CategoriaView(View):
    def get(self, request, categoria_id):
        categoria=CategoriaProd.objects.get(id=categoria_id)
        producto=producto.objects.filter(categorias=categoria)
        return render(request, "almacen/categoria.html", {'categoria': categoria, "producto": producto})

class TopProductosVendidos(View):
    def get_queryset(self, request):
        productos = Producto.objects.all().order_by('-ventas_totales')[:2]
        productos_data = []
        for producto in productos:
            if producto.descuento > 0:
                descuento_decimal = Decimal(producto.descuento) / Decimal(100)
                precio_descuento = (producto.precio * (Decimal(1) - descuento_decimal)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            else:
                precio_descuento = producto.precio
    
        productos_data.append({
        'id': producto.id,
        'nombre': producto.nomProduct,
        'precio': producto.precio,
        'precio_descuento': precio_descuento,
        'descuento': producto.descuento,
        'imagen1': producto.imagen1.url if producto.imagen1 else None,
            })

        return JsonResponse(productos_data, safe=False)