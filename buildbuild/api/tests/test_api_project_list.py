from django.test import TestCase
from django.test.client import Client

from projects.models import Project
from teams.models import Team
from buildbuild import attributes_for_tests

class TestAPIUserList(TestCase):
    fixtures = ['properties_data.yaml']
    def setUp(self):
        self.team = Team.objects.create_team(
            name="test_team_name",
        )
        self.project = Project.objects.create_project(
            name="test_project_name",
            team_name=self.team.name,
            properties = attributes_for_tests.properties_for_test,
        )

        self.client = Client()
        self.response = self.client.get("/api/projects/")

    def test_api_project_list_request_should_return_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_api_project_list_request_should_return_json(self):
        self.assertEqual(self.response["Content-Type"], "application/json")

    def test_api_project_list_request_should_contain_project_id_and_name(self):
        self.assertContains(self.response, self.project.id)
        self.assertContains(self.response, self.project.name)
