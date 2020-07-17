
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
import  bluetooth, hmac, getopt, sys, time, binascii, \
        struct, string, threading, asyncio, os

import logging as Log

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
from protocoltranslation.nanoble33sense import NanoBle33Sense
from classes.config import Config

# Workers
config_data = None

# -------------------------------------------------------------------------------
#   Provision Devices
# -------------------------------------------------------------------------------
async def provision_devices(ResetHCI, BluetoothInterface, ScanSeconds):

  provisiondevices = ProvisionDevices(Log, ProvisioningScope="NEW")
  await provisiondevices.provision_devices()
  return True

# -------------------------------------------------------------------------------
#   Scan Devices
# -------------------------------------------------------------------------------
async def scan_devices(ResetHCI, BluetoothInterface, ScanSeconds):
  if not 'SUDO_UID' in os.environ.keys():
    print("[ERROR][STOPPED] Scanning Devices requires Super User Priveleges")
    sys.exit(1)

  scandevices = ScanDevices(Log, BluetoothInterface, ScanSeconds)
  await scandevices.scan_for_devices(resethci=ResetHCI)
  return True

# -------------------------------------------------------------------------------
#   Read Data
# -------------------------------------------------------------------------------
async def read_data():

  provisiondevices = ProvisionDevices()
  await provisiondevices.discover_and_provision_devices()
  return True

async def main(argv):

    # execution state from args
    is_provisiondevices = False
    is_scandevices = False
    is_resethci = False

    short_options = "hvpsr"
    long_options = ["help", "verbose", "provisiondevices", "scandevices", "resethci"]
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print (str(err))
        #sys.exit(2)
    
    for current_argument, current_value in arguments:
        if current_argument in ("-v", "--verbose"):
            Log.basicConfig(format="%(levelname)s: %(message)s", level=Log.DEBUG)
            Log.info("Verbose mode...")
        else:
            Log.basicConfig(format="%(levelname)s: %(message)s")
        
        if current_argument in ("-p", "--provisiondevices"):
            Log.info("Provision Devices mode...")
            is_provisiondevices = True
        
        if current_argument in ("-s", "--scandevices"):
            Log.info("Scan Devices mode...")
            is_scandevices = True

        if current_argument in ("-r", "--resethci"):
            Log.info("Bluetooth Reset Interface mode...")
            is_resethci = True
    
    # Load Configuration File
    config = Config(Log)
    config_data = config.data

    if (is_scandevices):
      await scan_devices(is_resethci, config_data["BluetoothInterface"], config_data["ScanSeconds"])

    elif (is_provisiondevices):
      await provision_devices(is_resethci, config_data["BluetoothInterface"], config_data["ScanSeconds"])


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))

