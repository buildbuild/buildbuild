from django.test import TestCase
from django.test.client import Client

class TestViewIndex(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_user_index_request_should_return_200(self):
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 200)
