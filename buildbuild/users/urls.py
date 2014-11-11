from django.conf.urls import patterns, include, url
from users import views

from users.views import UsersIndexView, UserShowView 
from users.views import Login, Logout, SignUp, AccountView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url('^$', UsersIndexView.as_view(), name = "index"),
    url('^(?P<pk>\d+)$', UserShowView.as_view(), name = "show"),
    url(r'^login/', Login.as_view(), name="login"),
    url(r'^logout/', Logout.as_view(), name="logout"),
    url(r'^account/', login_required(AccountView.as_view()), name="account"),
    url(r'^signup/', SignUp.as_view(), name="signup"),
    url(r'^user_page/([0-9]+)/$', 'users.views.user_page', name="user_page"), 
)

