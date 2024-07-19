from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from tienda.models import Producto
from .carro import Carro

class AgregarProductoView(View):
    def post(self, request, producto_id):
        carro = Carro(request)
        producto = get_object_or_404(Producto, id=producto_id)

        cantidad_disponible = producto.stock
        cantidad_en_carro = carro.obtener_cantidad(producto)

        if cantidad_en_carro < cantidad_disponible:
            carro.agregar(producto)
            messages.success(request, f'Producto {producto.nomProduct} agregado al carrio.')
        else:
            messages.error(request, f'Lo sentidos, no hay suficiente cantidad disponible de {producto.nomProduct}.')

        return redirect('tienda')

class EliminarProductoView(View):
    def post(self, request, producto_id):
        carro = Carro(request)
        producto = Producto.objects.get(id=producto_id)
        carro.eliminar(producto)
        return redirect('tienda')

class DisminuirProductoView(View):
    def post(self, request, producto_id):
        carro = Carro(request)
        producto = Producto.objects.get(id=producto_id)
        carro.disminuir_producto(producto)
        return redirect('tienda')

class VaciarCarroView(View):
    def post(self, request):
        carro = Carro(request)
        carro.vaciar_carro()
        return redirect('tienda')
