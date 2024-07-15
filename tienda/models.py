from django.db import models

# Create your models here.
class CategoriaProd(models.Model):
    nombreCatProd = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Productos"
    
    def __str__(self):
        return self.nombreCatProd

class Producto(models.Model):
    nomProduct = models.CharField(max_length=100, help_text='Nombre del producto')
    categorias = models.ForeignKey(CategoriaProd, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2, help_text='Precio del producto')
    imagen1 = models.ImageField(upload_to="tienda/%Y/%m/%d/", null=True, blank=True, help_text='Imagen del producto frontal')
    imagen2 = models.ImageField(upload_to="tienda", null=True, blank=True, help_text='Imagen del producto trasera')
    imagen3 = models.ImageField(upload_to="tienda", null=True, blank=True, help_text='Imagen del producto lateral')
    descuento = models.IntegerField(default=0, help_text='Cantidad disponible en stock')
    sku = models.CharField(max_length=20, help_text='Número único del producto')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    


    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
    
    def __str__(self):
        return self.nombreProd
    
