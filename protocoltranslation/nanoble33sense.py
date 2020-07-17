# ==================================================================================
#   File:   NanoBLE33SENSE.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Models the Device Capabilities of the Nano BLE 33 SENSE.
#   Git:    https://github.com/Larouex/IoTCNanoBLESense33
#
#   Legend: R: Read, W: Write, N: Notify I: Indicate
#   ------------------------------------------------
#   VERSION             (RW)
#   BATTERY CHARGED     (RNI)
#   TELEMETRY FREQUENCY (RWNI)
#   ACCELEROMETER       (N)
#   GYROSCOPE           (N)
#   MAGNETOMETER        (N)
#   ORIENTATION         (N)
#   RGB LED             (RW)
#   BAROMETER           (RW)
#   TEMPERATURE         (RW)
#   HUMIDITY            (RW)
#   MICROPHONE          (RW)
#   AMBIENTLIGHT        (RW)
#   COLOR               (RW)
#   PROXIMITY           (RW)
#   GESTURE             (RW)
#
#   Online:   www.hackinmakin.com
#
#   (c) 2020 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)    
# ==================================================================================
import  bluetooth, hmac, sys, time, binascii, \
        struct, string, threading, asyncio, os

import logging as Log

# bluepy - Bluetooth LE interface for Python
from bluepy.btle import UUID, Peripheral

class NanoBle33Sense():

    def __init__(self, Log, Address):
        self.logger = Log
        self.data = []

        # Set the Peripheral
        self.addr = Address
        self.peripheral = Peripheral(Address, "public")

        # Load the Charateristics
        service_characteristics = NanoBLEServices(self.logger)
        self.characteristics = service_characteristics.data["larouex-ble-sense-"]

    def __del__(self):
        self.peripheral.disconnect()

    # -----------------------------------------------------------------------------------
    # Function: ReadTemperature
    # -----------------------------------------------------------------------------------
    def ReadTemperature(self):
        uuid = [x for x in self.characteristics["Characteristics"] if x.get("Name")=="TEMPERATURE_CHARACTERISTIC"]
        print(uuid)
        pass

    # -----------------------------------------------------------------------------------
    # Function: ReadHumidity
    # -----------------------------------------------------------------------------------
    def ReadHumidity():

        h = peripheral.getCharacteristics(uuid="1201")[0]
        if (h.supportsRead()):
            self.logger.info("Supports: {supports}".format(supports = h.propertiesToString()))
            val = binascii.b2a_hex(h.read())
            val = binascii.unhexlify(val)
            val = struct.unpack('f', val)[0]
            self.logger.info("Humidity: {humidity:.2f}".format(humidity = val))
        
        pass
