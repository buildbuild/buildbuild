from django.test import TestCase
from users.models import User

class UserNameTest(TestCase):
    def setUp(self):
        self.user = User()
        self.valid_email = "test@example.com"
        self.valid_password = "test_password"
        self.valid_name = "test_username"

    def test_user_should_have_test_field(self):
        try:
            self.user.name
        except AttributeError:
            self.fail("User should have name field")

    def test_user_with_name_args_shoud_have_name(self):
        user = User.objects.create_user(
                email = self.valid_email,
                password = self.valid_password,
                name = self.valid_name
                )
        self.assertEqual(self.valid_name, user.name)
