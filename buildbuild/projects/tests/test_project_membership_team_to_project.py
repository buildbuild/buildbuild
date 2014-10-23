from django.test import TestCase
from teams.models import Team
from django.utils import timezone
from projects.models import Project, ProjectMembership

class Membership_team_to_member_test(TestCase):
    def setUp(self):
        self.team_name = "Team1"
        self.second_team = "Team2"

        self.project_name = "Project1"
        self.second_project = "Project2"

        self.team = Team.objects.create_team(
            name = self.team_name
        )

        self.second_team = Team.objects.create_team(
            name = self.second_team
        )

        self.project = Project.objects.create_project(
            name = self.project_name,
        )
        
        self.second_project = Project.objects.create_project(
            name = self.second_project,
        )
        
        self.project_membership = ProjectMembership.objects.create_project_membership(
            project = self.project,
            team = self.team
        )
        self.project_membership = ProjectMembership.objects.create_project_membership(
            project = self.second_project,
            team = self.team
        )
       
    def test_get_all_project_teams(self):
        self.assertIsNotNone(self.team.project_teams.all())
 
    def test_project_could_get_all_project_teams(self):
        project_teams = self.team.project_teams.all()
        self.assertEqual(project_teams[0], self.project)
        self.assertEqual(project_teams[1], self.second_project)

    def test_team_could_leave_belonged_project(self):
        try:
            self.team.project_membership_project_team.leave_project(
                self.project.id
            )
        except ValidationError:
            self.fail("leave_project has occured an error")

    def test_leaved_team_cannot_belong_project(self):
        self.team.project_membership_project_team.leave_project(
            self.project.id
        )

        belonged_project = self.team.project_teams.all()
        self.assertNotIn(self.team, belonged_project)
