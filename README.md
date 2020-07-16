# Raspberry Pi "Protocol Translation" Gateway for Azure IoT Central

![alt text](./Assets/raspberry-pi-4-hero-shot.png "Project Hero Shot") 

## Overview
This repository is part of a training and project series for Azure IoT Central. The name of the series is "Raspberry Pi Gateway and Arduino Nano BLE Devices for Azure Iot Central" and is located at...

[LINK: Training & Project Site for Raspberry Pi Gateway and Arduino Nano BLE Devices for Azure Iot Central](http://www.hackinmakin.com/Raspberry%20Pi%20Gateway%20and%20BLE/index.html)

This project will enable a Raspberry Pi to act as a "Protocol Translation" Gateway connected to Azure IoT Central and send Telemerty on behalf of of the Devices we have created for this project. 

![Protocol Translation Gateway](./Assets/gateway-protocol-lrg.png)

## Features
This project is primarly a training and education project that is fully realized. You can take the componants and build out a working IoT system end to end.

* Automated Regisration and Provisioing of Nano BLE Devices

You may want to try the supporting projects for the Nano BLE Devices if you landed here out of sequence.

## Arduino Nano BLE 33 for Azure IoT Central
Here is the link to the Github for the project "Arduino Nano BLE 33 for Azure IoT Central", you should also start and follow up to this point in the training link reference at the start of the Readme.

[LINK: Arduino Nano BLE 33 for Azure IoT Central](https://github.com/Larouex/IoTCNanoBLE33)

We will be working with the following charactertics from our Nano BLE 33 Device and doing Protcol Translation to IoT Central...

* <b>VERSION</b>
* <b>BATTERY CHARGED</b>
* <b>TELEMETRY FREQUENCY</b>
* <b>ACCELEROMETER</b>
* <b>GYROSCOPE</b>
* <b>MAGNETOMETER</b>
* <b>ORIENTATION</b>
* <b>RGB LED</b>

## Arduino Nano BLE 33 SENSE for Azure IoT Central
Here is the link to the Github for the project "Arduino Nano BLE 33 SENSE for Azure IoT Central", you should also start and follow up to this point in the training link reference at the start of the Readme.

[LINK: Arduino Nano BLE 33 SENSE for Azure IoT Central](https://github.com/Larouex/IoTCNanoBLESense33)

We will be working with the following charactertics from our Nano BLE 33 SENSE Device and doing Protcol Translation to IoT Central...

* <b>VERSION</b>
* <b>BATTERY CHARGED</b>
* <b>TELEMETRY FREQUENCY</b>
* <b>ACCELEROMETER</b>
* <b>GYROSCOPE</b>
* <b>MAGNETOMETER</b>
* <b>ORIENTATION</b>
* <b>RGB LED</b>
* <b>BAROMETER</b>
* <b>TEMPERATURE</b>
* <b>HUMIDITY</b>
* <b>MICROPHONE</b>
* <b>AMBIENTLIGHT</b>
* <b>COLOR</b>
* <b>PROXIMITY</b>
* <b>GESTURE</b>

## Setting up Your Development Toolchain
The code in this repository depends on Ardunio, Visual Studio Code and PlatformIO.

### Your Local Machine
The development "toolchain" refers to all of the various tools, SDK's and bits we need to install on your machine to facilitate a smooth experience developing our BLE devices and the Raspberry Pi Gateway device. Our main development tool will be Visual Studio code. It has dependencies on tools from Arduino and other open source projects, but it will be the central place where all our development will occur making it easy to follow along  regardless of which operating system you are working on.

| - | Install These Tools |
|---|---|
| ![Python](./Assets/python-icon-100.png) | [LINK: Python 3 Installation Page](https://www.python.org/downloads/) - Pyhon is the programming language we will use to build applications for the Raspberry Pi. |
| ![Visual Studio Code](./Assets/vs-code-icon-100.png) | [LINK: Visual Studio Code Installation Page](https://code.visualstudio.com/download) - Visual Studio Code is a lightweight but powerful source code editor which runs on your desktop and is available for Windows, macOS and Linux. This is the IDE we will use to write code and deploy to the our BLE Devices and the Raspberry Pi Gateway.  |
| ![Docker](./Assets/docker-icon-100.png) | [LINK: Docker Desktop Install](https://www.docker.com/products/docker-desktop) - Docker Desktop is an application for MacOS and Windows machines for the building and sharing of containerized applications. |

### Upgrading pip
Pip is the package manager we will use to download packages

On Linux or macOS (Open Terminal):
```
    pip install -U pip
```
On Windows (from a CMD window or Powershell):
```
    python -m pip install -U pip
```

### Install all the Tools for Visual Studio Code
These are a set of tools we will use to develop our apps on the Raspberry Pi. You can open the Extensions sidebar with "Shift+Ctrl+X) or click the icon in the side navigator bar.

![alt text](./Assets/vs-code-python-sml.png "VS Code Python")

![alt text](./Assets/vs-code-remote-ssh-sml.png "VS Code Remote SSH")

![alt text](./Assets/vs-code-remote-edit-sml.png "VS Code Remote SSH Edit")

![alt text](./Assets/vs-code-docker-sml.png "VS Code Docker")

### Install the Azure CLI Tooling
The Azure command-line interface (Azure CLI) is a set of commands used to create and manage Azure resources. The Azure CLI is available across Azure services and is designed to get you working quickly with Azure, with an emphasis on automation.

Click the link below and install on your Desktop environment.

[LINK: Install the Azure CLI Tooling](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)


# Setting up the Development Environment on the Raspberry Pi
We will need to setup our Raspberry Pi with all of the capabilities we will need to develop for our Protcol Translation Gateway.

## Connecting to the Raspberry Pi using SSH
We will be connecting to the Raspberry Pi using the remote SSH capability of Visual Studio Code that we installed as part of our development toolchain. When you set the RPi up, we enabled the device to connect to our Wifi network. 

Now we want to find the IP address of our RPi and connect to via VS Code's Remote SSH tools. This will let us develop our code and test our application working remotely connected to the device.

* Here is the documetnation on the extension for VS Code...
[LINK: Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)

* Here is how we will connect to the Raspberry Pi...
[LINK: Remote development over SSH](https://code.visualstudio.com/remote-tutorials/ssh/getting-started)

## Connect to the Raspberry Pi

* Click on the green icon in the bottom left of Visual Studio Code, select "Remote-SSH:Connect to Host..."
* Enter in the connection IP. It will be "pi@your IP Address". For example "pi@192.186.1.174"
* You maybe prompted the first time to indetify the Operationing System, choose "Linux"
* Next, enter the Password for the Raspberry Pi, by default is is raspberry. You should change this right away!
* Open our Home Folder on the Raspberry Pi

  ![alt text](./Assets/vs-code-connect-remote-ssh-pi-open-home-folder.png "Pi SSH Connect Open Home Folder") 

* Click on left side of the main screen "Open Folder" and the navigation helper will open and default to "/home/pi/" press enter as that is right where we want to go!
  * You maybe prompted re-enter your password (which is no longer raspberry, right?)

## Create our Project Folder on the Raspberry Pi

* Click on "New Folder" icon
* Type in "Projects" and press enter to create the folder

  ![alt text](./Assets/vs-code-connect-remote-ssh-pi-create-project-folder.png "Pi SSH Connect Create Project Folder") 

## Update Python on the Raspberry Pi

From the terminal, run these two commands to bring your Python environments to the latest versions...

```` python
sudo apt-get install python3
sudo apt-get install python3
````
If it all comes back as up to date, then goodness!

## Build our Bluetooth Stack
BlueZ is official Linux Bluetooth protocol stack.

We will be using the latest version of BlueZ. As of the last update to this repository, it was version 5.54. You should work with the latest, stable release in future as experimental features like BLE will stabilize and improve.

Visit the bluez download page and copy the link to the latest source release (under the User Space BlueZ Package section)

Latest version (5.54) since this documentation was updated. Bet sure to get the latest.
http://www.bluez.org/


### Install Dependencies for BlueZ
````bash
sudo apt-get install -y git bc libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev
sudo apt-get install -y libreadline-dev autoconf
````
### Install json-c
````bash
cd ~
wget https://s3.amazonaws.com/json-c_releases/releases/json-c-0.13.tar.gz
tar -xvf json-c-0.13.tar.gz
cd json-c-0.13/
./configure --prefix=/usr --disable-static && make
sudo make install
````

### Install ell for BlueZ
````bash
cd ~
wget https://mirrors.edge.kernel.org/pub/linux/libs/ell/ell-0.6.tar.xz
tar -xvf ell-0.6.tar.xz
cd ell-0.6/
sudo ./configure --prefix=/usr
sudo make
sudo make install
````

### Get BlueZ Source Code, Compile/Build and Install
```` bash
cd ~
wget http://www.kernel.org/pub/linux/bluetooth/bluez-5.54.tar.xz
tar xvf bluez-5.54.tar.xz
cd bluez-5.54
sudo apt-get update
sudo apt-get install -y libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev
./configure --enable-library --enable-mesh --prefix=/usr --mandir=/usr/share/man --sysconfdir=/etc --localstatedir=/var
sudo make
sudo make install
````

We now need to let the Rasp[berry Pi's Raspian OS know that we want to use our newly compiled BlueZ Bluetoothh stack and tell systemd to use the new bluetooth daemon:

After opening this file, bluetooth.service, make sure the ExecStart line points to your new daemon
in /usr/libexec/bluetooth/bluetoothd, as shown in the screenshot below...

```` bash
sudo vi /lib/systemd/system/bluetooth.service
````
![Raspberry Pi Terminal Bluetooth ExecStart](./Assets/pi-terminal-bluetooth-execstart.png)

You still need to create a symlink from the old bluetoothd to the new one. First, rename the old file for backup... 

```` bash
sudo cp /usr/lib/bluetooth/bluetoothd /usr/lib/bluetooth/bluetoothd-543.orig
cd /usr/lib/bluetooth/
ls -l
````

You should see this oputput...
![Raspberry Pi Terminal Bluetooth ls](./Assets/pi-terminal-bluetooth-ls.png)

Create the symlink using the commands below...
```` bash
sudo ln -sf /usr/libexec/bluetooth/bluetoothd /usr/lib/bluetooth/bluetoothd
sudo systemctl daemon-reload
````

Finally; Let's double check the version of bluetoothd and meshctl...
```` bash
bluetoothd -v
meshctl -v
````
You should see this oputput...
![Raspberry Pi Terminal Bluetooth Version Check](./Assets/pi-terminal-bluetooth-version-check.png)

##### Start Bluetooth and Run Automatically

```` bash
systemctl status bluetooth
sudo systemctl start bluetooth
````

Set to run automatically...
```` bash
sudo systemctl enable bluetooth
````

##### Enable Bluetooth Low Energy Features
One final configuration change you can make is to enable the bluetooth low energy features in bluez.  These are special APIs that allow bluez to interact with bluetooth low energy devices, however they're still in development and put behind an experimental flag that must be enabled first.

To enable bluez's experimental features like BLE you can modify the bluez service configuration.  Edit this configuration by running:

```` bash
sudo nano /lib/systemd/system/bluetooth.service
````

Enable the experimental features by adding --experimental to the ExecStart line, for example the configuration should look like:

![Raspberry Pi Terminal Bluetooth Execstart Add Experimental](./Assets/pi-terminal-bluetooth-execstart-add-experimental.png)

Save the file and exit the editor by pressing 
* Ctrl-o
* Enter
* Ctrl-x.

Now tell systemd to reload its configuration files by running:

```` bash
sudo systemctl daemon-reload
sudo systemctl restart bluetooth
````

Once the bluez service is running you can check the experimental features are enabled by running the status command again.  You should see output similar to the following (notice the --experimental on the last line):

```` bash
systemctl status bluetooth
````

![Raspberry Pi Terminal Bluetooth Status Experimental](./Assets/pi-terminal-bluetooth-status_experimental.png)



### Verify that Bluetooth is Working for LE

```` bash
hciconfig

hci0:   Type: Primary  Bus: UART
        BD Address: DC:A6:32:B1:BD:39  ACL MTU: 1021:8  SCO MTU: 64:1
        UP RUNNING 
        RX bytes:1710 acl:0 sco:0 events:118 errors:0
        TX bytes:7521 acl:0 sco:0 commands:118 errors:0
````

Next up I started monitoring one of my Nano BLE 33 Devices in Advertising mode and ran this command... 
```` bash
sudo hcitool lescan
````
You can the device is detected in the scan from the Raspberry Pi and we are up and working!

![alt text](./Assets/le-scan-terminal-window.png "le scan") 

<b>NOTE:</b> If you get an error with LE Scan, try these commands...
```` bash
sudo hciconfig hci0 down
sudo hciconfig hci0 up
````

### Getting Started with Bluetooth and Gateway Coding
Now that we have everything ready to go on our desktop and Raspberry Pi, let's get started!

### Install Libraries

Install the libraries needed for the Raspberry Pi Gateway...
````bash
cd ~/Projects/IoTCRaspberryPiProtocolTranslationGateway/
pip3 install -r requirements.txt
````
Setup all our Bluetooth Python Libraries for BlueZ
````bash
sudo apt-get install bluez python-bluez
sudo apt-get install libbluetooth-dev
sudo python3 setup.py install
wget https://github.com/pybluez/pybluez/archive/master.tar.gz
tar xvf master.tar.gz
cd pybluez=master
sudo apt-get install libbluetooth-dev
sudo apt-get install libglib2.0-dev
sudo pip install bluepy
sudo python3 setup.py install
````



First off let's clone this repository to our Raspberry Pi...
```` bash
cd ~
cd Projects
git clone https://github.com/Larouex/IoTCRaspberryPiProtocolTranslationGateway.git
cd IoTCRaspberryPiProtocolTranslationGateway
````
##  Install required packages
```` bash
sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   python-setuptools libgstreamer1.0-dev git-core \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-{omx,alsa} python-dev libmtdev-dev \
   xclip xsel libjpeg-dev libgpiod2
````

### Set up a virtual environment and install required python packages
We use virtual environments is to keep dependencies required by different projects separated.

```` bash
python3 -m venv .env
source .env/bin/activate
pip3 install -r requirements.txt
````

### SECRETS!!! - Azure Connectivity and Protecting Your Secrets
Azure IoT Central is what we using for capturing Telemetry and Managing out Gateway and Devices. It is a powerful SaaS offering and we will be using the tools and visualizations to build out a rich application for our scenario. In order to connect our devices and gateway to IoT Central, we need to manage a set of secrets and we will store those secrets in Azure Key Vault. I highly recommend that you do this so you do not make a mistake and expose access to your application, gateway or devices.

I am going to assume the following when we work with Azure and Azure Portal...

* That you already have an Azure Account (If you don't, get started here [LINK: Create your Azure free account today](https://azure.microsoft.com/en-us/free/))
* That you have sufficient permissions in your Azure account to create Resource Groups and Resources
* That you are familiar creating and using resources with the Azure CLI or the Azure Portal [LINK: Azure Portal](https://portal.azure.com/))

### Create our Connection Secrets...

| Name | Secret (IoT Central Admin [Device Connection] Page)  | Content Type |
|---|---|---|
| raspberry-pi-protocol-translation-gateway-scopeid | Admin, Device Connection, Copy [ID scope] | Client Secret |
| raspberry-pi-protocol-translation-gateway-saskey-device-primary | Admin, Device Connection, Devices, View Keys, Copy [Primary Key] | Client Secret |
| raspberry-pi-protocol-translation-gateway-saskey-device-secondary | Admin, Device Connection, Devices, View Keys, Copy [Secondary Key] | Client Secret |
| raspberry-pi-protocol-translation-gateway-saskey-gateway-primary | Admin, Device Connection, Azure Edge devices, View Keys, Copy [Primary Key] | Client Secret |
| raspberry-pi-protocol-translation-gateway-saskey-gateway-secondary | Admin, Device Connection, Azure Edge devices, View Keys, Copy [Secondary Key] | Client Secret |

Once these are all created in Key Vault, your list should look like this...
![alt text](./Assets/azure-portal-key-vault-secrets-list.png "Azure Portal Key Vault Secrets List") 

https://docs.microsoft.com/en-us/azure/key-vault/certificates/quick-create-python

### Configure our Secrets for Local Development
There is a file in the root folder of the project named "secrets_template.json" and this file outlines the shape of Json we use to retreive secrets. It supports local and Key Vault usage. 

````json
{
  "UseKeyVault": true,
  "LocalSecrets": {
    "ScopeId": "",
    "DeviceConnect":{
      "SaSKeys":{
          "Primary": "",
          "Secondary": ""
      },
      "GatewayConnect":{
        "SaSKeys":{
            "Primary": "",
            "Secondary": ""
        }
      }
    }
  },
  "KeyVaultSecrets":{
    "KeyVaultUri": "",
    "ScopeId": "",
    "DeviceConnect":{
      "SaSKeys":{
          "Primary": "",
          "Secondary": ""
      },
      "GatewayConnect":{
        "SaSKeys":{
            "Primary": "",
            "Secondary": ""
        }
      }
    }
  }
}
````

The fist thing we will do is copy the "secrets_template.json" to a new file named "secrets.json" in the root folder of the project. Open this file in Visual Studio Code and let's get to configuring the options.

### I want to use the security and awesomeness of Key Vault!

* Set "UseKeyVault" to true
* From the Azure Portal, Goto your Key Vault Resource
* Goto Secrets
* Click onto your secret for Scope ID that we set up previously
* Click the copy button next to the "Secret Identifier"
* Paste it into the "KeyVaultUri" in the "secrets.json" file.
* Highlight and cut the remainder of url after .../secrets/ 
* Paste into the ScopeId field
* Repeat for all the secrets we setup previously and put into the right fields!

<b>Your file should look like this when completed...</b>

````json
{
  "UseKeyVault": true,
  "LocalSecrets": {
    "ScopeId": "",
    "DeviceConnect":{
      "SaSKeys":{
          "Primary": "",
          "Secondary": ""
      },
      "GatewayConnect":{
        "SaSKeys":{
            "Primary": "",
            "Secondary": ""
        }
      }
    }
  },
  "KeyVaultSecrets":{
    "KeyVaultUri": "https://<your-kv-resource-name>.vault.azure.net/secrets/ ",
    "ScopeId": "raspberry-pi-protocol-translation-gateway-scopeid/<your id number>",
    "DeviceConnect":{
      "SaSKeys":{
          "Primary": "raspberry-pi-protocol-translation-gateway-saskey-device-primary/<your id number>",
          "Secondary": "raspberry-pi-protocol-translation-gateway-saskey-device-secondary/<your id number>",
      },
      "GatewayConnect":{
        "SaSKeys":{
            "Primary": "raspberry-pi-protocol-translation-gateway-saskey-gateway-primary/<your id number>",
            "Secondary": "raspberry-pi-protocol-translation-gateway-saskey-gateway-secondary/<your id number>",
        }
      }
    }
  }
}
````
Save the file and you can ignore the "LocalSecrets" section.

<b>IMPORTANT: Make sure to check your .gitignore to verify that "secrets.json" is in the list so it does not get checked in! The file should be dithered in your Visual Studio Code Explorer window.</b>

### I don't want to use Key Vault!
If you are working locally and do not want to implement the security and awesomeness of Key Vault, then go ahead and set "UseKeyVault" to false. Copy all our your SaS key values from the Admin, Device Connection page in IoT Central...

````json
{
  "UseKeyVault": false,
   "LocalSecrets": {
    "ScopeId": "",
    "DeviceConnect":{
      "SaSKeys":{
          "Primary": "",
          "Secondary": ""
      },
      "GatewayConnect":{
        "SaSKeys":{
            "Primary": "",
            "Secondary": ""
        }
      }
    }

````
Save the file and you can ignore the "KeyVaultSecrets" section.

<b>IMPORTANT: Make sure to check your .gitignore to verify that "secrets.json" is in the list so it does not get checked in! The file should be dithered in your Visual Studio Code Explorer window.</b>

## Get Your Credentials for Azure Login

* Open a Terminal or Powershell session
* Login to the Azure CLI...

````bash
az login
````

* If the CLI can open your default browser, it will do so and load an Azure sign-in page.
* Otherwise, open a browser page at https://aka.ms/devicelogin and enter the authorization code displayed in your terminal.
* Sign in with your account credentials in the browser.

````bash
az ad sp create-for-rbac --name http://raspberry-pi-protocol-translation-gateway --skip-assignment
````

````json
{
  "appId": "<your appID>",
  "displayName": "raspberry-pi-protocol-translation-gateway",
  "name": "http://raspberry-pi-protocol-translation-gateway",
  "password": "<your password>",
  "tenant": "<your tenant>"
}
````

az keyvault set-policy --name larouex-prod-key-vault --spn "9afd63c4-91e2-4054-b068-aeb21dc291eb" --secret-permissions get set list delete backup recover restore purge

````bash
az keyvault set-policy --name <your key vault url> --spn <your password> --secret-permissions get set list delete backup recover restore purge
````

### Set up the Credentials in the Raspberry Pi
Let's go back to a terminal window and setup the variables on the Raspberry Pi. Use the values from the generated Jasn to set AZURE_CLIENT_ID ("appId"), AZURE_CLIENT_SECRET ("password") and AZURE_TENANT_ID ("tenant") environment variables. 

````bash
export AZURE_CLIENT_ID="<your appId>"
export AZURE_CLIENT_SECRET="<your password>"
export AZURE_TENANT_ID="<your tenant>"
export AZURE_SUBSCRIPTION_ID="<your tenant>"
````

Authorize the service principal to perform key operations in your Key Vault:

https://www.bluetooth.com/specifications/assigned-numbers/generic-access-profile/

## Provisioning BLE Devices

````json
{
  "DeviceNamePrefix": "larouex-ble-",
  "DeviceCapabilityModels": [
    {
      "Name": "sense-",
      "DCM": "urn:larouexiot:nanoble33sense:1"
    },
    {
      "Name": "33-",
      "DCM": "urn:larouexiot:nanoble33:1"
    }
  ],
  "Devices": [
    {
      "DeviceName": "Simulated Device",
      "Address": "6A:6A:6A:6A:6A:6A",
      "LastRSSI": "-91 dB",
      "DCM": "urn:larouexiot:nanoble33:1"
    },
    {
      "DeviceName": "larouex-ble-sense-0001",
      "Address": "c7:94:90:1c:8f:3c",
      "LastRSSI": "0 dB",
      "DCM": "urn:larouexiot:nanoble33sense:1"
    }
  ]
}
````
