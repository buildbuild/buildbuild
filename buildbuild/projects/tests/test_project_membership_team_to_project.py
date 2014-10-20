from django.test import TestCase
from teams.models import Team
from django.utils import timezone
from projects.models import Project, ProjectMembership

class Membership_team_to_member_test(TestCase):
    def setUp(self):
        self.team_name = "Team1"
        self.team_name_2 = "Team2"

        self.team = Team.objects.create_team(
            name = self.team_name
        )

        self.team_2 = Team.objects.create_team(
            name = self.team_name_2
        )


