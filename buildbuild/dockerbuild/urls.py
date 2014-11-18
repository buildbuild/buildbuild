from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^([0-9]+)/$', 'dockerbuild.views.build_page', name='build_page'),
    url(r'^([0-9]+)/new/$', 'dockerbuild.views.build_new', name='new'),
    url(r'^([0-9]+)/deploy/$', 'dockerbuild.views.deploy', name='deploy'),
    url(r'^([0-9]+)/my_project/$', 'dockerbuild.views.my_project', name='my_project'),
)
