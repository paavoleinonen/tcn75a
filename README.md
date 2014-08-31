tcn75a
======

Python script for reading TCN75A temperature sensor using python primarily on Raspberry Pi platform.

temperature(bus,address) function initiates single-shot temperature conversion with maximum resolution 
and returns the result. Errors are not handled gracefully.

## Requirements for Raspberry Pi:

* Install python-smbus packet:
  * apt-get install python-smbus
* Add following lines to /etc/modules:
  * i2c-bcm2708
  * i2c-dev

Other enviroments will require other module.

## Usage

Eiher execute the script with appropriate permissions or import it into larger project.

Example result:
````
pi@raspberrypi ~/tcn75a $ sudo ./tcn75a.py
Scanning all i2c busses..
bus 1, address 0: 28.062500
bus 1, address 1: 28.000000
````

