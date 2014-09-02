from django.test import TestCase
from users.models import User
from teams.models import Team

class team_composition_test(TestCase):
    def setUp(self):
        self.team = Team()

    def test_team_should_have_name(self):
        try:
            self.team.name
        except AttributeError:
            self.fail("team should have name")
    
    def test_team_should_not_have_users_before_save(self):
        try:
            self.team.name
        except ValueError:
            pass

    def test_team_should_have_users_after_save(self):
        self.team.name = "test_team"
        self.team.save()
        
        try:
            self.team.members
        except AttributeError:
            self.fail("team must have members after save")

            
