from django.test import TestCase
from projects.models import Project, ProjectMembership, Team
from django.utils import timezone
from django.core.exceptions import ValidationError
from buildbuild import attributes_for_tests

class ProjectMembership_test(TestCase):
    fixtures = ['properties_data.yaml']
    def setUp(self):
        self.team_name = "Team1"
        self.second_team_name = "Second_Team"
        self.project_name = "project1"
        self.second_project_name = "second_project"

        self.team = Team.objects.create_team(
            name = self.team_name
        )

        self.second_team = Team.objects.create_team(
            name = self.second_team_name
        )

        self.project = Project.objects.create_project(
            name = self.project_name,
            team_name = self.team.name,
            properties = attributes_for_tests.properties_for_test,
        )

        self.second_project = Project.objects.create_project(
            name = self.second_project_name,
            team_name = self.second_team.name,
            properties = attributes_for_tests.properties_for_test,
        )

        self.project_membership = ProjectMembership.objects.get(
                                      project = self.project,
                                      project_team = self.team,
                                  )

# Attribute
    def test_project_membership_must_have_date_joined(self):
        try:
            self.project_membership.date_joined
        except AttributeError:
            self.fail("project_membership should have date_joined")

# Validation
    def test_create_project_membership_project_argument_should_be_User_object(self):
        try:
            self.project_membership = ProjectMembership.objects.create_project_membership(
                project = self.project,
                team = self.project,
            )
        except :
            pass

    def test_create_project_membership_project_argument_should_be_Team_object(self):
        try:
            self.project_membership = ProjectMembership.objects.create_project_membership(
                project = self.team,
                team = self.team,
            )
        except ValidationError:
            pass

