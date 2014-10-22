from django.test import TestCase
from django.test.client import Client

from users.models import User

class LoginPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.valid_email = "test@example.com"
        self.valid_password = "test_password"
        self.invalid_password = "a"*5

        self.user = User.objects.create_user(
                email = self.valid_email,
                password = self.valid_password,
                )

        # need to find more eloquent way to test redirect url.
        self.TEST_SERVER_URL = "http://testserver"

    def test_logout(self):
        self.client.post("/login/", {
            "email": self.valid_email,
            "password": self.valid_password,
            })
        self.assertRedirects(
            self.client.post("/logout/"),
            "/",
            301,
        )

