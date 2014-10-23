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

class MakeProjectView(FormView):
    template_name = "projects/makeproject.html"
    form_class = MakeProjectForm

    def form_valid(self, form):
        def msg_error(msg=""):
            messages.add_message(
                self.request,
                messages.ERROR,
                msg
            )

        def msg_success(msg=""):
            messages.add_message(
                self.request,
                messages.SUCCESS,
                msg
            )
        
        project_invalid = "ERROR : invalid project name"
        project_already_exist = "ERROR : The project name already exists" 
        project_invalid_team_name = "ERROR : invalid team name"
        project_non_exist_team = "ERROR : The team name is not in teams DB"
        project_user_does_not_belong_team = "ERROR : The user doesn't belong the team"
        project_make_success = "Project created successfully"

        project_name = self.request.POST["projects_project_name"]
        team_name = self.request.POST["projects_team_name"]
        # Check valid project name
        try:
            Project.objects.validate_name(project_name)
        except ValidationError:
            msg_error(project_invalid)
            return HttpResponseRedirect(reverse("makeproject"))
        
        # Check uniqueness of project
        try:
            Project.objects.get(name = project_name)
        except ObjectDoesNotExist:
            pass
        else:
            msg_error(project_already_exist)
            return HttpResponseRedirect(reverse("makeproject"))
        
        # Check valid team name
        try:
            Team.objects.validate_name(team_name)
        except ValidationError:
            msg_error(project_invalid_team_name)
            return HttpResponseRedirect(reverse("maketeam"))
   
        # Check the team is in <teams DB>
        try:
            team = Team.objects.get(name = team_name)
        except ObjectDoesNotExist:
            msg_error(project_non_exist_team)
            return HttpResponseRedirect(reverse("makeproject"))

        # Check login user belong to the team
        user = self.request.user
        try:
            team.members.get_member(id = user.id)
        except ObjectDoesNotExist:
            msg_error(project_user_does_not_belong_team)
            return HttpResponseRedirect(reverse("makeproject"))
        
        # Login check is programmed in buildbuild/urls.py
        # link team to project using ProjectMembership
        project = Project.objects.create_project(project_name)

        project_membership = ProjectMembership.objects.create(
            project = project,
            project_team = team,
            is_admin = True,
        )
        project_membership.save()
        
        msg_success(project_make_success)
        return HttpResponseRedirect(reverse("home")) 

