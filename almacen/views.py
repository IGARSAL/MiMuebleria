from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from tienda.models import Producto, ReporteVentas
from .models import Pedido, LineaPedido
from carro.carro import Carro
from tienda.models import CategoriaProd
from django.shortcuts import render

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

