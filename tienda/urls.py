from django.urls import path
from django.conf import settings
from tienda.views import TiendaView
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('', TiendaView.as_view(), name='tienda'),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)