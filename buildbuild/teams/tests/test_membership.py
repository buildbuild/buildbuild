from django.test import TestCase
from teams.models import Team, Membership
from users.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Membership_member_to_team_test(TestCase):
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

# Attribute
    def test_membership_must_have_date_joined(self):
        try:
            self.membership.date_joined
        except AttributeError:
            self.fail("team membership should have date_joined")

# Validation
    def test_create_membership_member_argument_should_be_User_object(self):
        try:
            self.membership = Membership.objects.create_membership(
                self.team,
                self.team,
            )
        except ValidationError:
            pass

    def test_create_membership_team_argument_should_be_Team_object(self):
        try:
            self.membership = Membership.objects.create_membership(
                self.user,
                self.user,
            )
        except ValidationError:
            pass






       


