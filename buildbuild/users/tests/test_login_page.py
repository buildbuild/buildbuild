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

    def test_get_login_return_200(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    # POST with valid user information
    def test_post_with_valid_user_redirects_main_page_with_code_302(self):
        self.assertRedirects(
            self.client.post(
                "/login/", {
                    "email": self.valid_email,
                    "password": self.valid_password,
                }
            ),
            "/",
        )

    def test_post_with_invalid_user_redirects_to_login_with_code_302(self):
        self.assertRedirects(
            self.client.post(
                "/login/", {
                    "email": self.valid_email,
                    "password": self.invalid_password,
                }
            ),
            "/login/",
        )

    def test_post_with_no_user_information_error_message(self):
        response = self.client.post("/login/", {})
        self.assertContains(response, "This field is required.")

    def test_post_login_page_with_email_and_without_password_should_have_error_message(self):
        response = self.client.post("/login/", {
            "email": self.valid_email,    
        })
        self.assertContains(response, "This field is required.")

    def test_post_login_page_with_password_and_without_email_should_have_error_message(self):
        response = self.client.post("/login/", {
            "password": self.valid_password,
        })
        self.assertContains(response, "This field is required.")

