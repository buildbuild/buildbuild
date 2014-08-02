from django.test import TestCase

# Create your tests here.
from teams.models import Teams

class TeamsModelTest(TestCase):
	def setUp(self):
		pass
	#self.teams = Teams()
		

#from users.models import User
#
#from django.db import IntegrityError
#from django.core.exceptions import ValidationError
#
#
#    # Email
#    def test_user_should_have_email_field(self):
#        try:
#            self.user.email
#        except AttributeError:
#            self.fail("User should have email field")
#
#    def test_user_email_should_not_be_blank(self):
#        self.user.email = ""
#        self.user.password = self.valid_password
#        self.assertRaises(ValueError, self.user.save())
#
#    def test_user_should_have_unique_email(self):
#        self.user.email = self.valid_email
#        self.user.password = self.valid_password
#        self.user.save()
#
#        user_with_duplicate_email = User(email = self.user.email, password = self.valid_password)
#
#        self.assertRaises(IntegrityError, user_with_duplicate_email.save)
#
#    def test_user_with_invalid_email_should_not_be_valid(self):
#        self.assertRaises(ValidationError, User.users.create_user,
#                email = "INVALID_EMAIL",
#                password = self.valid_password
#                )
#
#    # Password
#    def test_user_should_have_password_field(self):
#        try:
#            self.user.password
#        except AttributeError:
#            self.fail("User should have password field")
#
#    def test_user_with_short_password_should_not_be_valid(self):
#        self.assertRaises(ValidationError, User.users.create_user,
#                email = self.valid_email,
