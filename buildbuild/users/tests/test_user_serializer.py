from django.test import TestCase

from users.models import User
from users.serializers import UserSerializer


class TestUserSerializer(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="test_password",
        )

    def test_user_serializer_return_serialized_data(self):
        serialized_user = UserSerializer(self.user)
        expected_data = {
            'id': self.user.id,
            'email': self.user.email,
        }
        self.assertEqual(serialized_user.data, expected_data)
