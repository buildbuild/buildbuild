from django.db import models
from users.models import User
from django.core.exceptions import ValidationError

# Create your models here.

class TeamManager(models.Manager):
    def create_team(self, name, **kwargs):
        team = self.model()
        self.validate_name(name)
        team.name = name

        if "contact_number" in kwargs:
            self.validate_contact_number(kwargs["contact_number"])
            team.contact_number = kwargs["contact_number"]

        if "website_url" in kwargs:
            self.validate_website_url(kwargs["website_url"])
            team.website_url = kwargs["website_url"]


        team.save(using = self._db)
        return team

    def get_all_team(self):
        return Team.objects.all()

    def get_team(self, name):
        self.validate_name(name)
        return Team.objects.get(name = name)

    def validate_name(self, name):
        if len(name) > 30 :
            raise ValidationError("Name cannot contain more than 30 characters")

    def validate_contact_number(self, contact_number):
        if len(contact_number) > 20:
            raise ValidationError("Contact number cannot contain more than 20 digits")

    def validate_website_url(self, website_url):
        if len(website_url) > 20:
            raise ValidationError("Website URL cannot contain more than 80 characters")



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
    website_url = models.URLField(max_length = 80)
    users = models.ManyToManyField(User, through = 'Membership')

    def __unicode__(self):
        return self.name

class Membership(models.Model):
    team = models.ForeignKey(Team)
    user = models.ForeignKey(User)
    date_joined = models.DateField()
    is_admin = models.BooleanField(default=False)


class WaitList(models.Model):
    team = models.ForeignKey(Team, related_name="waiting_list")
    user = models.ForeignKey(User, related_name="+")
    request_date = models.DateField()
