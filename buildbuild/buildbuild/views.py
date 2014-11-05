from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
 
class Home(TemplateView):
    template_name = "home.html"
   
    # context['var'] in views -> {{var}} in html
    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        user = self.request.user
        # login user?, or anonymous user
        if user.__class__.__name__ is "User":
            user = self.request.user
            context['team_list'] = user.member.all()
        """# in Case of anonymous user, nothing to do. but commented code is denoted.
        elif user.__class__.__name__ is "AnonymousUser":
            pass
        """
        return context

