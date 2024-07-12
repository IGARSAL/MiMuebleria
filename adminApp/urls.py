from django.contrib.auth import views as auth_views
from django.urls import include, path
from .views import RegisterView, EditView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('edit/', EditView.as_view(), name='edit'),
]