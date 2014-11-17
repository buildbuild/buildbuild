from django.test import TestCase
from teams.models import Team
from projects.models import Project, ProjectMembership
from buildbuild import attributes_for_tests

class Membership_team_to_member_test(TestCase):
    fixtures = ['properties_data.yaml']
    def setUp(self):
        self.team_name = "Team1"
        self.second_team_name = "Team2"

        self.project_name = "project1"
        self.second_project = "project2"

        self.team = Team.objects.create_team(
            name = self.team_name
        )

        self.second_team = Team.objects.create_team(
            name = self.second_team_name
        )

        self.project = Project.objects.create_project(
            name = self.project_name,
            team_name = self.team_name,
            properties = attributes_for_tests.properties_for_test,
        )
        
        self.second_project = Project.objects.create_project(
            name = self.second_project,
            team_name = self.second_team_name,
             properties = attributes_for_tests.properties_for_test,
        )

        # second team has two projects :
        self.project_membership = ProjectMembership.objects.create_project_membership(
            project = self.second_project,
            team = self.team
        )
       
    def test_get_all_project(self):
        self.assertIsNotNone(self.team.project_teams.all())
 
    def test_team_could_get_all_project_list(self):
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
