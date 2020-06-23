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

# uses the Azure IoT Device SDK for Python (Native Python libraries)
from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
from azure.iot.device import MethodResponse

# our classes
from classes.config import Config
from classes.dpscache import DpsCache
from classes.symmetrickey import SymmetricKey

reg_id = "d-001"
symmetric_key = "l7r52wdv4jEbSU2QCOYz/vfea5cTSKMv48uA9QlB8rP6H0pvS0bI7M9YEU3ZwurvQeBh3oWIGYTjfHutiZXnDg=="

sas = SymmetricKey(logging.getLogger())
config = Config(logging.getLogger())
dpscache = DpsCache(logging.getLogger())

asymmetric_key = sas.compute_derived_symmetric_key(reg_id, symmetric_key)
print(asymmetric_key)
print(config.data)
print(dpscache.data)
