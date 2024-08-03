import os
import logging
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from django.shortcuts import render, redirect
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.shortcuts import redirect, render
from django.conf import settings
from django.http import HttpResponse
import inicio.views as traer

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configura el flujo OAuth2
flow = Flow.from_client_secrets_file(
    'config/credentials.json',
    scopes=['https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/gmail.modify',
            'https://www.googleapis.com/auth/gmail.labels']
)
flow.redirect_uri = 'http://localhost:8000/gmail/oauth2callback2/'

from django.core.mail import send_mail
from django.http import HttpResponse
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from django.conf import settings

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def send_email(request):
    if request.method == 'POST':
        to = request.POST.get('to')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        
        if 'credentials' not in request.session:
            return redirect('gmail_auth')

        try:
            credentials = Credentials(**request.session['credentials'])
            
            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
                request.session['credentials'] = credentials_to_dict(credentials)
                
            service = build('gmail', 'v1', credentials=credentials)

            message = create_message('me', to, subject, body)
            send_message(service, 'me', message)

            return redirect('gmail_inbox')
        
        except HttpError as error:
            logger.error(f"Error al enviar el correo: {error}")
            return HttpResponse("Error al enviar el correo", status=500)
    
    return HttpResponse("Método no permitido", status=405)

def create_message(sender, to, subject, body):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import base64

    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_message(service, sender, message):
    try:
        message = service.users().messages().send(userId=sender, body=message).execute()
        logger.info(f"Mensaje enviado: {message['id']}")
        return message
    except HttpError as error:
        logger.error(f"Error al enviar el mensaje: {error}")
        raise


@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def gmail_auth(request):
    if 'credentials' in request.session:
        del request.session['credentials']
    authorization_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    return redirect(authorization_url)

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def oauth2callback2(request):
    try:
        flow.fetch_token(code=request.GET.get('code'))
        credentials = flow.credentials
        
        # Guarda las credenciales en la sesión
        request.session['credentials'] = credentials_to_dict(credentials)
        logger.info("Credenciales guardadas exitosamente")
        
        return redirect('gmail_inbox')
    except Exception as e:
        logger.error(f"Error en oauth2callback: {e}")
        return HttpResponse("Error during authentication process", status=400)

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def gmail_inbox(request):
    if 'credentials' not in request.session:
        logger.info("No se encontraron credenciales, redirigiendo a autenticación")
        return redirect('gmail_auth')
    
    try:
        credentials = Credentials(**request.session['credentials'])
        
        # Verifica si el token ha expirado y refresca si es necesario
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            request.session['credentials'] = credentials_to_dict(credentials)

        service = build('gmail', 'v1', credentials=credentials)
        
        results = service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])
        
        email_list = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email_list.append({
                'id': msg['id'],
                'subject': next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'), 'No Subject'),
                'snippet': msg['snippet']
            })
        
        return render(request, 'gmail_inbox.html', {'email_list': email_list})
    except HttpError as error:
        logger.error(f"Error al acceder a Gmail: {error}")
        if error.resp.status == 401:
            # Token expirado o inválido, intentar refrescar
            del request.session['credentials']
            return redirect('gmail_auth')
        elif error.resp.status == 403:
            return HttpResponse("Permisos insuficientes para acceder a los correos", status=403)
    return HttpResponse("Error al acceder a tus correos de Gmail", status=500)

@login_required
@user_passes_test(traer.es_superusuario, login_url='acceso_denegado')
def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }