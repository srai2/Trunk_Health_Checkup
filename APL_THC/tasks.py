from __future__ import absolute_import

from celery import shared_task
from APL_THC.models import Trunk
from APL_THC.helpers import get_cucm, TRUNK, add_trunk_name_and_status, add_trunk_values
import tng
from celery.task.schedules import crontab
from celery.task.schedules import crontab

def get_tng_value():
   cucm = get_cucm()
   for key, value in cucm.items():
        obj = list(Trunk.objects.filter(cluster=key))
        trunk = TRUNK(value, obj)
        add_trunk_name_and_status(trunk, key, obj)
        add_trunk_values(trunk, key)

@shared_task
def task():
    tng.run(get_tng_value)