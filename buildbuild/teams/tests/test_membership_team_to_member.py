from django.test import TestCase
from teams.models import Team, Membership
from users.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Membership_team_to_member_test(TestCase):
    def setUp(self):
        self.user_email = "test@example.com"
        self.user_password = "12345678"
        self.user_email_2 = "test2@example.com"

        self.team_name = "Team1"
        self.team_name_2 = "Team2"

        self.user = User.objects.create_user(
            email = self.user_email,
            password = self.user_password
        )

        self.team = Team.objects.create_team(
            name = self.team_name
        )

        self.user_2 = User.objects.create_user(
            email = self.user_email_2,
            password = self.user_password
        )

        self.team_2 = Team.objects.create_team(
            name = self.team_name_2
        )

        self.membership = Membership.objects.create_membership(
            self.team,
            self.user,
        )

    def test_team_could_get_all_members(self):
        try:
            self.team.members.all()
        except:
            self.fail("getting all team members failed")

# ObjectDoesNotExist
    def test_team_could_get_member(self):
        try:
            self.team.members.get_member(self.user.id)
        except:
            self.fail("getting team member failed")

    def test_team_could_exclude_team_member(self):
        try:
            self.team.membership_team.exclude_member(self.user.id)
        except ValidationError:
            self.fail("exclude_member has occured an error")
