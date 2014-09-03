from django.test import TestCase
from django.test.client import Client

from users.models import User

from users.views import SignUp
from django.core import mail
from django.conf import settings

from django.db.utils import OperationalError

from users import tasks

class Send_Email_Test(TestCase):
    def setUp(self):
        self.client = Client()
        self.valid_email = "test@example.com"
        self.valid_password = "test_password"
        self.invalid_password = "a"*5
        self.invalid_email = "invalid@gmail.com"

        self.user = User.objects.create_user(
                email = self.valid_email,
                password = self.valid_password
                )

    def test_send_mail_to_new_user_using_celery(self):
        self.assertTrue(tasks.send_mail_to_new_user.delay(self.user))

    def test_send_mail_to_new_user(self):
        mail.outbox = []
        mail.send_mail(
                settings.SUBJECT,
                settings.CONTENTS,
                self.valid_email,
                [self.valid_email],
                fail_silently=False
                )
 
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, settings.SUBJECT)

    def test_invalid_email_name_cannot_send_mail(self):
        mail.outbox = []
        mail.send_mail(
                settings.SUBJECT,
                settings.CONTENTS,
                self.invalid_email,
                [self.valid_email],
                fail_silently=False
                )
                
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

