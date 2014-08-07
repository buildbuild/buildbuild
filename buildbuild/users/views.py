from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView

from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib import messages

from django.core.urlresolvers import reverse

from django.conf import settings

from users.forms import LoginForm
from users.models import User

class Login(FormView):
    template_name = "users/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        email = self.request.POST["email"]
        password = self.request.POST["password"]
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                messages.add_message(self.request, messages.SUCCESS, "Successfully Login")
                return HttpResponseRedirect(reverse("login"))
            else:
                messages.add_message(self.request, messages.ERROR, "ERROR : Deativated User")
                return HttpResponseRedirect(reverse("login"))
        else:
            messages.add_message(self.request, messages.ERROR, "ERROR : Invalid Email / Password")
            return HttpResponseRedirect(reverse("login"))

class Logout(RedirectView):
    def get_redirect_url(self):
        logout(self.request)
        messages.add_message(self.request, messages.SUCCESS, "Successfully Logout")
        return reverse("login")
