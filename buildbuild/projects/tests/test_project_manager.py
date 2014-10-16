from django.test import TestCase
from projects.models import Project
from teams.models import Team
from django.db import IntegrityError
from django.core.exceptions import ValidationError

class TestProjectName(TestCase):
    def setUp(self):
        self.project_name = "test_project_name"

        self.project = Project.objects.create_project(
            name = self.project_name,
        )

    def test_project_should_have_unique_name(self):
        try:
           Project.objects.create_project(
                name = self.project_name, 
            )
        except IntegrityError:
            pass
    def test_project_name_is_at_most_64_characters(self):
        try:        
            Project.objects.create_project(
                name = "a" * 65,
            )
        except ValidationError:
            pass


            
