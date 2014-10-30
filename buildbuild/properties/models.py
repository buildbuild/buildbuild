from django.db import models
from jsonfield import JSONField
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import re

class AvailableLanguage(models.Model):
    lang = models.CharField(
               help_text = "This field informs available languages",
               max_length = 30,
               unique = True,
           )


class VersionListManager(models.Manager):
    def create_available_version(self, lang, ver):

        self.validate_lang(lang)
        self.validate_ver(ver)

        lang_ver = VersionList.objects.create(lang=lang, ver=ver)
        lang_ver.save(using = self._db)

    def validate_lang(self, lang):
        try:
            AvailableLanguage.objects.get(lang = lang)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("The language is not supported")

    # It only test available regex for <ver> value, not version service available
    def validate_ver(self, ver):
        if bool(re.match('^[0-9.]+$', ver)) is False:
            raise ValidationError(
                      "version should only be composed of numeric characters and ."
                  )

        try:
            VersionList.objects.get(ver = ver)
        except ObjectDoesNotExist:
            pass
        else:
            raise ValidationError("The version already exists")

    def get_version_list_for_each_language(self, lang):
        pass

class VersionList(models.Model):
    lang = models.CharField(
              help_text = "This field informs language",
              max_length = 30,
              default = "", # ex : "python"
          )

    ver = models.CharField(
              help_text = "This field informs version",
              max_length = 30,
              unique = True,
              default = "", # ex : "2.7.8"
          )

    objects = VersionListManager()

class DockerTextManager(models.Manager):
    def create_docker_text(self, lang, docker_text):
        Version.objects.validate_lang(lang)

        docker_text = DockerText.objects.create(docker_text = {lang : docker_text})
        docker_text.save(using = self._db)

class DockerText(models.Model):
    docker_text = JSONField(
                      help_text = "This field have docker text for each language",
                      unique = True,
                      default = {"" : ""} # ex : {"python" : <python docker text>}
                  )

    objects = DockerTextManager()
