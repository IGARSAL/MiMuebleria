from dashboard.views import Inicio
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
   
    path('', Inicio.as_view(), name="home"), 
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
