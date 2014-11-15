from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from teams.models import Team
from jsonfield import JSONField
import re
from properties.models import AvailableLanguage, VersionList, DockerText
from django.core.validators import URLValidator
from buildbuild import custom_msg

class ProjectManager(models.Manager):
    def create_project(self, name, team_name, **kwargs):
        # Initial setting
        project = self.model()
        swift_container = team_name + "__" + name

        # Validate first
        # project name, team name, swift container name
        self.validate_name(name)
        Team.objects.validate_name(team_name)
        self.validate_swift_container_name(
            swift_container,
            name,
            team_name,
        )
               
        self.properties_in_kwargs_is_required(kwargs)
        self.check_exist_team_name(team_name)
#        self.check_uniqueness_project_name(name, team_name)

        project.name = name
        project.team_name = team_name
        project.swift_container = swift_container

        # 'properties' value is passed by kwargs, but it is possible to change
        # properties value must be dict
        # properties must have following keys ->
        # language, version, git url, branch name
        properties = kwargs['properties']
        self.validate_properties(properties)
        self.check_keys_in_properties(properties)

        # Check validation about language & version
        VersionList.objects.validate_lang(properties['language'])       
        self.validate_version_of_language(
            properties['language'], 
            properties['version']
        )

        # Git URL & Git Branch
        validate_git_url = URLValidator()
        validate_git_url(properties['git_url'])
                    
        # Test for branch name should be needed.
        # It's just empty validator
        self.validate_branch_name(properties['branch_name'])
        
        # All validate & all check available attributes test passed? then, save
        project.properties = properties
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
       # test code, not yet
       if bool(re.match('^[a-zA-Z0-9_-]+$', name)) is False:
            raise ValidationError(
                     "team name cannot contain things but alphabet, '_', number"
                  )
    
    # Check if the version for language is in DB
    # Be aware it checks only validate about version, not language
    def validate_version_of_language(self, lang, ver):
        try:
            VersionList.objects.get(lang = lang, ver = ver)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                      "The version for " + lang + " is not supported"
                  )

    def properties_in_kwargs_is_required(self, kwargs):
        if "properties" not in kwargs:
            raise AttributeError(
                "'properties' in kwargs must be required"
            )

    def validate_properties(self, properties):
        if type(properties) is not dict:
            raise TypeError("properties must be dict")
    
    def validate_branch_name(self, branch_name):
        pass

    def validate_swift_container_name(self, swift_container_name, project_name, team_name):
        if len(swift_container_name) < 1:
            raise ValidationError(
                "swift container name must have more than 1 character"
            )
        if len(swift_container_name) > 130:
            raise ValidationError(
                'swift container name is too long'
            )
        if swift_container_name != (team_name + "__" + project_name):
            raise ValueError(
                'swift container name is not in rule'
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

        if "git_url" in kwargs:
            project.git_url = kwargs['git_url']

        if "branch_name" in kwargs:
            project.branch_name = kwargs['branch_name']

        project.save(using = self.db)

    def delete_project(self, id):
        project = Project.objects.get_project(id)
        project.delete()

        if project.id is None:
            return True
        else:
            raise OperationalError("delete project failed")

    def check_keys_in_properties(self, properties):
        if 'language' not in properties:
            raise KeyError("Language information was not submitted")

        if 'version' not in properties:
            raise KeyError("Version information was not submitted")

        if 'git_url' not in properties:
            raise KeyError("Git URL information was not submitted")

        if 'branch_name' not in properties:
            raise KeyError("Git Branch name information was not submitted")

    def check_exist_team_name(self, team_name):
        try:
            Team.objects.get(name = team_name)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                "The submitted team does not exist"
            )

class Project(models.Model):
    name = models.CharField(
               help_text = "Project name",
               max_length = 64,
               unique = True
           )
    properties = JSONField(
                     help_text = "Project language and version",
                     default = {
                                   'language' : '',
                                   'version' : '',
                                   'git_url' : '',
                                   'branch_name' : '',
                               },
                 )

    swift_container = models.CharField(
                    help_text = 'Open stack swift container name',
                    max_length = 130,
                    default = '',
                )

    objects = ProjectManager()
    
    project_wait_teams = models.ManyToManyField(
                             Team,
                             verbose_name = "project wait_teams", 
                             through = 'ProjectWaitList',
                             through_fields = ('project', 'project_wait_team'),
                             related_name="project_wait_teams"
                         )
    
    project_teams = models.ManyToManyField(
            Team,
            verbose_name = "project project_teams",
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
        #print project.project_teams.get_project_team(id = team.id)
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
           
    # Team -> project_membership_project_team -> leave_project
    def leave_project(self, id):
        try:
            project_membership = self.get(id = id)
        except ValidationError:
            raise ValidationError("The team doesn't belong the project")
        else:
            project_membership.delete()

    # Project -> project_membership_project -> exclude_project_team
    def exclude_project_team(self, id):
        try:
            project_team = self.get(id = id)
        except ValidationError:
            raise ValidationError("The project_team is not a team member")
        else:
            project_teamship.delete()        

class ProjectMembership(models.Model):
    project = models.ForeignKey(
            Project,
            verbose_name = "projectMembership project",
            related_name="project_membership_project",
            )
    project_team = models.ForeignKey(
            Team,
            verbose_name = "projectMembership project_team",
            related_name="project_membership_project_team",
            default = None,
            )
    date_joined = models.DateField(
                      help_text = "ProjectMembership date_joined when team joined the project",
                      auto_now_add=True
                  )
    is_admin = models.BooleanField(
                   help_text = "ProjectMembership is_admin",
                   default=False
               )
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
                  verbose_name = "projectWaitList project",  
                  related_name="project_wait_list_project",
              )
    project_wait_team = models.ForeignKey(
                            Team,
                            verbose_name = "projectWaitList project_wait_team",
                            related_name="project_wait_list_project_team",
                            default = None,
                        )
    date_requested = models.DateTimeField(
                         help_text = "ProjectWaitList date_requested when team" +
                            "send a request to join a project",
                         auto_now_add=True,
                     )
    objects = ProjectWaitListManager()
