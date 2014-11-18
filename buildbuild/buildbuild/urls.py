from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from buildbuild.views import Home
from teams.views import MakeTeamView
from projects.views import MakeProjectView
from django.contrib.auth.decorators import login_required
from teams.views import TeamList
from projects.views import MakeProjectView

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^api/', include('api.urls', namespace="api")),
    url(r'^admin/', include(admin.site.urls)),
    
    # users' urls
    url(r'^', include('users.urls', namespace='users')),
    
    # teams' urls
    url(r'^', include('teams.urls', namespace='teams')),
    url(r'^teams/$', TeamList.as_view(), name="teamlist"),
    url(r'^teams/([0-9]+)/$', 'teams.views.team_page', name='team_page'),
    
    # projects' urls
    url(r'^', include('projects.urls', namespace='projects')),

    # dockerbuild's urls
    url(
        r'^builds/', 
        include('dockerbuild.urls', namespace='builds')
    ),
)
