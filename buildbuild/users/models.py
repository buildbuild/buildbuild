from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import re
from django.db import OperationalError

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
            raise ValidationError(
                "user password length should be at least 6",
            )
        elif len(password) > 255:
            raise ValidationError(
                "user password max length is 255",
            )

    def validate_phonenumber(self, phonenumber):

        if len(phonenumber) < 8:
            raise ValidationError(
                "user phonenumber length should be at least 8",
            )
        elif len(phonenumber) > 30:
            raise ValidationError(
                "user phonenumber max length 30",
            )
       
        if bool(re.match('^[0-9]+$', phonenumber)):
            pass
        else:
            raise ValidationError(("user phonenumber should not be with character"))

    def validate_name(self, name):
        if len(name) > 30:
            raise ValidationError(("user name length should be at most 30"),
                                    code = 'invalid')
        if bool(re.match('^[ a-zA-Z_]+$', name)):
            pass
        else:
            raise ValidationError(("user name cannot contain things but alphabet, white space, '_'"))

    def get_user(self, id):
        try:
            user = User.objects.get(id=id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("not exist user id")
        return user

    def delete_user(self, id):
        user = User.objects.get(id=id)
        user.delete()

        if user.id is None:
            return True
        else:
            raise OperationalError("delete user failed")

    def update_user(self, id, **kwargs):
        user = User.objects.get_user(id)

        if 'name' or 'phonenumber' in kwargs:
            if 'phonenumber' in kwargs:
                self.validate_phonenumber(kwargs['phonenumber'])
                user.phonenumber = kwargs['phonenumber']
                user.save(using = self._db)
                           
            if 'name' in kwargs:
                self.validate_name(kwargs['name'])
                user.name = kwargs['name']
                user.save(using = self._db)
       
            return True
        else: 
            raise ValueError("required name or phonenumber")
 

    # get member from foreign key of MtoM
    def get_member(self, id):
        try:
            member = self.get(id = id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                str(id) + "is not contained in team member DB"
            )
        else:
            return member

    # get wait_member from foreign key of MtoM
    def get_wait_member(self, id):
        try:
            wait_member = self.get(id = id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                str(id) + "is not contained in team wait member DB"
            )
        else:
            return wait_member
 
class User(AbstractBaseUser):
    name = models.CharField(
        max_length = 30,
    )
    email = models.EmailField(
                verbose_name = "Email Address",
                max_length = 50,
                unique = True,
            )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    phonenumber = models.CharField(max_length=18)

    USERNAME_FIELD = 'email'

    # custom UserManager
    objects = UserManager()

    def deactivate(self):
        self.is_active = False
        return self.is_active

    def activate(self):
        self.is_active = True
        return self.is_active

    #TODO : To use the functions get_full_name and get_short_name
    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def is_staff(self):
        return self.is_admin
    
    #TODO : need to check django method
    def has_module_perms(self, app_label):
        return True
    
