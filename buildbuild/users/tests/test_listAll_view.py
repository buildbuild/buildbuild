from users.views import ListAllView, home
from django.test import TestCase
from django.test.client import RequestFactory
from django.test import Client
from users.models import User,UserManager

class ListAllViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.first_user = User()
        self.first_user.email = "first@example.com"
        self.first_user.password='12345678'
        self.first_user.phonenumber='01011111111'
        self.first_user.name='first'
        self.second_user = User()
        self.second_user.email = "second@example.com"
        self.second_user.password='12345678'
        self.second_user.phonenumber='01022222222'
        self.second_user.name='second'
        self.listAll_url = '/users/list/'

    def test_list_all_should_be_loaded_with_proper_url_with_user(self):
        self.first_user.save(using = User.objects._db)
        response = self.client.get(self.listAll_url)
        self.assertEqual(response.status_code, 200,
                         "Response Code should be 200(OK)")

    def test_list_all_should_raise_404_with_no_users(self):
        response = self.client.get(self.listAll_url)
        self.assertEqual(response.status_code, 404,
                         "Response Code should be 404(NOT FOUND) with no users in DB")

    def test_list_all_should_contain_user_with_saved_one_user(self):
        self.first_user.save(using = User.objects._db)
        response = self.client.get(self.listAll_url)
        self.assertContains(response,self.first_user.email)
        self.assertContains(response,self.first_user.name)
        self.assertContains(response,self.first_user.phonenumber)

    def test_list_all_should_contain_user_with_saved_two_user(self):
        self.first_user.save(using = User.objects._db)
        self.second_user.save(using = User.objects._db)
        response = self.client.get(self.listAll_url)
        self.assertContains(response,self.first_user.email)
        self.assertContains(response,self.first_user.name)
        self.assertContains(response,self.first_user.phonenumber)
        self.assertContains(response,self.second_user.email)
        self.assertContains(response,self.second_user.name)
        self.assertContains(response,self.second_user.phonenumber)