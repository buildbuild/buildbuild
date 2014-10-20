from django.test import TestCase
from teams.models import Team
from projects.models import Project, ProjectWaitList 
from django.utils import timezone

class project_manager_test(TestCase):
    def setUp(self):
        self.team_name = "Team1"
        self.team_name_2 = "Team2"

        self.project_name = "Project1"
        self.project_name_2 = "Project2"

        self.team = Team.objects.create_team(
            name = self.team_name
        )

        self.team_2 = Team.objects.create_team(
            name = self.team_name_2
        )

        self.project = Project.objects.create_project(
            name = self.project_name,
        )
        
        self.project_2 = Project.objects.create_project(
            name = self.project_name_2,
        )
        
        self.project_wait_list = ProjectWaitList.objects.create(
            project = self.project,
            wait_team = self.team
        )
        self.project_wait_list.save()
        
    def test_project_could_get_all_team_wait_list(self):
        try:
            self.project.team_wait_list.all()
        except:
            self.fail("getting all team list failed")
    def test_project_could_get_team_wait_list(self):
        try:
            self.project.team_wait_list.get_team(self.team_name)
        except:
            self.fail("getting a wait team from team wait list failed")

    def test_project_wait_list_must_have_date_joined(self):
        try:
            self.project_wait_list.date_requested
        except:
            self.fail("project_wait_list must have date_requested")

