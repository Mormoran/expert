from django.conf.urls import url

from . views import *

urlpatterns = [
    url(r'^parse_file/$', FileParser.as_view(), name='Parse'),
    url(r'^runs/$', RunsView.as_view(), name='runs'),
    url(r'^runs/chart$', ChartRunsView.as_view(), name='chart_runs'),
    url(r'^runinfo/(?P<runs_id>[0-9]+)/$', RunInfoView.as_view(),name='run'),
]