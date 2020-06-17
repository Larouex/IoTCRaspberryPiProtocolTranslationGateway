# Raspberry Pi "Protocol Translation" Gateway for Azure IoT Central

![alt text](./Assets/raspberry-pi-4-hero-shot.png "Project Hero Shot") 

## Overview
This repository is part of a training and project series for Azure IoT Central. The name of the series is "Raspberry Pi Gateway and Arduino Nano BLE Devices for Azure Iot Central" and is located at...

[LINK: Training & Project Site for Raspberry Pi Gateway and Arduino Nano BLE Devices for Azure Iot Central](http://www.hackinmakin.com/Raspberry%20Pi%20Gateway%20and%20BLE/index.html)

This project will enable a Raspberry Pi to act as a "Protocol Translation" Gateway connected to Azure IoT Central and send Telemerty on behalf of of the Devices we have created for this project. You should go back and create the Nano BLE Devices if you landed here out of sequence.

### Arduino Nano BLE 33 for Azure IoT Central
Here is the link to the Github for the project "Arduino Nano BLE 33 for Azure IoT Central", you should also start and follow up to this point in the training link reference at the start of the Readme.

[LINK: Arduino Nano BLE 33 for Azure IoT Central](https://github.com/Larouex/IoTCNanoBLE33)

### Arduino Nano BLE 33 SENSE for Azure IoT Central
Here is the link to the Github for the project "Arduino Nano BLE 33 SENSE for Azure IoT Central", you should also start and follow up to this point in the training link reference at the start of the Readme.

[LINK: Arduino Nano BLE 33 SENSE for Azure IoT Central](https://github.com/Larouex/IoTCNanoBLESense33)

## Setup the Development Toolchain

### Install Git
Git is the tool we use for version control and management of software assets. Our workshop will use it to clone the modules and also to save anything if you want

[LINK: Git Installation Page](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Install Visual Studio Code
This is the IDE we will use to write code, deploy to the RPi, etc. 

[LINK: Visual Studio Code Installation Page](https://code.visualstudio.com/download)

### Install Python
Pyhon is the language we will use to build applications for the Raspberry Pi

From the Python Org: 
* Python is powerful... and fast;
* plays well with others; 
* runs everywhere; 
* is friendly & easy to learn; 
* is Open.

[LINK: Python 3 Installation Page](https://www.python.org/downloads/)

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

![alt text](../Assets/vs-code-python.png "VS Code Python")

![alt text](../Assets/vs-code-remote-ssh.png "VS Code Remote SSH")

![alt text](../Assets/vs-code-remote-edit.png "VS Code Remote SSH Edit")

## [NEXT: Module 04 - Enabling Capabilities on the RPi](../Module04/README.md)