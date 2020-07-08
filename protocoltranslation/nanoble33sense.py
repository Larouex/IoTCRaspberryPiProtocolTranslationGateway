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
import logging
import bluetooth
import hmac
import getopt
import sys
import time
import binascii
import struct
import string

# bluepy - Bluetooth LE interface for Python
from bluepy import btle

class NanoBLE33SENSE():

    def __init__(self, logger):
        self.logger = logger
        self.data = []

# -----------------------------------------------------------------------------------
# Delegate: onTelemetryFrequencyCharacteristicWrite
# -----------------------------------------------------------------------------------
class onTelemetryFrequencyCharacteristicWrite(btle.DefaultDelegate):

    def __init__(self, params, logger):
        btle.DefaultDelegate.__init__(self)
        self.logger = logger
        self.data = []

    def handleNotification(self, cHandle, data):
        pass

# -----------------------------------------------------------------------------------
# Delegate: onAccelerometerNotification
# -----------------------------------------------------------------------------------
class onAccelerometerNotification(btle.DefaultDelegate):

    def __init__(self, logger):
        btle.DefaultDelegate.__init__(self)
        self.logger = logger
        self.data = []

    def handleNotification(self, cHandle, data):
        print(data)

# -----------------------------------------------------------------------------------
# Delegate: onGyroscopeNotification
# -----------------------------------------------------------------------------------
class onGyroscopeNotification(btle.DefaultDelegate):

    def __init__(self, params, logger):
        btle.DefaultDelegate.__init__(self)
        self.logger = logger
        self.data = []

    def handleNotification(self, cHandle, data):
        pass

# -----------------------------------------------------------------------------------
# Delegate: onMagnetometerNotification
# -----------------------------------------------------------------------------------
class onMagnetometerNotification(btle.DefaultDelegate):

    def __init__(self, params, logger):
        btle.DefaultDelegate.__init__(self)
        self.logger = logger
        self.data = []

    def handleNotification(self, cHandle, data):
        pass

# -----------------------------------------------------------------------------------
# Delegate: onOrientationNotification
# -----------------------------------------------------------------------------------
class onOrientationNotification(btle.DefaultDelegate):

    def __init__(self, params, logger):
        btle.DefaultDelegate.__init__(self)
        self.logger = logger
        self.data = []

    def handleNotification(self, cHandle, data):
        pass

# -----------------------------------------------------------------------------------
# Delegate: onRgbLedCharacteristicWrite
# -----------------------------------------------------------------------------------
class onRgbLedCharacteristicWrite(btle.DefaultDelegate):

    def __init__(self, params, logger):
        btle.DefaultDelegate.__init__(self)
        self.logger = logger
        self.data = []

    def handleNotification(self, cHandle, data):
        pass


# -----------------------------------------------------------------------------------
# Delegate: onBarometerCharacteristicRead
# -----------------------------------------------------------------------------------
class onBarometerCharacteristicRead(btle.DefaultDelegate):

    def __init__(self, params, logger):
        btle.DefaultDelegate.__init__(self)
        self.logger = logger
        self.data = []

    def handleNotification(self, cHandle, data):
        pass

# -----------------------------------------------------------------------------------
# Delegate: onTemperatureCharacteristicRead
# -----------------------------------------------------------------------------------
class onTemperatureCharacteristicRead(btle.DefaultDelegate):

    def __init__(self, params, logger):
        btle.DefaultDelegate.__init__(self)
        self.logger = logger
        self.data = []

    def handleNotification(self, cHandle, data):
        pass

# -----------------------------------------------------------------------------------
# Delegate: onHumidityCharacteristicRead
# -----------------------------------------------------------------------------------
class onHumidityCharacteristicRead(btle.DefaultDelegate):

    def __init__(self, params, logger):
        btle.DefaultDelegate.__init__(self)
        self.logger = logger
        self.data = []

    def handleNotification(self, cHandle, data):
        pass

# -----------------------------------------------------------------------------------
# Delegate: onMicrophoneNotification
# -----------------------------------------------------------------------------------
class onMicrophoneNotification(btle.DefaultDelegate):

    def __init__(self, params, logger):
        btle.DefaultDelegate.__init__(self)
        self.logger = logger
        self.data = []

    def handleNotification(self, cHandle, data):
        pass

# -----------------------------------------------------------------------------------
# Delegate: onAmbientLightNotification
# -----------------------------------------------------------------------------------
class onAmbientLightNotification(btle.DefaultDelegate):

    def __init__(self, params, logger):
        btle.DefaultDelegate.__init__(self)
        self.logger = logger
        self.data = []

    def handleNotification(self, cHandle, data):
        pass

# -----------------------------------------------------------------------------------
# Delegate: onColorNotification
# -----------------------------------------------------------------------------------
class onColorNotification(btle.DefaultDelegate):

    def __init__(self, params, logger):
        btle.DefaultDelegate.__init__(self)
        self.logger = logger
        self.data = []

    def handleNotification(self, cHandle, data):
        pass

# -----------------------------------------------------------------------------------
# Delegate: onProximityNotification
# -----------------------------------------------------------------------------------
class onProximityNotification(btle.DefaultDelegate):

    def __init__(self, params, logger):
        btle.DefaultDelegate.__init__(self)
        self.logger = logger
        self.data = []

    def handleNotification(self, cHandle, data):
        pass

# -----------------------------------------------------------------------------------
# Delegate: onGestureNotification
# -----------------------------------------------------------------------------------
class onGestureNotification(btle.DefaultDelegate):

    def __init__(self, params, logger):
        btle.DefaultDelegate.__init__(self)
        self.logger = logger
        self.data = []

    def handleNotification(self, cHandle, data):
        pass

# -----------------------------------------------------------------------------------
# Delegate: onGestureNotification
# -----------------------------------------------------------------------------------
class onGestureNotification(btle.DefaultDelegate):

    def __init__(self, params, logger):
        btle.DefaultDelegate.__init__(self)
        self.logger = logger
        self.data = []

    def handleNotification(self, cHandle, data):
        pass
