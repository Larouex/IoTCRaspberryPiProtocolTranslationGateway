
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
import time, logging, string, json, os, binascii, struct, threading, asyncio, datetime
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

    def __init__(self, Log, ProvisioningScope):
        self.logger = Log
        self.data = []
        self.new_devices = []
        self.characteristics = []
        self.provisioning_scope = ProvisioningScope
  
    async def provision_devices(self):

        # Load the Devices Cache File for any devices
        # that have already been provisioned
        devicescache = DevicesCache(self.logger)

        # Make a working copy of the cache file
        self.data = devicescache.data
        self.data["Devices"] = [x for x in self.data["Devices"] if x["DeviceName"] == "Simulated Device"]

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

          # Verbose
          self.logger.info("[SCOPE ID]: %s" % scope_id.value)
          self.logger.info("[DEVICE PRIMARY KEY]: %s" % device_primary_key.value)
          self.logger.info("[DEVICE SECONDARY KEY]: %s" % device_secondary_key.value)
          self.logger.info("[GATEWAY PRIMARY KEY]: %s" % gateway_primary_key.value)
          self.logger.info("[GATEWAY SECONDARY KEY]: %s" % gateway_secondary_key.value)

        # Symetric Key for handling Device Specific SaS Keys
        symmetrickey = SymmetricKey(self.logger)

        try:

            # Iterate the Discovered Devices and Provision
            # the devicescache.json file element [DeviceNamePrefix]...
            for device in devicescache.data["Devices"]:
              provision_this_device = False
              device_name = device["DeviceName"]
              dcm_for_device = device["DCM"]
              last_provisioned = device["LastProvisioned"]
              
              if (self.provisioning_scope == "ALL"):
                provision_this_device = True
              elif  (self.provisioning_scope == "NEW" and last_provisioned == None):
                provision_this_device = True
              else:
                self.logger.info("[NO ACTION] %s" % device_name)

              if provision_this_device:
                
                # Get a Device Specific Symetric Key
                device_symmetrickey = symmetrickey.compute_derived_symmetric_key(device_name, device_secondary_key.value)
                self.logger.info("[SYMETRIC KEY] %s" % device_symmetrickey)

                # Provision the Device
                self.logger.warning("[PROVISIONING] %s" % device_name)
                provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
                  provisioning_host=secrets.data["ProvisioningHost"],
                  registration_id=device_name,
                  id_scope=scope_id.value,
                  symmetric_key=device_symmetrickey,
                  websockets=True
                )

                provisioning_device_client.provisioning_payload = '{"iotcModelId":"%s"}' % (dcm_for_device)
                registration_result = await provisioning_device_client.register()

                newDevice = {
                      "DeviceName": device_name, 
                      "Address": device["Address"], 
                      "LastRSSI": device["LastRSSI"],
                      "DCM": dcm_for_device,
                      "LastProvisioned": datetime.datetime.now()
                    } 
                self.data["Devices"].append(newDevice)
        
        except Exception as ex:
            self.logger.error("[ERROR] %s" % ex)
            self.logger.error("[TERMINATING] We encountered an error scanning for BLE Devices" )
            return

        # Update the Cache
        devicescache.update_file(self.data)
        return
