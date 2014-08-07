from django.test import TestCase
from django.test import Client
from django.test.client import RequestFactory
from users.models import User
from users.views import ListOneView

class ListOneViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email = "user@example.com",
            password = '12345678',
            name = 'first',
            phonenumber = '01011111111'
        )
        self.no_saved_user = User()
        self.no_saved_user.email = "no@example.com"
        self.no_saved_user.password = '12341234'
        self.factory = RequestFactory()
        self.url = '/users/list/'

    def test_list_one_should_not_be_loaded_with_invalid_user(self):
        pass
        request = self.factory.get(self.url, {'email':self.no_saved_user.email})
        request.user = self.no_saved_user
        response = ListOneView.as_view()(request)
        self.assertEqual(response.status_code, 404)