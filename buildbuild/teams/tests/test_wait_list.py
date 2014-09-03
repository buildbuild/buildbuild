from django.test import TestCase
from teams.models import Team,TeamManager,WaitList
from users.models import User,UserManager
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db import OperationalError, IntegrityError

class TestWaitList(TestCase):
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
    def test_operation_of_wait_list(self):
        try:
            WaitList.objects.create(
                team = self.team,
                wait_member = self.user,
                )
        except:
            self.fail("test operation of wait_list failed")
    
    def test_get_wait_member_from_wait_list_module(self):
        WaitList.objects.create(
            team = self.team,
            wait_member = self.user,
            )
        
        try:
            WaitList.objects.get(
                    team=self.team,
                    wait_member=self.user
                    )
        except:
            self.fail("get wait_member failed from wait_list instance")
    
    def test_get_wait_member_from_team_instance(self):
        WaitList.objects.create(
            team = self.team,
            wait_member = self.user,
            )
        
        try:
            self.team.wait_members.all()
        except:
            self.fail("get wait_member failed from team instance")
 
    def test_should_have_date_requested(self):
        wait_list = WaitList.objects.create(
            team = self.team,
            wait_member = self.user,
            )
 
        try:
            wait_list.date_requested
        except AttributeError:
            self.fail("team membership should have date_requested")

    def test_get_wait_member_from_non_exist_team(self):
        WaitList.objects.create(
                team = self.team,
                wait_member = self.user,
                )
        try:
            WaitList.objects.get(
                    team=self.no_team,
                    wait_member = self.user
                    )
        except:
            pass 

    def test_get_wait_member_from_non_exist_user(self):
        WaitList.objects.create(
                team = self.team,
                wait_member = self.user,
                )
        try:
            WaitList.objects.getr(
                    team=self.team,
                    wait_member = self.no_user
                    )
        except:
            pass 


