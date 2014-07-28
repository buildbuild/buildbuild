from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    email = models.EmailField(
                verbose_name = "Email Address",
                max_length = 50,
                unique = True
            )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
