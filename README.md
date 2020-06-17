# Raspberry Pi "Protocol Translation" Gateway for Azure IoT Central

![alt text](./Assets/raspberry-pi-4-hero-shot.png "Project Hero Shot") 

## Overview
This repository is part of a training and project series for Azure IoT Central. The name of the series is "Raspberry Pi Gateway and Arduino Nano BLE Devices for Azure Iot Central" and is located at...

[LINK: Training & Project Site for Raspberry Pi Gateway and Arduino Nano BLE Devices for Azure Iot Central](http://www.hackinmakin.com/Raspberry%20Pi%20Gateway%20and%20BLE/index.html)

This project will enable a Raspberry Pi to act as a "Protocol Translation" Gateway connected to Azure IoT Central and send Telemerty on behalf of of the Devices we have created for this project. 

![Protocol Translation Gateway](./Assets/gateway-protocol-lrg.png)

You may wan go back and do the projects for the Nano BLE Devices if you landed here out of sequence.

### Arduino Nano BLE 33 for Azure IoT Central
Here is the link to the Github for the project "Arduino Nano BLE 33 for Azure IoT Central", you should also start and follow up to this point in the training link reference at the start of the Readme.

[LINK: Arduino Nano BLE 33 for Azure IoT Central](https://github.com/Larouex/IoTCNanoBLE33)

### Arduino Nano BLE 33 SENSE for Azure IoT Central
Here is the link to the Github for the project "Arduino Nano BLE 33 SENSE for Azure IoT Central", you should also start and follow up to this point in the training link reference at the start of the Readme.

[LINK: Arduino Nano BLE 33 SENSE for Azure IoT Central](https://github.com/Larouex/IoTCNanoBLESense33)

## Setting up Your Development Toolchain
The code in this repository depends on Ardunio, Visual Studio Code and PlatformIO.

### Your Local Machine
The development "toolchain" refers to all of the various tools, SDK's and bits we need to install on your machine to facilitate a smooth experience developing our BLE devices and the Raspberry Pi Gateway device. Our main development tool will be Visual Studio code. It has dependencies on tools from Arduino and other open source projects, but it will be the central place where all our development will occur making it easy to follow along  regardless of which operating system you are working on.

| - | Install These Tools |
|---|---|
| ![Python](./Assets/python-icon-100.png) | [LINK: Python 3 Installation Page](https://www.python.org/downloads/) - Pyhon is the programming language we will use to build applications for the Raspberry Pi. |
| ![Visual Studio Code](./Assets/vs-code-icon-100.png) | [LINK: Visual Studio Code Installation Page](https://code.visualstudio.com/download) - Visual Studio Code is a lightweight but powerful source code editor which runs on your desktop and is available for Windows, macOS and Linux. This is the IDE we will use to write code and deploy to the our BLE Devices and the Raspberry Pi Gateway.  |
| ![Docker](./Assets/docker-icon-100.png) | [LINK: Docker Desktop Install](https://www.docker.com/products/docker-desktop) - Docker Desktop is an application for MacOS and Windows machines for the building and sharing of containerized applications. |

Assuming everything is installed and working, Open Visual Studio Code and open the folder you cloned this repository into. You should see:

![Start](./Assets/vscode-startup-with-platformio.png)


## Setup the Development Toolchain

### Install Git
Git is the tool we use for version control and management of software assets. Our workshop will use it to clone the modules and also to save anything if you want

[LINK: Git Installation Page](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Install Visual Studio Code
This is the IDE we will use to write code, deploy to the RPi, etc. 

[LINK: Visual Studio Code Installation Page](https://code.visualstudio.com/download)

### Install Python
Pyhon is the programming language we will use to build applications for the Raspberry Pi

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

![alt text](./Assets/vs-code-python-sml.png.png "VS Code Python")

![alt text](./Assets/vs-code-remote-ssh-sml.png "VS Code Remote SSH")

![alt text](./Assets/vs-code-remote-edit-sml.png "VS Code Remote SSH Edit")

![alt text](./Assets/vs-code-dcoker-sml.png "VS Code Dcoker")

### Install the following for Python Development
These are a set of tools we will use to develop our apps on the Raspberry Pi. You can open the Extensions sidebar with "Shift+Ctrl+X) or click the icon in the side navigator bar.

[LINK: Azure IoT EdgeHub Dev Tool](https://pypi.org/project/iotedgehubdev/)
