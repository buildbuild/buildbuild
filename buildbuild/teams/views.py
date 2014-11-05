from django.shortcuts import render
from django.http import HttpResponseRedirect,request
from django.http import HttpResponse

from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic import DetailView

from django.contrib.auth import authenticate

from django.contrib import messages

from django.core.urlresolvers import reverse

from django.db import IntegrityError, OperationalError
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from teams.forms import MakeTeamForm
from teams.models import Team, Membership, WaitList
from users.models import User
from projects.models import Project
from django.shortcuts import render
from teams.models import AlreadyMemberError, AlreadyWaitMemberError
from buildbuild import custom_msg
from django.http import HttpResponseForbidden
# Warning : create team operation from view automatically make MtoM relationship

# when User click a team, team_page method will render team_page.html
# with the team argument 
def team_page(request, team_id):
    team = Team.objects.get_team(team_id)

    # user who is not the team member cannot access the team page
    try:
        user = request.user
        team.members.get_member(user.id)
    except ObjectDoesNotExist:
        return HttpResponseForbidden(custom_msg.forbidden)

    project_list = team.project_teams.all()
    return render(
               request,
               "teams/team_page.html",
               {
                   "team" : team,
                   "project_list" : project_list,
               },
           )            

def join_team(request, team_id):
    wait_member = request.user
    team = Team.objects.get(id=team_id)
    try:
        WaitList.objects.create_wait_list(team, wait_member)
    except AlreadyMemberError:
        messages.error(request, custom_msg.already_member)
        return HttpResponseRedirect(reverse("home"))
    except AlreadyWaitMemberError:
        messages.error(request, custom_msg.already_wait_member)
        return HttpResponseRedirect(reverse("home"))

    messages.success(request, custom_msg.request_join_team) 
    return HttpResponseRedirect(reverse("home"))

def search_team(request):
    search_team = request.GET['search_team']

    # Case insensitive filtering
    teams = Team.objects.filter(name__icontains = search_team) 
   
    return render(
               request,
               "teams/search_team_result.html",
               {
                   "teams" : teams,
                   "already_team_member" : custom_msg.already_team_member,
               },
           )            

class MakeTeamView(FormView):
    template_name = "teams/maketeam.html"
    form_class = MakeTeamForm

    def form_valid(self, form):
        # name field required 
        name = self.request.POST["teams_team_name"]
        
        # valid team name test
        try:
            Team.objects.validate_name(name)
        except ValidationError:
            messages.error(self.request, custom_msg.team_invalid)
            return HttpResponseRedirect(reverse("teams:maketeam")) 

        # unique team test
        try:
            Team.objects.get(name = name)
        except ObjectDoesNotExist:
            pass
        else:
            messages.error(self.request, custom_msg.team_already_exist)
            return HttpResponseRedirect(reverse("teams:maketeam"))          
 
        # Login check is programmed in buildbuild/urls.py
        # link user to team using Membership  
        user = self.request.user
        team = Team.objects.create_team(name)

        membership = Membership.objects.create_membership(
            team = team, 
            user = user, 
        )
        membership.is_admin = True
        membership.save()

        messages.success(self.request, custom_msg.team_make_success)
 
        return HttpResponseRedirect(reverse("home"))

