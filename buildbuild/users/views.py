from django.http import HttpResponseRedirect,request

from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic import DetailView

from django.contrib.auth import login, logout, authenticate

from django.contrib import messages

from django.core.urlresolvers import reverse

from users.models import User
from teams.models import Team
from projects.models import Project

from users.forms import LoginForm, SignUpForm

from django.db import IntegrityError, OperationalError
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from users import tasks
from django.core.validators import validate_email
from buildbuild import custom_msg
from django.shortcuts import render

def user_page(request, user_id):
    user = User.objects.get_user(user_id)
    return render(
               request,
               "users/user_page.html",
               {
                   "user" : user,
               },
           )

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

        # User authentication
        try:
            user = authenticate(email=email, password=password)
        except ValidationError:
            messages.error(self.request, custom_msg.user_email_not_exist)
            return HttpResponseRedirect(reverse("login"))
        else:
            next = ""

            if 'next' in self.request.GET:
                next = self.request.GET['next']

            if user is not None:
                if user.is_active:
                    login(self.request, user)
                    messages.success(self.request, custom_msg.user_login_success)

                    if next == "":
                        return HttpResponseRedirect(reverse("home"))
                    else:
                        return HttpResponseRedirect(next)
                else:
                    messages.error(self.request, custom_msg.user_deactivated)
                    return HttpResponseRedirect(reverse("login"))
            else:
                messages.error(self.request, custom_msg.user_invalid)
                return HttpResponseRedirect(reverse("login"))

class Logout(RedirectView):
    def get_redirect_url(self):
        user_logout_failed = "ERROR : logout failed"
        user_logout_success = "Successfully Logout"

        try:
            logout(self.request)
        except:
            messages.add_message(
                self.request,
                messages.ERROR,
                user_logout_failed
            )
            return HttpResponseRedirect(reverse("home"))
        else:
            messages.add_message(
                self.request,
                messages.SUCCESS,
                user_logout_success
            )
            return reverse("home")

class AccountView(DetailView):
    model = User
    template_name = 'users/account.html'

    context_object_name = "user_account"

    def get_object(self, queryset=None):
        return self.request.user

class SignUp(FormView):
    template_name = "users/signup.html"
    form_class = SignUpForm

    def form_valid(self, form):
        email = self.request.POST["email"]
        password = self.request.POST["password"]
        password_confirmation = self.request.POST["password_confirmation"]

        if password != password_confirmation:
            messages.error(
                self.request, 
                custom_msg.user_password_confirmation_error,
            )
            return HttpResponseRedirect(reverse("signup"))


        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(self.request, custom_msg.user_invalid_email)
            return HttpResponseRedirect(reverse("signup"))

        # Check Uniqueness of User
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            pass
        else:
            messages.error(self.request, custom_msg.user_already_exist)
            return HttpResponseRedirect(reverse("signup"))

        # Validate password
        try:
            User.objects.validate_password(password)
        except ValidationError:
            messages.error(self.request, custom_msg.user_invalid_password)
            return HttpResponseRedirect(reverse("signup"))

        # Create new user
        user = User.objects.create_user(email, password = password)
        messages.success(self.request, custom_msg.user_signup_success)

        # send Email, test should be programmed in tasks.py
        tasks.send_mail_to_new_user.delay(user)
        return HttpResponseRedirect(reverse("login"))

