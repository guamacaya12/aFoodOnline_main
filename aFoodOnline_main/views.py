
# Carga de librerías para llamar templates
from django.shortcuts import render
from django.http import HttpResponse


# Función para llamar al template "home"
def home(request):
    return render(request, 'home.html')

