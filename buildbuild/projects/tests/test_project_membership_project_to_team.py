from django.test import TestCase
from teams.models import Team
from projects.models import Project, ProjectMembership 
from django.utils import timezone
from buildbuild import attributes_for_tests

class project_membership_test(TestCase):
    fixtures = ['properties_data.yaml']
    def setUp(self):
        self.team_name = "Team1"
        self.second_team = "Team2"

        self.project_name = "Project1"
        self.second_project = "Project2"

        self.team = Team.objects.create_team(
            name = self.team_name
        )

        self.team_2 = Team.objects.create_team(
            name = self.second_team
        )

        self.project = Project.objects.create_project(
            name = self.project_name,
            team_name = self.team.name,
            properties = attributes_for_tests.properties_for_test,
        )
        
        self.project_2 = Project.objects.create_project(
            name = self.second_project,
            team_name = self.second_team,
            properties = attributes_for_tests.properties_for_test,
        )
        
    def test_project_could_get_all_project_teams(self):
        try:
            self.project.project_teams.all()
        except:
            self.fail("getting all team list failed")
    def test_project_could_get_project_teams(self):
        try:
            self.project.project_teams.get_project_team(self.team.id)
        except:
            self.fail("getting a team from team list failed")


