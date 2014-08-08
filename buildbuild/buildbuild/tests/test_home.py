from django.test import TestCase
from django.test.client import Client

class HomePageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_home_page_request_should_return_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
