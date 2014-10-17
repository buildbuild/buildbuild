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
        self.name = "buildbuild_team"
        self.invalid_name = "a" * 65

        # need to find more eloquent way to test redirect url.
        self.TEST_SERVER_URL = "http://testserver"

        self.valid_email = "test@example.com"
        self.valid_password = "test_password"

        # User authenticated, not destroyed in class
        self.user = User.objects.create_user(
                email = self.valid_email,
                password = self.valid_password,
                )

    def test_get_make_team_page_request_with_login_response_to_maketeam(self):
        self.client.post("/login/", {
            "email" : self.valid_email,
            "password" : self.valid_password,
        })
        response = self.client.get("/maketeam/")
        self.assertEqual(response._request.path, "/maketeam/")
 
    def test_get_make_team_page_without_login_redirect_to_login_page(self):
        response = self.client.get("/maketeam/", follow = True)
        self.assertEqual(response.wsgi_request.path, "/login/")
 
    def test_check_uniqueness_of_name(self):
        Team.objects.create_team(self.name)
        try:
            response = self.client.post("/maketeam/", {
                "teams_team_name":self.name,
                })
        except ValidationError:
            pass
    
    def test_post_vaild_team_information_redirect_to_main_page(self):
        self.client.post("/login/", {
            "email" : self.valid_email,
            "password" : self.valid_password,
        })
 
        response = self.client.post("/maketeam/", {
            "teams_team_name": self.name,
            },
            follow = True
            )
        self.assertEqual(response._request.path, "/")

    def test_post_invaild_team_name_redirect_to_make_team_page(self):
        self.client.post("/login/", {
            "email" : self.valid_email,
            "password" : self.valid_password,
        })
 
        response = self.client.post("/maketeam/", {
            "teams_team_name": self.invalid_name,
            },
            follow = True
            )
        self.assertEqual(response._request.path, "/maketeam/")

   
