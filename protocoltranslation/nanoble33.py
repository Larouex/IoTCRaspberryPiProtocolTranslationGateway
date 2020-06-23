# ==================================================================================
#   File:   nanoble33.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Models the Device Capabilities of the Nano BLE 33.
#   Git:    https://github.com/Larouex/IoTCNanoBLE33
#
#   Legend: R: Read, W: Write, N: Notify
#   ------------------------------------
#   VERSION             (RW)
#   BATTERY CHARGED     (R)
#   TELEMETRY FREQUENCY (RW)
#   ACCELEROMETER       (RN)
#   GYROSCOPE           (RN)
#   MAGNETOMETER        (RN)
#   ORIENTATION         (RN)
#   RGB LED         (RN)
#
#   Online:   www.hackinmakin.com
#
#   (c) 2020 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)    
# ==================================================================================
import logging

class Nano33BLE():

    def __init__(self, logger):
        self.logger = logger
        self.data = []
