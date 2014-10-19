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
            self.validate_name(kwargs['name'])
            user.name = kwargs["name"]

        if "phonenumber" in kwargs:
            self.validate_phonenumber(kwargs["phonenumber"])
            user.phonenumber = kwargs["phonenumber"]

        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password = password, **kwargs)

        user.is_admin = True
        user.is_staff = True   
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
        if bool(re.match('^[0-9]+$', phonenumber)):
            pass
        else:
            raise ValidationError(("user phonenumber should not be with character"))

    def validate_name(self, name):
        if len(name) > 20:
            raise ValidationError(("user name length should be at most 20"),
                                    code = 'invalid')
        if bool(re.match('^[ a-zA-Z_]+$', name)):
            pass
        else:
            raise ValidationError(("user name cannot contain things but alphabet, white space, '_'"))

    def get_user(self, email):
        try:
            validate_email(email)
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("User has " + email + " email does not exist")
        return user

    def delete_user(self, email):
        user = User.objects.get_user(email)
        user.deactivate()
        user.save(using = self._db)

    def update_user(self, email, **kwargs):
        user = User.objects.get_user(email)

        if 'phonenumber' in kwargs:
            self.validate_phonenumber(kwargs['phonenumber'])
            user.phonenumber = kwargs['phonenumber']

        if 'name' in kwargs:
            self.validate_name(kwargs['name'])
            user.name = kwargs['name']

        user.save(using = self._db)

    # get member from foreign key of MtoM
    def get_member(self, email):
        query = self.filter(email = email)
        try:
            member = query.get()
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(email + "is not team member")
        else:
            return member
 
class User(AbstractBaseUser):
    name = models.CharField(max_length = 20)
    email = models.EmailField(
                verbose_name = "Email Address",
                max_length = 50,
                unique = True,
            )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
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

    #TODO : To use the functions get_full_name and get_short_name
    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        if self.is_admin is True:
            return True
        else:
            return False
    
    def is_staff(self):
        return self.is_admin
    
    #TODO : need to check django method
    def has_module_perms(self, app_label):
        return True
    
