from django.urls import path
from django.conf import settings
from .views import tiendaCategoria, ProductosJsonView, ConfirmacionPedidoView
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('', tiendaCategoria.as_view(), name='tienda'),
    path('categoria/', tiendaCategoria.as_view(), name='categoria_view'),
    path('categoria/<int:categoria_id>/', tiendaCategoria.as_view(), name='categoria_view'),
    path('productos/', ProductosJsonView.as_view(), name='productos_json'),
    path('confirmacion-pedido/<int:pedido_id>/', ConfirmacionPedidoView.as_view(), name='confirmacion_pedido'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)