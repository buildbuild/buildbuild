from django.test import TestCase

from projects.models import Project
from projects.serializers import ProjectSerializer

class TestProjectSerializer(TestCase):
    def setUp(self):
        self.project = Project.objects.create_project(
            name="test_project_name",
            team_name="test_team_name"
        )

    def test_project_serializer_return_serialized_data(self):
        serialized_team = ProjectSerializer(self.project)
        expected_data = {
            'id': self.project.id,
            'name': self.project.name,
        }
        self.assertEqual(serialized_team.data, expected_data)
