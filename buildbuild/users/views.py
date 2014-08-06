from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import FormView

from users.forms import LoginForm

class Login(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = "/" # Not Implemented
