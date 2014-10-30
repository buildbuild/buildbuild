from properties.models import Language
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

class TestLanguage(TestCase):
    fixtures = ['properties_data.yaml']
    def setUp(self):
        pass

    def test_get_all_available_language(self):
        self.assertIsNotNone(Language.objects.all())

    def test_get_python(self):
        self.assertIsNotNone(Language.objects.get(lang="python"))

    def test_get_python_value_must_be_equal_to_python(self):
        language_object = Language.objects.get(lang="python")
        self.assertEqual("python", language_object.lang)

    def test_get_ruby(self):
        self.assertIsNotNone(Language.objects.get(lang="ruby"))

    def test_get_ruby_value_must_be_equal_to_ruby(self):
        language_object = Language.objects.get(lang="ruby")
        self.assertEqual("ruby", language_object.lang)

    def test_get_non_exsit_language_must_be_fail(self):
        self.assertRaises(
            ObjectDoesNotExist,
            Language.objects.get,
            lang="never_exist_lang"
        )


