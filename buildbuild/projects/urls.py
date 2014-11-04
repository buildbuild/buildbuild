from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.decorators import login_required
from projects.views import MakeProjectView

urlpatterns = patterns('',
    url(r'^makeproject/(?P<team_name>[ a-zA-Z0-9_]+)/$', login_required(MakeProjectView.as_view()), name="makeproject"),
    url(r'^project_page/([0-9]+)/$', 'projects.views.project_page', name='project_page'),
)
