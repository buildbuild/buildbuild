from properties.models import AvailableLanguage
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

class TestLanguage(TestCase):
    fixtures = ['properties_data.yaml']
    def setUp(self):
        self.non_exist_lang = "never_exist_lang"
        self.lang_python = "Python"
        self.lang_ruby = "Ruby"

    def test_get_all_available_language(self):
        self.assertIsNotNone(AvailableLanguage.objects.all())

    def test_get_python(self):
        self.assertIsNotNone(AvailableLanguage.objects.get(lang=self.lang_python))

    def test_get_python_value_must_be_equal_to_python(self):
        language_object = AvailableLanguage.objects.get(lang=self.lang_python)
        self.assertEqual(self.lang_python, language_object.lang)

    def test_get_ruby(self):
        self.assertIsNotNone(AvailableLanguage.objects.get(lang=self.lang_ruby))

    def test_get_ruby_value_must_be_equal_to_ruby(self):
        language_object = AvailableLanguage.objects.get(lang=self.lang_ruby)
        self.assertEqual(self.lang_ruby, language_object.lang)

    def test_get_non_exist_language_must_be_fail(self):
        self.assertRaises(
            ObjectDoesNotExist,
            AvailableLanguage.objects.get,
            lang = self.non_exist_lang,
        )


