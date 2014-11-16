from properties.models import AvailableLanguage, VersionList
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist, ValidationError

class TestVersion(TestCase):
    fixtures = ['properties_data.yaml']
    def setUp(self):
        self.non_exist_lang = "never_exist_lang"
        self.non_exist_ver = "0.0.0.0.0.0"
        self.invalid_ver = "only numeric characters & . available"
       
        self.lang_python = "Python"
        file_handler = open("media/lang_ver/python_ver_available", "r")
        self.ver_list_python = file_handler.read()
        
        self.lang_ruby = "Ruby"
        file_handler = open("media/lang_ver/ruby_ver_available", "r")
        self.ver_list_ruby = file_handler.read()
 

    def test_get_all_available_python_versions(self):
        self.assertIsNotNone(VersionList.objects.filter(lang="Python"))

    def test_get_all_available_ruby_versions(self):
        self.assertIsNotNone(VersionList.objects.filter(lang="Ruby"))

    def test_get_non_exist_language_must_be_fail(self):
        self.assertRaises(
            ObjectDoesNotExist,
            VersionList.objects.get,
            lang = self.non_exist_lang
        )

    def test_get_non_exist_version_must_be_fail(self):
        self.assertRaises(
            ObjectDoesNotExist,
            VersionList.objects.get,
            ver = self.non_exist_ver
        )

    def test_create_non_exist_language_must_be_fail(self):
        self.assertRaises(
            ObjectDoesNotExist,
            VersionList.objects.create_available_version,
            lang = self.non_exist_lang,
            ver = self.non_exist_ver,
        )

    def test_check_unique_version_name_in_create_available_version(self):
        self.assertRaises(
            ValidationError,
            VersionList.objects.create_available_version,
            lang = self.lang_python, 
            ver = self.ver_list_python[0]
        )

    def test_create_invalid_version_name_must_be_fail(self):
        self.assertRaises(
            ValidationError,
            VersionList.objects.create_available_version,
            lang = self.lang_python, 
            ver = self.invalid_ver
        )
    def test_create_valid_language_version_success(self):
        self.assertTrue(
            VersionList.objects.create_available_version(
                lang = self.lang_python, 
                ver = self.non_exist_ver,
            )
        )

    def test_get_python_version(self):
        version_list = VersionList.objects.filter(lang="python")
        len_of_ver_list_python = len(version_list)
        for index in range(len_of_ver_list_python):
            self.assertIn(
                version_list[index].ver,
                self.ver_list_python, 
            )

    def test_get_ruby_version(self):
        version_list = VersionList.objects.filter(lang="ruby")
        len_of_ver_list_ruby = len(version_list)
        for index in range(len_of_ver_list_ruby):
            self.assertIn(
                version_list[index].ver,
                self.ver_list_ruby, 
            )

