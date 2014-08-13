from django.test import TestCase
from projects.models import Project
from teams.models import Team
from django.db import IntegrityError
from django.core.exceptions import ValidationError

class TestProject(TestCase):
    def setUp(self):
        self.project = Project()

        # Project should belongs to a Team
        team = Team.objects.create_team(name = "test_team_name")
        self.project.team = team

    def test_project_should_have_name(self):
        try:
            self.project.name
        except AttributeError:
            self.fail("Project should have name")

    def test_project_should_have_unique_name(self):
        self.project.name = "test_project_name"
        self.project.save()
        project_with_duplicate_name = Project(name = self.project.name)

        self.assertRaises(IntegrityError, project_with_duplicate_name.save)

    def test_project_name_is_at_most_255_characters(self):
        self.assertRaises(
            ValidationError,
            Project.objects.create_project,
            name = "a" * 256,
        )

    def test_project_should_have_team_id(self):
        try:
            self.project.team
        except AttributeError:
            self.fail("Project should have team id")

