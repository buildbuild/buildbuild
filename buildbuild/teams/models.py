from django.db import models
from users.models import User
from django.core.exceptions import ValidationError

# Create your models here.

class TeamManager(models.Manager):
	def create_team(self, **kwargs):
		team = self.model()
	
		if "name" in kwargs:
			team.name = kwargs["name"]

		team.save(using = self._db)
		return team

class Team(models.Model):
	"""
	team model functions
	- team_name
	- team_position
	- team_permission
	- team_sign_up_form
	- team_email
	- team_contacet_number
	- team_website_url
	
	"""
	
	objects = TeamManager()
	name = models.CharField(max_length = 30, default = "team name is required")
#	team_email = models.EmailField(
#			verbose_name = "team Email Address",
#			max_length = 50,
#			unique = True,
#			)
		
