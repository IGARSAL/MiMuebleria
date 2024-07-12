from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class Cliente(models.Model):
    objects = None
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)
    codigo_postal = models.CharField(max_length=10)
    identiFed = models.CharField(max_length=50)
    colonia = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    no_Ext = models.CharField(max_length=10)
    no_int = models.CharField(max_length=10)

    def __str__(self):
        return f'Cliente of {self.User.username}'
    
#Señal para crear un perfil automáticamente cuando se crea un usuario
def create_user_cliente(sender, instance, created, **kwargs):
    if created:
        Cliente.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_cliente(sender, instance, **kwargs):
    instance.cliente.save()
    