from django.test import TestCase
from django.test.client import Client
from django.core.exceptions import ObjectDoesNotExist
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


    def test_get_make_team_page_request_with_login_response_to_maketeam(self):
        self.client.post("/login/", {
            "email" : self.user_email,
            "password" : self.user_password,
        })
        response = self.client.get("/maketeam/")
        self.assertEqual(response._request.path, "/maketeam/")
 
    def test_get_make_team_page_without_login_redirect_to_login_page(self):
        response = self.client.get("/maketeam/", follow = True)
        self.assertEqual(response.wsgi_request.path, "/login/")
 
    def test_check_uniqueness_of_name(self):
        Team.objects.create_team(self.team_name)
        try:
            response = self.client.post("/maketeam/", {
                "teams_team_name":self.team_name,
                })
        except ValidationError:
            pass
    
    def test_post_vaild_team_information_redirect_to_main_page(self):
        self.client.post("/login/", {
            "email" : self.user_email,
            "password" : self.user_password,
        })
 
        response = self.client.post("/maketeam/", {
            "teams_team_name": self.team_name,
            },
            follow = True
            )
        self.assertEqual(response._request.path, "/")

    def test_post_invaild_team_name_redirect_to_make_team_page(self):
        self.client.post("/login/", {
            "email" : self.user_email,
            "password" : self.user_password,
        })
 
        response = self.client.post("/maketeam/", {
            "teams_team_name": self.invalid_team_name,
            },
            follow = True
            )
        self.assertEqual(response._request.path, "/maketeam/")

    def test_user_who_created_team_should_have_membership_relation(self):
        self.client.post("/login/", {
            "email" : self.user_email,
            "password" : self.user_password,
        })
 
        self.client.post("/maketeam/", {
            "teams_team_name": self.team_name,
            }
        )
        team = Team.objects.get_team(id = 1)
        try:
            member = team.members.get_member(self.user.id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                "user_who_created_team_should_have_membership_relation"
            )

    def test_user_who_is_not_team_maker_should_not_have_membership_relation(self):
        self.client.post("/login/", {
            "email" : self.user_email,
            "password" : self.user_password,
        })
 
        self.client.post("/maketeam/", {
            "teams_team_name": self.team_name,
            }
        )
        team = Team.objects.get_team(id = 1)
        try:
            member = team.members.get_member(self.second_user.id)
        except ObjectDoesNotExist:
            pass


