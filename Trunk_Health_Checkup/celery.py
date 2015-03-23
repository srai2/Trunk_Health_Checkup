
from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Trunk_Health_Checkup.settings')

app = Celery('Trunk_Health_Checkup')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

CELERYBEAT_SCHEDULE = {
    # crontab(hour=0, minute=0, day_of_week='saturday')
    'schedule-name': {  # example: 'file-backup'
        'task': 'APL_THC.tasks.task',  # example: 'files.tasks.cleanup'
        'schedule': timedelta(seconds=30),
    },
}
#CELERY_TIMEZONE = 'UTC'

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))