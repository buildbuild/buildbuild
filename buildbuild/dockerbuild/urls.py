from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^build/([0-9]+)/$', 'dockerbuild.views.build', name='build'),
)
