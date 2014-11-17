from django.test import TestCase
from projects.models import Project
from teams.models import Team
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from buildbuild import attributes_for_tests

class TestProjectName(TestCase):
    fixtures = ['properties_data.yaml']
    def setUp(self):
        self.name = "test_project_name"
        self.second_name = "test_second_project_name"
        self.create_name = "test_project"
        self.invalid_long_length_name = "a" * 65
        self.team_name = "test_team_name"
        self.team_name_does_not_have_any_project_yet = "test_second_team_name"
        self.invalid_swift_container_name = self.team_name + "__" + self.second_name
        self.lang_python = "python"
        self.ver_python_278 = "2.7.8"
        self.valid_name_with_characters = "testproject0-_"
        self.project_name_with_capital_letters = "Projects" 

        self.team = Team.objects.create_team(self.team_name)
        self.team_name_does_not_have_any_project_yet = \
            Team.objects.create_team(
                self.team_name_does_not_have_any_project_yet
            )


        self.project = Project.objects.create_project(
            name = self.name,
            team_name = self.team_name,
            properties = attributes_for_tests.properties_for_test,
        )

        self.second_project = Project.objects.create_project(
            name = self.second_name,
            team_name = self.team_name,
            properties = attributes_for_tests.properties_for_test,
        )

    def test_create_project_must_contain_name(self):
        self.assertRaises(
            TypeError,
            Project.objects.create_project,
            team_name = self.team_name,
            properties = {self.lang_python : self.ver_python_278}
        )

    def test_create_project_name_with_available(self):
        Project.objects.create_project(
            name = self.valid_name_with_characters,
            team_name = self.team_name,
            properties = attributes_for_tests.properties_for_test,
        )

    def test_create_project_name_min_length_1(self):
        self.assertRaises(
            ValidationError,
            Project.objects.create_project,
            name = "",
            team_name = self.team_name
        )

    def test_project_name_max_length_64(self):
        self.assertRaises(
            ValidationError,
            Project.objects.create_project,
            name = self.invalid_long_length_name,
            team_name = self.team_name,
            properties = attributes_for_tests.properties_for_test,
        )

    def test_get_all_projects(self):
        projects = Project.objects.all()
        self.assertEqual(projects[0].name, self.project.name)
        self.assertEqual(projects[1].name, self.second_project.name)

    def test_check_project_unique_name(self):
        self.assertRaises(
            IntegrityError,
            Project.objects.create_project,
            name = self.name,
            team_name = self.team_name,
            properties = attributes_for_tests.properties_for_test,
        )

    def test_get_project_equal_to_project_targetted(self):
        get_project = Project.objects.get_project(self.project.id)
        self.assertEqual(
                self.project, 
                get_project, 
                "get_project should be equal to target project",
        )

    def test_properties_field_must_dict(self):
        self.assertRaises(
            TypeError,
            Project.objects.create_project,
            name = self.project.name,
            team_name = self.team_name_does_not_have_any_project_yet,
            properties = (self.lang_python, self.ver_python_278)
        )

    def test_project_team_name_required(self):
        self.assertRaises(
            TypeError,
            Project.objects.create_project,
            name = self.create_name,
            properties = attributes_for_tests.properties_for_test,
        )

    def test_swift_container_name_should_be_in_rule(self):
        #Rule : team_name + __ + project_name
        self.assertNotEqual(self.project.swift_container,
                         self.invalid_swift_container_name,
                         "Invalid swift container name must be not equal with model member")

    def test_project_name_with_capital_letters_must_be_not_allowed(self):
        self.assertRaises(
            ValidationError,
            Project.objects.create_project,
            name = self.project_name_with_capital_letters,
            team_name = self.team.name,
            properties = attributes_for_tests.properties_for_test,
        )
        
