from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
 
class Home(TemplateView):
    template_name = "home.html"
   
