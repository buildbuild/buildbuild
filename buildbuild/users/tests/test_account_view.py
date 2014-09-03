from django.test import TestCase
from django.test.client import Client

class TestAccountView(TestCase):
    def setUp(self):
        self.user_email = "test@test.com"
        self.user_password = "12345678"
        self.user_name = "Name Test"
        self.user_phone_number = "01012345678"

        self.client = Client()