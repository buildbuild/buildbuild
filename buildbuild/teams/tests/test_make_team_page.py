from django.test import TestCase
from django.test.client import Client
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError

from teams.views import MakeTeamView
from teams.models import Team
from users.models import User

class MakeTeamPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.team_name = "buildbuild_team"
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

        self.this_field_is_required =  "This field is required."
        self.max_value_exception = "Ensure this value has at most"
        self.team_invalid = "ERROR : invalid team name"
        self.team_already_exist = "ERROR : The team name already exists"
        self.team_make_success = "Team created successfully"

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

    # Test Code for Default Set function
    def test_post_login_set(self):
        self.post_login_set(self.user_email, self.user_password)

    # Default Set function, These are not Unit Test function
    def post_make_team_set(self, team_name="", follow=False):
        response = self.client.post(
                       "/maketeam/", {
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

    def test_get_make_team_page_request_with_login_response_to_maketeam(self):
        self.post_login_set(self.user_email, self.user_password)
        response = self.client.get("/maketeam/")
        self.assertEqual(response._request.path, "/maketeam/")
 
    def test_get_make_team_page_without_login_redirect_to_login_page(self):
        response = self.client.get("/maketeam/", follow = True)
        self.assertEqual(response.wsgi_request.path, "/login/")
 
    def test_check_uniqueness_of_name(self):
        self.post_login_set(self.user_email, self.user_password)
        self.post_make_team_set(self.team_name)
        response = self.post_make_team_set(self.team_name, follow = True)
        self.assertContains(response, self.team_already_exist)
    
    def test_post_vaild_team_information_redirect_to_main_page(self):
        self.post_login_set(self.user_email, self.user_password)
        response = self.post_make_team_set(self.team_name, follow = True)
        self.assertRedirects(response, "/")
        self.assertContains(response, self.team_make_success)

    def test_post_team_name_required(self):
        self.post_login_set(self.user_email, self.user_password)
        response = self.post_make_team_set(follow = True)
        self.assertContains(response, self.this_field_is_required)

    def test_post_team_name_more_than_max_length_error_message(self):
        self.post_login_set(self.user_email, self.user_password)
        response = self.post_make_team_set(self.invalid_team_name)
        self.assertContains(response, self.max_value_exception)

    def test_user_who_created_team_should_have_membership_relation(self):
        self.post_login_set(self.user_email, self.user_password)
        self.post_make_team_set(self.team_name)
        team = Team.objects.get_team(id = 1)
        self.assertIsNotNone(
            team.members.get_member(self.user.id),
        )
        self.assertEqual(
            team.members.get_member(self.user.id),
            self.user,
        )
    
    # The test code should be modified, after team request to join function added
    def test_user_who_is_not_team_maker_should_not_have_membership_relation(self):
        self.post_login_set(self.user_email, self.user_password)
        self.post_make_team_set(self.team_name)
        team = Team.objects.get_team(id = 1)

        # If not team member? then Error
        self.assertRaises(
            ObjectDoesNotExist,
            team.members.get_member,
            self.second_user.id,
        )


