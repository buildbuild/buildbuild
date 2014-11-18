from django.conf.urls import patterns, include, url
from users import views

from users.views import UsersIndexView, UserShowView 
from users.views import Login, Logout, SignUp, AccountView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url('^users/$', UsersIndexView.as_view(), name = "index"),
    url('^users/(?P<pk>\d+)$', UserShowView.as_view(), name = "show"),
    url(r'^users/account/', login_required(AccountView.as_view()), name="account"),
    url(r'^users/([0-9]+)/$', 'users.views.user_page', name="user_page"),

    url(r'^login/', Login.as_view(), name="login"),
    url(r'^logout/', Logout.as_view(), name="logout"),
    url(r'^signup/', SignUp.as_view(), name="signup"),

)

