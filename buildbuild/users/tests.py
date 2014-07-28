from django.test import TestCase
from users.models import User
from django.db import IntegrityError

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User()
        pass

    # Email
    def test_user_should_have_email_field(self):
        try:
            self.user.email
        except AttributeError:
            self.fail("User should have email field")

    def test_user_should_have_unique_email(self):
        unique_email = "username@organization.org"
        self.user.email = unique_email
        self.user.save()

        user_with_duplicate_email = User(email = self.user.email)
        self.assertRaises(IntegrityError, user_with_duplicate_email.save)

    # Password
    def test_user_should_have_password_field(self):
        try:
            self.user.password
        except AttributeError:
            self.fail("User should have password field")
