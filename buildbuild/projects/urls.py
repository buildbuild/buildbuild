from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.decorators import login_required
from projects.views import MakeProjectView

urlpatterns = patterns('',
)
