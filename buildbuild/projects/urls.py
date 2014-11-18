from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.decorators import login_required
from projects.views import MakeProjectView

urlpatterns = patterns('',
    url(
        r'^teams/([0-9]+)/projects/([0-9]+)/$', 
        'projects.views.project_page', 
        name='project_page',
    ),
    url(
        r'^teams/(?P<team_id>[0-9]+)/projects/new/$',
        login_required(MakeProjectView.as_view()),
        name="makeproject"
    ),  

)
