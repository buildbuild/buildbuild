from django.test import TestCase
from django.test.client import Client

from users.models import User

class LoginPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_email = "test@example.com"
        self.user_password = "test_password"
        self.invalid_password = "a"*5

        self.user = User.objects.create_user(
                email = self.user_email,
                password = self.user_password,
                )

        # need to find more eloquent way to test redirect url.
        self.TEST_SERVER_URL = "http://testserver"

    # Default Set function, These are not Unit Test function
    def post_login_set(self, user_email="", user_password="", follow = False):
        response = self.client.post(
                   "/users/login/", {
                       "email" : user_email,
                       "password" : user_password,
                       },
                       follow = follow
                   )
        return response

    # Test Code for Default Set function
    def test_post_login_set(self):
        self.post_login_set(self.user_email, self.user_password)

    def test_logout(self):
        self.post_login_set(self.user_email, self.user_password)
        self.assertRedirects(
            self.client.post("/users/logout/"),
            "/",
            301,
        )

