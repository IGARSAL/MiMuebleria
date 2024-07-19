from django.shortcuts import render
from django.views import View
from .models import Producto
from .forms import ProductoForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers


class TiendaView(View):
    def get(self, request):
        productos = Producto.objects.all()
        if request.headers.get('Accept') == 'application/json':
            productos_json = serializers.serialize('json', productos)
            return JsonResponse(productos_json, safe=False)    

        
        return render(request, "tienda.html", {"productos": productos})

class ProductosJsonView(View):
    def get(self, request):
        productos = Producto.objects.all()
        productos_json = serializers.serialize('json', productos)
        return JsonResponse(productos_json, safe=False)
