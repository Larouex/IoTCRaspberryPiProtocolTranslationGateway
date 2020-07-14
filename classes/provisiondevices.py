
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

    def __init__(self, Log):
        self.logger = Log
        self.data = []
        self.new_devices = []
        self.characteristics = []
  
    async def discover_and_provision_devices(self, resethci):

        self.logger.info("resethci: %s" % str(resethci))

        # Write flag
        new_devices_discovered = False

        # Load the Devices Cache File for any devices
        # that have already been provisioned
        devicescache = DevicesCache(self.logger)
        
        # Make a working copy of the cache file
        self.data = devicescache.data
        #print(self.data)

        if resethci:
            try:
                self.logger.info("hciconfig down..." )
                os.system("sudo hciconfig hci1 down")
                self.logger.info("hciconfig up..." )
                os.system("sudo hciconfig hci1 up")
            except:
                self.logger.warning("We encountered an error executing OS command hciconfig" )

        try:
            # Scan the BLE's that are Advertising
            self.logger.warning("Please Wait: Scanning for BLE Devices Advertising...(10 Seconds)" )
            scanner = Scanner(1).withDelegate(ScanDelegate())
            devices = scanner.scan(10.0)

            # Check the devices and add the ones that match the pattern indicated in
            # the devicescache.json file element [DeviceNamePrefix]...
            for device in devices:
              devicename = str(device.getValueText(9))
              if [x for x in self.data["Devices"] if x.get("Address")==device.addr]:
                self.logger.warning("[ALREADY PROVISIONED, SKIPPING] %s" % devicename)
              else:
                if devicename.startswith(self.data["DeviceNamePrefix"]):
                  new_devices_discovered = True
                  self.logger.warning("[FOUND NEW DEVICE] %s" % devicename)
                  
                  # Associate the IoTC Device Template
                  dcm_for_device = None
                  for deviceCapabilityModel in self.data["DeviceCapabilityModels"]:
                    self.logger.info("[DEVICE PREFEIX] %s" % self.data["DeviceNamePrefix"] + deviceCapabilityModel["Name"])
                    if devicename.startswith(self.data["DeviceNamePrefix"] + deviceCapabilityModel["Name"]):
                      dcm_for_device = deviceCapabilityModel["DCM"]
                      self.logger.info("[DEVICE DCM] %s" % dcm_for_device)
                  
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
        except:
            self.logger.error("[TERMINATING] We encountered an error scanning for BLE Devices" )
            self.logger.error("[TERMINATING] Try passing the --resethci parameter" )
            return

        if new_devices_discovered:
            
          # load the Services and Characteristic Maps
          service_characteristics = NanoBLEServices(self.logger)
          self.characteristics = service_characteristics.data
          self.logger.info("[service_characteristics] %s" % service_characteristics)

          scope_id = None
          device_primary_key = None
          device_secondary_key = None
          gateway_primary_key = None
          gateway_secondary_key = None

          # load the secrets
          secrets = Secrets(self.logger)
          if secrets.data["KeyVaultSecrets"]:
            self.logger.info("[USING KEY VAULT SECRETS]")
            
            # key vault account uri
            key_vault_uri = secrets.data["KeyVaultSecrets"]["KeyVaultUri"]
            self.logger.info("[KEY VAULT URI] %s" % key_vault_uri)

            tenant_id = secrets.data["KeyVaultSecrets"]["TenantId"]
            client_id = secrets.data["KeyVaultSecrets"]["ClientId"]
            client_secret = secrets.data["KeyVaultSecrets"]["ClientSecret"]
            
            # Get access to Key Vault Secrets
            credential = ClientSecretCredential(tenant_id, client_id, client_secret)
            self.logger.info("[credential] %s" % credential)
            secret_client = SecretClient(vault_url=key_vault_uri, credential=credential)
            self.logger.info("[secret_client] %s" % secret_client)

            # Read all of our Secrets for Accessing IoT Central
            scope_id = secret_client.get_secret(secrets.data["KeyVaultSecrets"]["ScopeId"])
            device_primary_key = secret_client.get_secret(secrets.data["KeyVaultSecrets"]["DeviceConnect"]["SaSKeys"]["Primary"])
            device_secondary_key = secret_client.get_secret(secrets.data["KeyVaultSecrets"]["DeviceConnect"]["SaSKeys"]["Secondary"])
            gateway_primary_key = secret_client.get_secret(secrets.data["KeyVaultSecrets"]["GatewayConnect"]["SaSKeys"]["Primary"])
            gateway_secondary_key = secret_client.get_secret(secrets.data["KeyVaultSecrets"]["GatewayConnect"]["SaSKeys"]["Secondary"])
          
          else:
            # Read all of our LOCAL Secrets for Accessing IoT Central
            self.logger.info("[USING LOCAL SECRETS]")
            scope_id = secret_client.get_secret(secrets.data["LocalSecrets"]["ScopeId"])
            device_primary_key = secret_client.get_secret(secrets.data["LocalSecrets"]["DeviceConnect"]["SaSKeys"]["Primary"])
            device_secondary_key = secret_client.get_secret(secrets.data["LocalSecrets"]["DeviceConnect"]["SaSKeys"]["Secondary"])
            gateway_primary_key = secret_client.get_secret(secrets.data["LocalSecrets"]["GatewayConnect"]["SaSKeys"]["Primary"])
            gateway_secondary_key = secret_client.get_secret(secrets.data["LocalSecrets"]["GatewayConnect"]["SaSKeys"]["Secondary"])


          # Verbose - User is SUDO :)  
          self.logger.info("[SCOPE ID]: %s" % scope_id.value)
          self.logger.info("[DEVICE PRIMARY KEY]: %s" % device_primary_key.value)
          self.logger.info("[DEVICE SECONDARY KEY]: %s" % device_secondary_key.value)
          self.logger.info("[GATEWAY PRIMARY KEY]: %s" % gateway_primary_key.value)
          self.logger.info("[GATEWAY SECONDARY KEY]: %s" % gateway_secondary_key.value)

          # Symetric Key for handling Device Specific SaS Keys
          symmetrickey = SymmetricKey(self.logger)

          try:
              for device in self.new_devices: 
                # Get the Device Name
                device_name = device["DeviceName"]
                
                # Get a Device Specific Symetric Key
                device_symmetrickey = symmetrickey.compute_derived_symmetric_key(device["DeviceName"], device_secondary_key.value)
                self.logger.info("[SYMETRIC KEY] %s" % device_symmetrickey)

                # Provision the Device
                self.logger.warning("[PROVISIONING] %s" % device_name)
                provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
                  provisioning_host=secrets.data["ProvisioningHost"],
                  registration_id=device["DeviceName"],
                  id_scope=scope_id.value,
                  symmetric_key=device_symmetrickey,
                  websockets=True
                )

                provisioning_device_client.provisioning_payload = '{"iotcModelId":"%s"}' % (device["DCM"])
                registration_result = await provisioning_device_client.register()
          except:
              self.logger.error("[TERMINATING] We encountered an error Provisioning the Device" )
              return
   
          # Update the Cache
          devicescache.update_file(self.data)
          return
