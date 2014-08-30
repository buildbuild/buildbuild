from django.conf.urls import patterns, url
from api import views

urlpatterns = patterns('',
    url(r'^users/$', views.UserList.as_view(), name="user-list"),

    url(r'^teams/$', views.TeamList.as_view(), name="team-list"),
    url(r'^teams/(?P<name>[a-zA-Z0-9-_]+)/$', views.TeamDetail.as_view(), name="team-detail"),
)
