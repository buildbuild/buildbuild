from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from users.views import Login
from users.views import Logout

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'buildbuild.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login/', Login.as_view(), name="login"),
    url(r'^logout/', Logout.as_view(), name="logout"),
    url(r'^admin/', include(admin.site.urls)),
)
