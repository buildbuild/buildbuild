from django.test import TestCase
from users.models import User
from django.core.exceptions import ValidationError

class UserNameTest(TestCase):
    def setUp(self):
        self.user = User()
        self.valid_email = "test@example.com"
        self.valid_password = "test_password"
        self.valid_name = "test_username"
        self.over_length_name = "aaaabbbbccccddddeeeef"
        self.invalid_name ="invalid_name1"

    def test_user_should_have_name_field(self):
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

    def test_name_with_more_than_21_character_should_not_be_allowed(self):
        self.assertRaises(ValidationError, User.objects.create_user,
                          email = self.valid_email,
                          password = self.valid_password,
                          name = self.over_length_name)

    def test_name_without_character_should_not_be_allowed(self):
        self.assertRaises(ValidationError, User.objects.create_user,
                          email = self.valid_email,
                          password = self.valid_password,
                          name = self.invalid_name)
