from django.views import View
from .models import Producto, CategoriaProd 
from almacen.models import Pedido
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .utils import calcular_precio_descuento
from decimal import Decimal, ROUND_HALF_UP

class ProductosJsonView(View):
    def get(self, request):
        productos = Producto.objects.all().order_by('-ventas_totales')[:5]
        
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

class ConfirmacionPedidoView(View):
    def get(self, request, pedido_id):
        pedido = get_object_or_404(Pedido, id=pedido_id, user=request.user)
        lineas_pedido = pedido.lineapedido_set.all()
        total_pedido = sum(linea.total_pedido for linea in lineas_pedido)
        context = {
            'pedido': pedido,
            'lineas_pedido': lineas_pedido,
            'total_pedido': total_pedido,
            
        }
        return render(request, 'confirmacion_pedido.html', context)

# Definimos la clase vista tiendaCategoria
class tiendaCategoria(View):
    def get(self, request, categoria_id=None):
        try:
            # Obtenemos el parámetro de consulta 'q' de la URL
            query = request.GET.get('q', '')
            
            # Obtenemos todas las categorías y productos
            categorias = CategoriaProd.objects.all()
            productos = Producto.objects.all()

            # Filtramos los productos por categoría si se proporciona categoria_id
            if categoria_id:
                categoria = get_object_or_404(CategoriaProd, id=categoria_id)
                productos = productos.filter(categorias=categoria)
            else:
                categoria = None

            # Filtramos los productos por el término de búsqueda si se proporciona una consulta
            if query:
                productos = productos.filter(nomProduct__icontains=query)

            # Calculamos el precio con descuento para cada producto
            for producto in productos:
                producto.precio_descuento = calcular_precio_descuento(producto)

            # Creamos el contexto con las categorías, productos y otros datos
            context = {
                'categoria': categoria,
                'productos': productos,
                'categorias': categorias,
                'query': query,
                'MEDIA_URL': producto.imagen1.url if producto.imagen1 else None,
            }
            
            # Renderizamos la plantilla HTML con el contexto
            return render(request, "tienda_categoria.html", context)

        except Exception as e:
            # Si ocurre un error, devolvemos una respuesta con el estado 500 y el mensaje de error
            return HttpResponse(status=500, content=str(e))
        
class CategoriaView(View):
    def get(self, request, categoria_id=None):
        try:
            query = request.GET.get('q', '')
            categorias = CategoriaProd.objects.all()
            productos = Producto.objects.all()

            if categoria_id:
                categoria = get_object_or_404(CategoriaProd, id=categoria_id)
                productos = productos.filter(categorias=categoria)
            else:
                categoria = None

            if query:
                productos = productos.filter(nomProduct__icontains=query)

            # Calcular precio con descuento para cada producto
            for producto in productos:

                if producto.descuento > 0:
                    descuento_decimal = Decimal(producto.descuento) / Decimal(100)
                    precio_descuento = (producto.precio * (Decimal(1) - descuento_decimal)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                else:
                    precio_descuento = producto.precio
                producto.precio_descuento = precio_descuento  # Asigna el precio con descuento como un atributo del producto
                # import pdb
                # pdb.set_trace()
            context = {
                'categoria': categoria,
                'productos': productos,
                'categorias': categorias,
                'query': query,
                'MEDIA_URL': 'http://127.0.0.1:8000/',
            }
            return render(request, "categoria.html", context)
        
        except Exception as e:
            return HttpResponse(status=500, content=str(e))