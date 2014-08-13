from django.test import TestCase
from teams.models import Team

class TeamContactNumberTest(TestCase):
    def setUp(self):
        self.team = Team()

    def test_team_should_have_contact_number_field(self):
        try:
            self.team.contact_number
        except AttributeError:
            self.fail("team should have contact number")
