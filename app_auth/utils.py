from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import jwt
import datetime
import os
import uuid

def send_verification_email(user,url,origin):
    subject = f'Verifica tu correo electrónico en {settings.SITE_NAME}'
    context = {
        "url":url,
        "user":user,
        "site_name":settings.SITE_NAME,
        "origin":origin
    }
    to_email=[user.email]
    from_email=settings.DEFAULT_FROM_EMAIL
    html_content = render_to_string('email_verification.html', context)
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, 'text/html')
    email.send()
    #Almacenar en los logs
    print(f"Verificación de email enviada al usuario: {user.username}\nEmail: {user.email}")
    return True

def send_reset_password_email(user,url):
    subject = f"Solicitud de restablecimiento de contraseña en {settings.SITE_NAME}"
    context = {
        "url":url,
        "user":user,
        "site_name":settings.SITE_NAME
    }
    to_email=[user.email]
    from_email=settings.DEFAULT_FROM_EMAIL
    html_content = render_to_string('reset_password.html', context)
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, 'text/html')
    email.send()
    #Almacenar en los logs
    print(f"Reestablecimiento de contrasseña para el usuario {user.username} enviado")
    return True

def generate_token(user):
    payload = {
        'user_id':str(user.id),
        'user_email': user.email,
        'exp': timezone.now() + datetime.timedelta(minutes=10)  # token expires in 10 minutes
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload, True
    except jwt.ExpiredSignatureError:
        return None, False  # token ha expirado
    except jwt.InvalidTokenError:
        return None, False  # token es inválido
    
def get_unique_filename(instance, filename):
    model_name = instance.__class__.__name__.lower()
    folder_mapping = {
        'user': 'users/',
        'default': 'others/',
    }
    try:
        folder = folder_mapping[model_name]
    except:
        folder = folder_mapping['default']

    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(folder, unique_filename)