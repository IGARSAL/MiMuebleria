from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Cliente

#Señal para crear un perfil automáticamente cuando se crea un usuario
@receiver(post_save, sender=User)
def create_user_cliente(sender, instance, created, **kwargs):
    if created:
        if not hasattr(instance, 'cliente'):
            Cliente.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_cliente(sender, instance, **kwargs):
    instance.cliente.save()