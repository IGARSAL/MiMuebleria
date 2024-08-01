from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Cliente
from tienda.models import Producto

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