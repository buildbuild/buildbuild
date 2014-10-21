from django.test import TestCase
from teams.models import Team, Membership
from users.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Membership_member_to_team_test(TestCase):
    def setUp(self):
        self.user_email = "test@example.com"
        self.user_password = "12345678"
        self.second_user_email = "test2@example.com"

        self.team_name = "Team1"
        self.second_team_name = "Team2"

        self.user = User.objects.create_user(
            email = self.user_email,
            password = self.user_password
        )

        self.team = Team.objects.create_team(
            name = self.team_name
        )

        self.second_user = User.objects.create_user(
            email = self.second_user_email,
            password = self.user_password
        )

        self.second_team = Team.objects.create_team(
            name = self.second_team_name
        )

        self.membership = Membership.objects.create_membership(
            self.team,
            self.user,
        )
        self.membership = Membership.objects.create_membership(
            self.second_team,
            self.user,
        )
      

    def test_get_all_belonged_team(self):
        self.assertIsNotNone(self.user.member.all())
 
    def test_member_could_get_all_belonged_team(self):
        belonged_team = self.user.member.all()
        self.assertEqual(belonged_team[0], self.team)
        self.assertEqual(belonged_team[1], self.second_team)
   
    def test_member_could_leave_belonged_team(self):
        try:
            self.user.membership_member.leave_team(self.team)
        except ValidationError:
            self.fail("leave_team has occured an error")

    def test_leaved_user_cannot_belong_team(self):
        self.user.membership_member.leave_team(self.team)
        belonged_team = self.user.member.all()
        self.assertNotIn(self.team, belonged_team)

