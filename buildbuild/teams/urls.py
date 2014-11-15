from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.decorators import login_required
from teams.views import MakeTeamView

urlpatterns = patterns('',
    url(r'^new/', login_required(MakeTeamView.as_view()), name="maketeam"),
    url(r'^search_team/$', 'teams.views.search_team', name='search_team'),
    url(r'^join_team/([0-9]+)/$', 'teams.views.join_team', name="join_team"),
    url(
        r'^accept_request_to_join_team/([0-9]+)-([0-9]+)/$', 
        'teams.views.accept_request_to_join_team',
        name = 'accept_request_to_join_team',
    )
)   
