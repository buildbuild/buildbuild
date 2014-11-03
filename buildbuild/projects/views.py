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
from buildbuild import custom_msg

# when User click a project in team page, 
# team_page.html links to project_page url denoted in projects' urlconf
# and project_page method in view render project_page.html 
# with the fields of project
def project_page(request, project_id):
    project = Project.objects.get_project(project_id)
    return render(
               request,
               "projects/project_page.html",
               {
                   "project" : project,
               },
           )            


class MakeProjectView(FormView):
    template_name = "projects/makeproject.html"
    form_class = MakeProjectForm

    def form_valid(self, form):
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
            messages.error(self.request, custom_msg.project_invalid)
            return HttpResponseRedirect(reverse("projects:makeproject"))
        
        # Check uniqueness of project
        try:
            Project.objects.get(name = project_name)
        except ObjectDoesNotExist:
            pass
        else:
            messages.error(self.request, custom_msg.project_already_exist)
            return HttpResponseRedirect(reverse("projects:makeproject"))
        
        # Check valid team name
        try:
            Team.objects.validate_name(team_name)
        except ValidationError:
            messages.error(self.request, custom_msg.project_invalid_team_name)
            return HttpResponseRedirect(reverse("projects:makeproject"))
  
        # Check the team is in <teams DB>
        try:
            team = Team.objects.get(name = team_name)
        except ObjectDoesNotExist:
            messages.error(self.request, custom_msg.project_non_exist_team)
            return HttpResponseRedirect(reverse("projects:makeproject"))

        # Login check is programmed in buildbuild/urls.py
        # Check login user belong to the team
        user = self.request.user
        try:
            team.members.get_member(id = user.id)
        except ObjectDoesNotExist:
            messages.error(self.request, custom_msg.project_user_does_not_belong_team)
            return HttpResponseRedirect(reverse("projects:makeproject"))
       
        # Both Language & Version form is needed
        if ("lang" in self.request.POST) and ("ver" in self.request.POST):
            lang = self.request.POST["lang"]
            ver = self.request.POST["ver"]
 
            try:
                VersionList.objects.validate_lang(lang)
            except ObjectDoesNotExist:
                messages.error(self.request, custom_msg.project_lang_invalid)
                return HttpResponseRedirect(reverse("projects:makeproject"))

            try:
                Project.objects.validate_version_of_language(lang, ver)
            except ObjectDoesNotExist:
                messages.error(self.request, custom_msg.project_ver_invalid)
                return HttpResponseRedirect(reverse("projects:makeproject"))

            properties = {
                             'language' : lang,
                             'version' : ver
                         }
            project = Project.objects.create_project(
                          name = project_name,
                          team_name = team.name,                      
                          properties = properties
                      )
        elif ("lang" in self.request.POST) or ("ver" in self.request.POST):
            messages.error(self.request, custom_msg.project_both_lang_and_ver_is_needed)
            return HttpResponseRedirect(reverse("projects:makeproject"))
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
        
        messages.success(self.request, custom_msg.project_make_success)
        return HttpResponseRedirect(reverse("home")) 

