from django.conf.urls import url
from django.contrib import admin

from users.api.views import (
    UserCreateAPIView,
    UserDeleteAPIView,
    UserDetailAPIView,
    UserListAPIView,
    UserUpdateAPIView,
)

urlpatterns = [
    url(r'^user/$', UserListAPIView.as_view(), name='user_list'),
    url(r'^user/create/$', UserCreateAPIView.as_view(), name='user_list_create'),
    url(r'^user/(?P<pk>\d+)/$', UserDetailAPIView.as_view(), name='user_list_detail'),
    url(r'^user/(?P<pk>\d+)/edit/$', UserUpdateAPIView.as_view(), name='user_list_update'),
    url(r'^user/(?P<pk>\d+)/delete/$', UserDeleteAPIView.as_view(), name='user_list_delete'),
]