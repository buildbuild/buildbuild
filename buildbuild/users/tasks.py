from __future__ import absolute_import

from django.core.mail import send_mail
from django.core import mail
from django.conf import settings
from celery import Celery
from celery import shared_task
from django.db import OperationalError

@shared_task
def send_mail_to_new_user(user):
    try:
        mail.send_mail(
            settings.SUBJECT, 
            settings.CONTENTS, 
            settings.EMAIL_HOST_USER, 
            [user.email], fail_silently=False
        )
    except:
        # For exception handling of views.py 
        raise OpertionalError("send mail with celery failed")
    return mail

