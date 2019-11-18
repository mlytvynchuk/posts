from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes

from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token
from news.celery import app
from django.contrib.auth import get_user_model




@app.task
def send_email_confirmation(user_id):
    UserModel = get_user_model()
    user = UserModel.objects.filter(pk=user_id).first()
    message = render_to_string('email/acc_active_email.html', {
                'user': user,
                'domain': 'localhost:8000',
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
    subject = "Email Confirmation on NEWS"
    email = EmailMessage(subject, message, to=[user.email])
    email.send()
