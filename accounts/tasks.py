from celery import shared_task
from config.celery import app
from .models import User
from django.core.mail import EmailMessage
from django.conf import settings
import re
from django.core.mail import send_mail




def sanitize_email(email):
    # Убираем новые строки и пробелы в начале и конце
    return re.sub(r'[\r\n]+', '', email.strip())



@shared_task
def send_verificaation_code(application_id):

    try:
        application = User.objects.get(pk=application_id)
    except User.DoesNotExist:
        return
    
    email = application.email
    verification_code = application.verification_code

    subject = 'Подтвердите вашу почту'
    message = f'Уважаемый клиент, пожалуйста поддтвердите свою почту. Ваш код поддтверждения: {verification_code}'
    from_email = sanitize_email('flagman-inc@yandex.ru')
    recipient_list = [sanitize_email(email)]

    email_message = EmailMessage(subject, message, from_email, recipient_list)

    email_message.send(fail_silently=False)


@shared_task
def send_password_reset_code(user_id):
    user = User.objects.get(id=user_id)
    subject = 'Восстановление пароля'
    message = f'Ваш код восстановления: {user.password_reset_code}'
    from_email = sanitize_email('flagman-inc@yandex.ru')
    send_mail(subject, message, sanitize_email(from_email), [sanitize_email(user.email)])


@shared_task
def send_verificaation_code_to_new_email(user_id):
    user = User.objects.get(id=user_id)
    from_email = 'flagman-inc@yandex.ru'
    if user.new_email:
        send_mail(
            'Подтверждение нового email',
            f'Ваш код подтверждения: {user.new_email_verification_code}',
            sanitize_email(from_email),
            [user.new_email],
        )


import firebase_admin
from firebase_admin import credentials, messaging
from config.settings import FIREBASE_CREDENTIALS_PATH
import os
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import json
from celery import shared_task


# firebase_app = None

# def initialize_firebase():
#     global firebase_app
#     if not firebase_app:
#         cred_path = FIREBASE_CREDENTIALS_PATH
#         cred = credentials.Certificate(cred_path)
#         firebase_app = firebase_admin.initialize_app(cred)

# def send_fcm_notification(token, title, body, data=None):
#     initialize_firebase()

#     message = messaging.Message(
#         notification=messaging.Notification(
#             title=title,
#             body=body,
#         ),
#         token=token,
#         data=data or {},
#     )

#     response = messaging.send(message)
#     return response


SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']

# Загружаем путь к service account из настроек
SERVICE_ACCOUNT_FILE = FIREBASE_CREDENTIALS_PATH

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    credentials.refresh(Request())
    return credentials.token


@shared_task
def send_fcm_notification_task(token, title, body, data=None):
    access_token = get_access_token()

    message = {
        "message": {
            "token": token,
            "notification": {
                "title": title,
                "body": body,
            },
            "data": data or {}
        }
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; UTF-8",
    }

    project_id = json.load(open(SERVICE_ACCOUNT_FILE))['project_id']
    url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"

    response = requests.post(url, headers=headers, json=message)

    if response.status_code != 200:
        print(f"🔥 Ошибка при отправке уведомления: {response.status_code}, {response.text}")
    print(f"✅ Уведомление отправлено: {response.json()}")

    return response.json()