from django.urls import path
from .views import ProcesarPedido
from django.conf import settings
from django.conf.urls.static import static

app_name = 'almacen' 
urlpatterns = [
    path('', ProcesarPedido.as_view(), name='procesar_pedido'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
