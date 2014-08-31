#!/usr/bin/env python

# Copyright (c) 2014, Paavo Leinonen <paavo.leinonen@iki.fi>
# This file is distributed under the MIT License.

# Requirements for Raspberry Pi:
#
# Install python-smbus packet:
# apt-get install python-smbus
# Add following lines to /etc/modules:
# i2c-bcm2708
# i2c-dev
#
# Other enviroments will require other modules 

import struct
import time

TCN75A_ADDRESS_BASE=0x48
TCN75A_ADDRESS_MASK=0x07

REG_TEMP=0x00
REG_CONFIG=0x01

CONFIG_ONE_SHOT=(1<<7)
CONFIG_12BIT=(3<<5)
CONFIG_SHUTDOWN=(1<<0)

OK_POLL_INTERVAL=1/5.
OK_POLL_MAX=5

def temperature(bus,address=0):
	# create chip address
	address=TCN75A_ADDRESS_BASE|(address&TCN75A_ADDRESS_MASK)

	# trigger single conversion
	bus.write_byte_data(address,REG_CONFIG,CONFIG_ONE_SHOT|CONFIG_12BIT|CONFIG_SHUTDOWN)

	# wait for conversion to finish
	convok=False
	for x in range(OK_POLL_MAX):
		time.sleep(OK_POLL_INTERVAL)
		if not (bus.read_byte_data(address,REG_CONFIG)&CONFIG_ONE_SHOT):
			convok=True
			break

	if not convok:
		raise Exception("Temperature conversion timed out")

	# read temperature register
	value=bus.read_word_data(address,REG_TEMP)
	# swap bytes and convert to 2 complement
	rawtemp=struct.unpack(">h",struct.pack("<H",value))
	# scale to degrees C
	temp=rawtemp[0]/256.

	return temp

def main():
	import smbus
	print("Scanning all i2c busses..")
	found=False
	busnum=0
	while True:
		try:
			bus=smbus.SMBus(busnum)
		except:
			break
		for a in range(TCN75A_ADDRESS_MASK+1):
			try:
				print("bus %d, address %d: %f"%(busnum,a,temperature(bus,a)))
				found=True
			except:
				pass
		busnum+=1
	if not found:
		if busnum==0:
			print("No i2c busses found")
		else:
			print("No sensors found")


if __name__=="__main__":
	main()
