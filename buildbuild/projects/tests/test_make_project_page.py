from django.test import TestCase
from django.test.client import Client
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from projects.views import MakeProjectView
from projects.models import Project

from teams.models import Team
from users.models import User

class MakeProjectPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.name = "buildbuild_project"
        self.team_name = "buildbuild_team"
        self.lang = "python"
        self.ver = "2.7.8"

        self.team = Team.objects.create_team(name = self.team_name)
 
        self.valid_email = "test@example.com"
        self.valid_password = "test_password"
        
        # need to find more eloquent way to test redirect url.
        self.TEST_SERVER_URL = "http://testserver"

        # User authenticated, not destroyed in class
        self.user = User.objects.create_user(
                email = self.valid_email,
                password = self.valid_password,
                )

        # Redirect to login page when Anonymous user try to access make project page
        self.login_template = ["users/login.html"]

    def test_get_make_project_page_request_with_login_response_to_makeproject(self):
        self.client.post("/login/", {
            "email" : self.valid_email,
            "password" : self.valid_password,
        })
        response = self.client.get("/makeproject/")
        self.assertEqual(response._request.path, "/makeproject/")
   
    def test_get_make_project_page_without_login_redirect_to_login_page(self):
        response = self.client.get("/makeproject/", follow = True)
        self.assertEqual(response.wsgi_request.path, "/login/")
 
    def test_check_uniqueness_of_name(self):
        self.client.post("/login/", {
            "email" : self.valid_email,
            "password" : self.valid_password,
        })
 
        try:
            response = self.client.post("/makeproject/", {
                "name":self.name,
            })
            response = self.client.post("/makeproject/", {
                "name":self.name,
            })
        except IntegrityError:
            pass

    def test_post_project_with_valid_name_should_redirect_to_home(self):
        self.client.post("/login/", {
            "email" : self.valid_email,
            "password" : self.valid_password,
        })
        response = self.client.post("/makeproject/", {
            "projects_project_name" : self.name,
            },
            follow = True,
            )
        self.assertEqual(response._request.path, "/")

       
    def test_post_without_project_name_redirect_to_make_project_page(self):
        self.client.post("/login/", {
            "email" : self.valid_email,
            "password" : self.valid_password,
        })
        response = self.client.post("/makeproject/", {
            "team_name" : self.team_name,
            "lang" : self.lang,
            "ver" : self.ver,
            },
            follow = True,
            )
        self.assertEqual(response._request.path, "/makeproject/")
   
    """
    def test_post_properties_without_either_lang_and_ver_redirect_to_makeproject(self):
        response = self.client.post("/makeproject/", {
            "name" : self.name,
            "lang" : self.lang,
            })
        self.assertEqual(response.status_code, 302)

        response = self.client.post("/makeproject/", {
            "name" : self.name,
            "ver" : self.ver,
            })
        self.assertEqual(response.status_code, 302)
    
    def test_post_available_project_valid_information_return_302(self):
        response = self.client.post("/makeproject/", {
            "name": self.name,
            })
        self.assertEqual(response.status_code, 302)

    """
