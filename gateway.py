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
import logging
import bluetooth
import hmac
import getopt
import sys

# uses the Azure IoT Device SDK for Python (Native Python libraries)
from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
from azure.iot.device import MethodResponse

# our classes
from classes.config import Config
from classes.dpscache import DpsCache
from classes.symmetrickey import SymmetricKey

def main(argv):
    short_options = "hv"
    long_options = ["help", "verify"]
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print (str(err))
        sys.exit(2)
    for current_argument, current_value in arguments:
        if current_argument in ("-v", "--verify"):
            print ("Verificatioon mode...")
            #reg_id = "d-001"
            #symmetric_key = ""
            #sas = SymmetricKey(logging.getLogger())
            config = Config(logging.getLogger())
            dpscache = DpsCache(logging.getLogger())
            #asymmetric_key = sas.compute_derived_symmetric_key(reg_id, symmetric_key)
            #print(asymmetric_key)
            print(config.data)
            print(dpscache.data)

if __name__ == "__main__":
   main(sys.argv[1:])

