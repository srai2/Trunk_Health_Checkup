__author__ = 'sandeep'

import tng
import os
from CUCM.trunk import TRUNK, SEA_CUCM,SFO_CUCM,LHR_CUCM
from autolib import tb_config

def get_cucm():
    cucm = {
        "sea": SEA_CUCM(tb_config.sea_cucm1),
        "lhr": LHR_CUCM(tb_config.lhr_cucm1),
        "sfo": SFO_CUCM(tb_config.sfo_cucm1)
    }
    return cucm


def get_trunk_status():
    cucm = get_cucm()
    for key, value in cucm.items():
        cucm_xlib = value.cucm_xlib
        obj = list(TRUNK_MODEL.objects.filter(cluster=key))
        for trunk_name in obj:
            obj = TRUNK_MODEL.objects.filter(name=trunk_name, cluster=key)
            sip_trunk = cucm_xlib.get_sip_trunk(trunk_name)
            sip_profile = str(sip_trunk.sip_profile_name)
            security_profile = str(sip_trunk.security_profile_name)
            trp = str(sip_trunk.use_trusted_relay_point)
            device_pool = str(sip_trunk.device_pool_name)
            obj.update(sip_profile=sip_profile,security_profile=security_profile,trp=trp, device_pool=device_pool)
            print obj

        # obj = list(TRUNK_MODEL.objects.filter(cluster=key))
        # trunk = TRUNK(value, obj)
        #
        # trunk_status = trunk.get_trunk_status()
        # print key + "Adding Trunk"
        # if len(obj)<1:
        #     trunk_obj = []
        #     for status in trunk_status:
        #         trunk_obj.append(TRUNK_MODEL(name=status[0], status=status[1], cluster=key))
        #
        #     TRUNK_MODEL.objects.bulk_create(trunk_obj)
        # else:
        #     for status in trunk_status:
        #         obj = TRUNK_MODEL.objects.filter(name=status[0], cluster=key)
        #         obj.status = status[1]
        #         obj.save()
        # print key + "Added Successfully"


# Start execution here!
if __name__ == '__main__':
    print "Starting population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Trunk_Health_Checkup.settings')
    from APL_THC.models import Trunk as TRUNK_MODEL
    tng.run(get_trunk_status)