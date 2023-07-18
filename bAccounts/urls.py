
from django.urls import path
from . import views 

# Son todas las URLS de la plataforma, asociadas a las cuentas.
# Estas URLS se ven en "aFoodOnline_main" dentro de "URLs", con otra instrucción de lectura.

urlpatterns = [
      # Función y formulario para registrar un usuario nuevo
        path('registerUser/', views.registerUser, name = 'registerUser')
      # Función y formulario para registrar un vendedor nuevo        
      , path('registerVendor/', views.registerVendor, name = 'registerVendor')
      # Función y formulario para hacer log in de un usuario ya registrado
      , path('login/', views.login, name = 'login')
      # Función y formulario para hacer log out de cualquier usuario
      , path('logout/', views.logout, name = 'logout')
      # Te lleva a tu cuenta
      , path('myAccount/', views.myAccount, name = 'myAccount')      
      # Te lleva al dashboard de cliente
      , path('custDashboard/', views.custDashboard, name = 'custDashboard')            
      # Te lleva al dashboard de vendedor
      , path('vendorDashboard/', views.vendorDashboard, name = 'vendorDashboard')       

]
