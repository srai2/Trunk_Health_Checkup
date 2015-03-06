__author__ = 'sandeep'

import tng
import os
from CUCM.trunk import TRUNK, SEA_CUCM,SFO_CUCM,LHR_CUCM

def get_cucm():
    cucm = {
        "sea": SEA_CUCM(),
        "lhr": LHR_CUCM(),
        "sfo": SFO_CUCM()
    }
    return cucm

#TODO: Need Process in this function to minimize time duration
def create_or_update_trunks():
    #creating cucm cluster and cucm xlib
    cucm = get_cucm()
    for key, value in cucm.items():
        #getting one type of clusetr
        obj = list(TRUNK_MODEL.objects.filter(cluster=key))
        #creating object of TRUNK by using clusetr and xlib
        #If obj is not created then init will call Trunk.get_trunk name()
        trunk = TRUNK(value, obj)
        #Getting trunk status of one type of cluster
        trunk_status = trunk.get_trunk_status()
        if len(obj)<1:
            trunk_obj = []
            for status in trunk_status:
                trunk_obj.append(TRUNK_MODEL(name=status[0], status=status[1], cluster=key))
            #Creating trunk object in bulk
            TRUNK_MODEL.objects.bulk_create(trunk_obj)
            obj = list(TRUNK_MODEL.objects.filter(cluster=key))
        else:
            for status in trunk_status:
                #Getting trunk status and updating the value in that obj
                obj = TRUNK_MODEL.objects.filter(name=status[0], cluster=key)
                obj.status = status[1]
                obj.update(status=status[1])
        #Getting the trunk values and updating in that trunk object
        for trunk_values in trunk.get_trunk_values():
            obj = TRUNK_MODEL.objects.filter(name=trunk_values[0], cluster=key)

            obj.update(sip_profile=trunk_values[1],security_profile=trunk_values[2],
                       trp=trunk_values[3], device_pool=trunk_values[4])


# Start execution here!
if __name__ == '__main__':
    print "Starting population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Trunk_Health_Checkup.settings')
    from APL_THC.models import Trunk as TRUNK_MODEL
    tng.run(create_or_update_trunks)