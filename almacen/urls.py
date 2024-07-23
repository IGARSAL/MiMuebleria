from django.urls import path
from .views import ProcesarPedido, TopProductosVendidos
from django.conf import settings
from django.conf.urls.static import static

app_name = 'almacen' 
urlpatterns = [
    path('', ProcesarPedido.as_view(), name='procesar_pedido'),
    path('topproductos/', TopProductosVendidos.as_view(), name='top_productos')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
