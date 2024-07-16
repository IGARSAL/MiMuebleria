from django.contrib.auth import views as auth_views
from django.urls import include, path
from .import views
from .views import RegisterView, EditView, DeleteUserView
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('edit/', EditView.as_view(), name='edit'),
    path('delete/', DeleteUserView.as_view(), name='delete_account'),
]