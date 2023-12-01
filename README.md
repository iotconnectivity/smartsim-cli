# smartsim-cli

A `cli` tool to **simulate IoT SIM requests**. This tool interacts with  IoT Platform.

## Table of Contents

- [Description](#description)
- [Usage](#usage)
- [Installation](#installation)
- [Roadmap](#roadmap)
- [Support](#support)
- [Contributing](#contributing)

## Description

Simulate the behaviour of IoT SIM embedded applications. Learn how the embedded applications interacts with the IoT Platform. IoT SIM includes the following embedded apps:

* **Zero Touch Provisioning**: IoT SIM will download your device configuration from cloud.
* **SIM2Cloud Encryption**: IoT SIM will upload your device telemetry to cloud.

The embedded apps uses TLSv1.3 (PresharedKey) for a secure interaction with IoT Platform.

Do you want to see real case scenarios? Check our Arduino tutorials 👇

👉 **Arduino Nano IoT Board**: Turning Arduino Nano into an IoT board with IoT SIM and **SIM2Cloud Encryption** application: https://create.arduino.cc/projecthub/kostiantynchertov/tls-1-3-for-arduino-nano-649610

👉 **On Boarding an Arduino MKR GSM 1400**: Auto-configuring Arduino GSM boards with IoT SIM and **Zero Touch Provisioning**: https://create.arduino.cc/projecthub/kostiantynchertov/tls-1-3-for-arduino-nano-649610

## Usage

In order to use this script you need, in advance, to request from IoT Platform:

* TLSPROXY_KEYENC: The Server Key to encrypt pre-shared keys.
* API_USER: Your username for IoT Platform.
* API_PASS: Your password for IoT Platform.

We recommend you to use the `./config.yml` file to store those. The `smartsim-cli` tool accepts settings from environment variables or defaults to `./config.yml` file. Command line arguments prevail over `./config.yml` or the environment variables.

### Getting help

First check `smartsim-cli` integrated help:

```
usage: smartsim-cli [-h] {psk,device,simulate} ...

A cli tool to manage IoT Sm@rtSIM SIM keys and simulate ZTP and STC requests against a cloud server.

positional arguments:
  {psk,device,simulate}
                        commands available
    psk                 Manage PSK (preshared-key) for physical and simulated SIM
    device              Add device config or get device data
    simulate            Simulate Zero-Touch-Provisioning or SIM2Cloud-Encryption requests

optional arguments:
  -h, --help            show this help message and exit
```

### Generate and upload a PreShared Key

As optional first step you may change the PreShared Key in your SIM and in the server. To run this command the SIM shall be inserted into a PCSC-compatible reader

```
$ python3 smartsim-cli psk setkey -k 404142434445464748494a4b4c4d4e4f
2021-07-05 15:50:32,101 - SmartSIM - INFO - PSK installed on SIM correctly.
2021-07-05 15:50:50,061 - SmartSIM - INFO - PSK Updated for 894450250918638964
2021-07-05 15:50:50,697 - SmartSIM - INFO - Save the key later use: 404142434445464748494a4b4c4d4e4f
2021-07-05 15:50:51,351 - SmartSIM - INFO - You may want to store it on the config file: ./config.yml
```

### Simulate an IoT SIM SIM2Cloud-Encryption request

Well, that was a simple HTTPS POST request to the API, but now let's upload a random json payload to cloud, through the TLSv1.3-PSK proxy. In a real case scenario the device can invoke the SIM to do this:

```
$ python3 smartsim-cli simulate stc -i 894450061193083409 -d mydevice1 -k 585b354a4c4a52645d372b2c6a494b3c -j '{"temperature": "21"}'
2021-05-12 18:40:59,801 - SmartSIM - INFO - TLS1.3-PSK session stablished. Initialising operation
2021-05-12 18:36:33,774 - SmartSIM - INFO - b'{"temperature":"21","iccid":"894450061193083409","deviceid":"mydevice1"}'
```

### Simulate an IoT SIM Zero Touch Provisioning request

Now let's add a configuration for the device:

```
$ python3 smartsim-cli device addconfig -i 894450061193083409 -d mydevice1 -j '{"apn":"apaclte-apn", "platform":"iot.devicemanagement.com"}'
2021-05-12 18:38:25,605 - SmartSIM - INFO - Configuration added for device mydevice1 with sim 894450061193083409 on the cloud
2021-05-12 18:38:25,606 - SmartSIM - INFO - {"configuration": {"version": "20210512-183824", "config": {"apn": "data641003", "platform":"iot.devicemanagement.com"}}}
```

And this configuration will be ready on the cloud. In a real case scenario, the device will just require the sim card to download this configuration.

```
$ python3 smartsim-cli simulate ztp -i 894450061193083409 -d mydevice1 -k 585b354a4c4a52645d372b2c6a494b3c
2021-05-12 18:40:59,801 - SmartSIM - INFO - TLS1.3-PSK session stablished. Initialising operation
2021-05-12 18:40:59,802 - SmartSIM - INFO - b'{"configuration": {"version": "20210512-183824", "config": {"apn": "data641003", "platform":"iot.devicemanagement.com"}}}'
```

## Installation

*Note: The `smartsim-cli` tool has been implemented with `Python3`. Before starting, make sure you have python3 installed.*

We recommend the use of a virtual environment, but this is an optional first step:

```
~/smartsim-cli$ python3 -m venv .env
~/smartsim-cli$ source .env/bin/activate
```

And now install dependencies:

```
~/smartsim-cli$ python3 -m pip install -r requirements.txt
```

## Roadmap

* Full CRUD methods for IoT Platform (some are still not implemented on `smartsim-cli`).