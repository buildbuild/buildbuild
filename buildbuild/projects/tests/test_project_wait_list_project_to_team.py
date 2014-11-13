from django.test import TestCase
from teams.models import Team
from projects.models import Project, ProjectWaitList 
from django.utils import timezone

class project_manager_test(TestCase):
    def setUp(self):
        self.team_name = "Team1"
        self.team_name_2 = "Team2"

        self.project_name = "Project1"
        self.second_project_name = "Project2"

        self.team = Team.objects.create_team(
            name = self.team_name
        )

        self.team_2 = Team.objects.create_team(
            name = self.team_name_2
        )

        self.project = Project.objects.create_project(
            name = self.project_name,
            team_name = self.team_name
        )
        
        self.second_project = Project.objects.create_project(
            name = self.second_project_name,
            team_name = self.team_name_2
        )
        
        self.project_wait_list = ProjectWaitList.objects.create_project_wait_list(
            project = self.project,
            team = self.team
        )
        self.project_wait_list.save()
        
    def test_project_could_get_all_project_project_wait_teams(self):
        try:
            self.project.project_wait_teams.all()
        except:
            self.fail("getting all team list failed")
    def test_project_could_get_project_project_wait_team(self):
        try:
            self.project.project_wait_teams.get_project_team(self.team.id)
        except:
            self.fail("getting a wait team from team wait list failed")


