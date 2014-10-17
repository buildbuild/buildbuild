from django.test import TestCase
from projects.models import Project
from teams.models import Team
from django.db import IntegrityError
from django.core.exceptions import ValidationError

class TestProjectName(TestCase):
    def setUp(self):
        self.project_name = "test_project_name"
        self.second_project_name = "test_second_project_name"
        self.invalid_long_length_name = "a" * 31
 
        self.project = Project.objects.create_project(
            name = self.project_name,
        )
        self.second_project = Project.objects.create_project(
            name = self.second_project_name,
        )

# Attribute
    def test_create_project_must_contain_name(self):
        try:
            project = Project.objects.create_project(
                name = ""
            )
        except AttributeError:
            pass

# Validation
    def test_project_name_is_restricted_30_characters(self):
        try:        
            Project.objects.create_project(
                name = self.invalid_long_length_name,
            )
        except ValidationError:
            pass

    def test_get_all_projects(self):
        projects = Project.objects.all()

        self.assertQuerysetEqual(
            projects, 
            ["<Project: "+self.project.name+">",
            "<Project: "+self.second_project.name+">"],
            ordered=False
        )

# Integrity
    def test_project_should_have_unique_name(self):
        try:
           Project.objects.create_project(
                name = self.project_name, 
            )
        except IntegrityError:
            pass

# Assert
    def test_get_project_equal_to_project_targetted(self):
        get_project = Project.objects.get_project(self.project_name)
        self.assertEqual(
                self.project, 
                get_project, 
                "get_project should be equal to tart project",
        )
           
