from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth import authenticate
from users.models import User, UserManager
from users.forms import LoginForm
from users.models import User
from django.core.exceptions import ObjectDoesNotExist

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
                return HttpResponse("Success")
            else:
                return HttpResponse("Not Active")
        else:
            return HttpResponse("Not Valid")