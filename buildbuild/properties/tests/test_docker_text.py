from properties.models import AvailableLanguage, VersionList, DockerText
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError

class TestVersion(TestCase):
    fixtures = ['properties_data.yaml']
    def setUp(self):
        self.non_exist_lang = "never_exist_lang"
       
        self.lang_python = "Python"
        self.lang_ruby = "Ruby"

    def test_get_python_docker_text(self):
        self.assertIsNotNone(DockerText.objects.get(lang=self.lang_python))
         
    def test_get_ruby_docker_text(self):
        self.assertIsNotNone(DockerText.objects.get(lang=self.lang_ruby))

    # docker text have unique language field now. But it is possible to change.
    def test_check_unique_lang_name_in_create_docker_text(self):
        self.assertRaises(
            IntegrityError,
            DockerText.objects.create_docker_text,
            lang = self.lang_python,
            docker_text = "",
        )

