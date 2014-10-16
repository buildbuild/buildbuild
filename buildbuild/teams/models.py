from django.db import models
from django.utils import timezone
from users.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
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

    def validate_name(self, name):
        if len(name) > 30:
            raise ValidationError(
                ("team name length should be at most 30"),
                code = 'invalid'
            )
        if bool(re.match('^[ a-zA-Z_]+$', name)):
            pass
        else:
            raise ValidationError(
                "team name cannot contain things but alphabet, white space, '_'"
            )

    def get_team(self, name):
        try:
            self.validate_name(name)
            team = Team.objects.get(name = name)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("The team name does not exist")
        else:
            return team

    def delete_team(self, name):
        team = Team.objects.get_team(name)
        team.deactivate()
        team.save(using = self._db)

    def validate_name(self, name):
        if len(name) > 30 :
            raise ValidationError("Name cannot contain more than 30 characters")

    def validate_contact_number(self, contact_number):
        if len(contact_number) > 20:
            raise ValidationError("Contact number cannot contain more than 20 digits")

    def validate_website_url(self, website_url):
        if len(website_url) > 255:
            raise ValidationError("Website URL cannot contain more than 255 characters")

class Team(models.Model):
    name = models.CharField(max_length = 30, unique=True)
    contact_number = models.CharField(max_length = 20)
    website_url = models.URLField(max_length = 255)

    objects = TeamManager()
 
    wait_members = models.ManyToManyField(
            User, 
            through = 'WaitList',
            through_fields = ('team', 'wait_member'),
            related_name="wait_list",
            )
    
    members = models.ManyToManyField(
            User, 
            through = 'Membership',
            through_fields = ('team', 'member'),
            related_name="membership",
            )
  
    def __unicode__(self):
        return self.name
 
class Membership(models.Model):
    team = models.ForeignKey(
            Team, 
            related_name="membership_team",
            )
    member = models.ForeignKey(
            User, 
            related_name="membership_member",
            )
    date_joined = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

class WaitList(models.Model):
    team = models.ForeignKey(
            Team, 
            related_name="wait_list_team",
            )
    wait_member = models.ForeignKey(
            User, 
            related_name="wait_list_user",
            )
    date_requested = models.DateTimeField(auto_now_add=True)
