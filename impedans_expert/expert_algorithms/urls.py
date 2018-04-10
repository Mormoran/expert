from django.conf.urls import url

from django.contrib.auth.decorators import login_required

from . views import *

urlpatterns = [
    url(r'^algorithm/select/$', login_required(SelectAlgorithm.as_view()), name='algorithm_selector'),
    url(r'^results/display/$', login_required(ResultsDisplay.as_view()), name='results_display'),
    url(r'^algorithm/z_score/$', login_required(RunZScore.as_view()), name='z_score'),
    url(r'^algorithm/trained_z_score/$', RunTrainedZScore.as_view(), name='trained_z_score'),
    url(r'^algorithm/training/$', TrainingPage.as_view(), name='trainer'),
]

