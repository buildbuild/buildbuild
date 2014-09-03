from django.test import TestCase
from django.test.client import Client

from users.models import User
from teams.models import Team
from teams.models import Membership


class TestAPITeamUserList(TestCase):
    def setUp(self):
        """
        * test scenario
        - 1 team
        - 2 users belongs to team ( A, B )
        - 1 user not belongs to team ( C )

        request teamuser-list API
        - response should contain A, B users info
        - response should not contain C user info
        """
        self.team = Team.objects.create_team(
            name="test_teamname"
        )
        self.first_user_belongs_to_team = User.objects.create_user(
            email="test_username_first@example.com",
            password="test_password",
        )
        self.second_user_belongs_to_team = User.objects.create_user(
            email="test_username_second@example.com",
            password="test_password",
        )
        self.user_not_belongs_to_team = User.objects.create_user(
            email="test_username_third@example.com",
            password="test_password",
        )

        """
        * should implement later using some eloquent method.
        there is no method for make relation between user and team
        in this test case, going to use Membership Model directly.
        """

        self.first_membership = Membership()
        self.first_membership.team = self.team
        self.first_membership.user = self.first_user_belongs_to_team
        self.first_membership.save()

        self.second_membership = Membership()
        self.second_membership.team = self.team
        self.second_membership.user = self.second_user_belongs_to_team
        self.second_membership.save()

        self.client = Client()
        self.response = self.client.get("/api/teams/" + self.team.name + "/users/")

        self.not_exist_teamname = "test_teamname_not_exist"
        self.response_with_not_exist_teamname = \
            self.client.get("/api/teams/" + self.not_exist_teamname + "/users/")

    def test_api_teamuser_list_request_should_return_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_api_teamuser_list_request_with_not_exist_teamname_should_return_200(self):
        self.assertEqual(self.response_with_not_exist_teamname.status_code, 404)

    def test_api_teamuser_list_request_should_return_json(self):
        self.assertEqual(self.response["Content-Type"], "application/json")

    def test_api_teamuser_list_request_should_contain_users_belong_to_team(self):
        self.assertContains(self.response, self.first_user_belongs_to_team.email)
        self.assertContains(self.response, self.second_user_belongs_to_team.email)

    def test_api_teamuser_list_request_should_not_contain_user_not_belong_to_team(self):
        self.assertNotContains(self.response, self.user_not_belongs_to_team.email)
