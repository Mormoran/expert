from django.conf.urls import url
from django.contrib import admin

from expert_import.api.views import (
    RunPropertiesCreateAPIView,
    RunPropertiesDeleteAPIView,
    RunPropertiesDetailAPIView,
    RunPropertiesListAPIView,
    RunPropertiesUpdateAPIView,
    RunsCreateAPIView,
    RunsDeleteAPIView,
    RunsDetailAPIView,
    RunsListAPIView,
    RunsUpdateAPIView
)

urlpatterns = [
    url(r'^runs/$', RunsListAPIView.as_view(), name='runs_list'),
    url(r'^runs/create/$', RunsCreateAPIView.as_view(), name='runs_list_create'),
    url(r'^runs/(?P<pk>\d+)/$', RunsDetailAPIView.as_view(), name='runs_list_detail'),
    url(r'^runs/(?P<pk>\d+)/edit/$', RunsUpdateAPIView.as_view(), name='runs_list_update'),
    url(r'^runs/(?P<pk>\d+)/delete/$', RunsDeleteAPIView.as_view(), name='runs_list_delete'),

    url(r'^run-properties/$', RunPropertiesListAPIView.as_view(), name='properties_list'),
    url(r'^run-properties/create/$', RunPropertiesCreateAPIView.as_view(), name='properties_list_create'),
    url(r'^run-properties/(?P<pk>\d+)/$', RunPropertiesDetailAPIView.as_view(), name='properties_list_detail'),
    url(r'^run-properties/(?P<pk>\d+)/edit/$', RunPropertiesUpdateAPIView.as_view(), name='properties_list_update'),
    url(r'^run-properties/(?P<pk>\d+)/delete/$', RunPropertiesDeleteAPIView.as_view(), name='properties_list_delete'),
]