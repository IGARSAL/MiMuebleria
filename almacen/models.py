from django.db import models
from tienda.models import Producto
from django.db.models import F, Sum, FloatField
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class Pedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='LineaPedido', related_name='pedidos')
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ], default='pendiente')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return self.lineapedido_set.aggregate(
            total=Sum(F("producto__precio") * F("cantidadVendida"), output_field=FloatField())
        )["total"] or 0.0

    class Meta:
        db_table = 'pedidos'
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['id']
    
    def __str__(self):
        return f"Pedido #{self.id} - Cliente: {self.user.username}"

class LineaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidadVendida = models.IntegerField(default=1)
    total_pedido = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cantidadVendida} unidades de {self.producto.nomProduct}'

    class Meta:
        db_table = 'lineas_pedidos'
        verbose_name = "Línea de Pedido"
        verbose_name_plural = "Líneas de Pedido"
        ordering = ['id']

