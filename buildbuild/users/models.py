from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class UserManager(BaseUserManager):
    def create_user(self, email, user_name, phone_number, organization, password=None):
        """
        :param email: Email Address , Unique ID
        :param user_name: Read User Name like Kim Junho
        :param phone_number: Contactable phone number
        :param organization: It describes where user is in
        :param password = Password, In this case, It must be defined by user
        :return: MyUser object
        """

        if not email:
            raise ValueError('Users must have an unique email address')

        user = self.model(
            email = self.normalize_email(email),
            user_name = user_name,
            phone_number = phone_number,
            organization = organization,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin_user(self, email, user_name, phone_number, organization, password, **kwargs):
        """
        :param email: Email Address, Unique ID
        :param user_name: Read User Name like Kim Junho
        :param phone_number: Contactable phone number
        :param organization: It describes where user is in
        :param password = Password
        :param **kwargs = Keyword : Check Whether System, Organization admin Fields are set.
        :return: MyUser object
        """

        user = self.create_user(
            email=email,
            user_name=user_name,
            phone_number=phone_number,
            organization=organization,
            password=password,
        )

        if "is_admin" in kwargs["is_admin"] and kwargs['is_admin']:
            user.is_admin = True

        if "is_org_admin" in kwargs["is_org_admin"] and kwargs['is_org_admin']:
            user.is_org_admin = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )

    user_name = models.CharField(max_length=8)
    phone_number = models.CharField(max_length=20)
    organization = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_org_admin = models.BooleanField(default=False)
    #Password Field is predefined by super class

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name','phone_number','organization']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email

    def is_system_admin(self):
        return self.is_admin

    def is_organization_admin(self):
        return self.is_org_admin

    def is_user_active(self):
        return self.is_active