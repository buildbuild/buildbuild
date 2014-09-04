from django.conf.urls import patterns, include, url
from users import views

from users.views import UsersIndexView
from users.views import UserShowView

urlpatterns = patterns('',
    url('^$', UsersIndexView.as_view(), name = "index"),
    url('^(?P<pk>\d+)$', UserShowView.as_view(), name = "show"),
)

