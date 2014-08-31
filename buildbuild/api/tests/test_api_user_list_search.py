from django.test import TestCase
from django.test.client import Client

from users.models import User


class TestAPIUserListSearch(TestCase):
    def setUp(self):
        self.test_string = "test_string"
        self.user_with_test_string = User.objects.create_user(
            email="test_user_with_" + self.test_string + "@example.com",
            password="test_password",
        )
        self.user_without_test_string = User.objects.create_user(
            email="test_user@example.com",
            password="test_password",
        )

        self.client = Client()
        self.response = self.client.get("/api/users/?search=" + self.test_string)

    def test_api_user_list_search_should_return_valid_result(self):
        self.assertContains(self.response, self.user_with_test_string.email)
        self.assertNotContains(self.response, self.user_without_test_string.email)
