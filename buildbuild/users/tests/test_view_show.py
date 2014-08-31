from django.test import TestCase
from django.test.client import Client

from users.models import User

class TestViewShow(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email = "test_user@example.com",
            password = "test_password",
        )
        self.client = Client()

    def test_get_user_show_with_valid_user_id_request_should_return_200(self):
        response = self.client.get("/users/" + str(self.user.id))
        self.assertEqual(response.status_code, 200)

    def test_get_user_show_with_valid_user_id_should_contain_user_info(self):
        response = self.client.get("/users/" + str(self.user.id))
        self.assertContains(response, self.user.email)
        self.assertContains(response, self.user.password)
