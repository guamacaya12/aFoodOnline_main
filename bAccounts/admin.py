
from django.contrib import admin
# Importa la clase "User" y la clase "UserProfile"
from .models import User, UserProfile
#Importa la clase User Admin (django nativa)
from django.contrib.auth.admin import UserAdmin


#_________________________________________________________________________________________________MODELOS
# Register your models here.


# Clase para convertir campo de password (en registro de usuarios dentro de la plataforma ADMIN) en "no editable"
class CustomUserAdmin(UserAdmin):
    # Instrucciones para mostrar determinados campos del modelo (registro de usuario) en el campo admin
    list_display = ('email', 'first_name', 'last_name', 'username', 'role', 'is_active')
    # ordenar los campos (el menos significa descendencia)
    ordering = ('-date_joined' , )
    # Convierte a "no editable" campo de password (se verifica en la consola de administración)
    filter_horizontal = ()
    list_filter =()
    fieldsets =()


# registro de usuarios
admin.site.register(User, CustomUserAdmin)

# registro de perfiles de usuario
admin.site.register(UserProfile)
