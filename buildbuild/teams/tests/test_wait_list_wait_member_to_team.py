from django.test import TestCase
from teams.models import Team, WaitList
from users.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class WaitList_wait_member_to_team_test(TestCase):
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
        
    def test_wait_member_could_get_all_belonged_team(self):
        try:
            self.user.wait_member.all()
        except:
            self.fail("getting all team belonged failed")
   
    def test_wait_member_could_cancel_to_request_to_join_team(self):
        try:
            self.user.wait_list_wait_member.cancel_to_request_to_team(self.team)
        except ValidationError:
            self.fail("cancel to request to team has occured an error")
