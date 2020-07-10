
# ==================================================================================
#   File:   provisiondevices.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Provisions Devices and updates cache file and do device provisioning 
#           via DPS for IoT Central
#
#   Online: www.hackinmakin.com
#
#   (c) 2020 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)    
# ==================================================================================
import time, logging, string, json, os, binascii, struct, threading
from bluepy.btle import Scanner, DefaultDelegate, Peripheral
from classes.getdevicecapabilitymodel import GetDeviceCapabilityModel
from classes.devicescache import DevicesCache
from classes.secrets import Secrets
from classes.nanobleservices import NanoBLEServices
from azure.keyvault.certificates import CertificateClient, CertificatePolicy,CertificateContentType, WellKnownIssuerNames 
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.keyvault.keys import KeyClient
from azure.identity import ClientSecretCredential
from classes.symmetrickey import SymmetricKey

# -------------------------------------------------------------------------------
#   Delegate Class to Handle Discovered Devices
# -------------------------------------------------------------------------------
class ScanDelegate(DefaultDelegate):
    
    def __init__(self):
        DefaultDelegate.__init__(self)

    def HandleDiscovery(self,dev,new_dev,new_dat):
        if new_dev:
            pass
        if new_dat:
            pass

# -------------------------------------------------------------------------------
#   ProvisionDevices Class
# -------------------------------------------------------------------------------
class ProvisionDevices():

    timer = None
    timer_ran = False
    dcm_value = None

    def __init__(self):
        self.logger = logging.getLogger()
        self.data = []
        self.new_devices = []
        self.characteristics = []
    
    def get_device_dcm(self, uuid, peripheral):

        timer = None
        global dcm_value

        # now let's query the Device for it's assigned IoT Central DCM
        # (Device Capability Model) and this will assign the device to the proper
        # template for telemetry, properties, views etc.
        dcm = peripheral.getCharacteristics(uuid=uuid)[0]
        print("[DCM] %s" % dcm)
        if (dcm.supportsRead()):
            print("Supports: {supports}".format(supports = dcm.propertiesToString()))
            val = binascii.b2a_hex(dcm.read())
            val = binascii.unhexlify(val)
            dcm_value = struct.unpack('s', val)[0]
            print("[DCM FROM DEVICE] %s" % dcm_value)
        timer_ran = True
        return 

    def discover_and_provision_devices(self):

        # Write flag
        new_devices_discovered = False

        # Load the Devices Cache File for any devices
        # that have already been provisioned
        devicescache = DevicesCache(self.logger)
        
        # Make a working copy of the cache file
        self.data = devicescache.data
        #print(self.data)

        # Scan the BLE's that are Advertising
        print("Please Wait: Scanning for BLE Devices Advertising...(10 Seconds)" )
        scanner = Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(10.0)

        # Check the devices and add the ones that match the pattern indicated in
        # the devicescache.json file element [DeviceNamePrefix]...
        for device in devices:
          devicename = str(device.getValueText(9))
          if [x for x in self.data["Devices"] if x.get("Address")==device.addr]:
            print("[ALREADY PROVISIONED, SKIPPING] %s" % devicename)
          else:
            if devicename.startswith(self.data["DeviceNamePrefix"]):
              new_devices_discovered = True
              print("[FOUND NEW DEVICE] %s" % (devicename))
              
              newDevice = {
                  "DeviceName": devicename, 
                  "Address": str(device.addr), 
                  "LastRSSI": "%s dB" % str(device.rssi)
                } 
              
              # Merge the Data with the New Devices, this is the
              # one we commit to the devicescache.json when completed  
              self.data["Devices"].append(newDevice)

              # working list of just the new devices in this session
              self.new_devices.append(newDevice)

            else:
              #print("NOT")
              pass
        
        if new_devices_discovered:
          # load the Services and Characteristic Maps
          service_characteristics = NanoBLEServices(self.logger)
          self.characteristics = service_characteristics.data
          print("[service_characteristics] %s" % service_characteristics)

          # load the secrets
          secrets = Secrets(self.logger)
          if secrets.data["KeyVaultSecrets"]:
            key_vault_uri = secrets.data["KeyVaultSecrets"]["KeyVaultUri"]
            tenant_id = secrets.data["KeyVaultSecrets"]["TenantId"]
            client_id = secrets.data["KeyVaultSecrets"]["ClientId"]
            client_secret = secrets.data["KeyVaultSecrets"]["ClientSecret"]
            print("[KEY VAULT URI] %s" % key_vault_uri)
            
            # Get access to Key Vault Secrets
            credential = ClientSecretCredential(tenant_id, client_id, client_secret)
            print("[credential] %s" % credential)
            secret_client = SecretClient(vault_url=key_vault_uri, credential=credential)
            print("[secret_client] %s" % secret_client)

            # Read alll of our Secrets for Accessing IoT Central
            scope_id = secret_client.get_secret(secrets.data["KeyVaultSecrets"]["ScopeId"])
            device_primary_key = secret_client.get_secret(secrets.data["KeyVaultSecrets"]["DeviceConnect"]["SaSKeys"]["Primary"])
            device_secondary_key = secret_client.get_secret(secrets.data["KeyVaultSecrets"]["DeviceConnect"]["SaSKeys"]["Secondary"])
            gateway_primary_key = secret_client.get_secret(secrets.data["KeyVaultSecrets"]["GatewayConnect"]["SaSKeys"]["Primary"])
            gateway_secondary_key = secret_client.get_secret(secrets.data["KeyVaultSecrets"]["GatewayConnect"]["SaSKeys"]["Secondary"])
            
            print("[SCOPE ID]: %s" % scope_id.value)
            print("[DEVICE PRIMARY KEY]: %s" % device_primary_key.value)
            print("[DEVICE SECONDARY KEY]: %s" % device_secondary_key.value)
            print("[GATEWAY PRIMARY KEY]: %s" % gateway_primary_key.value)
            print("[GATEWAY SECONDARY KEY]: %s" % gateway_secondary_key.value)

            # Symetric Key for handling Device Specific SaS Keys
            symmetrickey = SymmetricKey(self.logger)

            for device in self.new_devices: 
              # Get the Device Name
              device_name = device["DeviceName"]
              print("[PROVISIONING] %s" % device_name)
              
              # Get a Device Specific Symetric Key
              device_symmetrickey = symmetrickey.compute_derived_symmetric_key(device["DeviceName"], device_secondary_key.value)
              print("[SYMETRIC KEY] %s" % device_symmetrickey)

              # Pluck the details on the DCM characteristic
              dcm_characteristic = [x for x in self.characteristics["Characteristics"] if x.get("Name")=="DCM_CHARACTERISTIC"]
              print("[DCM_CHARACTERISTIC] %s" % dcm_characteristic[0])
              print("[DCM_CHARACTERISTIC UUID] %s" % dcm_characteristic[0]["UUID"])

              get_dcm = GetDeviceCapabilityModel()
              dcm_value = get_dcm.get_device_dcm(device["Address"], dcm_characteristic[0]["UUID"])

              print("[DCM] %s" % dcm_value)
      
            # Update the Cache
            devicescache.update_file(self.data)
          else:
            print("[USING LOCAL SECRETS]")
            pass
        
        #print(self.data)

        pass
