from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import Http404
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView

from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from users.models import User, UserManager
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings

from users.forms import LoginForm
from users.forms import SignUpForm
from users.models import User

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db import OperationalError
from django.core.exceptions import ValidationError

"""
from django.core.mail import send_mail
from django.conf import settings
"""
from users import tasks

def home(request):
    if request.method == 'GET':
        return render(request, 'users/home.html')
    elif request.method == 'POST':
        return redirect("/users/list/" + request.POST['id'])

class ListAllView(ListView):
    template_name = 'users/listAll.html'
    context_object_name = 'userList'

    def get_queryset(self):
        if User.objects.count() == 0:
            raise Http404

        return User.objects.order_by('id')

class ListOneView(DetailView):
    template_name = 'users/listOne.html'
    model = User
    context_object_name = 'user'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            obj = queryset.get(email=self.kwargs['email'])
        except ObjectDoesNotExist:
            raise Http404
        return obj

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
                messages.add_message(
                        self.request, 
                        messages.SUCCESS, 
                        "Successfully Login"
                        )
                return HttpResponseRedirect(reverse("home"))
            else:
                messages.add_message(
                        self.request, 
                        messages.ERROR, 
                        "ERROR : Deativated User"
                        )
                return HttpResponseRedirect(reverse("login"))
        else:
            messages.add_message(
                    self.request, 
                    messages.ERROR, 
                    "ERROR : Invalid Email / Password"
                    )
            return HttpResponseRedirect(reverse("login"))

class Logout(RedirectView):
    def get_redirect_url(self):
        logout(self.request)
        messages.add_message(
                self.request, 
                messages.SUCCESS, 
                "Successfully Logout")
        return reverse("home")

class SignUp(FormView, User):
    template_name = "users/signup.html"
    form_class = SignUpForm
    
    def form_valid(self, form):
        email = self.request.POST["email"]
        password = self.request.POST["password"]

        try:
            User.objects.create_user(email, password = password)
        except ValidationError:
            messages.add_message(
                    self.request,
                    messages.ERROR,
                    "ERROR : detected invalid information"
                    )
            return HttpResponseRedirect(reverse("signup"))           
        except IntegrityError:
            messages.add_message(
                    self.request, 
                    messages.ERROR, 
                    "ERROR : The account already exists"
                    )
            return HttpResponseRedirect(reverse("signup"))
        else: 
            messages.add_message(
                    self.request, 
                    messages.SUCCESS, 
                    "Successfully Signup"
                    )
            try:
                tasks.send_mail_to_new_user_using_celery.delay()
            except OperationalError:
             messages.add_message(
                    self.request, 
                    messages.ERROR, 
                    "Sign-up email was not sended"
                    )
               
            return HttpResponseRedirect(reverse("home"))

        
