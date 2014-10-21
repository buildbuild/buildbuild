from django.db import models
from django.core.exceptions import ValidationError
from teams.models import Team
from jsonfield import JSONField
import re

class ProjectManager(models.Manager):
    def create_project(self, name, **kwargs):
        project = self.model()
        self.validate_name(name)
        project.name = name

        if "team_name" in kwargs:
            project.team_name = kwargs['team_name']
        if "properties" in kwargs:
            project.properties = kwargs['properties']
        if "docker_text" in kwargs:
            project.docker_text = kwargs['docker_text']

        project.save(using = self.db)

        return project

    def validate_name(self, name):
       if len(name) < 1:
            raise ValidationError(
                "project name length should be at most 64",
            )
       if len(name) > 64:
            raise ValidationError(
                "project name max length is 64",
            )

    def get_project(self, id):
        try:
            project = Project.objects.get(name = name)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("The id not exist in project DB")
        else:
            return project

    # Update project needed to add functions, and test code
    def update_project(self, id, **kwargs):
        project = Project.objects.get_project(id)
        if "properties" in kwargs:
            project.properties = kwargs['properties']
        if "docker_text" in kwargs:
            project.docker_text = kwargs['docker_text']

        project.save(using = self.db)


    def delete_project(self, id):
        project = Project.objects.get_project(id)
        project.delete()

        if project.id is None:
            return True
        else:
            raise OperationalError("delete project failed")

class Project(models.Model):
    name = models.CharField(max_length = 64, unique = True)
    properties = JSONField(default = ('','') )
    docker_text = models.TextField(default = '')
    objects = ProjectManager()
    
    project_wait_teams = models.ManyToManyField(
            Team, 
            through = 'ProjectWaitList',
            through_fields = ('project', 'project_wait_team'),
            related_name="project_wait_teams"
            )
    
    project_teams = models.ManyToManyField(
            Team, 
            through = 'ProjectMembership',
            through_fields = ('project', 'project_team'),
            related_name="project_teams"
            )
    
class ProjectMembership(models.Model):
    project = models.ForeignKey(
            Project, 
            related_name="membership_project",
            )
    project_team = models.ForeignKey(
            Team, 
            related_name="membership_project_team",
            default = None,
            )
    date_joined = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

class ProjectWaitList(models.Model):
    project = models.ForeignKey(
            Project, 
            related_name="wait_list_project",
            )
    project_wait_team = models.ForeignKey(
            Team, 
            related_name="wait_list_project_team",
            default = None,
            )
    date_requested = models.DateTimeField(auto_now_add=True)

