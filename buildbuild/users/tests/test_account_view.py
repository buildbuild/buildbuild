from django.test import TestCase
from django.test.client import Client

from users.models import User

class TestAccountView(TestCase):
    def setUp(self):
        self.user_email = "test@test.com"
        self.user_password = "12345678"
        self.user_name = "Name Test"
        self.user_phone_number = "01012345678"

        self.invalid_user_password = "00000000"

        self.client = Client()

        self.user = User.objects.create_user(
            email=self.user_email,
            password=self.user_password,
            name = self.user_name,
            phonenumber=self.user_phone_number
        )

    def test_after_login_can_move_account_page(self):
        self.client.post("/login/", {
            "email": self.user_email,
            "password": self.user_password,
            })
        response = self.client.get("/account/")
        self.assertEqual(response.status_code, 200)

    def test_invalid_login_can_not_move_account_page(self):
        self.client.post("/login/", {
            "email": self.user_email,
            "password": self.invalid_user_password,
            })
        response = self.client.get("/account/")
        self.assertEqual(response.status_code, 302)
        #If login is success, login redirect must not be happen

    def test_account_page_should_contain_user_info(self):
        self.client.post("/login/", {
            "email": self.user_email,
            "password": self.user_password,
            })
        response = self.client.get("/account/")
        self.assertContains(response, self.user_email)
        self.assertContains(response, self.user_name)
        self.assertContains(response, self.user_phone_number)