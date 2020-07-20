# ==================================================================================
#   File:   provisiondevices.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Raspberry Pi "Protocol Translation" Gateway for Azure IoT Central
#           This module provisions devices and updates the devicescache. 
#           It either re-provisions all devices or just those that have null in
#           LastProvisioned option in the file i.e "LastProvisioned": null
#
#   Online:   www.hackinmakin.com
#
#   (c) 2020 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)    
# ==================================================================================
import  getopt, sys, time, string, threading, asyncio, os
import logging as Log

# our classes
from classes.provisiondevices import ProvisionDevices
from classes.config import Config

# -------------------------------------------------------------------------------
#   Provision Devices
# -------------------------------------------------------------------------------
async def provision_devices(BluetoothInterface, ResetHCI, ScanSeconds):

  scanfordevices = ScanForDevices(Log, BluetoothInterface, ResetHCI, ScanSeconds)
  await scanfordevices.scan_for_devices()
  return True

async def main(argv):

    # execution state from args
    reprovision_all_devices = None

    short_options = "hva"
    long_options = ["help", "verbose", "all"]
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print (str(err))
    
    for current_argument, current_value in arguments:
        if current_argument in ("-h", "--help"):
            print("HELP for provisiondevices.py")
            print("------------------------------------------------------------------------------------------------------------------")
            print("-h or --help - Print out this Help Information")
            print("-v or --verbose - Debug Mode with lots of Data will be Output to Assist with Debugging")
            print("-a or --all - Re-Provision all Devices with IoT Central (default=LastProvisioned(null))")
            print("------------------------------------------------------------------------------------------------------------------")
            sys.exit()

        if current_argument in ("-v", "--verbose"):
            Log.basicConfig(format="%(levelname)s: %(message)s", level=Log.DEBUG)
            Log.info("Verbose mode...")
        else:
            Log.basicConfig(format="%(levelname)s: %(message)s")
        
        if current_argument in ("-a", "--all"):
            Log.info("Re-Provision All Devices mode...")
            is_resethci = True
        
    # Load Configuration File
    config = Config(Log)
    config_data = config.data
    
    if reprovision_all_devices == None:
      reprovision_all_devices = config_data["ReprovisionAllDevices"]

    await scan_for_devices(BluetoothInterface=bluetooth_interface, ResetHCI=is_resethci, ScanSeconds=scan_seconds)

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))

