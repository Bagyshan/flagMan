from celery import shared_task
from config.celery import app
from .models import User
from django.core.mail import EmailMessage
from django.conf import settings
import re




def sanitize_email(email):
    # Убираем новые строки и пробелы в начале и конце
    return re.sub(r'[\r\n]+', '', email.strip())



@shared_task
def send_verificaation_code(application_id):
    application = User.objects.get(pk=application_id)
    email = application.email
    verification_code = application.verification_code

    subject = 'Подтвердите вашу почту'
    message = f'Уважаемый клиент, пожалуйста поддтвердите свою почту. Ваш код поддтверждения: {verification_code}'
    from_email = sanitize_email('flagman-inc@yandex.ru')
    recipient_list = [sanitize_email(email)]

    email_message = EmailMessage(subject, message, from_email, recipient_list)

    email_message.send()