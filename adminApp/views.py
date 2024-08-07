from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from .forms import ClienteEditForm, UserEditForm, UserRegistrationForm, RangoFechaForm
from .models import Cliente
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.views.generic import ListView
from django.views.generic.edit import FormView
from tienda.models import Producto, CategoriaProd, ReporteVentas
from django.views import View
import csv
import logging


class ReporteVentasView(FormView):
    template_name = 'adminApp/reportes.html'
    form_class = RangoFechaForm
    
    def form_valid(self, form):
        fecha_inicio = form.cleaned_data['fecha_inicio']
        fecha_fin = form.cleaned_data['fecha_fin']
        ventas = ReporteVentas.objects.filter(fecha__date__range=[fecha_inicio, fecha_fin]) \
                                .values('producto__nomProduct') \
                                .annotate(total_cantidad=Sum('cantidad'), total_venta=Sum('total_venta')) \
                                .order_by('producto__nomProduct')
        context = self.get_context_data(form=form)
        context['ventas'] = ventas
        context['fecha_inicio'] = fecha_inicio
        context['fecha_fin'] = fecha_fin
        return self.render_to_response(context)
    
class CerrarSesionView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
    
class DeleteUserView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'adminApp/delete_confirm.html')
    
    def post(self, request):
        user = request.user
        try:
            user.delete()
            messages.success(request, 'Tu cuenta ha sido eliminada correctamente.')
            return redirect('home')
        except:
            messages.error(request, 'Hubo un error al eliminar tu cuenta.')
            return redirect('login')
        
class RegisterView(View):
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
            #Verificar si ya existe un objeto Cliente
            if not hasattr(new_user, 'cliente'):
                Cliente.objects.create(user=new_user)
            return render(request, 'adminApp/register_done.html', {'new_user': new_user})
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

logger = logging.getLogger(__name__)

class dataView(ListView):
    template_name = 'upload/csv.html'
    model = Producto
    context_object_name = 'obj'

    def get(self, request, **kwargs):
        if not self.request.user.has_module_perms('adminApp.view_Producto'):
            return redirect('login')
        return super().get(request, **kwargs)

def cargar_csv(request):
    template_name = "upload/upload_cvs.html"
    error_message = None
    dato_erroneo = []

    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")
        if csv_file:
            try:
                    csv_file.open('r')
                    reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
                    for line in reader:
                        fileds = line
                        if len(fileds) > 1:
                            data_dict = {
                                "nomProduct": fileds[0],
                                "categorias_id": fileds[1],
                                "precio": fileds[2],
                                "imagen1": fileds[3],
                                "imagen2": fileds[4],
                                "imagen3": fileds[5],
                                "ventas_totales": fileds[6],
                                "descuento": fileds[7],
                                "stock": fileds[8],
                                "sku": fileds[9],
                               
                            }
                            if not is_duplicate(data_dict["sku"]) and validar_datos(data_dict):
                                guardar_producto(data_dict)

                            else:
                                dato_erroneo.append(data_dict)
                    if dato_erroneo:
                        messages.warning(request, 'algunos datos no se cargaron correctamente.')
                    else:
                        messages.success(request, 'Archivo CVS cargado correctamente')
            except Exception as ex:
                logger.error(f"Error al procesar el archivo CSV: {repr(ex)}")
                messages.error(request, 'Error al procesar el archivo CSV')
                
        else: 
            messages.error(request, 'No se ha cargado ningún archivo.')

    return render(request, template_name)

def buscar_categoria(categoria_nombre):
    try:
        return CategoriaProd.objects.get(id=categoria_nombre)
    except CategoriaProd.DoesNotExist:
        return None

def is_duplicate(sku):
    return Producto.objects.filter(sku=sku).exists()

def validar_datos(data):
    try:
        if not data["nomProduct"]:
            raise ValueError("El nombre del producto esta vacío.")
        
        if not data["categorias_id"]:
            raise ValueError("La categoría está vacía.")
        
        precio = float(data["precio"])
        if precio <=0:
            raise ValueError("El precio debe ser un número positivo")
        
        if not data["imagen1"]:
            data["imagaen1"] = 'path/to/default-image.jpg'
        
        if not data["imagen2"]:
            data["imagaen2"] = 'path/to/default-image.jpg'
        
        if not data["imagen3"]:
            data["imagaen3"] = 'path/to/default-image.jpg'
        
        ventas_totales = int(data["ventas_totales"])
        if ventas_totales < 0:
            raise ValueError("Las ventas totales no pueden ser negativas.")
        
        descuento = float(data["descuento"])
        if not(0 <= descuento <= 100):
            raise ValueError("El descuento debe estar entre 0 y 100.")
        
        stock = int(data["stock"])
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        
        if not data["sku"]:
            raise ValueError("El SKU está vacío")
        return True
    except (ValueError, TypeError) as e:
        logger.error(f"Error de validación: {e}")
        return False

def guardar_producto(data):
    producto = Producto(
        nomProduct=data["nomProduct"],
        categorias_id=data["categorias_id"],
        precio=data["precio"],
        imagen1=data["imagen1"],
        imagen2=data["imagen2"],
        imagen3=data["imagen3"],
        ventas_totales=data["ventas_totales"],
        descuento=data["descuento"],
        stock=data["stock"],
        sku=data["sku"]
    )
    producto.save()


