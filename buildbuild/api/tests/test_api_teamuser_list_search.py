from django.test import TestCase
from django.test.client import Client

from teams.models import Team
from teams.models import Membership
from users.models import User


class TestAPITeamUserListSearch(TestCase):
    """
    * Test Scenario

    - 2 teams ( first_team, second_team )
    - we are going to search for first_team
    ( /api/teams/first_team_name/users/?search={query} )

    - 3 users
        - A : user_in_first_team_with_test_string
        - B : user_in_first_team_without_test_string
        - C : user_in_second_team_with_test_string

    - search result should ...
        - contain A
        - NOT contain B
        - NOT contain C
    """
    def setUp(self):
        # Generate Teams
        self.first_team = Team.objects.create_team(
            name="test_teamname_first",
        )
        self.second_team = Team.objects.create_team(
            name="test_teamname_second",
        )

        self.test_string = "test_string"

        # Generate Users
        self.user_in_first_team_with_test_string = User.objects.create_user(
            email="test_username_with" + self.test_string + "@firstteam.com",
            password="test_password",
        )
        self.user_in_first_team_without_test_string = User.objects.create_user(
            email="test_username_without" + "@firstteam.com",
            password="test_password",
        )
        self.user_in_second_team_with_test_string = User.objects.create_user(
            email="test_username_with_" + self.test_string + "@secondteam.com",
            password="test_password",
        )

        # Generate Membership
        self.first_membership = Membership()
        self.first_membership.team = self.first_team
        self.first_membership.user = self.user_in_first_team_with_test_string
        self.first_membership.save()

        self.second_membership = Membership()
        self.second_membership.team = self.first_team
        self.second_membership.user = self.user_in_first_team_without_test_string
        self.second_membership.save()

        self.third_membership = Membership()
        self.third_membership.team = self.second_team
        self.third_membership.user = self.user_in_second_team_with_test_string
        self.third_membership.save()

        # Get Response
        self.client = Client()
        self.response = self.client.get("/api/teams/" + self.first_team.name + "/users/?search=" + self.test_string)

    def test_api_teamuser_list_search_should_return_valid_result(self):
        self.assertContains(self.response, self.user_in_first_team_with_test_string.email)
        self.assertNotContains(self.response, self.user_in_first_team_without_test_string.email)
        self.assertNotContains(self.response, self.user_in_second_team_with_test_string.email)
