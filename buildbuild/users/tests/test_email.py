from django.test import TestCase
from users.models import User

from django.db import IntegrityError
from django.core.exceptions import ValidationError

class UserEmailTest(TestCase):
    def setUp(self):
        self.user = User()
        self.valid_email = "test@example.com"
        self.valid_password = "test_password"

    def test_user_should_have_email_field(self):
        try:
            self.user.email
        except AttributeError:
            self.fail("User should have email field")

    def test_user_email_should_not_be_blank(self):
        self.user.email = ""
        self.user.password = self.valid_password
        self.assertRaises(ValueError, self.user.save())

    def test_user_should_have_unique_email(self):
        self.user.email = self.valid_email
        self.user.password = self.valid_password
        self.user.save()

        user_with_duplicate_email = User(email = self.user.email, password = self.valid_password)

        self.assertRaises(IntegrityError, user_with_duplicate_email.save)

    def test_user_with_invalid_email_should_not_be_valid(self):
        self.assertRaises(ValidationError, User.objects.create_user,
                email = "INVALID_EMAIL",
                password = self.valid_password
                )
