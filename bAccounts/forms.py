
# Librería para importar formularios
from django import forms
# Importa la función User ára extraer los campos necesarios
from .models import User




#Crea la clase UserForm (registra nuevos restaurantes )
class UserForm(forms.ModelForm):
    #Creamos campo para confirmar el password
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number',  'password']