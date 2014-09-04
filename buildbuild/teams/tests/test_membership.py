from django.test import TestCase
from teams.models import Team, Membership
from users.models import User
from django.utils import timezone

"""
get specific member(s) from membership (mtom) should get
from Membership module. Because team instance could find
all members even if a member belonged not to that team.
"""

class team_manager_test(TestCase):
    def setUp(self):
        self.user_email = "test@example.com"
        self.user_password = "12345678"
        self.no_user_email = "no@example.com"

        self.team_name = "Team1"
        self.no_team_name = "NoTeam"

        self.user = User.objects.create_user(
            email = self.user_email,
            password = self.user_password
        )

        self.team = Team.objects.create_team(
            name = self.team_name
        )

        self.no_user = User.objects.create_user(
            email = self.no_user_email,
            password = self.user_password
        )

        self.no_team = Team.objects.create_team(
            name = self.no_team_name
        )

    def test_operation_of_membership(self):
        try:
            Membership.objects.create(
                    team = self.team,
                    member = self.user,
                    )
        except:
            self.fail("test operation of membership failed")

    def test_get_all_members_from_team_instance(self):
        Membership.objects.create(
                team = self.team,
                member = self.user,
                )
        try:
            self.team.members.all()
        except:
            self.fail("getting all member failed from team instance")

    def test_get_member_from_membership_module(self):
        Membership.objects.create(
                team = self.team,
                member = self.user,
                )
        try:
            Membership.objects.get(
                    team=self.team,
                    member = self.user,
                    )
        except:
            self.fail("getting member failed from membership module")
 

    def test_team_should_have_is_admin(self):
        membership = Membership.objects.create(
            team = self.team,
            member = self.user,
            )
        
        try:
            membership.is_admin
        except AttributeError:
            self.fail("team membership should have is_admin")

    def test_should_have_date_joined(self):
        membership = Membership.objects.create(
            team = self.team,
            member = self.user,
            )
 
        try:
            membership.date_joined
        except AttributeError:
            self.fail("team membership should have date_joined")

    def test_get_member_from_non_exist_team(self):
        Membership.objects.create(
                team = self.team,
                member = self.user,
                )
        try:
            Membership.objects.getr(
                    team=self.no_team,
                    member = self.user
                    )
        except:
            pass 

    def test_get_member_from_non_exist_user(self):
        Membership.objects.create(
                team = self.team,
                member = self.user,
                )
        try:
            Membership.objects.getr(
                    team=self.team,
                    member = self.no_user
                    )
        except:
            pass 


