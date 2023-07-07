
# Carga de librerías para llamar templates
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

# Importa librería para mensajes de login y logout
from django.contrib import messages

# importa el UserForm del archivo forms.py
from .forms import  UserForm
from. models import *

# importa el form del archivo vendor/forms.py
from vendor.forms import *

# Utiliza los campos del formulario User, para hacer el rgistro de usuario en bAccounts
def registerUser(request):
    #VERIFICAR SI SE GUARDA EL USUARIO, EN CASO DE QUE NO, SE REGRESA AL FORMULARIO
    if request.method == 'POST':
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
    if request.method =='POST':
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