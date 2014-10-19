from django.db import models
from django.utils import timezone
from users.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import re

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
        if len(name) > 64:
            raise ValidationError(
                ("team name length should be at most 64"),
                code = 'invalid'
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

    def validate_contact_number(self, contact_number):
        if len(contact_number) > 20:
            raise ValidationError("Contact number cannot contain more than 20 digits")
        if bool(re.match('^[0-9]+$', contact_number)):
            pass
        else:
            raise ValidationError(("team contact number should not be with character"))

    def validate_website_url(self, website_url):
        if len(website_url) > 255:
            raise ValidationError("Website URL cannot contain more than 255 characters")
  
    # Get belonged team from related name of Membership
    def get_belonged_team(self, name):
        query = self.filter(name = name)
        try:
            team = query.get()
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(name + "is not the team member")
        else:
            return team


class Team(models.Model):
    name = models.CharField(max_length = 64, unique=True)
    contact_number = models.CharField(max_length = 20)
    website_url = models.URLField(max_length = 255)

    objects = TeamManager()
 
    wait_members = models.ManyToManyField(
            User, 
            through = 'WaitList',
            through_fields = ('team', 'wait_member'),
            related_name="wait_member",
            )
    
    members = models.ManyToManyField(
            User, 
            through = 'Membership',
            through_fields = ('team', 'member'),
            related_name="member",
            )
  
    def __unicode__(self):
        return self.name

class MembershipManager(models.Manager):
    def create_membership(self, team_name, member_email):
        # Does our DB contain the team & user?
        team = Team.objects.get_team(team_name)
        user = User.objects.get_user(member_email)

        # Does the member already exist? 
        try:
            team.members.get_member(email = member_email)
        except ObjectDoesNotExist:
            membership = self.create(
                team = team,            
                member = user,
            )
            membership.save(using = self._db)
            return membership
        else:
            raise ValidationError(user.email + " is already the team member")
class Membership(models.Model):
    team = models.ForeignKey(
            Team, 
            related_name="membership_team",
            )
    member = models.ForeignKey(
            User, 
            related_name="membership_member",
            )
    objects = MembershipManager()
    
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
