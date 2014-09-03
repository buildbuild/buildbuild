from django.test import TestCase
from django.test.client import Client

from users.models import User


class TestAPIUserList(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="test_password",
        )
        self.client = Client()
        self.response = self.client.get("/api/users/")

    def test_api_user_list_request_should_return_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_api_user_list_request_should_return_json(self):
        self.assertEqual(self.response["Content-Type"], "application/json")

    def test_api_user_list_request_should_contain_user_id_and_email(self):
        self.assertContains(self.response, self.user.id)
        self.assertContains(self.response, self.user.email)
