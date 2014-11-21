from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from buildbuild.views import Home
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', login_required(Home.as_view()), name='home'),
    url(r'^admin/', include(admin.site.urls)),
   
    # api's urls
    url(r'^api/', include('api.urls', namespace="api")),

    # users' urls
    url(r'^', include('users.urls', namespace='users')),
    
    # teams' urls
    url(r'^', include('teams.urls', namespace='teams')),
    
    # projects' urls
    url(r'^', include('projects.urls', namespace='projects')),

    # dockerbuild's urls
    url(
        r'^builds/', 
        include('dockerbuild.urls', namespace='builds')
    ),
)
