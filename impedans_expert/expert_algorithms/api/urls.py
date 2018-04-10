from django.conf.urls import url
from django.contrib import admin

from expert_algorithms.api.views import (
    AlgorithmCreateAPIView,
    AlgorithmDeleteAPIView,
    AlgorithmDetailAPIView,
    AlgorithmListAPIView,
    AlgorithmUpdateAPIView,
    AlgorithmRunCreateAPIView,
    AlgorithmRunDeleteAPIView,
    AlgorithmRunDetailAPIView,
    AlgorithmRunListAPIView,
    AlgorithmRunUpdateAPIView,
    AlgorithmRunResultsCreateAPIView,
    AlgorithmRunResultsDeleteAPIView,
    AlgorithmRunResultsDetailAPIView,
    AlgorithmRunResultsListAPIView,
    AlgorithmRunResultsUpdateAPIView,
    AlgorithmTimeResultsCreateAPIView,
    AlgorithmTimeResultsDeleteAPIView,
    AlgorithmTimeResultsDetailAPIView,
    AlgorithmTimeResultsListAPIView,
    AlgorithmTimeResultsUpdateAPIView,
    AlgorithmStateCreateAPIView,
    AlgorithmStateDeleteAPIView,
    AlgorithmStateDetailAPIView,
    AlgorithmStateListAPIView,
    AlgorithmStateUpdateAPIView
)

urlpatterns = [
    url(r'^algorithms/$', AlgorithmListAPIView.as_view(), name='algorithms_list'),
    url(r'^algorithms/create/$', AlgorithmCreateAPIView.as_view(), name='algorithms_list_create'),
    url(r'^algorithms/(?P<pk>\d+)/$', AlgorithmDetailAPIView.as_view(), name='algorithms_list_detail'),
    url(r'^algorithms/(?P<pk>\d+)/edit/$', AlgorithmUpdateAPIView.as_view(), name='algorithms_list_update'),
    url(r'^algorithms/(?P<pk>\d+)/delete/$', AlgorithmDeleteAPIView.as_view(), name='algorithms_list_delete'),

    url(r'^algorithm-run/$', AlgorithmRunListAPIView.as_view(), name='algorithm_run_list'),
    url(r'^algorithm-run/create/$', AlgorithmRunCreateAPIView.as_view(), name='algorithm_run_list_create'),
    url(r'^algorithm-run/(?P<pk>\d+)/$', AlgorithmRunDetailAPIView.as_view(), name='algorithm_run_list_detail'),
    url(r'^algorithm-run/(?P<pk>\d+)/edit/$', AlgorithmRunUpdateAPIView.as_view(), name='algorithm_run_list_update'),
    url(r'^algorithm-run/(?P<pk>\d+)/delete/$', AlgorithmRunDeleteAPIView.as_view(), name='algorithm_run_list_delete'),

    url(r'^algorithm-run-results/$', AlgorithmRunResultsListAPIView.as_view(), name='algorithm_run_results_list'),
    url(r'^algorithm-run-results/create/$', AlgorithmRunResultsCreateAPIView.as_view(), name='algorithm_run_results_list_create'),
    url(r'^algorithm-run-results/(?P<pk>\d+)/$', AlgorithmRunResultsDetailAPIView.as_view(), name='algorithm_run_results_list_detail'),
    url(r'^algorithm-run-results/(?P<pk>\d+)/edit/$', AlgorithmRunResultsUpdateAPIView.as_view(), name='algorithm_run_results_list_update'),
    url(r'^algorithm-run-results/(?P<pk>\d+)/delete/$', AlgorithmRunResultsDeleteAPIView.as_view(), name='algorithm_run_results_list_delete'),

    url(r'^algorithm-time-results/$', AlgorithmTimeResultsListAPIView.as_view(), name='algorithm_time_results_list'),
    url(r'^algorithm-time-results/create/$', AlgorithmTimeResultsCreateAPIView.as_view(), name='algorithm_time_results_list_create'),
    url(r'^algorithm-time-results/(?P<pk>\d+)/$', AlgorithmTimeResultsDetailAPIView.as_view(), name='algorithm_time_results_list_detail'),
    url(r'^algorithm-time-results/(?P<pk>\d+)/edit/$', AlgorithmTimeResultsUpdateAPIView.as_view(), name='algorithm_time_results_list_update'),
    url(r'^algorithm-time-results/(?P<pk>\d+)/delete/$', AlgorithmTimeResultsDeleteAPIView.as_view(), name='algorithm_time_results_list_delete'),

    url(r'^algorithm-state/$', AlgorithmStateListAPIView.as_view(), name='algorithm_state_list'),
    url(r'^algorithm-state/create/$', AlgorithmStateCreateAPIView.as_view(), name='algorithm_state_list_create'),
    url(r'^algorithm-state/(?P<pk>\d+)/$', AlgorithmStateDetailAPIView.as_view(), name='algorithm_state_list_detail'),
    url(r'^algorithm-state/(?P<pk>\d+)/edit/$', AlgorithmStateUpdateAPIView.as_view(), name='algorithm_state_list_update'),
    url(r'^algorithm-state/(?P<pk>\d+)/delete/$', AlgorithmStateDeleteAPIView.as_view(), name='algorithm_state_list_delete'),
]