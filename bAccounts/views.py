
# Carga de librerías para llamar templates
from django.shortcuts import render
from django.http import HttpResponse

#Crea tus vistas aquú
def registerUser(request):
    return render(request, 'bAccounts/registerUser.html')
