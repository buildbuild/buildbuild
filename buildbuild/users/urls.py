from django.conf.urls import patterns, include, url
from users import views

from users.views import UsersIndex

urlpatterns = patterns('',
    url('^', UsersIndex.as_view(), name = "index"),
)

