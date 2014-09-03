from django.test import TestCase
from django.test.client import Client

from teams.models import Team


class TestAPITeamDetail(TestCase):
    def setUp(self):
        self.team = Team.objects.create_team(
            name="test_teamname"
        )
        self.client = Client()
        self.response = self.client.get("/api/teams/" + self.team.name + "/")

    def test_api_team_detail_request_should_return_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_api_team_detail_request_should_return_json(self):
        self.assertEqual(self.response["Content-Type"], "application/json")

    def test_api_team_detail_request_should_contain_team_id_and_name(self):
        self.assertContains(self.response, self.team.id)
        self.assertContains(self.response, self.team.name)
