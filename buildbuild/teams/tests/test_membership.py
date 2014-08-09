from django.test import TestCase
from teams.models import Team, Membership
from users.models import User

class team_manager_test(TestCase):
    def setUp(self):
        self.membership = Membership()

    def test_team_membership_should_have_is_admin(self):
        try:
            self.membership.is_admin
        except AttributeError:
            self.fail("team membership should have is_admin")
    def test_team_membership_should_have_date_joined(self):
        try:
            self.membership.date_joined
        except AttributeError:
            slef.fail("tema membership should have date_joined")
