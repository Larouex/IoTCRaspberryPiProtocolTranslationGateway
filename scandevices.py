# ==================================================================================
#   File:   scandevices.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Raspberry Pi "Protocol Translation" Gateway for Azure IoT Central
#           This module scans for devices and updates the devicescache. We run
#           it seperate as it is SUDO and we do not want to install our packages
#           tec under sudo
#
#   Online:   www.hackinmakin.com
#
#   (c) 2020 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)    
# ==================================================================================
import  getopt, sys, time, string, threading, asyncio, os
import logging as Log

# our classes
from classes.scandevices import ScanDevices
from classes.config import Config

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

async def main(argv):

    # execution state from args
    is_resethci = False

    short_options = "hvr"
    long_options = ["help", "verbose", "resethci"]
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
        
        if current_argument in ("-r", "--resethci"):
            Log.info("Bluetooth Reset Interface mode...")
            is_resethci = True
    
    # Load Configuration File
    config = Config(Log)
    config_data = config.data

    await scan_devices(is_resethci, config_data["BluetoothInterface"], config_data["ScanSeconds"])

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))

