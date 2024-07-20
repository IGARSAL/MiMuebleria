from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from miMuebleria import settings
from tienda.models import Producto
from .models import Pedido, LineaPedido
from carro.carro import Carro
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
from carro.context_processors import importe_total_carro


class ProcesarPedido(LoginRequiredMixin, View):
    login_url = '/adminApp/login'

    pedido = Pedido.objects.create(user=request.user)
    carro= Carro(request)
    lineas_pedido = []
    total_pedido = 0

    for key, value in carro.carro.items():
        cantidad = int(value["cantidad"])
        precio = float(value["precio"])
        total_linea = cantidad * precio
        

