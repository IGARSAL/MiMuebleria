
from django.conf.urls.static import static
from django.urls import include, path
from .import views
from .views import RegisterView, EditView, DeleteUserView
from django.conf import settings
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('edit/', EditView.as_view(), name='edit'),
    path('delete/', DeleteUserView.as_view(), name='delete_account'),
]  