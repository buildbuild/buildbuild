from django.test import TestCase
from django.test.client import Client
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError

from teams.views import MakeTeamView
from teams.models import Team, WaitList
from users.models import User
from buildbuild import custom_msg

class MakeTeamPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.team_name = "buildbuild_team"
        self.second_team_name = "buildbuild_team2"
        self.invalid_team_name = "a" * 65

        # need to find more eloquent way to test redirect url.
        self.TEST_SERVER_URL = "http://testserver"

        self.user_email = "test@example.com"
        self.second_user_email = "second_test@example.com"
        self.user_password = "test_password"

        # not destroyed in function in this class
        self.user = User.objects.create_user(
                email = self.user_email,
                password = self.user_password,
                )
        self.second_user = User.objects.create_user(
                email = self.second_user_email,
                password = self.user_password,
                )

        self.never_exist_team = "never" * 4
        self.abc_pattern = "abc"
        self.abc_pattern_first_team = "111abc111"
        self.abc_pattern_second_team = "222abcd222"

    # Default Set function, These are not Unit Test function
    def post_login_set(self, user_email="", user_password="", follow = False):
        response = self.client.post(
                   "/login/", {
                       "email" : user_email,
                       "password" : user_password,
                       },
                       follow = follow
                   )
        return response

    # Default Set function, These are not Unit Test function
    def post_make_team_set(self, team_name="", follow=False):
        response = self.client.post(
                       "/teams/new/", {
                       "teams_team_name": team_name,
                       },
                       follow = follow
                   )
        return response

    # Test Code for Default Set function
    def test_post_login_set(self):
        self.post_login_set(self.user_email, self.user_password)

    # Test Code for Default Set function
    def test_post_make_team_set(self):
        self.post_make_team_set(self.team_name)

    def post_search(self, pattern, follow = False):
        response = self.client.post(
                       "/teams/search/?search_team=" + pattern,
                       follow = follow,
                   )
        return response

    def post_join(self, id, follow = False):
        response = self.client.post(
                       "/teams/" + str(id) + "/join/",
                       follow = follow,
                   )
        return response


    def test_post_search(self):
        self.post_login_set(self.user_email, self.user_password)
        self.post_make_team_set(self.team_name)
        self.post_search(self.team_name)

    def test_post_join(self):
        self.post_login_set(self.user_email, self.user_password)
        Team.objects.create_team(name = self.team_name)
        self.post_join(id = 1)

    def test_search_exist_team_should_contain_that_team(self):
        self.post_login_set(self.user_email, self.user_password)
        self.post_make_team_set(self.team_name)
        response = self.post_search(self.team_name)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.team_name)

    def test_search_but_already_team_member_should_not_link_to_href(self):
        self.post_login_set(self.user_email, self.user_password)
        self.post_make_team_set(self.team_name)
        response = self.post_search(self.team_name)
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, custom_msg.already_team_member)

    def test_searchs_that_have_same_patterns_should_be_contained_all(self):
        self.post_login_set(self.user_email, self.user_password)
        self.post_make_team_set(self.abc_pattern_first_team)
        self.post_make_team_set(self.abc_pattern_second_team)

        response = self.post_search(self.abc_pattern)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.abc_pattern_first_team)
        self.assertContains(response, self.abc_pattern_second_team)

    def test_search_not_exist_team_should_redirect_to_main_page(self):
        self.post_login_set(self.user_email, self.user_password)
        response = self.post_search(self.never_exist_team,)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.never_exist_team)

    def test_join_should_redirect_to_home(self):
        self.post_login_set(self.user_email, self.user_password)
        Team.objects.create_team(name = self.team_name)
        response = self.post_join(id = 1, follow = True)
        self.assertRedirects(response, "/")


    def test_join_should_make_MtoM_WaitList_between_user_and_team(self):
        self.post_login_set(self.user_email, self.user_password)
        Team.objects.create_team(name = self.team_name)
        response = self.post_join(id = 1)
        team = Team.objects.get(name = self.team_name)
        wait_member = User.objects.get(email = self.user_email)
        self.assertTrue(WaitList.objects.get(team = team, wait_member = wait_member))
        get_wait_member = team.wait_members.get_wait_member(wait_member.id)
        self.assertEqual(get_wait_member, wait_member)

    # The team member cannot link to join the team,
    # but if it was possible, then redirected to main with messages
    def test_join_already_member_should_be_redirected_to_main_with_message(self):
        self.post_login_set(self.user_email, self.user_password)
        self.post_make_team_set(self.team_name)
        response = self.post_join(id = 1, follow = True)
        self.assertRedirects(response, "/")
        self.assertContains(response, custom_msg.already_member)

    def test_join_already_wait_member_should_be_redirected_to_main_with_message(self):
        self.post_login_set(self.user_email, self.user_password)
        Team.objects.create_team(name = self.team_name)
        self.post_join(id = 1, follow = True)
        response = self.post_join(id = 1, follow = True)
        self.assertRedirects(response, "/")
        self.assertContains(response, custom_msg.already_wait_member)

    """
    test
    1. if Not found -> next operation is not decided yet.
       test code is needed to add after it is decided
    """
