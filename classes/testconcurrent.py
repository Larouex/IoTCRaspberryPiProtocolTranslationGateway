import struct, time
from bluepy.btle import *


class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print(data)

p = Peripheral(None)
p.connect("c7:94:90:1c:8f:3c","public",1)
p.setDelegate(MyDelegate())
print("Connected")
time.sleep(10)

ble_service = p.getServiceByUUID("6F165338-0001-43B9-837B-41B1A3C86EC1")
data_chrc = ble_service.getCharacteristics("1101")[0]

data_chrc.write(bytes("\x01")) 
time.sleep(1.0)


try:
    while True:
        if p.waitForNotifications(1.0):
            print("Notification")
            continue
    print("Waiting")
finally:
    p.disconnect()
    print ("Disconnected")
    
    