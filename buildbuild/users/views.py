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
            messages.error(self.request, custom_msg.user_signup_error)
            messages.info(self.request, custom_msg.user_email_not_exist)
            return HttpResponseRedirect(reverse("users:login"))
        else:
            next = ""

            if 'next' in self.request.GET:
                next = self.request.GET['next']

            if user is not None:
                if user.is_active:
                    login(self.request, user)
                    messages.success(
                        self.request, 
                        custom_msg.user_login_success
                    )
                    messages.info(
                        self.request, 
                        custom_msg.user_login_success_info
                    )

                    if next == "":
                        return HttpResponseRedirect(reverse("home"))
                    else:
                        return HttpResponseRedirect(next)
                else:
                    messages.error(self.request, custom_msg.user_signup_error)
                    messages.info(self.request, custom_msg.user_deactivated)
                    return HttpResponseRedirect(reverse("users:login"))
            else:
                messages.error(self.request, custom_msg.user_signup_error)
                messages.info(self.request, custom_msg.user_invalid)
                return HttpResponseRedirect(reverse("users:login"))

class Logout(RedirectView):
    def get_redirect_url(self):
        try:
            logout(self.request)
        except:
            messages.error(self.request, custom_msg.user_logout_error)
            messages.info(self.request, custom_msg.user_logout_error_info)
            return HttpResponseRedirect(reverse("home"))
        else:
            messages.success(self.request, custom_msg.user_logout_success)
            messages.info(self.request, custom_msg.user_logout_success_info)
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
        is_available_user_name = False

        # Password confirmation
        if password != password_confirmation:
            messages.error(
                self.request, 
                custom_msg.user_signup_error,
            )           
            messages.info(
                self.request, 
                custom_msg.user_password_confirmation_error,
            )
            return HttpResponseRedirect(reverse("users:signup"))

        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(self.request, custom_msg.user_signup_error)
            messages.info(self.request, custom_msg.user_invalid_email)
            return HttpResponseRedirect(reverse("users:signup"))

        # Check Uniqueness of User
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            pass
        else:
            messages.error(self.request, custom_msg.user_signup_error)
            messages.info(self.request, custom_msg.user_already_exist)
            return HttpResponseRedirect(reverse("users:signup"))

        # Validate password
        try:
            User.objects.validate_password(password)
        except ValidationError:
            messages.error(self.request, custom_msg.user_signup_error)
            messages.info(self.request, custom_msg.user_invalid_password)
            return HttpResponseRedirect(reverse("users:signup"))

        # Validate user name
        if 'user_name' in self.request.POST:
            try:
                User.objects.validate_name(
                    self.request.POST['user_name']
                )
            except ValidationError:
                messages.error(self.request, custom_msg.user_signup_error)
                messages.info(
                    self.request, 
                    custom_msg.user_name_max_length_error
                )
                return HttpResponseRedirect(reverse("users:signup"))
            else:
                is_available_user_name = True 

        # Create new user
        user = User.objects.create_user(
                   email, 
                   password = password
               )
        
        # User name update
        if is_available_user_name:
            User.objects.update_user(
                id = user.id,
                name = self.request.POST['user_name'],
            )

        messages.success(self.request, custom_msg.user_signup_success)
        messages.info(self.request, custom_msg.user_signup_success_info)
        
        # send Email, test should be programmed in tasks.py
        tasks.send_mail_to_new_user.delay(user)
        return HttpResponseRedirect(reverse("users:login"))

