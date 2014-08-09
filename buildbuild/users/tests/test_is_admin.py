from django.test import TestCase
from users.models import User

class UserIsAdminTest(TestCase):
    def setUp(self):
        self.user = User()
        self.valid_email = "test@example.com"
        self.valid_password = "test_password"

    def test_user_should_have_is_admin_field(self):
        try:
            self.user.is_admin
        except AttributeError:
            self.fail("User should have is_admin field")

    def test_user_with_no_is_admin_args_shoud_not_be_admin(self):
        user = User.objects.create_user(
                email = self.valid_email,
                password = self.valid_password,
                )
        self.assertFalse(user.is_admin)
