from django.test import TestCase
from django.test.client import Client

from users.models import User

from django.core.exceptions import ObjectDoesNotExist

from users.views import SignUp
from buildbuild import custom_msg

class SignUpPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_email = "test@example.com"
        self.user_password = "test_password"
        self.invalid_password = "a"*5

        # need to find more eloquent way to test redirect url.
        self.TEST_SERVER_URL = "http://testserver"

    # Default Set function, These are not Unit Test function
    def post_signup_set(self, user_email="", user_password="", follow=False):
        response = self.client.post(
                       "/signup/", {
                           "email" : user_email,
                           "password" : user_password,
                       },
                       follow = follow
                   )
        return response

    # Test Code for Default Set function
    def test_post_signup_set(self):
        self.post_signup_set(self.user_email, self.user_password)

    def test_get_response_to_signup_page(self):
        response = self.client.get("/signup/", follow = True)
        self.assertEqual(response.wsgi_request.path, "/signup/")
    
    def test_post_sign_up_user_must_be_unique_and_redirects_to_signup_page_and_error_message(self):
        self.post_signup_set(self.user_email, self.user_password)
        response = self.post_signup_set(self.user_email, self.user_password, follow = True)
        self.assertRedirects(response, "/signup/",)
        self.assertContains(response, custom_msg.user_already_exist)

    def test_post_available_new_user_information_redirect_to_login_page(self):
        response = self.post_signup_set(self.user_email, self.user_password, follow = True)
        self.assertRedirects(response, "/login/",)
        self.assertContains(response, custom_msg.user_signup_success)
    
    def test_post_invalid_user_password_return_signup(self):
        response = self.post_signup_set(self.user_email, self.invalid_password, follow = True)
        self.assertRedirects(response, "/signup/",)
        self.assertContains(response, custom_msg.user_invalid_password)
    
    # POST with no user information
    def test_post_signup_page_with_no_user_information_should_have_error_message(self):
        response = self.post_signup_set()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, custom_msg.this_field_is_required)

    
