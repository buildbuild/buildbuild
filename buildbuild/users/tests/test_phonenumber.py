from django.test import TestCase
from users.models import User

from django.core.exceptions import ValidationError


class UserPhonenumberTest(TestCase):
    def setUp(self):
        self.user = User()
        self.valid_email = "test@example.com"
        self.valid_password = "test_password"

        self.numeric_phonenumber = "1" * 30
        self.hyphen_contained_phonenumber = "123-456-789"
        self.only_hyphen_phonenumber = "-" * 30
        self.invalid_too_short_phonenumber = "1" * 7
        self.invalid_too_long_phonenumber = "1" * 31
        self.invalid_not_digit_phonenumber = "1234567a"

    def test_user_should_have_phonenumber_field(self):
        self.assertIsNotNone(self.user.phonenumber)

    def test_user_with_too_short_phonenumber(self):
        self.assertRaises(ValidationError, User.objects.create_user,
                          email=self.valid_email,
                          password=self.valid_password,
                          phonenumber=self.invalid_too_short_phonenumber)

    def test_user_too_long_phonenumber(self):
        self.assertRaises(ValidationError, User.objects.create_user,
                          email=self.valid_email,
                          password=self.valid_password,
                          phonenumber=self.invalid_too_long_phonenumber)

    def test_user_with_digit_should_not_be_valid(self):
        self.assertRaises(ValidationError, User.objects.create_user,
                            email=self.valid_email,
                            password=self.valid_password,
                            phonenumber=self.invalid_not_digit_phonenumber)
