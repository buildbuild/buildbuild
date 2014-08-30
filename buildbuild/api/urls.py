from django.conf.urls import patterns, url
from api import views

urlpatterns = patterns('',
    url(r'^users/$', views.UserList.as_view(), name="user-list"),
    url(r'^teams/$', views.TeamList.as_view(), name="team-list"),
)
