
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
from .utils import detectUser, send_verification_email

# Importar decorador de DJANGO para detectar el login de usuario / # Restringir al vendedor de acceder al tablero del cliente
from django.contrib.auth.decorators import login_required, user_passes_test

# Restringir al vendedor de acceder al tablero del cliente
from django.core.exceptions import PermissionDenied

# Para decodificar el token enviando por correo
from django.utils.http import urlsafe_base64_decode
# Generador de tokens
from django.contrib.auth.tokens import default_token_generator


from datetime import datetime






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
        messages.warning(request, 'Estás correctamente autenticado ')
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

            # Send verification email (sirve para verificar si el usuario confirma su cuenta de correo a dónde se envía token)
            # Activación de usuario
            
            
            # Envía el correo para  restablecimiento de contraseña
            mail_subject =  'Por favor activa tu cuenta'
            # mail templates
            email_template = 'bAccounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Tu cuenta de cliente se ha dado de alta, se te ha enviado un correo para activarla ')
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


# Register vendor (fusiona forms (user and vendor))
def registerVendor(request):
    # Esta instrucción es para que, una vez que el usuario ha hecho login, 
    # no pueda volver a ver la pantalla de login, porqué ya está autenticado.
    if request.user.is_authenticated:
        messages.warning(request, 'Estás correctamente autenticado ')
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

            # Envía el correo para  restablecimiento de contraseña
            mail_subject =  'Por favor activa tu cuenta '
            # mail templates
            email_template = 'bAccounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            #MENSAJES
            messages.success(request, 'Tu cuenta de socio se ha dado de alta, se te ha enviado un correo para activarla ')
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

# Función de activación de usuario (se envía token por correo)
def activate (request, uidb64, token):
    #Revisar si el usuario utiliza el token, validarlo vs base de datos y en caso de que
    # sea correcto, guardar la información
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Si el usuario existe, guardar su estatus de activación
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Tu cuenta ha sido activada con éxito ')
        return redirect('myAccount')
    else:
        messages.error(request, 'Link de activación inválido ')
        return redirect('myAccount')

# Vista para login
def login(request):
    # Esta instrucción es para que, una vez que el usuario ha hecho login, 
    # no pueda volver a ver la pantalla de login, porqué ya está autenticado.
    if request.user.is_authenticated:
        messages.warning(request, 'Has ingresado correctamente al sistema ')
        return redirect('myAccount')
    elif request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']
        # Función de autenticación de usuarios existente en DJANGO
        user = auth.authenticate(email=email, password = password)

        # Si los campos fueron llenados
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Has ingresado correctamente al sistema ')
            return redirect('myAccount')
        # En caso de que el usuario o contraseña estén mal
        else:
            messages.error(request, 'Las credenciales no son correctas ')
            return redirect('login')

    return render(request, 'bAccounts/login.html')


#Salida del sistema y retorno al portal de login
def logout(request):
    auth.logout(request)
    messages.info(request, 'Has salido correctamente del sistema ')
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



# Gestión de contraseñas
def forgot_password(request):
    # Si alguien solicita el restablecimiento de la contraseña
    if request.method == 'POST':
        email = request.POST['email']
        # Verificamos si el mail existe en la base de datos
        if User.objects.filter(email= email).exists():
            user = User.objects.get(email__exact = email)

            # Envía el correo para  restablecimiento de contraseña
            mail_subject =  'Por favor resetea tu contraseña'
            # mail templates
            email_template = 'bAccounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            
            
            messages.success(request, 'El link para restablecer tu contraseña se envío al correo registrado ')
            return redirect('login')
        else:
            messages.error(request, 'La cuenta no existe ')
            return redirect('forgot_password')
    return render(request, 'bAccounts/forgot_password.html')

# Validación de usuario para reestablecer password
def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Te redirige a la página para restablecer tu password
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('myAccount')


# Función que te lleva a la página de restablecimiento de contraseña
def reset_password(request):
      if request.method == 'POST':
          password = request.POST['password']
          confirm_password = request.POST['confirm_password']
          
          # Si las contraseñas coinciden guarda el nuevo password
          # La sesión de usuario (pk) sigue activa por la función de validación de correo (reset_password_validate)
          if password == confirm_password:
              pk = request.session.get('uid')
              user = User.objects.get(pk = pk)
              user.set_password(password)
              user.is_active = True
              user.save()
              messages.success(request, 'La contraseña se restableció correctamente  ')
              return redirect('login')
          else:
            messages.error(request, 'Las contraseñas no coinciden  ')
            return redirect('reset_password')
            
      return render(request, 'bAccounts/reset_password.html')