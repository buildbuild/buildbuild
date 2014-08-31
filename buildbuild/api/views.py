from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import filters

from users.models import User
from users.serializers import UserSerializer

from teams.models import Team
from teams.serializers import TeamSerializer

from projects.models import Project
from projects.serializers import ProjectSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('email', )


class TeamList(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class ProjectList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class TeamDetail(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    lookup_field = "name"


class TeamUserList(generics.ListAPIView):
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('email', )

    def get_queryset(self):
        teamname = self.kwargs['name']
        team = get_object_or_404(Team, name=teamname)
        return team.users.all()


class TeamProjectList(generics.ListAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        teamname = self.kwargs['name']
        team = get_object_or_404(Team, name=teamname)
        return team.project_set.all()
