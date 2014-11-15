from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^/build_page/([0-9]+)/$', 'dockerbuild.views.build_page', name='build_page'),
    url(r'^/build_page/([0-9]+)/build_new/$', 'dockerbuild.views.build_new', name='build_new'),
)
