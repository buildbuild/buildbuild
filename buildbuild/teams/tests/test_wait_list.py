from django.test import TestCase
from teams.models import Team, WaitList
from users.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class WaitList_test(TestCase):
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

# Attribute
    def test_wait_list_must_have_date_requested(self):
        try:
            self.wait_list.date_requested
        except AttributeError:
            self.fail("team wait_list should have date_requested")

# Validation
    def test_create_wait_list_member_argument_should_be_User_object(self):
        try:
            self.wait_list = WaitList.objects.create_wait_list(
                self.team,
                self.team,
            )
        except ValidationError:
            pass

    def test_create_wait_list_team_argument_should_be_Team_object(self):
        try:
            self.wait_list = WaitList.objects.create_wait_list(
                self.user,
                self.user,
            )
        except ValidationError:
            pass

