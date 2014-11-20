from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory

from buildbuild.views import Home

from users.models import User

class HomePageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user_email = "test@example.com"
        self.user_password = "test_password"
        self.user = User.objects.create_user(
                    email = self.user_email,
                    password = self.user_password,
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

    def test_get_home_page_with_login_should_return_200(self):
        self.post_login_set(self.user_email, self.user_password)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_get_home_page_without_login_should_return_302_and_redirect_to_login_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?next=/")

    def test_home_page_with_no_user_session_should_have_login_text(self):
        response = self.client.get("/")
        # self.assertContains(response, "login")

    def test_home_page_with_user_session_should_have_logout_text(self):
        request = self.factory.get("/")
        request.user = self.user
        view = Home.as_view()
        response = view(request)

        self.assertContains(response, "logout")
