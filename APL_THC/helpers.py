__author__ = 'sandeep'

import tng
import os
from CUCM.trunk import TRUNK, SEA_CUCM, SFO_CUCM, LHR_CUCM


def get_cucm():
    cucm = {
        "sea": SEA_CUCM(),
        "lhr": LHR_CUCM(),
        "sfo": SFO_CUCM()
    }
    return cucm


def add_trunk_name_and_status(trunk, key, obj):
    #Getting trunk status of one type of cluster
    trunk_status = trunk.get_trunk_status()
    if len(obj)<1:
        trunk_obj = []
        for status in trunk_status:
            trunk_obj.append(TRUNK_MODEL(name=status[0], status=status[1], cluster=key))
        #Creating trunk object in bulk
        TRUNK_MODEL.objects.bulk_create(trunk_obj)
    else:
        for status in trunk_status:
            #Getting trunk status and updating the value in that obj
            obj = TRUNK_MODEL.objects.filter(name=status[0], cluster=key)
            obj.status = status[1]
            obj.update(status=status[1])

def add_trunk_values(trunk, key):
    #Getting the trunk values and updating in that trunk object
    for trunk_values in trunk.get_trunk_values():
        obj = TRUNK_MODEL.objects.filter(name=trunk_values[0], cluster=key)

        obj.update(sip_profile=trunk_values[1],security_profile=trunk_values[2],
                   trp=trunk_values[3], device_pool=trunk_values[4])


def add_route_pattern(trunk, key):
    list_pattern = trunk.get_route_pattern_names()
    for route_pattern, trunk_name in list_pattern.items():
        try:
            trunk_obj = TRUNK_MODEL.objects.get(name=trunk_name, cluster=key)
            RoutePattern.objects.get_or_create(trunk=trunk_obj, pattern=route_pattern)
        except:
            pass



#TODO: Need Process in this function to minimize time duration
def Main():
    #creating cucm cluster and cucm xlib
   cucm = get_cucm()
   for key, value in cucm.items():
        obj = list(TRUNK_MODEL.objects.filter(cluster=key))
        trunk = TRUNK(value, obj)
        add_trunk_name_and_status(trunk, key, obj)
        add_trunk_values(trunk, key)#Taking to much time
        add_route_pattern(trunk, key)




  # Start execution here!
if __name__ == '__main__':
    print "Starting APL_THC backend script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Trunk_Health_Checkup.settings')
    from APL_THC.models import Trunk as TRUNK_MODEL,RoutePattern
    tng.run(Main)