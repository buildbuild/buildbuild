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

from teams.forms import MakeTeamForm
from teams.models import Team

class MakeTeamView(FormView):
    template_name = "teams/maketeam.html"
    form_class = MakeTeamForm

    def form_valid(self, form):
        name = self.request.POST["name"]

        try:
            team = Team.objects.create_team(name)
        except ValidationError:
            messages.add_message(
                    self.request,
                    messages.ERROR,
                    "ERROR : invalid information detected"
                    )
            return HttpResponseRedirect(reverse("maketeam"))           
        except IntegrityError:
            messages.add_message(
                    self.request, 
                    messages.ERROR, 
                    "ERROR : The team name already exists"
                    )
            return HttpResponseRedirect(reverse("maketeam"))
        else: 
            messages.add_message(
                    self.request, 
                    messages.SUCCESS, 
                    "Team created successfully"
                    )
            return HttpResponseRedirect(reverse("home")) 

