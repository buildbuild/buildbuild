from django.db import models
from django.utils import timezone
from users.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import re
from django.core.validators import URLValidator

class TeamManager(models.Manager):
    def create_team(self, name, **kwargs):
        team = self.model()
        self.validate_name(name)
        team.name = name

        if "contact_number" in kwargs:
            self.validate_contact_number(kwargs["contact_number"])
            team.contact_number = kwargs["contact_number"]

        if "team_url" in kwargs:
            # It checks validation, scheme, unicode
            validate_team_url = URLValidator()
            validate_team_url(kwargs["team_url"])
            team.team_url = kwargs["team_url"]

        team.save(using = self._db)

        return team

    def validate_name(self, name):
        if len(name) < 1:
            raise ValidationError(
                "team name length should be at most 64",
            )
        elif len(name) > 64:
            raise ValidationError(
                "team name length should be at most 64",
            )
        
        # test code, not yet
        if bool(re.match('^[a-zA-Z0-9_]+$', name)) is False:
            raise ValidationError(
                     "team name cannot contain things but alphabet, '_', number"
                  )
        

    def get_team(self, id):
        try:
            team = Team.objects.get(id = id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("The id is not contained in team DB")
        else:
            return team

    def delete_team(self, id):
        team = Team.objects.get_team(id)
        team.delete()

        if team.id is None:
            return True
        else:
            raise OperationalError("delete team failed")

    def validate_contact_number(self, contact_number):
        if len(contact_number) > 20:
            raise ValidationError("Contact number cannot contain more than 20 digits")
        if bool(re.match('^[0-9-]+$', contact_number)):
            pass
        else:
            raise ValidationError(("team contact number should not be with character"))

    # get team from foreign key of MtoM
    def get_project_team(self, id):
        try:
            team = self.get(id = id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                str(id) + "is not contained in project team DB"
            )
        else:
            return team

    # get wait_team from foreign key of MtoM
    def get_project_wait_team(self, id):
        try:
            wait_team = self.get(id = id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                str(id) + "is not contained in project wait team DB"
            )
        else:
            return wait_team

class Team(models.Model):
    name = models.CharField(
        help_text = "Team name",
        max_length = 64,
        unique=True,
    )
    contact_number = models.CharField(
                        help_text = "Team contact_number to inform something or contact",
                        max_length = 20,
                     )

    team_url = models.URLField(
                      help_text = "Team team_url",
                      default = "",
                  )

    objects = TeamManager()
 
    wait_members = models.ManyToManyField(
                       User,
                       verbose_name = "team wait_members",
                       through = 'WaitList',
                       through_fields = ('team', 'wait_member'),
                       related_name="wait_member",
                   )
    
    members = models.ManyToManyField(
                  User,
                  verbose_name = "team members for team",
                  through = 'Membership',
                  through_fields = ('team', 'member'),
                  related_name="member",
              )

class MembershipManager(models.Manager):
    def create_membership(self, team, user):
        if user.__class__.__name__ is not "User":
            raise ValidationError("user argument must be User object")
        if team.__class__.__name__ is not "Team":
            raise ValidationError("team argument must be Team object")

        # Does the member already exist? 
        try:
            team.members.get_member(id = user.id)
        except ObjectDoesNotExist:
            membership = self.model(
                team = team, 
                member = user,
            )
            membership.save(using = self._db)
            return membership
        else:
            raise AlreadyMemberError(member.email + " is already the team member")
    
    # User -> membership_member -> leave_team
    def leave_team(self, id):
        try:
            membership = self.get(id = id)
        except ValidationError:
            raise ValidationError("The team id is not a member's belonged team")
        membership.delete()

    # Team -> membership_team -> exclude_member
    def exclude_member(self, id):
        try:
            membership = self.get(id = id)
        except ValidationError:
            raise ValidationError("The member is not a team member")
        membership.delete()
    
class Membership(models.Model):
    team = models.ForeignKey(
               Team,
               verbose_name = "membership team",
               related_name="membership_team",
           )
    member = models.ForeignKey(
                 User,
                 verbose_name = "membership member",
                 related_name="membership_member",
             )
    objects = MembershipManager()
    
    date_joined = models.DateTimeField(
                      help_text = "Membership date_joined when the member joined the team",
                      auto_now_add=True,
                  )
    is_admin = models.BooleanField(
                   help_text = "Membership is_admin",
                   default=False
               )

class WaitListManager(models.Manager):
    def create_wait_list(self, team, wait_member):
        if wait_member.__class__.__name__ is not "User":
            raise ValidationError("wait_member argument must be User object")
        if team.__class__.__name__ is not "Team":
            raise ValidationError("team argument must be Team object")

        # Does the member already exist? 
        try:
            team.members.get_member(id = wait_member.id)
        except ObjectDoesNotExist:
            pass
        else:
            raise AlreadyMemberError(wait_member.email + "is already the team member")
 
        # Does the wait_member already exist? 
        try:
            team.wait_members.get_member(id = wait_member.id)
        except ObjectDoesNotExist:
            wait_list = self.model(
                team = team, 
                wait_member = wait_member,
            )
            wait_list.save(using = self._db)
            return wait_list
        else:
            raise AlreadyWaitMemberError(wait_member.email + " is already the team member")

    # User -> wait_list_user -> cancel_to_request_to_team
    def cancel_to_request_to_team(self, team):
        try:
            wait_list = self.get(team = team)
        except ValidationError:
            raise ValidationError("The team is not a member's requested team")
        wait_list.delete()

    # Team -> wait_list_team -> reject_to_join_team
    def reject_to_join_team(self, wait_member):
        try:
            wait_list = self.get(wait_member = wait_member)
        except ValidationError:
            raise ValidationError("The wait_wait_member is not a team member")
        wait_list.delete()

class WaitList(models.Model):
    team = models.ForeignKey(
               Team, 
               verbose_name = "waitList team",
               related_name="wait_list_team",
           )
    wait_member = models.ForeignKey(
                      User,
                      verbose_name = "waitList wait_member",
                      related_name="wait_list_wait_member",
                  )
    date_requested = models.DateTimeField(
                         help_text = "WaitList date_requested when user " +
                             "send a request to join a team",
                         auto_now_add=True,
                     )

    objects = WaitListManager()

class AlreadyMemberError(Exception):
    pass

class AlreadyWaitMemberError(Exception):
    pass
