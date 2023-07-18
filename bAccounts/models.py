
# Librería por defecto de Django para crear modelos
from django.db import models

#Importar librería para crear nuestro propio modelo de gestión de usuarios
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.db.models.fields.related import ForeignKey, OneToOneField

#Librería para importar "signals" (que es una especie de trigger para conectar datos entre modelos)
from django.db.models.signals import post_save, pre_save

#Funciona para el decorador (que permite conectar usuario con perfil)
from django.dispatch import receiver

# Create your models here-----------------------------------------------------------------

# Se crea una clase para dar de alta super usuarios (es un modelo definido por el desarrollador)
# a diferencia del modelo que viene por defecto en el panel de admin de Django

#Esta clase únicamente contiene métodos, no campos
class UserManager(BaseUserManager):
    # Create a regular user
    def create_user(self, first_name, last_name, username, email, password =None):
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have an username')
        
        user = self.model(
              email = self.normalize_email(email)
            , username = username
            , first_name = first_name
            , last_name = last_name
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    # Create a super user
    def create_superuser(self, first_name, last_name, username, email, password =None):
        user = self.create_user(
              email = self.normalize_email(email)
            , username=username
            , password=password
            , first_name=first_name
            , last_name=last_name )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    

# Crear modelo de usuarios (tabla)
class User(AbstractBaseUser):
    
    # Default values for choices
    VENDOR = 1
    CUSTOMER = 2

    #Lista de selección dentro del modelo
    ROLE_CHOICE =(
        (VENDOR, 'Vendor')
        , (CUSTOMER, 'Customer')
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)
    
    #Required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)
    is_superadmin = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    # Con esto le decimos a django que utilice nuestro modelo de gestión de usuarios
    objects = UserManager()

    def __str__(self):
        return self.email
    
    # "perm" indica a DJANGO cuales son los permisos que tiene cada usuario
    # "app_label" indica cual es la app a la que tiene permisos ese usuario
    def has_perm(self, perm, obj = None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    # Esta función se utiliza para detectar
    # Cuál dashboard se muestra cuando un usuario hace login
    # Se asocia con el template "dashboard"
    def get_role(self):
        if self.role == 1:
            user_role ='Vendor'
        elif self.role ==2:
            user_role ='Customer'
        return user_role
        print(f"Rol de usuario {user_role}")

    #--------------CLASS USER PROFILE (perfil de usuario)
class UserProfile(models.Model):
    # el oneToOneField obliga  aque un usuario solo pueda tener un perfil, el modo CASCADE, hace que se borre el perfil, cuando el usuario es borrado
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # def full_address(self):
    #     return f'{self.address_line_1}, {self.address_line_2}'

    # Devuelve la dirección de correo cuando se ha creado el usuario
    def __str__(self):
        return self.user.email


