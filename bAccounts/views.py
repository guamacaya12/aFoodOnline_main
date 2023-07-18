
# Carga de librerías para llamar templates
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

# Importa librería para mensajes de login y logout
from django.contrib import messages, auth

# importa el UserForm del archivo forms.py
from .forms import  UserForm
from. models import *

# importa el form del archivo vendor/forms.py
from vendor.forms import *

# Hoja de funciones (utilerías in house)
from .utils import *

# Importar decorador de DJANGO para detectar el login de usuario / # Restringir al vendedor de acceder al tablero del cliente
from django.contrib.auth.decorators import login_required, user_passes_test

# Restringir al vendedor de acceder al tablero del cliente
from django.core.exceptions import PermissionDenied

# Restringir al vendedor de acceder al tablero del cliente
def check_role_vendor(user):
    if user.role ==1:
        return True
    else:
        raise PermissionDenied
# Restringir al cliente de acceder al tablero del vendedor
def check_role_customer(user):
    if user.role ==2:
        return True
    else:
        raise PermissionDenied


# Utiliza los campos del formulario User, para hacer el rgistro de usuario en bAccounts
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Estás correctamente autenticado')
        return redirect('dashboard')
    #VERIFICAR SI SE GUARDA EL USUARIO, EN CASO DE QUE NO, SE REGRESA AL FORMULARIO
    elif request.method == 'POST':
    # print(request.POST)
        #Guardar los datos si el formulario es válido (los campos del formulario se pasan en "request.POST")
        form = UserForm(request.POST)
        if form.is_valid():
            # password = form.cleaned_data['password']
            # # Permite preguardar la información del formulario en una variable llamada "user"
            # user = form.save(commit=False)
            # user.set_password(password)
            # # Por defecto, lo guarda con el role de "CUSTOMER"
            # user.role = User.CUSTOMER   
            # Guarda la información del usuario
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name = first_name, last_name = last_name, username = username, email = email, password = password)
            user.role = User.CUSTOMER
            user.save()
            # una vez que se guardan los datos, te regresa a la página del registro de usuario
            messages.success(request, 'Se han almacenado los registros con éxito')
            return redirect('registerUser')
        else:  
            messages.error(request, form.errors)
            # messages.error(request, form.non_field_errors)             
            # messages.error(request, form.errors)
    
    
    # En caso de que no se hayan guardado bien los datos, te regresa al formulario
    else:
        form = UserForm()
    context = {'form': form,}
        #Pasamos el contexto (campos) del usuario al formulario de la ruta registerUser.html
    return render(request, 'bAccounts/registerUser.html', context)


# Register vendor (fusionate forms (user and vendor))
def registerVendor(request):
    # Esta instrucción es para que, una vez que el usuario ha hecho login, 
    # no pueda volver a ver la pantalla de login, porqué ya está autenticado.
    if request.user.is_authenticated:
        messages.warning(request, 'Estás correctamente autenticado')
        return redirect('dashboard')
    
    elif request.method =='POST':
        #guarda los datos y crea el usuario
        form = UserForm(request.POST)
        #EL files es para recibir también los archivos
        v_form = VendorForm(request.POST, request.FILES)
        if form .is_valid() and v_form.is_valid:
            # Guarda la información del usuario
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name = first_name, last_name = last_name, username = username, email = email, password = password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            #MENSAJES
            messages.success(request, 'Se han almacenado los registros con éxito, por favor espere para aprobación')
            return redirect('registerVendor')

        else:
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()
# El contexto es un diccionario que se pasa al formulario
    context = {
        'form':form
        , 'v_form':v_form
    }
    return render(request, 'bAccounts/registerVendor.html', context)


# Vista para login
def login(request):
    # Esta instrucción es para que, una vez que el usuario ha hecho login, 
    # no pueda volver a ver la pantalla de login, porqué ya está autenticado.
    if request.user.is_authenticated:
        messages.warning(request, 'Estás correctamente autenticado')
        return redirect('myAccount')
    elif request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']
        # Función de autenticación de usuarios existente en DJANGO
        user = auth.authenticate(email=email, password = password)

        # Si los campos fueron llenados
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Haz hecho login correctamente')
            return redirect('myAccount')
        # En caso de que el usuario o contraseña estén mal
        else:
            messages.error(request, 'Las credenciales no son correctas')
            return redirect('login')

    return render(request, 'bAccounts/login.html')


#Salida del sistema y retorno al portal de login
def logout(request):
    auth.logout(request)
    messages.info(request, 'Has salido correctamente de la plataforma')
    return redirect('login')

# this decorator send the user to login page in case they are not logged
@login_required(login_url='login')
# We get data from the utils.py (to detect the user type)
def myAccount(request):
    # Identify user type with request
    user = request.user
    # Choice the corresponding URL through user type
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


# Tablero del cliente
# this decorator send the user to login page in case they are not logged
@login_required(login_url='login')
# Restringe vista de usuario a otros dashboards
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'bAccounts/custDashboard.html')


# Tablero del vendedor
# this decorator send the user to login page in case they are not logged
@login_required(login_url='login')
# Restringe vista de usuario a otros dashboards
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'bAccounts/vendorDashboard.html')
