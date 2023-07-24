
# This file is designed to save helpfuls utilitys developed by the owner


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string # Envío de correos desde python
from django.utils.http import urlsafe_base64_encode # Codificar la llave primaria del usuario (que se envía por correo)
from django.utils.encoding import force_bytes  # Codificar la llave primaria del usuario (que se envía por correo)
from django.contrib.auth.tokens import default_token_generator # Genera el token que se envía por correo
from django.core.mail import EmailMessage  #Envío de correos electrónicoss
from django.conf import settings # Importar settings del mismo django


# This function is helpful to identify if the user is a vendor or a customer.
def detectUser(user):
    if user.role==1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role ==2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
         redirectUrl = '/admin'

    
    #  Envía correo para envío de correos (activación, reset de password)
    #  mail_subject e email_template se gestionan dinámicamente
    
def send_verification_email(request, user, mail_subject, email_template):
        # El remitente por defecto se establece en "settings"
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template, 
                               {
                                   'user': user, 
                                   'domain':current_site,
                                   'uid': urlsafe_base64_encode(force_bytes(user.pk)),   #User primary key codificado
                                   'token': default_token_generator.make_token(user),  # el token enviado por mail
                                   
                               })
    to_email = user.email # El correo del usuario al que se enviará el token
    mail = EmailMessage(mail_subject, message, from_email, to= [to_email]) # Cuerpo del mensaje
    mail.send()



    # # Envía correo con token para activar usuario
# def send_verification_email(request, user):
#     # El remitente por defecto se establece en "settings"
#     from_email = settings.DEFAULT_FROM_EMAIL
#     current_site = get_current_site(request)
#     mail_subject = 'Por favor activa tu cuenta'
#     message = render_to_string('bAccounts/emails/account_verification_email.html', 
#                                {
#                                    'user': user, 
#                                    'domain':current_site,
#                                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),   #User primary key codificado
#                                    'token': default_token_generator.make_token(user),  # el token enviado por mail
                                   
#                                })
#     to_email = user.email # El correo del usuario al que se enviará el token
#     mail = EmailMessage(mail_subject, message, from_email, to= [to_email]) # Cuerpo del mensaje
#     mail.send()