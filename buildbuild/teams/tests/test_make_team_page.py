from django.test import TestCase
from django.test.client import Client
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from teams.views import MakeTeamView
from teams.models import Team

class MakeTeamPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.valid_name = "buildbuild_team"

        # need to find more eloquent way to test redirect url.
        self.TEST_SERVER_URL = "http://testserver"

    def test_get_make_team_page_request_should_return_200(self):
        response = self.client.get("/maketeam/")
        self.assertEqual(response.status_code, 200)
    
    def test_check_uniqueness_of_team_name(self):
        Team.objects.create_team(self.valid_name)

        try:
            respanse = self.client.post("/maketeam/", {
                "name":self.valid_name,
                })
        except:
            pass

    def test_post_available_team_information_return_302(self):
        response = self.client.post("/maketeam/", {
            "name": self.valid_name,
            })
        self.assertEqual(response.status_code, 302)

    def test_post_available_information_redirect_to_home(self):
        response = self.client.post("/maketeam/", {
             "name": self.valid_name,
            })
        self.assertEqual(response["Location"], self.TEST_SERVER_URL + "/")
 
