from django.test import TestCase
from users.models import User
from teams.models import Team

class team_website_url_test(TestCase):
    def setUp(self):
        self.team = Team()

    # when after team url form added, the test will be continued
    def test_team_should_have_team_url(self):
        pass
