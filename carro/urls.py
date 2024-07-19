from django.urls import path
from .views import AgregarProductoView, EliminarProductoView, DisminuirProductoView, VaciarCarroView

app_name="carro"


urlpatterns = [
    path('agregar/<int:producto_id>/', AgregarProductoView.as_view(), name='agregar_producto'),
    path('eliminar/<int:producto_id>/', EliminarProductoView.as_view(), name='eliminar_producto'),
    path('disminuir/<int:producto_id>/', DisminuirProductoView.as_view(), name='disminuir_producto'),
    path('vaciar/', VaciarCarroView.as_view(), name='vaciar_carro'),
]