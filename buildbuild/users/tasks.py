from __future__ import absolute_import

from django.core.mail import send_mail
from django.conf import settings
from celery import Celery

app = Celery('users')

@app.task(name="send_mail_to_new_user_using_celery", bind=True)
def send_mail_to_new_user_using_celery(self):
    is_send_mail_correctly = send_mail(
        settings.SUBJECT, 
        settings.CONTENTS, 
        settings.EMAIL_HOST_USER, 
        ['buidlbuild@gmail.com'], fail_silently=False
        )
    return is_send_mail_correctly

@app.task(name='add', bind=True)
def print_print(self):
    print "gogo celery"
