from django.urls import path
from .views import ProcesarPedido
app_name = 'almacen' 
urlpatterns = [
    path('', ProcesarPedido.as_view(), name='procesar_pedido'),
]