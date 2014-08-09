from users.views import ListAllView, home
from django.test import TestCase
from django.test.client import RequestFactory
from django.test import Client

class HomeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.invalid_url = '/invalid'
        self.client = Client()

    def test_home_page_should_be_succeed_with_root_url(self):
        request = self.factory.get('/')
        response = home(request)

        self.assertEqual(response.status_code, 200,
                         "Root Page should be redirected to home")

    def test_users_root_should_be_loaded(self):
        request = self.factory.get('/users')
        response = home(request)

        self.assertEqual(response.status_code, 200,
                         "/users/ Page should be redirected to home")


    def test_invalid_url_should_not_be_redirected_to_home(self):
        response = self.client.get(self.invalid_url)

        self.assertEqual(response.status_code, 404,
                        "Wrong Page should be not redirected to home Response Code : " + str(response.status_code))

