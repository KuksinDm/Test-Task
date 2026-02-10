from __future__ import absolute_import, unicode_literals

import logging.config
import os

from celery import Celery
from django.conf import settings as django_settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")
logging.config.dictConfig(django_settings.LOGGING)
app.autodiscover_tasks()
