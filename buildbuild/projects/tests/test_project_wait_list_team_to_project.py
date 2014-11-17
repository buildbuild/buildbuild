from django.test import TestCase
from teams.models import Team
from projects.models import Project, ProjectWaitList 
from django.utils import timezone
from buildbuild import attributes_for_tests

class project_manager_test(TestCase):
    fixtures = ['properties_data.yaml']
    def setUp(self):
        self.team_name = "Team1"
        self.team_name_2 = "Team2"

        self.project_name = "project1"
        self.second_project_name = "project2"

        self.team = Team.objects.create_team(
            name = self.team_name
        )

        self.team_2 = Team.objects.create_team(
            name = self.team_name_2
        )
        
        self.project = Project.objects.create_project(
            name = self.project_name,
            team_name = self.team_name,
            properties = attributes_for_tests.properties_for_test,
        )
        
        self.second_project = Project.objects.create_project(
            name = self.second_project_name,
            team_name = self.team_name_2,
            properties = attributes_for_tests.properties_for_test,
        )
        
        self.project_wait_list = ProjectWaitList.objects.create_project_wait_list(
            project = self.project,
            team = self.team
        )
        self.project_wait_list.save()
        
    def test_project_wait_team_could_get_all_projects(self):
        try:
            self.team.project_wait_teams.all()
        except:
            self.fail("getting all project list failed")

