from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from users.models import User
from teams.models import Team
from projects.models import Project

def search_object_form(request):
    msg = ""
    object_does_not_exist = "The Team or Project does not exist"
    if 'search_object_text' in request.GET:
        search_object_text = request.GET['search_object_text']
        msg = ""
        try:
            team = Team.objects.get(name = search_object_text) 
        except:
            pass
        else:
            msg += "Team : " + team.name + "\n"

        try:
            project = Project.objects.get(name = search_object_text)
        except:
            pass
        else:
            msg += "Project : " + project.name + "\n"
    
        if msg is "":
            messages.error(request, object_does_not_exist)
        else:
            messages.success(request, msg)
    else:
        msg = 'You submitted an empty form.'
        messages.warning(request, msg)
    return HttpResponseRedirect("/")
 
class Home(TemplateView):
    template_name = "home.html"

