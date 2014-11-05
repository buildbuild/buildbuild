from django.test import TestCase
from users.models import User

class UserIsActiveTest(TestCase):
    def setUp(self):
        self.valid_email = "test@example.com"
        self.valid_password = "test_password"

        self.user = User.objects.create_user(
            email = self.valid_email,
            password = self.valid_password,
        )

    def test_user_should_have_is_active_value(self):
        self.assertIsNotNone(self.user.is_active)

    def test_is_active_default_true(self):
        self.assertTrue(self.user.is_active)

    def test_deactivate(self):
        self.assertFalse(self.user.deactivate())

    def test_activate(self):
        self.user.deactivate()
        self.user.activate()
        self.assertTrue(self.user.is_active)


