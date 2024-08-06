
from django.conf.urls.static import static
from django.urls import include, path
from . import views
from .views import RegisterView, EditView, DeleteUserView, CerrarSesionView, dataView
from django.conf import settings
from .views import ReporteVentasView
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('edit/', EditView.as_view(), name='edit'),
    path('delete/', DeleteUserView.as_view(), name='delete_account'),
    path('cerrar_sesion', CerrarSesionView.as_view(), name="cerrar_sesion"),
    path('csv/', dataView.as_view(), name="csv"),
    path('csv/upload', views.cargar_csv, name='cargar_csv'),
    path('reporte-ventas/', ReporteVentasView.as_view(), name='reporte_ventas'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
