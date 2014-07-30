__author__ = 'riskkim'

from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('users.views',
    url(r'^$', views.index),
    )