# ==================================================================================
#   File:   gateway.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Raspberry Pi "Protocol Translation" Gateway for Azure IoT Central
#
#   Online:   www.hackinmakin.com
#
#   (c) 2020 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)    
# ==================================================================================
import  logging, bluetooth, hmac, getopt, sys, time, binascii, \
        struct, string, threading, asyncio, os

# bluepy - Bluetooth LE interface for Python
from bluepy.btle import Scanner, DefaultDelegate
    
# uses the Azure IoT Device SDK for Python (Native Python libraries)
from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
from azure.iot.device import MethodResponse

# our classes
from classes.provisiondevices import ProvisionDevices
from classes.config import Config
from classes.dpscache import DpsCache
from classes.symmetrickey import SymmetricKey
from classes.nanobleservices import NanoBLEServices
from protocoltranslation.nanoble33sense import onAccelerometerNotification

peripheral = None
timer = None

# -------------------------------------------------------------------------------
#   Provision Devices, must be run using SUDO
# -------------------------------------------------------------------------------
def provision_devices():
  if not 'SUDO_UID' in os.environ.keys():
    print("[ERROR][STOPPED] Provisioning Devices requires Super User Priveleges")
    sys.exit(1)

  provisiondevices = ProvisionDevices()
  provisiondevices.discover_and_provision_devices()
  return True

def gather():

    global timer
    timer = None

    #for service in dev.getServices():
    #  print(service)
    #  for characteristic in service.getCharacteristics():
    #    print("Characteristic - id: %s\tname (if exists): %s\tavailable methods: %s" % (str(characteristic.uuid), str(characteristic), characteristic.propertiesToString()))


    t = peripheral.getCharacteristics(uuid="1101")[0]
    print(t)
    if (t.supportsRead()):
        print("Supports: {supports}".format(supports = t.propertiesToString()))
        val = binascii.b2a_hex(t.read())
        val = binascii.unhexlify(val)
        val = struct.unpack('f', val)[0]
        print("Temperature: {temp:.2f}".format(temp = val))

    h = peripheral.getCharacteristics(uuid="1201")[0]
    print(h)
    if (h.supportsRead()):
        print("Supports: {supports}".format(supports = h.propertiesToString()))
        val = binascii.b2a_hex(h.read())
        val = binascii.unhexlify(val)
        val = struct.unpack('f', val)[0]
        print("Humidity: {humidity:.2f}".format(humidity = val))


    peripheral.setDelegate( onAccelerometerNotification(logging.getLogger()) )
    a = peripheral.getCharacteristics(uuid="4001")[0]
    #a.write( setup_data )

    while True:
      if a.waitForNotifications():
        continue
        print("Waiting...")

    peripheral.disconnect()

def search():         
    devices = bluetooth.discover_devices(duration=20, lookup_names = True)
    return devices

def find_service(_device_name, _service_uuid, _characteristic_uuid):
    print("Device Name: " + _device_name)
    print("Service UUID: " + _service_uuid)
    print("Characteristic UUID: " + _characteristic_uuid)
    #service = bluetooth.find_service( name = _device_name, uuid = _service_uuid )
    service = bluetooth.find_service(address = "C7:94:90:1C:8F:3C" )
    
    if service:
      self.port = service[0]["port"]
      self.host = service[0]["host"]
      return 1
    else:
        return 0

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)


def main(argv):

    short_options = "hvp"
    long_options = ["help", "verify", "provisiondevices"]
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print (str(err))
        #sys.exit(2)
    for current_argument, current_value in arguments:
        if current_argument in ("-v", "--verify"):
            print ("Verification mode...")
        
        if current_argument in ("-p", "--provisiondevices"):
            print ("Provision Devices mode...")
            provision_devices()




if __name__ == "__main__":
    main(sys.argv[1:])
    #timer = threading.Timer(15.0, gather)
    #timer.start()
