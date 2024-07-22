from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.db import transaction
from tienda.models import Producto, ReporteVentas
from .models import Pedido, LineaPedido
from carro.carro import Carro
from django.views.generic import ListView

class ProcesarPedido(LoginRequiredMixin, View):
    login_url = '/adminApp/login'

    def post(self, request):
        carro = Carro(request)
        pedido = Pedido.objects.create(user=request.user)
        lineas_pedido = []
        total_pedido = 0

        try:
            with transaction.atomic():
                for key, value in carro.carro.items():
                    cantidad = int(value["stock"])
                    precio = float(value["precio"])
                    total_linea = cantidad * precio
                    total_pedido += total_linea

                    try:
                        producto = Producto.objects.get(id=key)
                        if producto.stock < cantidad:
                            messages.error(request, f"No existen suficientes productos en almacen para {producto.nomProduct}")
                            return redirect("inicio")

                        producto.stock -= cantidad
                        producto.ventas_totales += cantidad
                        producto.save()

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
                        transaction.set_rollback(True)
                        return redirect("inicio")

                LineaPedido.objects.bulk_create(lineas_pedido)
                pedido.total_pedido = total_pedido
                pedido.save()

                # Vaciar el carrito después de procesar el pedido
                carro.vaciar_carro()

                # Redirigir al usuario a una página de confirmación o similar
                messages.success(request, "Pedido procesado exitosamente.")
                return redirect("pagina_de_confirmacion")

        except Exception as e:
            messages.error(request, f"Se produjo un error al procesar el pedido: {str(e)}")
            return redirect("home")
        
class TopProductosVendidos(ListView):
    model =Producto
    template_name = 'reportes/topproductos.html'
    context_object_name = 'productos'

    def get_queryset(self):
        return Producto.objects.all().order_by('-ventas_totales')[:10]

