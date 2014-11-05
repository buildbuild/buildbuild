from django.test import TestCase
from django.test.client import Client

from teams.models import Team
from projects.models import Project, ProjectMembership

class TestAPITeamProjectList(TestCase):
    def setUp(self):
        """
        * test scenario
        - 1 team
        - 2 projects belongs to team ( A, B )
        - 1 project not belongs to team ( C )

        request teamproject-list API
        - response should contain A, B projects info
        - response should not contain C project info
        """
        self.team = Team.objects.create_team(
            name="test_teamname"
        )
        self.other_team = Team.objects.create_team(
            name="test_other_teamname"
        )

        self.first_project_belongs_to_team = Project.objects.create_project(
            name="test_project_name_first",
        )
        self.second_project_belongs_to_team = Project.objects.create_project(
            name="test_project_name_second",
        )
        self.project_not_belongs_to_team = Project.objects.create_project(
            name="test_project_name_third",
        )

        """
        * should implement later using some eloquent method.
        there is no method for make relation between user and team
        in this test case, going to use Membership Model directly.
        """
        self.first_project_membership = ProjectMembership()
        self.first_project_membership.project_team = self.team
        self.first_project_membership.project = self.first_project_belongs_to_team
        self.first_project_membership.save()

        self.second_project_membership = ProjectMembership()
        self.second_project_membership.project_team = self.team
        self.second_project_membership.project = self.second_project_belongs_to_team
        self.second_project_membership.save()
 

        self.client = Client()
        self.response = self.client.get("/api/teams/" + self.team.name + "/projects/")

        self.not_exist_teamname = "test_teamname_not_exist"
        self.response_with_not_exist_teamname = \
            self.client.get("/api/teams/" + self.not_exist_teamname + "/users/")

    def test_api_teamproject_list_request_should_return_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_api_teamproject_list_request_with_not_exist_teamname_should_return_200(self):
        self.assertEqual(self.response_with_not_exist_teamname.status_code, 404)

    def test_api_teamproject_list_request_should_return_json(self):
        self.assertEqual(self.response["Content-Type"], "application/json")

    def test_api_teamproject_list_request_should_contain_projects_belong_to_team(self):
        self.assertContains(self.response, self.first_project_belongs_to_team.name)
        self.assertContains(self.response, self.second_project_belongs_to_team.name)

    def test_api_teamproject_list_request_should_not_contain_user_not_belong_to_team(self):
        self.assertNotContains(self.response, self.project_not_belongs_to_team.name)


