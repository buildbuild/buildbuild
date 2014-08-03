from django.test import TestCase
from users.models import User

from django.core.exceptions import ValidationError


class UserPhonenumberTest(TestCase):
    def setUp(self):
        self.user = User()
        self.valid_email = "test@example.com"
        self.valid_password = "test_password"

        self.valid_phonenumber = "12345678"
        self.invalid_short_phonenumber = "1234567"
        self.invalid_not_digit_phonenumber = "1234567a"

    def test_user_should_have_phonenumber_field(self):
        try:
            self.user.phonenumber
        except AttributeError:
            self.fail("User should have phonenumber field")

    def test_user_phonenumber_is_at_least_8_digit(self):
        self.user.phonenumber = self.valid_phonenumber
        self.assertGreaterEqual(len(self.user.phonenumber), 8, "phone number is less than 8")

    def test_user_with_short_phonenumber_should_not_be_valid(self):
        self.assertRaises(ValidationError, User.objects.create_user,
                          email=self.valid_email,
                          password=self.valid_password,
                          phonenumber=self.invalid_short_phonenumber)

    def test_user_with_digit_should_not_be_valid(self):
        self.assertRaises(ValidationError, User.objects.create_user,
                            email=self.valid_email,
                            password=self.valid_password,
                            phonenumber=self.invalid_not_digit_phonenumber)