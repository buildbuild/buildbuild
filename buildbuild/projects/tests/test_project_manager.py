from django.test import TestCase
from projects.models import Project
from teams.models import Team
from django.db import IntegrityError
from django.core.exceptions import ValidationError

class TestProjectName(TestCase):
    def setUp(self):
        self.project = Project()

        # Project should belongs to a Team
        self.team = Team.objects.create_team(name = "test_team_name")
        self.project.team = self.team

    def test_project_should_have_unique_name(self):
        self.project.name = "test_project_name"
        self.project.save()
        project_with_duplicate_name = Project(name = self.project.name)
        self.assertRaises(IntegrityError, project_with_duplicate_name.save)

    def test_project_name_is_at_most_64_characters(self):
        self.assertRaises(
            ValidationError,
            Project.objects.create_project,
            name = "a" * 65,
            team = self.team
        )
