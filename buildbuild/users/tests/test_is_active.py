from django.test import TestCase
from users.models import User

class UserIsActiveTest(TestCase):
    def setUp(self):
        self.user = User()
        self.valid_email = "test@example.com"
        self.valid_password = "test_password"

    def test_user_should_have_is_active_field(self):
        try:
            self.user.is_active
        except AttributeError:
            self.fail("User should have is_active field")

    def test_user_with_no_is_active_args_shoud_be_active(self):
        user = User.objects.create_user(
                email = self.valid_email,
                password = self.valid_password,
                )
        self.assertTrue(user.is_active)

    def test_user_model_should_have_activate_method(self):
        deactive_user = User.objects.create(
                email = self.valid_email,
                password = self.valid_password,
                is_active = False,
                )
        activated_user = deactive_user.activate()
        self.assertTrue(activated_user.is_active)

    def test_user_model_should_have_deactivate_method(self):
        active_user = User.objects.create(
                email = self.valid_email,
                password = self.valid_password,
                # default value for is_active is True
                )
        deactivated_user = active_user.deactivate()
        self.assertFalse(deactivated_user.is_active)
