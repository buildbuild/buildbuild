from django.test import TestCase
from projects.models import Project

class TestProject(TestCase):
    def setUp(self):
        pass

    def test_project_should_have_name(self):
        try:
            project = Project()
            project.name
        except AttributeError:
            self.fail("Project should have name")
