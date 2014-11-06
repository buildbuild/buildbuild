from django.test import TestCase
from keystoneclient.v2_0 import client
from keystoneclient import exceptions

class KeystoneClientTest(TestCase):
    def setUp(self):
        self.auth_url = 'http://61.43.139.143:5000/v2.0'
        self.token = '0120b90111df48feb5c727081afb859f'
        self.endpoint = 'http://61.43.139.143:35357/v2.0'

    def test_keystone_object_should_be_created_successfully(self):
        keystone = client.Client(auth_url=self.auth_url,
                                 token=self.token,
                                 endpoint=self.endpoint)

        self.assertIsNone(keystone.auth_ref)

    def test_keystone_object_without_auth_url_should_be_arise_error(self):
        self.assertRaises(exceptions.AuthorizationFailure,
                          client.Client,
                          token = self.token)