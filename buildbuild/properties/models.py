from django.db import models
from jsonfield import JSONField
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import re

class Language(models.Model):
    lang = models.CharField(
               help_text = "This field informs available languages",
               max_length = 30,
               unique = True,
           )
                         

class VersionManager(models.Manager):
    def create_ver(self, lang_ver):
        if type(lang_ver) is not dict:
            raise ValidationError("lang_ver must be dict")

        self.validate_lang(lang_ver.keys())
        self.validate_ver(lang_ver.values())

        Version.objects.create(lang_ver)

    def validate_lang(self, lang):
        # buildbuild language char field use string field
        # So <list -> string> using ''.join(object) method
        lang = ''.join(lang)
        try:
            Language.objects.get(lang = lang)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("The language is not supported")

    # It only test the available regex, not version service available
    def validate_ver(self, ver):
        ver = ''.join(ver)
        if bool(re.match('^[0-9.]+$', ver)) is False:
            raise ValidationError(
                      "version should only be composed of numberic characters and ."
                  )

class Version(models.Model):
    lang_ver = JSONField(
              help_text = "This field informs available languages and  versions",
              unique = True,
              default = {"" : ""} # ex : {"python" : "2.7.8"}
          )

    objects = VersionManager()

class DockerTextManager(models.Manager):
    def create_docker_text(self, lang_ver, docker_text):
        if type(lang_ver) is not dict:
            raise ValidationError("lang_ver must be dict")

        Version.objects.validate_lang(lang_ver.keys())
        Version.objects.validate_ver(lang_ver.values())

        lang = lang_ver.keys()
        lang = lang.join(lang)

        DockerText.objects.create(docker_text = {lang : docker_text}) 

class DockerText(models.Model):
    docker_text = JSONField(
                      help_text = "This field have docker texts for each language",
                      unique = True,
                      default = {"" : ""} # ex : {"python" : <python docker text>}
                  )

    objects = DockerTextManager()
