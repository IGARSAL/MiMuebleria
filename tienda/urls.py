from django.urls import path
from django.conf import settings
from .views import TiendaView, ProductosJsonView, CategoriaView, ConfirmacionPedidoView
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('', TiendaView.as_view(), name='tienda'),
    path('productos/', ProductosJsonView.as_view(), name='productos_json'),
    path('categoria/', CategoriaView.as_view(), name='categoria_view'),
    path('categoria/<int:categoria_id>/', CategoriaView.as_view(), name='categoria_view'),
    path('confirmacion-pedido/<int:pedido_id>/', ConfirmacionPedidoView.as_view(), name='confirmacion_pedido'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)