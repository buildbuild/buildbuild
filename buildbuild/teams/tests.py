from django.test import TestCase
from users.models import User
from teams.models import Team

#from django.core.exceptions import ObjectDoesNotExist
#from django .core.exceptions import ValidationError
#import re

class team_composition_test(TestCase):
	def setUp(self):
		self.team = Team()

	def test_does_team_exists(self):
		try: 
			self.team
		except AttributeError:
			self.fail("team should exists")
		pass	
