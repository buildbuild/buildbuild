from django.test import TestCase
from users.models import User

from django.core.exceptions import ValidationError

class UserPasswordTest(TestCase):
    def setUp(self):
        self.user = User()
        self.valid_email = "test@example.com"
        self.valid_password = "123456"
        self.too_short_password = "a" * 5
        self.too_long_password = "a" * 256

    def test_user_should_have_password(self):
        self.assertIsNotNone(self.user.password)

    def test_user_password_validate(self):
        self.user.password = self.valid_password
        self.assertGreaterEqual(
            len(self.user.password),
            6,
            "phone number is less than 6",
        )

    def test_user_password_too_short(self):
        self.assertRaises(
            ValidationError, 
            User.objects.create_user,
            email = self.valid_email,
            password = self.too_short_password
        )

    def test_user_password_too_long(self):
        self.assertRaises(
            ValidationError, 
            User.objects.create_user,
            email = self.valid_email,
            password = self.too_long_password
        )

    def test_user_password_should_be_encrypted(self):
        user = User.objects.create_user(
            email = self.valid_email, 
            password = self.valid_password
        )
        self.assertNotEqual(self.valid_password, user.password)
