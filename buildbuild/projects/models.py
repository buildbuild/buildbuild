from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
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
            project = Project.objects.get(id = id)
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
    
class ProjectMembershipManager(models.Manager):
    def create_project_membership(self, project, team):
        if team.__class__.__name__ is not "Team":
            raise ValidationError("team argument must be Team object")
        if project.__class__.__name__ is not "Project":
            raise ValidationError("project argument must be Project object")

        # Does the member already exist? 
        try:
            project.project_teams.get_project_team(id = team.id)
        except ObjectDoesNotExist:
            project_membership = self.model(
                project = project, 
                project_team = team,
            )
            project_membership.save(using = self._db)
            return project_membership
        else:
            raise ValidationError(team.name + "is already the project member")
            
class ProjectMembership(models.Model):
    project = models.ForeignKey(
            Project, 
            related_name="project_membership_project",
            )
    project_team = models.ForeignKey(
            Team, 
            related_name="project_membership_project_team",
            default = None,
            )
    date_joined = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    objects = ProjectMembershipManager()

class ProjectWaitListManager(models.Manager):
    def create_project_wait_list(self, project, team):
        if team.__class__.__name__ is not "Team":
            raise ValidationError("team argument must be Team object")
        if project.__class__.__name__ is not "Project":
            raise ValidationError("project argument must be Project object")

        # Does the project_wait_project already exist? 
        try:
            project.project_wait_teams.get_project_team(id = team.id)
        except ObjectDoesNotExist:
            project_wait_list = self.model(
                project = project, 
                project_wait_team = team,
            )
            project_wait_list.save(using = self._db)
            return project_wait_list
        else:
            raise ValidationError("The project wait team name is already the project wait team")

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
    objects = ProjectWaitListManager()
