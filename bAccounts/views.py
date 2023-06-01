
# Carga de librerías para llamar templates
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

# importa el UserForm del archivo forms.py
from .forms import  UserForm
from. models import User

# Utiliza los campos del formulario User, para hacer el rgistro de usuario en bAccounts
def registerUser(request):
    #VERIFICAR SI SE GUARDA EL USUARIO, EN CASO DE QUE NO, SE REGRESA AL FORMULARIO
    if request.method == 'POST':
        print(request.POST)
        #Guardar los datos si el formulario es válido (los campos del formulario se pasan en "request.POST")
        form = UserForm(request.POST)
        if form.is_valid():
            # Permite preguardar la información del formulario en una variable llamada "user"
            user = form.save(commit=False)
            # Por defecto, lo guarda con el role de "CUSTOMER"
            user.role = User.CUSTOMER   
            # Guarda la información del usuario
            user.save()
            # una vez que se guardan los datos, te regresa a la página del registro de usuario
            return redirect('registerUser')
    else:
    # En caso de que no se hayan guardado bien los datos, te regresa al formulario
        form = UserForm()
    context = {
        'form': form, 
    }
    #Pasamos el contexto (campos) del usuario al formulario de la ruta registerUser.html
    return render(request, 'bAccounts/registerUser.html', context)
