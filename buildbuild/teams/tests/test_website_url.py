from django.test import TestCase
from users.models import User
from teams.models import Team

class team_website_url_test(TestCase):
    def setUp(self):
        self.team = Team()

    def test_team_should_have_website_url(self):
        try:
            self.team.website_url
        except AttributeError:
            self.fail("team should have website_url")
