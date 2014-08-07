from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from users.models import User, UserManager
# Create your views here.

def home(request):
    return render(request, 'users/home.html')

class ListAllView(ListView):

    template_name = 'users/listAll.html'
    context_object_name = 'userList'

    def get_queryset(self):
        """Return the all signed users."""
        return User.objects.order_by('id')