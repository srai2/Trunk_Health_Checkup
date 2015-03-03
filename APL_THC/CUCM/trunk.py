__author__ = 'sandeep'

import xlib
import tng
from autolib import tb_config
from multiprocessing import Process, Queue, Lock


class SEA_CUCM:
    def __init__(self, ip):

        tng.api.create_devices(dict(sea_ip=ip),
                               defaults=dict(username=tb_config.cucm_username,
                                             password=tb_config.cucm_password,
                                             rootpassword=tb_config.cucm_password))

        self.cucm=tng.api.get_system('sea_ip')
        self.cucm_xlib=xlib.api.create_device(self.cucm)

class LHR_CUCM:
    def __init__(self, ip):

        tng.api.create_devices(dict(lhr_ip=ip),
                               defaults=dict(username=tb_config.cucm_username,
                                             password=tb_config.cucm_password,
                                             rootpassword=tb_config.cucm_password))

        self.cucm=tng.api.get_system('lhr_ip')
        self.cucm_xlib=xlib.api.create_device(self.cucm)

class SFO_CUCM:
    def __init__(self, ip):

        tng.api.create_devices(dict(sfo_ip=ip),
                               defaults=dict(username=tb_config.cucm_username,
                                             password=tb_config.cucm_password,
                                             rootpassword=tb_config.cucm_password))

        self.cucm=tng.api.get_system('sfo_ip')
        self.cucm_xlib=xlib.api.create_device(self.cucm)

class TRUNK:
    def __init__(self, clstr, trunks=None):
        self.cucm = clstr.cucm
        self.cucm_xlib = clstr.cucm_xlib
        self.trunks = trunks or self.get_trunk_names()

    def get_trunk_status(self):
        print "getting trunk status"
        q = Queue()
        p_list = []
        status_list = []
        fac = self.cucm.soap.serviceability.factory
        lock = Lock()
        for trunk in self.trunks:
            p_list.append(Process(target=self._get_trunk_status, args=(fac, trunk, q, lock)))
        for p in p_list:
            p.start()
            p.join()
        while not q.empty():
            status_list.append(q.get())
        print "completed: trunk status"
        return status_list


    def get_trunk_names(self):
        print "getting trunk name"
        trunk_uuid = self.cucm_xlib._get_uuids_helper('listSipTrunk', criteria='name', value='%')
        trunks = []
        for t in trunk_uuid:
            trunks.append(str(self.cucm_xlib._get_uuid_helper('getSipTrunk', criteria='uuid', value=t)['sipTrunk'].name))
        print "completed: trunk name"
        return trunks

    def _get_trunk_status(self, fac, name, q, lock):
        """
        Gives status of a trunk
        """
        # Create search item to look for the phone
        item = fac.create('SelectItem')
        item.Item = name

        # Define the Search criteria
        sc = fac.create('CmSelectionCriteria')
        sc.MaxReturnedDevices = 1
        sc.DeviceClass = 'Any'
        sc.Model = 255
        sc.Status = 'Any'
        sc.SelectBy = 'Name'
        sc.SelectItems.item.append(item)
        sc.DownloadStatus = 'Any'
        sc.Protocol = 'Any'

        # Obtain the node
        service = self.cucm.soap.serviceability.service
        try:
            trunk = service.selectCmDevice(CmSelectionCriteria=sc)
        except:
            pass
        q.put([name, self._parse_trunk_status(trunk)])

    def _parse_trunk_status(self, trunk):
        """
        Parse phone status returned from CUCM
        """
        try:
            num_trunks = trunk.SelectCmDeviceResult.TotalDevicesFound
            if num_trunks == 0:
                return None

            cmNodes = trunk.SelectCmDeviceResult.CmNodes
            devices = []
            for cmDevices in cmNodes.item:
                if cmDevices.CmDevices is not None:
                    devices.append(cmDevices.CmDevices)
            for device in devices:
                status = device.item[0].Status
        except:
            pass
        try:
            status
        except NameError:
            status = 'Rejected'

        if status == 'Registered':
            status = 'Up'
        if status == 'Rejected':
            status = 'Unknown'
        elif status == 'Unknown':
            status = 'Down'
        elif status == 'UnRegistered':
            status = 'Partial Service'
        return status
