from django.test import TestCase

from teams.models import Team
from teams.serializers import TeamSerializer


class TestTeamSerializer(TestCase):
    def setUp(self):
        self.team = Team.objects.create_team(
            name="test_name"
        )

    def test_team_serializer_return_serialized_data(self):
        serialized_team = TeamSerializer(self.team)
        expected_data = {
            'id': self.team.id,
            'name': self.team.name,
        }
        self.assertEqual(serialized_team.data, expected_data)
