from django.test import TestCase
from users.models import User

from django.db import IntegrityError
from django.core.exceptions import ValidationError

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User()
        self.valid_email = "username@organization.org"
        self.valid_password = "foobar"
        pass

    # Email
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
        self.assertRaises(ValidationError, User.users.create_user,
                email = "INVALID_EMAIL",
                password = self.valid_password
                )

    # Password
    def test_user_should_have_password_field(self):
        try:
            self.user.password
        except AttributeError:
            self.fail("User should have password field")

    def test_user_with_short_password_should_not_be_valid(self):
        self.assertRaises(ValidationError, User.users.create_user,
                email = self.valid_email,
                password = "foo" )

    # is_admin
    def test_user_with_no_is_admin_args_shoud_not_be_admin(self):
        user = User.users.create_user(
                email = self.valid_email,
                password = self.valid_password,
                )
        self.assertFalse(user.is_admin)

    def test_user_with_is_admin_args_shoud_be_admin(self):
        user = User.users.create_user(
                email = self.valid_email,
                password = self.valid_password,
                is_admin = True,
                )
        self.assertTrue(user.is_admin)

    # is_active
    def test_user_with_no_is_active_args_shoud_be_active(self):
        user = User.users.create_user(
                email = self.valid_email,
                password = self.valid_password,
                )
        self.assertTrue(user.is_active)

    def test_user_model_should_have_deactivate_method(self):
        active_user = User.users.create(
                email = self.valid_email,
                password = self.valid_password,
                # default value for is_active is True
                )
        deactivated_user = active_user.deactivate()
        self.assertFalse(deactivated_user.is_active)

    def test_user_model_should_have_activate_method(self):
        deactive_user = User.users.create(
                email = self.valid_email,
                password = self.valid_password,
                is_active = False,
                )
        activated_user = deactive_user.activate()
        self.assertTrue(activated_user.is_active)

    # name
    def test_user_with_name_args_shoud_have_name(self):
        valid_name = "USERNAME"
        user = User.users.create_user(
                email = self.valid_email,
                password = self.valid_password,
                name = valid_name
                )
        self.assertEqual(valid_name, user.name)

    # UserManager
    def test_user_should_be_created_via_user_manager(self):
        try:
            user = User.users.create_user(
                    email = self.valid_email,
                    password = self.valid_password,
                    )
        except:
            self.fail("User should be created via UserManager")

    def test_user_password_should_be_encrypted(self):
        user = User.users.create_user( email = self.valid_email, password = self.valid_password )
        self.assertNotEqual(self.valid_password, user.password)

    # check phone number
    def test_user_should_have_phonenumber_field(self):
        try:
            self.user.phonenumber
        except AttributeError:
            self.fail("User should have phonenumber field")

    def test_user_phonenumber_is_at_least_8_digit(self):
        self.user.phonenumber = "12345678"
        self.assertGreaterEqual(len(self.user.phonenumber),8,"phone number is less than 8")

    def test_user_with_short_phonenumber_should_not_be_valid(self):
        self.assertRaises(ValidationError, User.users.create_user,
                email = self.valid_email,
                password = self.valid_password,
                phonenumber = "1234567")


