from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have an email address")

        validate_email(email)

        user = self.model(email = self.normalize_email(email))
        user.set_password(password)
        user.save(using = self._db)
        return user

class User(AbstractBaseUser):
    email = models.CharField(
                verbose_name = "Email Address",
                max_length = 50,
                unique = True,
            )

    # custom UserManager
    users = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
