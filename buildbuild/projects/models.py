from django.db import models
from django.core.exceptions import ValidationError

class ProjectManager(models.Manager):
    def create_project(self, name):
        project = self.model()
        self.validate_name(name)
        project.name = name
        project.save()

        return project


    def validate_name(self, name):
        if len(name) > 20:
            raise ValidationError("project name is at most 255 chracters")

class Project(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    objects = ProjectManager()
