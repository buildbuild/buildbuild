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
from django.core.exceptions import ValidationError

from projects.forms import MakeProjectForm
from projects.models import Project

from projects.models import Project

class MakeProjectView(FormView):
    template_name = "projects/makeproject.html"
    form_class = MakeProjectForm

    def form_valid(self, form):
        # name field required
        try:
            self.request.POST["projects_project_name"]
        except ValidationError:
            messages.add_message(
                    self.request,
                    messages.ERROR,
                    "ERROR : project name form empty"
                    )
            return HttpResponseRedirect(reverse("makeproject"))           
        else:
            name = self.request.POST["projects_project_name"]

        # valid and unique team name test
        try:        
            project = Project.objects.create_project(name)
        except ValidationError:
            messages.add_message(
                    self.request,
                    messages.ERROR,
                    "ERROR : invalid project name"
                    )
            return HttpResponseRedirect(reverse("makeproject"))          
        except IntegrityError:
            messages.add_message(
                    self.request, 
                    messages.ERROR, 
                    "ERROR : The project name already exists"
                    )
            return HttpResponseRedirect(reverse("makeproject"))
        else: 
            # needed to add to link project to team using Project Memberhip 
            messages.add_message(
                    self.request, 
                    messages.SUCCESS, 
                    "Project created successfully"
                    )
            return HttpResponseRedirect(reverse("home")) 

