from django.test import TestCase
from users.models import User
from django.core.exceptions import ObjectDoesNotExist,ValidationError

class TestUserManager(TestCase):
    def setUp(self):
        self.user = User()
        self.valid_email = "test@example.com"
        self.valid_password = "test_password"
        self.not_created_user_email = "nouser@example.com"

        self.old_phonenumber = "0123456789"
        self.new_phonenumber = "9876543210"
        self.new_invalid_phonenumber = "a1234567"
        self.new_short_length_phonenumber = "1234"

        self.old_name = "OldName"
        self.new_name = "NewName"
        self.new_invalid_name = "NewName1234"
        self.new_over_length_name = "aaaabbbbccccddddeeeef"

    def test_user_should_be_created_via_user_manager(self):
        try:
            user = User.objects.create_user(
                    email = self.valid_email,
                    password = self.valid_password,
                    )
        except:
            self.fail("User should be created via UserManager")

    def test_get_user_should_return_user_via_user_manager(self):
        _user = User.objects.create_user(
                    email = self.valid_email,
                    password = self.valid_password,
                    )
        try:
            user = User.objects.get_user(
                    email = _user.email
                    )
        except:
            self.fail("UserManager should return user via get_user")

    def test_get_user_with_invalid_email_should_be_fail(self):
        self.assertRaises(ObjectDoesNotExist, User.objects.get_user,
                          email=self.not_created_user_email
                        )

    def test_delete_user_must_disable_is_active_via_user_manager(self):
        user = User.objects.create_user(
                    email = self.valid_email,
                    password = self.valid_password,
                    )
        User.objects.delete_user(user.email)
        user = User.objects.get_user(
                    email = self.valid_email
                )
        self.assertEqual(False, user.is_active,
                         "is_active should be False")

    def test_update_user_must_update_phonenumber_field_via_user_manager(self):
        user = User.objects.create_user(
                    email = self.valid_email,
                    password = self.valid_password,
                    phonenumber = self.old_phonenumber
                    )
        User.objects.update_user(email = user.email,
                                 phonenumber = self.new_phonenumber
        )
        user = User.objects.get_user(user.email)
        self.assertNotEqual(user.phonenumber, self.old_phonenumber,
                         "Updated Phonenumber should not be equal with old one.")

    def test_update_user_must_not_update_invalid_phonenumber_via_user_manager(self):
        user = User.objects.create_user(
                    email = self.valid_email,
                    password = self.valid_password,
                    phonenumber = self.old_phonenumber
                    )
        self.assertRaises(ValidationError, User.objects.update_user,
                          email = self.valid_email,
                          phonenumber = self.new_invalid_phonenumber)

    def test_update_user_must_not_update_short_phonenumber_via_user_manager(self):
        user = User.objects.create_user(
                    email = self.valid_email,
                    password = self.valid_password,
                    phonenumber = self.old_phonenumber
                    )
        self.assertRaises(ValidationError, User.objects.update_user,
                          email = self.valid_email,
                          phonenumber = self.new_short_length_phonenumber)

    def test_update_user_must_update_name_field_via_user_manager(self):
        user = User.objects.create_user(
                    email = self.valid_email,
                    password = self.valid_password,
                    name = self.old_name
                    )
        User.objects.update_user(email = user.email,
                                 name = self.new_name
        )
        user = User.objects.get_user(user.email)
        self.assertNotEqual(user.name, self.old_name,
                         "Updated Name "+ user.name +" should not be equal with old one.")

    def test_update_user_must_not_update_invalid_name_via_user_manager(self):
        user = User.objects.create_user(
                    email = self.valid_email,
                    password = self.valid_password,
                    name = self.old_name
                    )
        self.assertRaises(ValidationError, User.objects.update_user,
                          email = self.valid_email,
                          name = self.new_invalid_name)

    def test_update_user_must_not_update_over_length_name_via_user_manager(self):
        user = User.objects.create_user(
                    email = self.valid_email,
                    password = self.valid_password,
                    name = self.old_name
                    )
        self.assertRaises(ValidationError, User.objects.update_user,
                          email = self.valid_email,
                          name = self.new_over_length_name)

    def test_update_user_must_not_update_all_both_one_is_wrong_phonenumber(self):
        user = User.objects.create_user(
                    email = self.valid_email,
                    password = self.valid_password,
                    name = self.old_name,
                    phonenumber = self.old_phonenumber
                    )
        self.assertRaises(ValidationError, User.objects.update_user,
                          email = self.valid_email,
                          name = self.new_name,
                          phonenumber = self.new_invalid_phonenumber)

    def test_update_user_must_not_update_all_both_one_is_wrong_name(self):
        user = User.objects.create_user(
                    email = self.valid_email,
                    password = self.valid_password,
                    name = self.old_name,
                    phonenumber = self.old_phonenumber
                    )
        self.assertRaises(ValidationError, User.objects.update_user,
                          email = self.valid_email,
                          name = self.new_invalid_name,
                          phonenumber = self.new_phonenumber)

    def test_update_user_must_not_update_all_both_are_wrong(self):
        user = User.objects.create_user(
                    email = self.valid_email,
                    password = self.valid_password,
                    name = self.old_name,
                    phonenumber = self.old_phonenumber
                    )
        self.assertRaises(ValidationError, User.objects.update_user,
                          email = self.valid_email,
                          name = self.new_invalid_name,
                          phonenumber = self.new_invalid_phonenumber)
