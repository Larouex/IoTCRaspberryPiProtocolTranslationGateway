# ==================================================================================
#   File:   provisiondevices.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Provisions Devices and updates cache file and do device provisioning 
#           via DPS for IoT Central
#
#   Online: www.hackinmakin.com
#
#   (c) 2020 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)    
# ==================================================================================
import time, logging, string, json, os
from bluepy.btle import Scanner, DefaultDelegate
from classes.devicescache import DevicesCache
from azure.keyvault.certificates import CertificateClient, CertificatePolicy,CertificateContentType, WellKnownIssuerNames 
from azure.identity import DefaultAzureCredential

# -------------------------------------------------------------------------------
#   Delegate Class to Handle Discovered Devices
# -------------------------------------------------------------------------------
class ScanDelegate(DefaultDelegate):
    
    def __init__(self):
        DefaultDelegate.__init__(self)

    def HandleDiscovery(self,dev,new_dev,new_dat):
        if new_dev:
            pass
        if new_dat:
            pass

# -------------------------------------------------------------------------------
#   ProvisionDevices Class
# -------------------------------------------------------------------------------
class ProvisionDevices():

    def __init__(self):
        self.logger = logging.getLogger()
        self.data = []
    
    def discover_and_provision_devices(self):

        # Write flag
        new_devices_discovered = False

        # Load the Devices Cache File for any devices
        # that have already been provisioned
        devicescache = DevicesCache(self.logger)
        
        # Make a working copy of the cache file
        self.data = devicescache.data
        #print(self.data)

        # Scan the BLE's that are Advertising
        print("Please Wait: Scanning for BLE Devices Advertising...(10 Seconds)" )
        scanner = Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(10.0)

        # Check the devices and add the ones that match the pattern indicated in
        # the devicescache.json file element [DeviceNamePrefix]...
        for device in devices:
          devicename = str(device.getValueText(9))
          if [x for x in self.data["Devices"] if x.get("Address")==device.addr]:
            print("[ALREADY PROVISIONED, SKIPPING] %s" % devicename)
          else:
            if devicename.startswith(self.data["DeviceNamePrefix"]):
              new_devices_discovered = True
              print("[FOUND NEW DEVICE, PROVISIONING] %s" % (devicename))
              newDevice = {
                  "DeviceName": devicename, 
                  "Address": str(device.addr), 
                  "LastRSSI": "%s dB" % str(device.rssi)
                } 
              self.data["Devices"].append(newDevice)
            else:
              #print("NOT")
              pass
        
        if new_devices_discovered:
          devicescache.update_file(self.data)
        
        #print(self.data)

        pass
