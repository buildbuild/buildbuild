from django.test import TestCase
from django.test.client import Client

from users.models import User

class TestViewShow(TestCase):
    def setUp(self):
        pass

    def test_get_user_show_with_valid_user_id_request_should_return_200(self):
        pass
