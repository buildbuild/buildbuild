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

    def test_get_signup_page_request_should_return_200(self):
        response = self.client.get("/signup/")
        self.assertEqual(response.status_code, 200)
    
    def test_check_uniqueness_of_new_user_information_from_signup_page(self):
        User.objects.create_user(self.valid_email, self.valid_password)

        try:
            response = self.client.post("/signup/", {
                "email":self.valid_email,
                "password":self.valid_password,
                })
        except:
            pass
    
    def test_post_signup_page_with_available_new_user_information_should_return_302(self):
        response = self.client.post("/signup/", {
            "email": self.valid_email,
            "password": self.valid_password,
            })
        self.assertEqual(response.status_code, 302)
    
    def test_post_signup_page_with_available_user_information_should_redirect_to_home(self):
        response = self.client.post("/signup/", {
            "email": self.valid_email,
            "password": self.valid_password,
            })
        self.assertEqual(response["Location"], self.TEST_SERVER_URL + "/")
   
    def test_post_signup_page_with_non_available_user_information_should_return_302(self):
        response = self.client.post("/signup/", {
            "email": self.valid_email,
            "password": self.invalid_password,
            })
        self.assertEqual(response.status_code, 302)
    
    def test_post_signup_page_with_non_available_user_information_should_redirect_to_signup(self):
        response = self.client.post("/signup/", {
            "email": self.valid_email,
            "password": self.invalid_password,
            })
        self.assertEqual(response["Location"], self.TEST_SERVER_URL + "/signup/")
    
    # POST with no user information
    def test_post_signup_page_with_no_user_information_should_have_error_message(self):
        response = self.client.post("/signup/", {})
        self.assertContains(response, "This field is required.")
    
