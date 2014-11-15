from django.test import TestCase
from django.test.client import Client

from users.models import User

class TestAccountView(TestCase):
    def setUp(self):
        self.user_email = "test@test.com"
        self.user_password = "12345678"
        self.user_name = "Name_Test"
        self.user_phone_number = "01012345678"

        self.invalid_user_password = "00000000"

        self.client = Client()

        self.user = User.objects.create_user(
            email=self.user_email,
            password=self.user_password,
            name = self.user_name,
            phonenumber=self.user_phone_number
        )
    # Default Set function, These are not Unit Test function
    def post_login_set(self, user_email="", user_password="", follow = False):
        response = self.client.post(
                   "/login/", {
                       "email" : user_email,
                       "password" : user_password,
                       },
                       follow = follow
                   )
        return response

    # Test Code for Default Set function
    def test_post_login_set(self):
        self.post_login_set(self.user_email, self.user_password)

    def test_after_login_can_move_account_page(self):
        self.post_login_set(self.user_email, self.user_password)
        response = self.client.get("/users/account/")
        self.assertEqual(response.status_code, 200)

    def test_invalid_login_can_not_move_account_page(self):
        self.post_login_set(self.user_email, self.invalid_user_password)
        response = self.client.get("/users/account/")
        self.assertEqual(response.status_code, 302)
        #If login is success, login redirect must not be happen

    def test_account_page_should_contain_user_info(self):
        self.post_login_set(self.user_email, self.user_password)
        response = self.client.get("/users/account/")
        self.assertContains(response, self.user_email)
        self.assertContains(response, self.user_name)
        self.assertContains(response, self.user_phone_number)

    def test_non_login_user_should_get_result_next_parameter(self):
        response = self.client.get("/users/account/")
        self.assertEqual(str(response.url), "http://testserver/login/?next=/users/account/")

    def test_after_login_user_should_redirect_to_account_page(self):
        self.post_login_set(self.user_email, self.user_password)
        response = self.client.post("/login/?next=/users/account/", {
            "email": self.user_email,
            "password": self.user_password,
            })
        self.assertEqual(str(response.url), "http://testserver/users/account/")

