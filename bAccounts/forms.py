
# Librería para importar formularios
from django import forms
# Importa la función User ára extraer los campos necesarios
from .models import User
# Importa librería para mensajes de login y logout
from django.contrib import messages

#Crea la clase UserForm (registra nuevos restaurantes )
class UserForm(forms.ModelForm):
    #Creamos campo para confirmar el password
    password = forms.CharField(label = 'password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label = 'confirm_password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number',  'password']
    
    # Función que evalúa si los passwords son iguales, en caso de que no, lanza un error de formulario.
    # Se utiliza una función súper, para sobre escribir el formulario de usuario registrado con los datos limpios (clean)
    def clean(self):
        #cleaned_data = super(UserForm, self).clean()
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', 'Las contraseñas no coinciden')
            # self.add_error('','')
            # raise forms.ValidationError('Las contraseñas no coinciden')
    
    def display_errors(self, request):
        non_field_errors = self.non_field_errors()

        if non_field_errors:
            messages.error(request, non_field_errors.as_text())