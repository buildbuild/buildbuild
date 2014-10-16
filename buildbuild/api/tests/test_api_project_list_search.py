from django.test import TestCase
from django.test.client import Client

from projects.models import Project
from teams.models import Team


class TestAPIProjectListSearch(TestCase):
    def setUp(self):
        self.test_string = "test_string"
        self.team = Team.objects.create_team(
            name="test_team_name",
        )
        self.project_with_test_string = Project.objects.create_project(
            name="test_project_name_with" + self.test_string,
        )
        self.project_without_test_string = Project.objects.create_project(
            name="test_project_name_without",   # +self.test_string
                                                # intentionally excluded
                                                # for valid search result
        )

        self.client = Client()
        self.response = self.client.get("/api/projects/?search=" + self.test_string)

    def test_api_project_list_search_should_return_valid_result(self):
        self.assertContains(self.response, self.project_with_test_string.name)
        self.assertNotContains(self.response, self.project_without_test_string.name)
