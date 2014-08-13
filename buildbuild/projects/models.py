from django.db import models
from teams.models import Team

class ProjectManager(models.Model):
    def create_project(self, name, owner, src_url, **kwargs):

    def validate_name(self, name):
        if len(name) > 20
            raise ValidationError("Project name length should be at most 20")


class Project(models.Model):
    name = models.CharField(max_length=20)
    own_team = models.ForeignKey(Team)
    src_url = models.UrlField(max_length=30)

    USERNAME_FIELD = 'name'
