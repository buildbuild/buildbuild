from django.db import models
from django.core.exceptions import ValidationError
from teams.models import Team

class ProjectManager(models.Manager):
    def create_project(self, name):
        project = self.model()
        self.validate_name(name)
        project.name = name

        project.save(using = self.db)

        return project

    def validate_name(self, name):
        if len(name) > 64:
            raise ValidationError("project name is at most 64 chracters")

    def get_project(self, name):
        return Project.objects.get(name = name)


class Project(models.Model):
    name = models.CharField(max_length = 64, unique = True)

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

