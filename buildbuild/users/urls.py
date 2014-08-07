from django.conf.urls import patterns, include, url
from users import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^list/$', views.ListAllView.as_view(), name='listAll'),
    url(r'^list/(?P<email>[ a-zA-Z0-9_@\.]+)/$', views.ListOneView.as_view(), name='listOne'),
    #url(r'^users/', include('users.urls')),
)

