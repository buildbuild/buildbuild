from django.test import TestCase
from users.models import User

from django.core.exceptions import ValidationError

class UserPasswordTest(TestCase):
    def setUp(self):
        self.user = User()
        self.valid_email = "test@example.com"
        self.valid_password = "123456"
        self.invalid_password = "12345"

    def test_user_should_have_password_field(self):
        try:
            self.user.password
        except AttributeError:
            self.fail("User should have password field")

    def test_user_password_is_at_least_6_digit(self):
        self.user.password = self.valid_password
        self.assertGreaterEqual(len(self.user.password),6,"phone number is less than 6")

    def test_user_with_short_password_should_not_be_valid(self):
        self.assertRaises(ValidationError, User.objects.create_user,
                email = self.valid_email,
                password = self.invalid_password )

    def test_user_password_should_be_encrypted(self):
        user = User.objects.create_user( email = self.valid_email, password = self.valid_password )
        self.assertNotEqual(self.valid_password, user.password)
