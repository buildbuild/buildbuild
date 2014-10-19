from django.test import TestCase
from teams.models import Team, Membership
from users.models import User
from django.utils import timezone

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
            team_name = self.team.name,
            member_email = self.user.email,
        )
        self.user = User.objects.get_user(self.user_email)
        
    def test_member_could_get_all_belonged_team(self):
        try:
            self.user.member.all()
        except:
            self.fail("getting all team belonged failed")
   
    # Attribute
    def test_membership_must_have_date_joined(self):
        try:
            self.membership.date_joined
        except AttributeError:
            self.fail("team membership should have date_joined")

