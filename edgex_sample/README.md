# EdgeX Foundry on Raspberry Pi

## Intro

This tutorial explains the different steps necessary to run EdgeX Foundry on a Raspberry Pi. 
In order to complete this tutorial you will need the following items:

* Raspberry Pi 3B+
* Micro SD card (we used a 16GB card)
* HDMI cable
* Keyboard
* Monitor
* Ethernet cable (optional)


Furthermore, we will need to install a 64-bit OS on the Raspberry PI as EdgeX is dependent on MongoDB, which requires 64-bit. This means that you will not be able to use the popular Raspbian OS, since Raspbian is 32-bit.

## Step 1: Setting Up the Raspberry Pi

First, you will need to flash **Ubuntu Server ARM64** on your Micro SD card.

1. Download the ISO file for Ubuntu Server found here: https://ubuntu.com/download/server/arm. *Make sure you downloaded the 64-bit version as EdgeX will not run on 32-bit.*

2. Download Balena Etcher, which will allow you to flash the Ubuntu ISO image on you SD card: https://www.balena.io/etcher/

3. Insert you SD card in the SD card reader.

4. Open Balena Etcher and follow the instructions. Once Balena Etcher is done flashing, eject the SD card. 

5. Insert the Micro SD card into the Raspberry Pi and turn it on.

6. Follow the instructions on the screen to finish setting the operating system.

## Step 2: Installing Go, Docker

1. Install go:

This step is necessary only if you wish to build your own device service locally. Alternatively, you can use one of the devices service provided by the EdgeX community in the docker-compose file. 

```
$ sudo snap install --classic go

// Reboot is required to complete the installation
$ sudo reboot
```

2. Install Docker:

```
$ sudo apt-get update
$ sudo apt install docker.io
$ sudo systemctl start docker
$ sudo systemctl enable docker

// check if installation was successful:
$ docker —version
```

## Step 3: Installing Docker Compose

Installing Docker Compose on ARM is not trivial. The easiest way is to install via pip. 

1. Install pip3

```
$ sudo apt-get install python3-pip
```

2. Docker Compose has two dependencies that are not shipped with Ubuntu Server ARM64:  `libssl-dev` and `libffi-dev`. You will need to install them:

```
$ sudo apt-get install libssl-dev libffi-dev
```

3. Install Docker Compose:

```
$ pip3 install docker-compose
```

## Step 4: Run EdgeX

At this point in the tutorial, you have all the prerequisites necessary to run EdgeX. You will need to download the ARM64 compose file and start it.

1. Download the compose file found in this directory:

```
$ wget https://github.com/vmware-samples/automotive-iot-samples/edgex_sample/docker-compose.yml
```

2. Run it:

```
$ docker-compose up -d
```

## Step 5: Build and run device-gps (optional)

We contributed a GPS device service as part of our Automotive IoT Sample work. The device service contains a mock data file to allow users to use the device service without buying a GPS device. 

1. You will first need to create a swap file, as the Raspberry Pi does not have enough RAM to build the device service. More info here: https://linuxize.com/post/how-to-add-swap-space-on-ubuntu-18-04/.

```
$ sudo fallocate -l 1G /swapfile
$ sudo chmod 600 /swapfile
$ sudo mkswap /swapfile
$ sudo swapon /swapfile
```

2. Clone the `device-gps` repo and build:

```
$ git clone github.com/edgexfoundry-holding/device-gps
$ cd device-gps
$ make build
```

3. At this point, you are ready to start the GPS Device Service.

```
$ cd cmd/
$ ./device-gps
```

Kill the device service with `ctrl + c`.
