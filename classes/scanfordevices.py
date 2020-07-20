# ==================================================================================
#   File:   scanfordevices.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Scans for BLW Devices and updates the cache file
#
#   Online: www.hackinmakin.com
#
#   (c) 2020 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)    
# ==================================================================================
import time, logging, string, json, os, binascii, struct, threading, asyncio
from bluepy.btle import Scanner, DefaultDelegate, Peripheral
from classes.devicescache import DevicesCache

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
#   ScanDevices Class
# -------------------------------------------------------------------------------
class ScanForDevices():

    timer = None
    timer_ran = False
    dcm_value = None

    def __init__(self, Log, IFace, ResetHCI, ScanSeconds):
        self.logger = Log
        self.data = []
        self.new_devices = []
        self.characteristics = []
        self.iface = IFace
        self.resethci = ResetHCI
        self.scan_seconds = ScanSeconds
  
    async def scan_for_devices(self):

        self.logger.info("resethci: %s" % str(self.resethci))
        self.logger.info("Bluetooth Interface: %s" % str(self.iface))

        # Write flag
        new_devices_discovered = False

        # Load the Devices Cache File for any devices
        # that have already been provisioned
        devicescache = DevicesCache(self.logger)
        
        # Make a working copy of the cache file
        self.data = devicescache.data

        if self.resethci:
            try:
                self.logger.info("hciconfig down..." )
                os.system("sudo hciconfig hci%s down" % self.iface)
                self.logger.info("hciconfig up..." )
                os.system("sudo hciconfig hci%s up" % self.iface)
            except:
                self.logger.warning("We encountered an error executing OS command hciconfig" )

        try:
            # Scan the BLE's that are Advertising
            self.logger.warning("Please Wait: Scanning for BLE Devices Advertising...(%s Seconds)" % self.scan_seconds)
            scanner = Scanner(self.iface).withDelegate(ScanDelegate())
            devices = scanner.scan(float(self.scan_seconds))

            # Check the devices and add the ones that match the pattern indicated in
            # the devicescache.json file element [DeviceNamePrefix]...
            for device in devices:
              devicename = str(device.getValueText(9))
              if [x for x in self.data["Devices"] if x.get("Address")==device.addr]:
                self.logger.warning("[ALREADY DISCOVERED, SKIPPING] %s" % devicename)
              else:
                
                # Check our Pattern for Matching Names
                new_device = False
                dcm_for_device = None
                for name_dcm in self.data["DeviceCapabilityModels"]:
                  if devicename.startswith(name_dcm["DeviceNamePrefix"]):
                    self.logger.warning("[FOUND NEW DEVICE] %s" % devicename)
                    new_device = True
                
                if new_device:
                  new_devices_discovered = True
                  
                  newDevice = {
                      "DeviceName": devicename, 
                      "Address": str(device.addr), 
                      "LastRSSI": "%s dB" % str(device.rssi),
                      "DCM": name_dcm["DCM"],
                      "DeviceInfoInterface": name_dcm["DeviceInfoInterface"],
                      "DeviceInfoInterfaceInstanceName": name_dcm["DeviceInfoInterfaceInstanceName"],
                      "NanoBLEInterface": name_dcm["NanoBLEInterface"],
                      "NanoBLEInterfaceInstanceName": name_dcm["NanoBLEInterfaceInstanceName"],
                      "LastProvisioned": None
                    } 
                  
                  # Associate the IoTC Device Template
                  self.logger.info("[NEW DEVICE INFO] %s" % newDevice)
                  
                  # Merge the Data with the New Devices, this is the
                  # one we commit to the devicescache.json when completed  
                  self.data["Devices"].append(newDevice)

                  # working list of just the new devices in this session
                  self.new_devices.append(newDevice)

                else:
                  pass
        except Exception as ex:
            self.logger.error("[ERROR] %s" % ex)
            self.logger.error("[TERMINATING] We encountered an error scanning for BLE Devices" )
            return

        if new_devices_discovered:
          # Update the Cache
          devicescache.update_file(self.data)
          return
