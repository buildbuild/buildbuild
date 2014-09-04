from django.test import TestCase
from django.test.client import Client

from teams.models import Team
from projects.models import Project


class TestAPITeamUserListSearch(TestCase):
    """
    * Test Scenario

    - 2 teams ( first_team, second_team )
    - we are going to search for first_team
    ( /api/teams/first_team_name/projects/?search={query} )

    - 3 projects
        - A : project_in_first_team_with_test_string
        - B : project_in_first_team_without_test_string
        - C : project_in_second_team_with_test_string

    - search result should ...
        - contain A
        - NOT contain B
        - NOT contain C
    """
    def setUp(self):
        # Generate Teams
        self.first_team = Team.objects.create_team(
            name="test_teamname_first",
        )
        self.second_team = Team.objects.create_team(
            name="test_teamname_second",
        )

        self.test_string = "test_string"

        # Generate Projects
        self.project_in_first_team_with_test_string = Project.objects.create_project(
            team=self.first_team,
            name="in_team_with" + self.test_string,
        )
        self.project_in_first_team_without_test_string = Project.objects.create_project(
            team=self.first_team,
            name="in_team_without",
        )
        self.project_in_second_team_with_test_string = Project.objects.create_project(
            team=self.second_team,
            name="not_in_team_with" + self.test_string,
        )

        # Get Response
        self.client = Client()
        self.response = self.client.get("/api/teams/" + self.first_team.name + "/projects/?search=" + self.test_string)

    def test_api_teamuser_list_search_should_return_valid_result(self):
        self.assertContains(self.response, self.project_in_first_team_with_test_string.name)
        self.assertNotContains(self.response, self.project_in_first_team_without_test_string.name)
        self.assertNotContains(self.response, self.project_in_second_team_with_test_string.name)
