from django.test import TestCase
from teams.models import Team,TeamManager
from django.core.exceptions import ValidationError

class TestTeamManager(TestCase):
    def setUp(self):
        self.team = Team()
        self.team.name = "Team1"

        self.valid_team_name = "TeamTeam"
        self.valid_second_team_name = "TeamTeam2"
        self.invalid_long_length_name = "a" * 31
        self.invalid_long_length_contact_number = "a" * 21
        self.invalid_long_length_website_url = "a" * 256

    def test_team_should_be_generated_using_create_team(self):
        try:
            team = Team.objects.create_team(
                name = self.valid_team_name
            )
        except:
            self.fail("Create Team must create team object successfully")

    def test_teams_should_be_get_using_get_all_teams(self):
        team = Team.objects.create_team(
            name = self.valid_team_name
        )
        second_team = Team.objects.create_team(
            name = self.valid_second_team_name
        )

        teams = Team.objects.get_all_team()

        self.assertQuerysetEqual(teams, ["<Team: "+team.name+">",
                                          "<Team: "+second_team.name+">"],
                                 ordered=False)

    def test_get_team_should_be_equal_to_proper_team(self):
        proper_team = Team.objects.create_team(
        name = self.valid_team_name
        )
        test_team = Team.objects.get_team(self.valid_team_name)
        self.assertEqual(proper_team.name, test_team.name, "get_team should be equal to same team name")

    def test_more_than_30_letters_team_name_must_raise_validation_error(self):
        try:
            team = Team.objects.create_team(
                   name = self.invalid_long_length_name
                )
        except ValidationError:
            pass
        else:
            self.fail("More than 30 letters name should raise ValidationError")

    def test_more_than_20_digits_team_contact_number_must_raise_validation_error(self):
        try:
            team = Team.objects.create_team(
                    name = self.valid_team_name,
                    contact_number = self.invalid_long_length_contact_number
                )
        except ValidationError:
            pass
        else:
            self.fail("More than 20 digits phonenumber should raise ValidationError")

    def test_more_than_255_letters_team_website_url_must_raise_validation_error(self):
        try:
            team = Team.objects.create_team(
                    name = self.valid_team_name,
                    website_url = self.invalid_long_length_website_url
                )
        except ValidationError:
            pass
        else:
            self.fail("More than 255 letters website_url should raise ValidationError")


