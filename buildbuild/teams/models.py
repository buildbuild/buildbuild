from django.db import models

# Create your models here.

class Teams():
	pass


#from django.db import models
#from django.contrib.auth.models import AbstractBaseUser
#from django.contrib.auth.models import BaseUserManager
#from django.core.validators import validate_email
#
#from django.core.exceptions import ValidationError
#
#class UserManager(BaseUserManager):
#    def create_user(self, email, password, **kwargs):
#        if not email:
#            raise ValueError("User must have an email address")
#
#
#        validate_email(email)
#        self.validate_password(password)
#
#        user = self.model(email = self.normalize_email(email))
#        user.set_password(password)
#
#        if "name" in kwargs:
#            user.name = kwargs["name"]
#
#        if "is_admin" in kwargs and kwargs["is_admin"]:
#            user.is_admin = True
#
#        if "is_org_admin" in kwargs and kwargs["is_org_admin"]:
#            user.is_org_admin = True
#
#        user.save(using = self._db)
#        return user
#
#    def validate_password(self, password):
#        if len(password) < 6:
#            raise ValidationError("user password length should be at least 6")
#
#class User(AbstractBaseUser):
#    name = models.CharField(max_length = 20)
#    email = models.EmailField(
#                verbose_name = "Email Address",
#                max_length = 50,
#                unique = True,
#            )
#
#    is_active = models.BooleanField(default=True)
#    is_admin = models.BooleanField(default=False)
#    is_org_admin = models.BooleanField(default=False)
#
#    # custom UserManager
#    users = UserManager()
#
