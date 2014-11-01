from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponseRedirect,request

from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic import DetailView

from django.contrib.auth import authenticate

from django.contrib import messages

from django.core.urlresolvers import reverse

from django.db import IntegrityError
from django.db import OperationalError
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from projects.forms import MakeProjectForm
from projects.models import Project, ProjectMembership
from teams.models import Team
from properties.models import AvailableLanguage, VersionList, DockerText

class MakeProjectView(FormView):
    template_name = "projects/makeproject.html"
    form_class = MakeProjectForm

    def form_valid(self, form):
        project_invalid = "ERROR : invalid project name"
        project_already_exist = "ERROR : The project name already exists" 
        project_invalid_team_name = "ERROR : invalid team name"
        project_non_exist_team = "ERROR : The team name is not in teams DB"
        project_user_does_not_belong_team = "ERROR : The user doesn't belong the team"
        project_lang_invalid = "ERROR : The language is not supported"
        project_ver_invalid = "ERROR : The version is not suppoerted"
        project_both_lang_and_ver_is_needed = \
            "ERROR : Both Language and Version should be submitted"
        project_make_success = "Project created successfully"

        project = Project()
        project_name = self.request.POST["projects_project_name"]
        team_name = self.request.POST["projects_team_name"]

        lang = ""
        ver = ""
        properties = (lang, ver)
         
        # Check valid project name
        try:
            Project.objects.validate_name(project_name)
        except ValidationError:
            messages.error(self.request, project_invalid)
            return HttpResponseRedirect(reverse("makeproject"))
        
        # Check uniqueness of project
        try:
            Project.objects.get(name = project_name)
        except ObjectDoesNotExist:
            pass
        else:
            messages.error(self.request, project_already_exist)
            return HttpResponseRedirect(reverse("makeproject"))
        
        # Check valid team name
        try:
            Team.objects.validate_name(team_name)
        except ValidationError:
            messages.error(self.request, project_invalid_team_name)
            return HttpResponseRedirect(reverse("maketeam"))
  
        # Check the team is in <teams DB>
        try:
            team = Team.objects.get(name = team_name)
        except ObjectDoesNotExist:
            messages.error(self.request, project_non_exist_team)
            return HttpResponseRedirect(reverse("makeproject"))

        # Login check is programmed in buildbuild/urls.py
        # Check login user belong to the team
        user = self.request.user
        try:
            team.members.get_member(id = user.id)
        except ObjectDoesNotExist:
            messages.error(self.request, project_user_does_not_belong_team)
            return HttpResponseRedirect(reverse("makeproject"))
       
        # Both Language & Version form is needed
        if ("lang" in self.request.POST) and ("ver" in self.request.POST):
            lang = self.request.POST["lang"]
            ver = self.request.POST["ver"]
 
            try:
                VersionList.objects.validate_lang(lang)
            except ObjectDoesNotExist:
                messages.error(self.request, project_lang_invalid)
                return HttpResponseRedirect(reverse("makeproject"))

            try:
                Project.objects.validate_ver_for_lang(lang, ver)
            except ObjectDoesNotExist:
                messages.error(self.request, project_ver_invalid)
                return HttpResponseRedirect(reverse("makeproject"))

            properties = {lang : ver}
            project = Project.objects.create_project(
                          name = project_name,
                          team_name = team.name,                      
                          properties = properties
                      )
        elif ("lang" in self.request.POST) or ("ver" in self.request.POST):
            messages.error(self.request, project_both_lang_and_ver_is_needed)
            return HttpResponseRedirect(reverse("makeproject"))
        # Or team name & project form submitted, not both language & version
        else:
             project = Project.objects.create_project(
                           name = project_name,
                           team_name = team.name,
                       )
           
        # link team to project using ProjectMembership
        project_membership = ProjectMembership.objects.create_project_membership(
                                 project = project,
                                 team = team,
                             )
        project_membership.is_admin = True
        project_membership.save()
        
        messages.success(self.request, project_make_success)
        return HttpResponseRedirect(reverse("home")) 

