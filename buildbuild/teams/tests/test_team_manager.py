from django.test import TestCase
from teams.models import Team,TeamManager

class TestTeamManager(TestCase):
    def setUp(self):
        self.team = Team()
        self.team.name = "Team1"

        self.valid_team_name = "TeamTeam"

    def test_team_should_be_generated_using_create_team(self):
        try:
            team = Team.objects.create_team(
                name = self.valid_team_name
            )
        except:
            self.fail("Create Team must create team object successfully")

    def test_teams_should_be_get_using_get_all_teams(self):
        pass
