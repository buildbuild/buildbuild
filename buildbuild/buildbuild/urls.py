from django.conf.urls import patterns, include, url

from django.contrib import admin
from users import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'buildbuild.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('users.urls',namespace='users')),
)
