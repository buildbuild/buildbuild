from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email

from django.core.exceptions import ValidationError, ObjectDoesNotExist
import re

class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("User must have an email address")


        validate_email(email)
        self.validate_password(password)

        user = self.model(email = self.normalize_email(email))
        user.set_password(password)

        if "name" in kwargs:
            user.name = kwargs["name"]

        if "phonenumber" in kwargs:
            self.validate_phonenumber(kwargs["phonenumber"])
            user.phonenumber = kwargs["phonenumber"]

        if "is_admin" in kwargs and kwargs["is_admin"]:
            user.is_admin = True

        user.save(using = self._db)
        return user

    def validate_password(self, password):
        if len(password) < 6:
            raise ValidationError(("user password length should be at least 6"),
                                  code='invalid')
    def validate_phonenumber(self, phonenumber):
        if len(phonenumber) < 8:
            raise ValidationError(("user phonenumber length should be at least 8"),
                                  code='invalid')
        if not bool(re.match('^[0-9]$', phonenumber)):
            raise ValidationError(("user phonenumber should not be with character"))

    def get_user(self, email):
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("User has " + email + " email does not exist")

class User(AbstractBaseUser):
    name = models.CharField(max_length = 20)
    email = models.EmailField(
                verbose_name = "Email Address",
                max_length = 50,
                unique = True,
            )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    phonenumber = models.CharField(max_length=18)

    # custom UserManager
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def deactivate(self):
        self.is_active = False
        return self

    def activate(self):
        self.is_active = True
        return self
