from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Cliente
from tienda.models import Producto
from django.utils import timezone
from datetime import datetime

class RangoFechaForm(forms.Form):
    fecha_inicio = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        fecha_actual = timezone.now().date()

        if fecha_inicio and fecha_inicio > fecha_actual:
            self.add_error('fecha_inicio', 'La fecha de inicio no puede ser posteriror a la fecha ')
        
        if fecha_fin and fecha_fin > fecha_actual:
            self.add_error('fecha_fin', 'La fecha de fin no puede ser posterior a la fecha actual')

        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            self.add_error('fecha_inicio', 'La fecha de inicio no puede ser posterior a la fecha de fin')

        return cleaned_data 

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', 
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Repeat password', 
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        widgets ={ 
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo electronico ya existe, por favor utiliza otra dirección de correo eletrónico ")
        return email
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cd.get('password2')
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model =User
        fields = ['first_name', 'last_name', 'email']

class ClienteEditForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['telefono', 'codigo_postal', 'identiFed', 'colonia', 'direccion', 'no_Ext', 'no_int']

class dataForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"

