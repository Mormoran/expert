from django.conf.urls import url

from django.contrib.auth.decorators import login_required

from . views import *

urlpatterns = [
    # url(regex=r'^/$', login_required(UserListView.as_view()), name='list'), # REACTIVATE THIS FOR ADMINS ONLY AFTER PERMISSIONING IS DONE
    url(r'^~redirect/$', login_required(UserRedirectView.as_view()), name='redirect'),
    url(r'^(?P<username>[\w.@+-]+)/$', login_required(UserDetailView.as_view()), name='detail'),
    url(r'^~update/$', login_required(UserUpdateView.as_view()), name='update'),
]
#regex=
