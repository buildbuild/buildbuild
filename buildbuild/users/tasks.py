from __future__ import absolute_import

from django.core.mail import send_mail
from django.conf import settings
from celery import Celery

users = Celery('users')

@users.task(name="send_mail_to_new_user_using_celery", bind=True)
def send_mail_to_new_user(self, user):
    is_send_mail_correctly = send_mail(
        settings.SUBJECT, 
        settings.CONTENTS, 
        settings.EMAIL_HOST_USER, 
        [user.email], fail_silently=False
        )
    return is_send_mail_correctly

