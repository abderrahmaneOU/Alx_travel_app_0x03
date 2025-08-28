from __future__ import absolute_import, unicode_literals
import os
from alx_travel_app.celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app_0x00.settings')

app = Celery('alx_travel_app_0x00')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
