from django.test import TestCase
from users.models import User
from django.core.exceptions import ObjectDoesNotExist

class TestUserManager(TestCase):
    def setUp(self):
        self.user = User()
        self.valid_email = "test@example.com"
        self.valid_password = "test_password"
        self.not_created_user_email = "nouser@example.com"

    def test_user_should_be_created_via_user_manager(self):
        try:
            user = User.objects.create_user(
                    email = self.valid_email,
                    password = self.valid_password,
                    )
        except:
            self.fail("User should be created via UserManager")

    def test_get_user_should_return_user_via_user_manager(self):
        _user = User.objects.create_user(
                    email = self.valid_email,
                    password = self.valid_password,
                    )
        try:
            user = User.objects.get_user(
                    email = _user.email
                    )
        except:
            self.fail("UserManager should return user via get_user")

    def test_get_user_with_invalid_email_should_be_fail(self):
        self.assertRaises(ObjectDoesNotExist, User.objects.get_user,
                          email=self.not_created_user_email
                        )

    def test_delete_user_must_disable_is_active_via_user_manager(self):
        user = User.objects.create_user(
                    email = self.valid_email,
                    password = self.valid_password,
                    )
        User.objects.delete_user(user.email)
        user = User.objects.get_user(
                    email = self.valid_email
                )
        self.assertEqual(False, user.is_active,
                         "is_active should be False")