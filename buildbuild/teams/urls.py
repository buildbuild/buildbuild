from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.decorators import login_required
from teams.views import MakeTeamView

urlpatterns = patterns('',
    url(r'^new/', login_required(MakeTeamView.as_view()), name="new"),
    url(r'^search/$', 'teams.views.search_team', name='search'),
    url(r'^([0-9]+)/join/$', 'teams.views.join_team', name="join"),
    url(
        r'^([0-9]+)/accept/users/([0-9]+)/$', 
        'teams.views.accept_request_to_join_team',
        name = 'accept',
    )
)   
