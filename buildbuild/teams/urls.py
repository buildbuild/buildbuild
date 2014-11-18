from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.decorators import login_required
from teams.views import MakeTeamView, TeamList

urlpatterns = patterns('',
    url(r'^teams/new/', login_required(MakeTeamView.as_view()), name="new"),
    url(r'^teams/search/$', 'teams.views.search_team', name='search'),
    url(r'^teams/([0-9]+)/join/$', 'teams.views.join_team', name="join"),
    url(
        r'^teams/([0-9]+)/accept/users/([0-9]+)/$', 
        'teams.views.accept_request_to_join_team',
        name = 'accept',
    ),
    url(r'^teams/([0-9]+)/$', 'teams.views.team_page', name='team_page'),
    url(r'^teams/$', TeamList.as_view(), name="teamlist"),

)   
