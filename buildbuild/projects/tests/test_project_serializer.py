from django.test import TestCase

from projects.models import Project
from projects.serializers import ProjectSerializer
from buildbuild import attributes_for_tests
from teams.models import Team

class TestProjectSerializer(TestCase):
    fixtures = ['properties_data.yaml']
    def setUp(self):
        test_team_name = "test_team_name"
        Team.objects.create_team(test_team_name)
        self.project = Project.objects.create_project(
            name="test_project_name",
            team_name="test_team_name",
            properties = attributes_for_tests.properties_for_test,
        )

    def test_project_serializer_return_serialized_data(self):
        serialized_team = ProjectSerializer(self.project)
        expected_data = {
            'id': self.project.id,
            'name': self.project.name,
        }
        self.assertEqual(serialized_team.data, expected_data)
