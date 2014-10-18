from django.test import TestCase
from teams.models import Team,TeamManager
from django.core.exceptions import ValidationError, ObjectDoesNotExist

class TestTeamManager(TestCase):
    def setUp(self):
        self.team = Team()
        self.team.name = "firstTeam"

        self.valid_team_name = "TeamTeam"
        self.valid_second_team_name = "SecondTeam"
        self.invalid_long_length_name = "a" * 65
        self.invalid_long_length_contact_number = "a" * 21
        self.invalid_long_length_website_url = "a" * 256
            
        self.team = Team.objects.create_team(
            name = self.valid_team_name
        )

        self.second_team = Team.objects.create_team(
            name = self.valid_second_team_name
        )

# Attribute
    def test_create_team_must_contain_name(self):
        try:
            team = Team.objects.create_team(
                name = ""
            )
        except ValidationError:
            pass
# Validation
    def test_team_name_is_restricted_to_64_characters(self):
        try:
            team = Team.objects.create_team(
                name = self.invalid_long_length_name
            )
        except ValidationError:
            pass

    def test_get_all_teams(self):
        teams = Team.objects.all()

        self.assertQuerysetEqual(
            teams, 
            ["<Team: "+self.team.name+">",
            "<Team: "+self.second_team.name+">"],
            ordered=False,
        )

    def test_more_than_64_letters_team_name_must_raise_validation_error(self):
        try:
            team = Team.objects.create_team(
                   name = self.invalid_long_length_name
                )
        except ValidationError:
            pass
        else:
            self.fail("More than 64 letters name should raise ValidationError")

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
    
    # ObjectDoesNotExist
    def test_team_manager_could_delete_team(self):
        self.team.delete()
        try:
            Team.objects.get_team(name = self.valid_team_name), 
        except ObjectDoesNotExist:
            pass 

# Assert
    def test_get_team_equal_to_team_targetted(self):
        get_team = Team.objects.get_team(self.valid_team_name)
        self.assertEqual(
                self.team, 
                get_team, 
                "get_team  should be equal to target team",
        )
   
