from django.test import TestCase
from teams.models import Team,TeamManager,WaitList
from users.models import User,UserManager
from django.core.exceptions import ObjectDoesNotExist

class TestWaitList(TestCase):
    def setUp(self):
        self.user_email = "test@example.com"
        self.user_password = "12345678"
        self.user = User()

        self.non_exist_user_email = "no@example.com"

        self.team_name = "Team1"
        self.team = Team()

        self.non_exist_team_name = "NoTeam"
        
        User.objects.create_user(
            email = self.user_email,
            password = self.user_password
        )

        Team.objects.create_team(
            name = self.team_name
        )

    def test_user_and_team_should_be_put_wait_list_using_manager(self):
        try:
            WaitList.objects.append_list(
                team_name=self.team_name,
                user_email=self.user_email
            )
        except:
            self.fail("Append to wait list should be success.")

    def test_append_wait_list_should_not_be_working_with_invalid_argument(self):
        self.assertRaises(
            ObjectDoesNotExist,WaitList.objects.append_list,
            team_name = self.team_name,
            user_email = self.non_exist_user_email
        )

    def test_appended_wait_list_should_be_get_using_manager_with_team_argument(self):
        self.assertRaises(
            ObjectDoesNotExist, WaitList.objects.get_wait_list,
            team_name = self.non_exist_team_name
        )

    def test_delete_list_should_be_removed_from_list(self):
        WaitList.objects.append_list(
            team_name=self.team_name,
            user_email=self.user_email
        )
        WaitList.objects.delete_from_list(team_name=self.team_name)
        self.assertRaises(
            ObjectDoesNotExist, WaitList.objects.get_wait_list,
            team_name = self.team_name
        )

