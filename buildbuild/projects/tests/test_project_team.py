from django.test import TestCase
from projects.models import Project
from teams.models import Team
from django.core.exceptions import ObjectDoesNotExist

class TestProjectTeam(TestCase):
    def setUp(self):
        self.project = Project()
        team = Team.objects.create_team(name = "test_team_name")
        self.project.team = team

    def test_project_should_have_team_id(self):
        try:
            self.project.team
        except AttributeError:
            self.fail("Project should have team id")

