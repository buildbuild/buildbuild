from django.test import TestCase
from projects.models import Project
from teams.models import Team
from django.db import IntegrityError
from django.core.exceptions import ValidationError

class TestProjectName(TestCase):
    def setUp(self):
        self.project = Project()
        self.valid_team_name = "test_team_name"
        self.valid_project_name = "test_project_name"
        self.team = Team.objects.create_team(name = self.valid_team_name)
        self.project.team = self.team

    def test_project_manager_could_create_project(self):
        self.assertTrue(
                Project.objects.create_project(
                    name = self.valid_project_name, 
                    team = self.team
                )
        )

    def test_project_should_have_unique_name(self):
        try:
            Project.objects.create_project(
                name = self.valid_project_name, 
                team = self.team
            )
            Project.objects.create_project(
                name = self.valid_project_name, 
                team = self.team
            )
        except IntegrityError:
            pass
    def test_project_name_is_at_most_64_characters(self):
        try:        
            Project.objects.create_project(
                name = "a" * 65,
                team = self.team,
            )
        except ValidationError:
            pass


            
