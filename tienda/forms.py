from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ('nomProduct', 'categorias', 'precio', 'imagen1', 'imagen2', 'imagen3', 'sku')
        labels = {'nomProduct': 'Nombre del producto',
                   'categorias':' Categorias', 
                   'precio': 'Precio del producto',
                   'imagen1': 'Imagen del producto frontal',
                   'imagen2': 'Imagen del producto trasera',
                   'imagen2': 'Imagen del producto lateral',
                   'descuento': 'Descuento del producto',
                   'sku': 'Numero unico del producto',
                  }
        widgets = {'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'precio': forms.TextInput(attrs={'class':'form-control'}),
            'categorias': forms.Select(attrs={'class':'form-control'}),
            'imagen1': forms.FileInput(attrs={'class':'form-control', 'name1': 'imagen1' }),
            'imagen2': forms.FileInput(attrs={'class':'form-control', 'name2': 'imagen2' }),
            'imagen3': forms.FileInput(attrs={'class':'form-control', 'name3': 'imagen3' })
            }