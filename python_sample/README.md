

# automotive-iot-samples

## Overview

This repository contains a sample autmotive edge-based IoT application. The application is comprised of the "edge" and "cloud or data center" parts and organized accordingly in two top level sub-directories.  `car_edge/` contains the code that will live on the Raspberry PI, in the car. Note, you could try it out on your laptop or any other device that has bluetooth, but for our purposes here we shall assume it is a Raspberry PI. This Raspberry Pi has to be connected to a GPS sensor and an ODB sensor in order to collect the data. `cloud_API_endpoint/` contains the different endpoints running in the cloud. More information on each part can be found in their respective subdirectories.

## Try it out

Instructions on how to run each part of the application can be found in each subdirectory.

### Prerequisites

We used a Raspebrry PI 3B+ to act as an edge gateway living in the car. To this RPI are connected two sensors: a USB GPS sensor and a Bluetooth ODBII sensor. The code in car edge will automatically connect to them and react drive data.

## Documentation

## Releases & Major Branches

## Contributing

The automotive-iot-samples project team welcomes contributions from the community. If you wish to contribute code and you have not
signed our contributor license agreement (CLA), our bot will update the issue when you open a Pull Request. For any
questions about the CLA process, please refer to our [FAQ](https://cla.vmware.com/faq). For more detailed information,
refer to [CONTRIBUTING.md](CONTRIBUTING.md).

## License
