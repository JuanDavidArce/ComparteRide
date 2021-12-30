"""Celery tasks"""


# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone


# Models
from cride.users.models import User
from time import sleep


# Celery
from celery.decorators import task


# Utilities
from datetime import timedelta
import jwt


def gen_verification_token(user):
    """Create JWT token that the user can use to verify ist account"""
    exp_date = timezone.now() + timedelta(days=3)
    payload = {
        'user':user.username,
        'exp':int(exp_date.timestamp()),
        'type':'email_confirmation',

    }

    token = jwt.encode(payload, settings.SECRET_KEY,algorithm='HS256')
    return token.decode()
 
@task(name='send_confirmation_email',max_retries=3)
def send_confirmation_email(user_pk):
    """Send account verification link to given user"""
    for i in range(30):
        sleep(1)
        print('sleeping',str(i+1))
    user= User.objects.get(pk =user_pk)
    verification_token = gen_verification_token(user)
    subject='Welcome @{}! Verify your account to start using Comparte Ride'.format(user.username)
    from_email= 'comparte Ride <noreply@comparteride.com>'
    content = render_to_string('emails/users/account_verification.html',{'token':verification_token,'user':user})
    msg = EmailMultiAlternatives(subject,content,from_email,[user.email])
    msg.attach_alternative(content,"text/html")
    msg.send()


