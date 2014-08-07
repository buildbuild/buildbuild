from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth import authenticate
from users.models import User, UserManager
from django.conf import settings
from users.forms import LoginForm
from users.models import User

def home(request):
    if request.method == 'GET':
        return render(request, 'users/home.html')
    elif request.method == 'POST':
        return redirect("/users/list/" + request.POST['id'])

class ListAllView(ListView):
    template_name = 'users/listAll.html'
    context_object_name = 'userList'

    def get_queryset(self):
        """Return the all signed users."""
        return User.objects.order_by('id')

class ListOneView(DetailView):
    template_name = 'users/listOne.html'
    model = User
    context_object_name = 'user'

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
