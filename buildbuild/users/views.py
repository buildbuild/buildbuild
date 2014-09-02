from django.http import HttpResponseRedirect,request

from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic import DetailView

from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from users.models import User

from users.forms import LoginForm


class UsersIndexView(ListView):
    template_name = 'users/index.html'
    model = User


class UserShowView(DetailView):
    template_name = "users/show.html"
    model = User


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
                self.request.session['email'] = email
                return HttpResponseRedirect(reverse("login"))
            else:
                messages.add_message(self.request, messages.ERROR, "ERROR : Deactivated User")
                return HttpResponseRedirect(reverse("login"))
        else:
            messages.add_message(self.request, messages.ERROR, "ERROR : Invalid Email / Password")
            return HttpResponseRedirect(reverse("login"))


class Logout(RedirectView):
    def get_redirect_url(self):
        logout(self.request)
        messages.add_message(self.request, messages.SUCCESS, "Successfully Logout")
        return reverse("home")

class AccountView(DetailView):
    model = User
    template_name = 'users/account.html'

    slug_field = "email"
    context_object_name = "user_account"

    def get_object(self, queryset=None):
        return User.objects.get(email = self.request.session['email'])