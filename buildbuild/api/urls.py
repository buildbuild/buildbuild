from django.conf.urls import patterns, url
from api import views

urlpatterns = patterns('',
    url(r'^users/$', views.UserList.as_view(), name="user-list"),
)
