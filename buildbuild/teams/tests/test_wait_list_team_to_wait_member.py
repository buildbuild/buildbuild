from django.test import TestCase
from teams.models import Team, WaitList
from users.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class WaitList_team_to_wait_member_test(TestCase):
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

        self.wait_list = WaitList.objects.create_wait_list(
            self.team,
            self.user,
        )

    def test_team_could_get_all_wait_members(self):
        try:
            self.team.wait_members.all()
        except:
            self.fail("getting all wait_members failed")

# ObjectDoesNotExist
    def test_team_could_get_wait_member(self):
        try:
            self.team.wait_members.get_wait_member(self.user_email)
        except:
            self.fail("getting team wait_member failed")

    def test_team_could_reject_to_join_team(self):
        try:
            self.team.wait_list_team.reject_to_join_team(self.user)
        except ValidationError:
            self.fail("reject_to_join_to_team has occured an error")
