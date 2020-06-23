# Raspberry Pi "Protocol Translation" Gateway for Azure IoT Central

![alt text](./Assets/raspberry-pi-4-hero-shot.png "Project Hero Shot") 

## Overview
This repository is part of a training and project series for Azure IoT Central. The name of the series is "Raspberry Pi Gateway and Arduino Nano BLE Devices for Azure Iot Central" and is located at...

[LINK: Training & Project Site for Raspberry Pi Gateway and Arduino Nano BLE Devices for Azure Iot Central](http://www.hackinmakin.com/Raspberry%20Pi%20Gateway%20and%20BLE/index.html)

This project will enable a Raspberry Pi to act as a "Protocol Translation" Gateway connected to Azure IoT Central and send Telemerty on behalf of of the Devices we have created for this project. 

![Protocol Translation Gateway](./Assets/gateway-protocol-lrg.png)

You may want to try the supporting projects for the Nano BLE Devices if you landed here out of sequence.

### Arduino Nano BLE 33 for Azure IoT Central
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

### Arduino Nano BLE 33 SENSE for Azure IoT Central
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


### Setting up the Development Environment on the Raspberry Pi
We will need to setup our Raspberry Pi with all of the capbailities we will need to develop for our Protcol Translation Gateway.

#### Connecting to the Raspberry Pi using SSH
We will be connecting to the Raspberry Pi using the remote SSH capability of Visual Studio Code that we installed as part of our development toolchain. When you set the RPi up, we enabled the device to connect to our Wifi network. 

Now we want to find the IP address of our RPi and connect to via VS Code's Remote SSH tools. This will let us develop our code and test our application working remotely connected to the device.

Here is the documetnation on the extension for VS Code...
[LINK: Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)

Here is how we will connect to the Raspberry Pi...
[LINK: Remote development over SSH](https://code.visualstudio.com/remote-tutorials/ssh/getting-started)

#### Connect to the Raspberry Pi

* Click on the green icon in the bottom left of Visual Studio Code, select "Remote-SSH:Connect to Host..."
* Enter in the connection IP. It will be "pi@your IP Address". For example "pi@192.186.1.174"
* You maybe prompted the first time to indetify the Operationing System, choose "Linux"
* Next, enter the Password for the Raspberry Pi, by default is is raspberry. You should change this right away!
* Open our Home Folder on the Raspberry Pi

  ![alt text](./Assets/vs-code-connect-remote-ssh-pi-open-home-folder.png "Pi SSH Connect Open Home Folder") 

* Click on left side of the main screen "Open Folder" and the navigation helper will open and default to "/home/pi/" press enter as that is right where we want to go!
  * You maybe prompted re-enter your password (which is no longer raspberry, right?)

#### Create our Project Folder on the Raspberry Pi

  ![alt text](./Assets/vs-code-connect-remote-ssh-pi-create-project-folder.png "Pi SSH Connect Create Project Folder") 

#### Update Python on the Raspberry Pi

From the terminal, run these two commands to bring your Python environments to the latest versions...

```` python
sudo apt-get install python3
sudo apt-get install python
````

#### Build our Bluetooth Stack

We will be using the lastest version of BlueZ

Visit the bluez download page and copy the link to the latest source release (under the User Space BlueZ Package section)

Latest version (5.54) since this documentation was updated. Bet sure to get the latest.
http://www.bluez.org/


```` bash
cd ~
wget http://www.kernel.org/pub/linux/bluetooth/bluez-5.37.tar.xz
tar xvf bluez-5.37.tar.xz
cd bluez-5.37
sudo apt-get update
sudo apt-get install -y libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev
./configure --enable-library
make
````

```` bash
systemctl status bluetooth
sudo systemctl start bluetooth
````

Run automatically
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

```` bash
[Unit]
Description=Bluetooth service
Documentation=man:bluetoothd(8)
ConditionPathIsDirectory=/sys/class/bluetooth
 
[Service]
Type=dbus
BusName=org.bluez
ExecStart=/usr/local/libexec/bluetooth/bluetoothd --experimental               
NotifyAccess=main
#WatchdogSec=10
#Restart=on-failure
CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
LimitNPROC=1
 
[Install]
WantedBy=bluetooth.target
Alias=dbus-org.bluez.service
````

Save the file and exit the editor by pressing 
* Ctrl-o
* Enter
* Ctrl-x.

Now tell systemd to reload its configuration files by running:

```` bash
sudo systemctl daemon-reload
sudo systemctl restart bluetooth
systemctl status bluetooth
````

Once the bluez service is running you can check the experimental features are enabled by running the status command again.  You should see output similar to the following (notice the --experimental on the last line):

```` bash
 Download: fileCopy Code
● bluetooth.service - Bluetooth service
   Loaded: loaded (/lib/systemd/system/bluetooth.service; disabled)
   Active: active (running) since Mon 2016-02-29 05:15:55 UTC; 4s ago
     Docs: man:bluetoothd(8)
 Main PID: 1022 (bluetoothd)
   Status: "Running"
   CGroup: /system.slice/bluetooth.service
           └─1022 /usr/local/libexec/bluetooth/bluetoothd --experimental
````

