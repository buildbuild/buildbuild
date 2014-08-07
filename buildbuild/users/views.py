from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth import authenticate
from users.models import User, UserManager
from django.conf import settings
from users.forms import LoginForm
from users.models import User

def home(request):
    return render(request, 'users/home.html')

class ListAllView(ListView):

    template_name = 'users/listAll.html'
    context_object_name = 'userList'

    def get_queryset(self):
        """Return the all signed users."""
        return User.objects.order_by('id')

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
                return HttpResponse("Success")
            else:
                return HttpResponse("Not Active")
        else:
            return HttpResponse("Not Valid")
