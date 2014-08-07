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
	- team_contact_number
	- team_website_url
	
	"""
	
	objects = TeamManager()
	name = models.CharField(max_length = 30)
	contact_number = models.CharField(max_length = 20)
	website_url = models.CharField(max_length = 50)
	users =  models.ManyToManyField(User)

		
