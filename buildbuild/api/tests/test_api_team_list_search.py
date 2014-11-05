from django.test import TestCase
from django.test.client import Client

from teams.models import Team


class TestAPITeamListSearch(TestCase):
    def setUp(self):
        self.test_string = "test_string"
        self.team_with_test_string = Team.objects.create_team(
            name="team_name_with_" + self.test_string,
            # prefix 'test_' is excluded in this test case
            # because of model validation ( max_length=30 on Team.name )
        )
        self.team_without_test_string = Team.objects.create_team(
            name="team_name_without_",  # + self.test_string,
        )

        self.client = Client()
        self.response = self.client.get("/api/teams/?search=" + self.test_string)

    def test_api_team_list_search_should_return_valid_result(self):
        self.assertContains(self.response, self.team_with_test_string.name)
        self.assertNotContains(self.response, self.team_without_test_string.name)
