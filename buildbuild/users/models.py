from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, username, phone, organization, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            phone = phone,
            organization = organization,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name = "email address",
        max_length = 255,
        unique = True,
    )
    username = models.CharField(max_length = 20)
    phone = models.CharField(max_length = 20)
    organization = models.CharField(max_length = 20)
    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)
    is_org_admin = models.BooleanField(default = False)

    objects = UserManager()

    USERNAME_FILED = "email"
    REQUIRED_FILEDS = ["username", "phone", "organization"]

    def get_full_name(self):
        return self.email
    def get_short_name(self):
        return self.email
    def __unicode__(self):
        return self.email
