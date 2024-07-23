from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import Producto, CategoriaProd # Asegúrate de importar tu modelo Producto
from decimal import Decimal, ROUND_HALF_UP  # Importa Decimal y el método de redondeo adecuado
from django.conf import settings

class ProductosJsonView(View):
    def get(self, request):
        productos = Producto.objects.all()
        
        # Calcular precio con descuento para cada producto
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
    
class TiendaView(View):
    def get(self, request):
        productos = Producto.objects.all()
        context = {
            "productos": productos,
            "MEDIA_URL": settings.MEDIA_URL
        }
        # Calcular precio con descuento para cada producto
        for producto in productos:
            if producto.descuento > 0:
                descuento_decimal = Decimal(producto.descuento) / Decimal(100)
                precio_descuento = (producto.precio * (Decimal(1) - descuento_decimal)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            else:
                precio_descuento = producto.precio
            producto.precio_descuento = precio_descuento  # Asigna el precio con descuento como un atributo del producto
        
        if request.headers.get('Accept') == 'application/json':
            # Serialización para JSON
            productos_data = []
            for producto in productos:
                productos_data.append({
                    'id': producto.id,
                    'nombre': producto.nomProduct,
                    'precio': float(producto.precio),
                    'precio_descuento': float(producto.precio_descuento),
                    'descuento': producto.descuento,
                    'imagen1': producto.imagen1.url if producto.imagen1 else None,
                })
            
            return JsonResponse(productos_data, safe=False)
        
        return render(request, "tienda.html", {"productos": productos})
    
class CategoriaView(View):
    def get(self, request, categoria_id=None):
        query = request.GET.get('q', '')
        categorias = CategoriaProd.objects.all()
        productos = Producto.objects.all()

        if categoria_id:
            categoria = CategoriaProd.objects.get(id=categoria_id)
            productos = productos.filter(categorias=categoria)
        else:
            categoria = None

        if query:
            productos = productos.filter(nomProduct__icontains=query)

        context = {
            'categoria': categoria,
            'productos': productos,
            'categorias': categorias,
            'query': query
        }
        return render(request, "categoria.html", context)
