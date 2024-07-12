from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import ClienteEditForm, UserEditForm
from django.views import View
from .forms import UserRegistrationForm
from .models import Cliente

class RegisterView(LoginRequiredMixin, View):
    def get(self, request):
        user_form =UserRegistrationForm()
        return render(request, 'adminApp/register.html', {'user_form': user_form})

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #Crea un nuevo usuario, pero evita guardarlo todavía
            new_user = user_form.save(commit=False)
            #Establecer un objeto Usuario
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Cliente.objects.create(user=new_user)
            return render(request, 'adminApp/register_done.html', {'new_user': new_user})
        else:
            return render(request, 'adminApp/register.html', {'user_form': user_form})
        
class EditView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        cliente_form = ClienteEditForm(instance=request.user.cliente)
        return render(request, 'adminApp/edit.html', {'user_form': user_form, 'cliente_form': cliente_form})

    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        cliente_form = ClienteEditForm(instance=request.user.cliente, data=request.POST, files=request.FILES)
        
        if user_form.is_valid() and cliente_form.is_valid():
            user_form.save()
            cliente_form.save()
            messages.success(request, 'El perfil fue actualizado correctamente')
        else:
            messages.error(request, 'Error al actualizar el perfil')
            
        return render(request, 'adminApp/edit.html', {'user_form': user_form, 'cliente_form': cliente_form})
