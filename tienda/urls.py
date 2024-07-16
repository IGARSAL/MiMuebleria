from django.urls import path
from tienda.views import TiendaView

urlpatterns = [
    path('', TiendaView.as_view(), name='tienda'),
]