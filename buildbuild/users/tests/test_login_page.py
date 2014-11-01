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

        self.this_field_is_required =  "This field is required."
        self.user_login_success = "Successfully Login"
        self.user_invalid_password = "ERROR : invalid user password"
        self.user_invalid = "ERROR : invalid email or password"

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

    def test_get_login_return_200(self):
        response = self.client.get("/users/login/")
        self.assertEqual(response.status_code, 200)

    # POST with valid user information
    def test_post_with_valid_user_redirects_main_page_with_message(self):
        response = self.post_login_set(self.user_email, self.user_password, follow = True)
        self.assertRedirects(response, "/",)
        self.assertContains(response, self.user_login_success)

    def test_post_with_invalid_password_redirects_to_login_with_message(self):
        response = self.post_login_set(self.user_email, self.invalid_password, follow = True)
        self.assertRedirects(response, "/users/login/",)
        self.assertContains(response, self.user_invalid)

    def test_post_with_no_user_information_error_message(self):
        response = self.post_login_set()
        self.assertContains(response, self.this_field_is_required)

    def test_post_login_page_with_email_and_without_password_should_have_error_message(self):
        response = self.post_login_set(user_email = self.user_email)
        self.assertContains(response, self.this_field_is_required)

    def test_post_login_page_with_password_and_without_email_should_have_error_message(self):
        response = self.post_login_set(user_password = self.user_password)
        self.assertContains(response, self.this_field_is_required)

