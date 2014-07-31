from django.test import TestCase
from users.models import User

class TestUserManager(TestCase):
    def setUp(self):
        self.user = User()
        self.valid_email = "test@example.com"
        self.valid_password = "test_password"

    def test_user_should_be_created_via_user_manager(self):
        try:
            user = User.objects.create_user(
                    email = self.valid_email,
                    password = self.valid_password,
                    )
        except:
            self.fail("User should be created via UserManager")
