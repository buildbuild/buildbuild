from django.test import TestCase
from django.test.client import Client
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from projects.views import MakeProjectView
from projects.models import Project

from teams.models import Team
from users.models import User
from buildbuild import custom_msg


class MakeProjectPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.project_name = "buildbuild_project"
        self.team_name = "buildbuild_team"
        self.second_team_name = "must_be_created_by_post_method"
        self.lang = "python"
        self.ver = "2.7.8"

        self.user_email = "test@example.com"
        self.user_password = "test_password"
        
        self.TEST_SERVER_URL = "http://testserver"

        self.user = User.objects.create_user(
            email = self.user_email,
            password = self.user_password,
        )

    # Default Set function, These are not Unit Test function
    def post_login_set(self, user_email="", user_password="", follow = False):
        response = self.client.post(
                       "/users/login/", {
                           "email" : user_email,
                           "password" : user_password,
                       },
                       follow = follow
                   )
        return response

    # Default Set function, These are not Unit Test function
    def post_make_team_set(self, team_name="", follow=False):
        response = self.client.post(
                       "/teams/maketeam/", {
                       "teams_team_name": team_name,
                       },
                       follow = follow
                   )
        return response

    # Default Set function, These are not Unit Test function
    def post_make_project_set(self, name="", team_name="", follow=False, **kwargs):

        if "properties" in kwargs:
            properties = kwargs["properties"]
            Language = 0
            Version = 1
            response = self.client.post(
                           "/projects/makeproject/", {
                               "projects_project_name" : name,
                               "projects_team_name" : team_name,
                               "lang" : properties[Language],
                               "ver" : properties[Version],
                           },
                           follow = follow
                       )
        else:
            response = self.client.post(
                           "/projects/makeproject/", {
                               "projects_project_name" : name,
                               "projects_team_name" : team_name
                           },
                           follow = follow
                       )
        return response  

    # Test Code for Default Set function
    def test_post_make_project_set(self):
        self.post_make_project_set(self.project_name, team_name = self.team_name)

    # Test Code for Default Set function
    def test_post_login_set(self):
        self.post_login_set(self.user_email, self.user_password)

    # Test Code for Default Set function
    def test_post_make_team_set(self):
        self.post_make_team_set(self.team_name)

    def test_get_make_project_page_request_with_login(self):
        self.post_login_set()
        response = self.client.get("/projects/makeproject/")
        self.assertEqual(response.wsgi_request.path, "/projects/makeproject/")
   
    def test_get_make_project_page_without_login_redirect_to_login_page(self):
        response = self.client.get("/projects/makeproject/", follow = True)
        self.assertEqual(response.wsgi_request.path, "/users/login/")
 
    def test_check_uniqueness_of_project_name(self):
        self.post_login_set(self.user_email, self.user_password)
        self.post_make_team_set(self.team_name)
        self.post_make_team_set(self.second_team_name)
        self.post_make_project_set(name = self.project_name, team_name = self.team_name)
        response = self.post_make_project_set(self.project_name, team_name = self.second_team_name, follow = True)
        self.assertRedirects(response, "/projects/makeproject/")
        self.assertContains(response, custom_msg.project_already_exist)

    def test_post_project_with_valid_informations_should_redirect_to_home(self):
        self.post_login_set(self.user_email, self.user_password)
        self.post_make_team_set(self.team_name, follow = True)
        response = self.post_make_project_set(name = self.project_name, team_name = self.team_name, follow = True)
        self.assertRedirects(response, "/")
        self.assertContains(response, custom_msg.project_make_success)

    def test_post_without_project_name_redirect_to_make_project_page(self):
        self.post_login_set(self.user_email, self.user_password)
        self.post_make_team_set(self.team_name)
        response = self.post_make_project_set(
            team_name = self.team_name,
            follow = True,
            properties = (self.lang, self.ver)
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, custom_msg.this_field_is_required)    
    
    def test_post_properties_with_lang_and_without_ver_raise_error_and_redirect_to_makeproject(self):
        self.post_login_set(self.user_email, self.user_password)
        self.post_make_team_set(self.team_name)
        response = self.client.post(
                       "/projects/makeproject/", {
                           "projects_project_name" : self.project_name,
                           "projects_team_name" : self.team_name,
                           "lang" : self.lang
                       },
                       follow = True
                   )
        self.assertRedirects(response, "/projects/makeproject/")
        self.assertContains(response, custom_msg.project_both_lang_and_ver_is_needed)    

    def test_post_properties_without_lang_and_with_ver_raise_error_and_redirect_to_makeproject(self):
        self.post_login_set(self.user_email, self.user_password)
        self.post_make_team_set(self.team_name)
        response = self.client.post(
                       "/projects/makeproject/", {
                           "projects_project_name" : self.project_name,
                           "projects_team_name" : self.team_name,
                           "ver" : self.ver
                       },
                       follow = True
                   )
        self.assertRedirects(response, "/projects/makeproject/")
        self.assertContains(response, custom_msg.project_both_lang_and_ver_is_needed)    


