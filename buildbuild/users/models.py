from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class UserManager(BaseUserManager):
    #Create
    def create_user(self, email, user_name, phone_number, organization, password=None):
        """
        :param email: Email Address , Unique ID
        :param user_name: Read User Name like Kim Junho
        :param phone_number: Contactable phone number
        :param organization: It describes where user is in
        :param password = Password, In this case, It must be defined by user
        :return: MyUser object
        """

        # Validation
        User.objects.validate_email(email)

        #Save and Return
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

    #Retreive
    def get_user(self, email):
        User.objects.validate_email(email)
        try:
            user = User.objects.get(email__exact=email)
        except User.DoesNotExist:
            raise User.DoesNotExist
        if user.is_active:
            return user

    #Update
    def update_user(self, email, **kwargs):
        User.objects.validate_email(email)
        user = User.objects.get_user(email)
        if 'user_name' in kwargs['user_name']:
            user.user_name = kwargs['user_name']
        elif 'phone_number' in kwargs['phone_number']:
            user.phone_number = kwargs['phone_number']
        elif 'organization' in kwargs['organization']:
            user.organization = kwargs['organization']
        elif 'password' in kwargs['password']:
            user.set_password(kwargs['password'])

        user.save(using=self._db)

    #Delte
    def delete_user(self, email):
        User.objects.validate_email(email)

        user = User.objects.get_user(email)
        user.is_active = False

    def validate_email(self, email):
        if not email:
            raise ValueError("Email must be entered.")

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