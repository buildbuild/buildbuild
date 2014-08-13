from django.test import TestCase
from projects.models import Project
from django.db import IntegrityError

class TestProject(TestCase):
    def setUp(self):
        pass

    def test_project_should_have_name(self):
        try:
            project = Project()
            project.name
        except AttributeError:
            self.fail("Project should have name")

    def test_project_should_have_unique_name(self):
        project = Project()
        project_with_duplicate_name = Project()
        project.name = "abc"
        project.save()
        project_with_duplicate_name.name = project.name
        self.assertRaises(IntegrityError, project_with_duplicate_name.save)
