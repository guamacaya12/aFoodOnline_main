"""
Django settings for aFoodOnline_main project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
#Librería para proteger información sensible (.envs + .gitignore)
from decouple import config

import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bAccounts',
    'vendor'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aFoodOnline_main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static'
            ],
        },
    },
]

WSGI_APPLICATION = 'aFoodOnline_main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

#Librería para proteger información sensible (.envs + .gitignore)
#from decouple import config

DATABASES = {
    'default': {
          'ENGINE': config('DB_ENGINE')
        , 'NAME': config('DB_NAME')
        , 'USER':config('DB_USER')
        , 'PASSWORD': config('DB_PASSWORD')
        , 'HOST': config('DB_HOST')
    }
}

# Le decimos a django que utilice nuestro modelo de gestión de usuarios (bAccounts)
AUTH_USER_MODEL = 'bAccounts.User'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
# Configuración de archivos estáticos (html-css-js)

STATIC_ROOT = BASE_DIR/'static'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIR =[
    'aFoodOnline_main/static/'
]
# STATICFILES_DIR = [
#    os.path.join(BASE_DIR, 'aFoodOnline_main/static/')
# ]






# Configuración de archivos multimedia (imágenes que cargan los usuarios para dar de alta un perfil)
# Para soportar estas rutas, las carpetas se crean de forma automática en la carpeta raíz.
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR/'media'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Alertas y notificaciones (establacerlas en color rojo cuando sean errores, pero los colores son dinámicos)
# se utiliza en la página html de alertas
from django.contrib.messages import constants as messages
MESSAGE_TAGS={
    messages.ERROR:'danger',
}

# Configuración de correo (envío de correos electrónicos para autenticación de doble factor)
EMAIL_BACKEND = config('EMAIL_BACKEND') 
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast = int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
# Nombre del remitente que aparecerá en la bandeja de entrada 
# Se utiliza también en la función "send_verification_email"
DEFAULT_FROM_EMAIL = 'FoodOnline Marketplace <tzuppa@baobyte.com>'