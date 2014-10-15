from django.test import TestCase
from teams.models import Team,WaitList
from users.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError

class TestWaitList(TestCase):
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

        wait_list = WaitList.objects.create(
            team = self.team,
            wait_member = self.user,
        )
        wait_list.save()

    def test_team_could_get_all_wait_lists(self):
        try:
            self.team.wait_members.all()
        except: 
            self.fail("getting all wait_lists failed")

    def test_team_could_get_wait_member(self):
        try:
            self.team.wait_members.get_user(self.user_email)
        except: 
            self.fail("getting a wait_user failed")

