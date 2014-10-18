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
        if len(name) > 64:
            raise ValidationError(
                ("project.name length should be at most 64"),
                code = 'invalid'
            )

    def get_project(self, name):
        try:
            self.validate_name(name)
            project = Project.objects.get(name = name)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("The project.name does not exist")
        else:
            return project

    # Update project needed to add functions, and test code
    def update_project(self, name, **kwargs):
        project = Project.objects.get_project(name)
        if "properties" in kwargs:
            project.properties = kwargs['properties']
        if "docker_text" in kwargs:
            project.docker_text = kwargs['docker_text']

        project.save(using = self.db)


    def delete_project(self, name):
        project = Project.objects.get_project(name)
        project.deactivate()
        project.save(using = self._db)

class Project(models.Model):
    name = models.CharField(max_length = 64, unique = True)
    properties = JSONField(default = ('','') )
    docker_text = models.TextField(default = '')
    objects = ProjectManager()
    
    team_wait_list = models.ManyToManyField(
            Team, 
            through = 'ProjectWaitList',
            through_fields = ('project', 'wait_team'),
            related_name="project_wait_list"
            )
    
    team_list = models.ManyToManyField(
            Team, 
            through = 'ProjectMembership',
            through_fields = ('project', 'team'),
            related_name="project_membership"
            )
    
    def __unicode__(self):
        return self.name

class ProjectWaitList(models.Model):
    project = models.ForeignKey(
            Project, 
            related_name="project_wait_list_project",
            )
    wait_team = models.ForeignKey(
            Team, 
            related_name="project_wait_list_team",
            )
    date_requested = models.DateTimeField(auto_now_add=True)

class ProjectMembership(models.Model):
    project = models.ForeignKey(
            Project, 
            related_name="project_membership_project",
            )
    team = models.ForeignKey(
            Team, 
            related_name="project_membership_team",
            )
    date_joined = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

