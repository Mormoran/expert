from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# if not settings.configured:
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')  # pragma: no cover

app = Celery('impedans_expert')

# app.autodiscover_tasks()

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)