from django.test import TestCase
from django.test.client import Client

from users.models import User

class LoginPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.valid_email = "test@example.com"
        self.valid_password = "test_password"

        self.user = User.objects.create_user(
                email = self.valid_email,
                password = self.valid_password,
                )

        # need to find more eloquent way to test redirect url.
        self.TEST_SERVER_URL = "http://testserver"

    def test_get_login_page_request_should_return_200(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    # POST with valid user information
    def test_post_login_page_with_valid_user_information_should_return_302(self):
        response = self.client.post("/login/", {
            "email": self.valid_email,
            "password": self.valid_password,
            })
        self.assertEqual(response.status_code, 302)

    def test_post_login_page_with_valid_user_information_should_redirect_to_home(self):
        response = self.client.post("/login/", {
            "email": self.valid_email,
            "password": self.valid_password,
            })
        self.assertEqual(response["Location"], self.TEST_SERVER_URL + "/")

    # POST with invalid user information
    def test_post_login_page_with_invalid_user_information_should_return_302(self):
        response = self.client.post("/login/", {
            "email": self.valid_email,
            "password": "foobar",
            })
        self.assertEqual(response.status_code, 302)

    def test_post_login_page_with_invalid_user_information_should_redirect_to_login(self):
        response = self.client.post("/login/", {
            "email": self.valid_email,
            "password": "foobar",
            })
        self.assertEqual(response["Location"], self.TEST_SERVER_URL + "/login/")
