from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory

from buildbuild.views import Home

from users.models import User

class HomePageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
                    email = "test@example.com",
                    password = "test_password",
                )

    def test_get_home_page_request_should_return_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_with_no_user_session_should_have_login_text(self):
        response = self.client.get("/")
        self.assertContains(response, "login")

    def test_home_page_with_user_session_should_have_logout_text(self):
        request = self.factory.get("/")
        request.user = self.user
        view = Home.as_view()
        response = view(request)

        self.assertContains(response, "logout")
