"""
URL configuration for aFoodOnline_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Para conectar con la plataforma de administración
from django.contrib import admin
# Librería para habilitar las rutas de los archivos
from django.urls import path, include
# Importa las funciones del archivo views
from . import views 

# Funciones para habilitar las carpetas de MEDIA (dónde se suben las imágenes de los perfiles  de usuario)
from django.conf import settings
from django.conf.urls.static import static



# LISTA DE RUTAS

urlpatterns = [
      path('admin/', admin.site.urls)

    , path('', views.home , name = 'home')
    #Incluir las URL de la app bAccounts, y nombrarla accounts
    , path('accounts/', include('bAccounts.urls'), name = 'accounts')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Con esta instrucción (después del signo +) se indica dónde guardar
# los archivos multimedia de los usuarios y perfiles creados
# los parámetros  (MEDIA_URL y MEDIA_ROOT) se ponen en "settings"