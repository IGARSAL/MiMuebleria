from django.shortcuts import render
from django.views import View
from .models import Producto
from .forms import ProductoForm
from django.contrib.auth.decorators import login_required

class TiendaView(View):
    def get(self, request):
        productos = Producto.objects.all()
        return render(request, "tienda.html", {"productos": productos})
    
