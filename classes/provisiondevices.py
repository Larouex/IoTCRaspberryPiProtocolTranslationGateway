
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
import time, logging, string, json, os, binascii, struct, threading, asyncio
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

# uses the Azure IoT Device SDK for Python (Native Python libraries)
from azure.iot.device.aio import ProvisioningDeviceClient

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
  
    async def discover_and_provision_devices(self):

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
              print("[FOUND NEW DEVICE] %s" % devicename)
              
              # Associate the IoTC Device Template
              dcm_for_device = None
              for deviceCapabilityModel in self.data["DeviceCapabilityModels"]:
                print("[DEVICE PREFEIX] %s" % self.data["DeviceNamePrefix"] + deviceCapabilityModel["Name"])
                if devicename.startswith(self.data["DeviceNamePrefix"] + deviceCapabilityModel["Name"]):
                  dcm_for_device = deviceCapabilityModel["DCM"]
                  print("[DEVICE DCM] %s" % dcm_for_device)
              
              newDevice = {
                  "DeviceName": devicename, 
                  "Address": str(device.addr), 
                  "LastRSSI": "%s dB" % str(device.rssi),
                  "DCM": dcm_for_device
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
              
              # Get a Device Specific Symetric Key
              device_symmetrickey = symmetrickey.compute_derived_symmetric_key(device["DeviceName"], device_secondary_key.value)
              print("[SYMETRIC KEY] %s" % device_symmetrickey)

              print("[PROVISIONING] %s" % device_name)

              # Provision the Device
              provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
                provisioning_host=secrets.data["ProvisioningHost"],
                registration_id=device["DeviceName"],
                id_scope=scope_id.value,
                symmetric_key=device_symmetrickey,
                websockets=True
              )

              provisioning_device_client.provisioning_payload = '{"iotcModelId":"%s"}' % (device["DCM"])
              registration_result = await provisioning_device_client.register()
      
            # Update the Cache
            devicescache.update_file(self.data)
          else:
            print("[USING LOCAL SECRETS]")
            pass
        
        #print(self.data)

        pass
