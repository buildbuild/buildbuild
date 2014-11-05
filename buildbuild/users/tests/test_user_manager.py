from django.test import TestCase
from users.models import User
from django.core.exceptions import ObjectDoesNotExist,ValidationError

class TestUserManager(TestCase):
    def setUp(self):
        self.valid_email = "test@example.com"
        self.second_valid_email = "secondtest@example.com"
        self.superuser_email = "superuser@example.com"
        self.valid_password = "test_password"
        self.not_created_user_email = "nouser@example.com"

        self.not_created_user_id = 0

        self.old_phonenumber = "0123456789"
        self.new_phonenumber = "9876543210"
        self.new_invalid_phonenumber = "a1234567"
        self.new_short_length_phonenumber = "1234"

        self.old_name = "OldName"
        self.new_name = "NewName"
        self.new_invalid_name = "NewName1234"
        self.new_over_length_name = "a" * 31

        self.user = User.objects.create_user(
            email = self.valid_email,
            password = self.valid_password,
        )

        self.superuser = User.objects.create_superuser(
            email = self.superuser_email,
            password = self.valid_password,
        )
        
    def test_create_user(self):
        self.assertIsNotNone(
            User.objects.create_user(
                email = self.second_valid_email,
                password = self.valid_password,
            )
        )

    def test_get_user(self):
        self.assertIsNotNone(
            User.objects.get_user(
                id = self.user.id
            )
        )

    def test_returned_object_of_get_user_assertEqual_original_user(self):
        returned_user = User.objects.get_user(
            id = self.user.id
        )
        self.assertEqual(returned_user,self.user)

    def test_get_user_with_invalid_email_should_be_fail(self):
        self.assertRaises(
            ObjectDoesNotExist, 
            User.objects.get_user,
            id=self.not_created_user_id
        )

    def test_delete_user(self):
        self.assertTrue(
            User.objects.delete_user(id = self.user.id)
        )

    def test_get_user_must_be_fail_to_deleted_user(self):
        User.objects.delete_user(self.user.id)
        try:
            User.objects.get_user(
                id = self.user.id
            )
        except ObjectDoesNotExist:
            pass

    def test_update_user(self):
        user = User.objects.get_user(
            id = self.user.id,
        )
        self.assertTrue(
            User.objects.update_user(
                id = user.id,
            )
        )

    def test_update_user_phonenumber(self):
        user = User.objects.get_user(
            id = self.user.id,
        )
        User.objects.update_user(
            id = user.id,
            phonenumber = self.new_phonenumber,
        )
        user = User.objects.get_user(user.id)
        self.assertEqual(
            user.phonenumber, 
            self.new_phonenumber,
            "Updated Phonenumber should be equal to the new.",
        )

    def test_update_user_invalid_phonenumber(self):
        self.assertRaises(
            ValidationError, 
            User.objects.update_user,
            id = self.user.id,
            phonenumber = self.new_invalid_phonenumber,
        )

    def test_update_user_too_short_phonenumber(self):
        self.assertRaises(
            ValidationError, 
            User.objects.update_user,
            id = self.user.id,
            phonenumber = self.new_short_length_phonenumber
        )

    def test_update_user_name(self):
        User.objects.update_user(
            id = self.user.id,
            name = self.new_name,
        )
        user = User.objects.get_user(self.user.id)
        self.assertEqual(
            user.name, 
            self.new_name,
            "Updated Name should be equal to the new."
        )

    def test_update_user_invalid_name(self):
        self.assertRaises(
            ValidationError, 
            User.objects.update_user,
            id = self.user.id,
            name = self.new_invalid_name
        )

    def test_update_user_over_length_name(self):
        self.assertRaises(
            ValidationError,
            User.objects.update_user,
            id = self.user.id,
            name = self.new_over_length_name
        )

    def test_update_user_with_invalid_phonenumber(self):
        self.assertRaises(ValidationError, User.objects.update_user,
                          id = self.user.id,
                          name = self.new_name,
                          phonenumber = self.new_invalid_phonenumber)

    def test_update_user_must_not_update_all_both_one_is_wrong_name(self):
        self.assertRaises(ValidationError, User.objects.update_user,
                          id = self.user.id,
                          name = self.new_invalid_name,
                          phonenumber = self.new_phonenumber)

    def test_update_user_must_not_update_all_both_are_wrong(self):
        self.assertRaises(ValidationError, User.objects.update_user,
                          id = self.user.id,
                          name = self.new_invalid_name,
                          phonenumber = self.new_invalid_phonenumber)

    def test_create_superuser(self):
        self.assertTrue(
            User.objects.create_superuser(
                email = self.second_valid_email,
                password = self.valid_password,
            )
        )

    def test_get_user_about_superuser(self):
        user = User.objects.get_user(
            id = self.superuser.id,
        )
        self.assertEqual(user, self.superuser)

    def test_superuser_admin_permission(self):
        self.assertTrue(self.superuser.is_admin)
        self.assertTrue(self.superuser.is_staff)
    
    def test_not_superuser_admin_permission(self):
        self.assertFalse(self.user.is_staff())

    def test_get_full_name_should_be_same_as_email(self):
        self.assertEqual(self.user.email, self.user.get_full_name())

    def test_get_short_name_should_be_same_as_email(self):
        self.assertEqual(self.user.email, self.user.get_short_name())

