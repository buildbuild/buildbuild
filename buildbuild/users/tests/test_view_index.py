from django.test import TestCase
from django.test.client import Client

from users.models import User


class TestViewIndex(TestCase):
    def setUp(self):
        self.first_user = User.objects.create_user(
            email = "test_first_user@example.com",
            password = "test_password",
        )
        self.second_user = User.objects.create_user(
            email = "test_second_user@example.com",
            password = "test_password",
        )
        self.client = Client()

    def test_get_user_index_request_should_return_200(self):
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 200)

    def test_get_user_index_page_should_contain_user_email(self):
        response = self.client.get("/users/")
        self.assertContains(response, self.first_user.email)
        self.assertContains(response, self.second_user.email)
