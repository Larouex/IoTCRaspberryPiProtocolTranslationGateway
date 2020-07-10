
# ==================================================================================
#   File:   getdevicecapabilitymodel.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Creates a Connection to the Nano BLE Device and Reads the 
#           Device Capability Model to send via DPS for IoT Central
#           Association to the Device Template
#
#   Online: www.hackinmakin.com
#
#   (c) 2020 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)    
# ==================================================================================
import time, logging, string, json, os, binascii, struct, threading
from bluepy.btle import Peripheral

# -------------------------------------------------------------------------------
#   GetDeviceCapabilityModel Class
# -------------------------------------------------------------------------------
class GetDeviceCapabilityModel():

    timer = None
    timer_ran = False
    peripheral = None
    uuid = None
    dcm_value = None

    def __init__(self):
        self.logger = logging.getLogger()
    
    def connect_device_dcm(self):
        timer = None
        global dcm_value

        # now let's query the Device for it's assigned IoT Central DCM
        # (Device Capability Model) and this will assign the device to the proper
        # template for telemetry, properties, views etc.
        dcm = peripheral.getCharacteristics(uuid=uuid)[0]
        print("[DCM] %s" % dcm)
        if (dcm.supportsRead()):
            print("Supports: {supports}".format(supports = dcm.propertiesToString()))
            val = binascii.b2a_hex(dcm.read())
            val = binascii.unhexlify(val)
            dcm_value = struct.unpack('s', val)[0]
            print("[DCM FROM DEVICE] %s" % dcm_value)
        timer_ran = True
        return 
    
    def get_device_dcm(self, passed_addr, passed_uuid):
        global peripheral, uuid
        
        uuid = passed_uuid
        peripheral = Peripheral(passed_addr)

        timer = threading.Timer(15.0, self.connect_device_dcm)
        timer.start()
              
        global timer_ran
        timer_ran = False

        while timer_ran == False:
            continue

        return dcm_value

