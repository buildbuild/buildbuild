from django.test import TestCase
from django.test.client import Client

from users.models import User

from django.core.exceptions import ObjectDoesNotExist

from users.views import SignUp

class SignUpPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.valid_email = "test@example.com"
        self.valid_password = "test_password"
        self.invalid_password = "a"*5

        # need to find more eloquent way to test redirect url.
        self.TEST_SERVER_URL = "http://testserver"

    def test_get_response_to_signup_page(self):
        response = self.client.get("/signup/", follow = True)
        self.assertEqual(response.wsgi_request.path, "/signup/")
    
    def test_post_sign_up_user_must_be_unique(self):
        User.objects.create_user(self.valid_email, self.valid_password)
        self.assertRedirects(
            self.client.post(
                "/signup/", {
                    "email":self.valid_email,
                    "password":self.valid_password,
                }
            ),
            "/",
        )
    
    def test_post_available_new_user_information_redirect_to_login_page(self):
        self.assertRedirects(
            self.client.post(
                "/signup/", {
                    "email":self.valid_email,
                    "password":self.valid_password,
                }
            ),
            "/login/",
        )
  
    def test_post_invalid_user_information_return_signup(self):
        self.assertRedirects(
            self.client.post(
                "/signup/", {
                    "email":self.valid_email,
                    "password":self.invalid_password,
                }
            ),
            "/signup/",
        )

    # POST with no user information
    def test_post_signup_page_with_no_user_information_should_have_error_message(self):
        response = self.client.post("/signup/", {})
        self.assertContains(response, "This field is required.")
    
