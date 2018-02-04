#!/usr/bin/env python

#      Roobert V2 - second version of home robot project
#      ________            ______             _____ 
#      ___  __ \______________  /_______________  /_
#      __  /_/ /  __ \  __ \_  __ \  _ \_  ___/  __/
#      _  _, _// /_/ / /_/ /  /_/ /  __/  /   / /_  
#      /_/ |_| \____/\____//_.___/\___//_/    \__/
#
#     Project website: http://roobert.springwald.de
#
#     ##############################
#     # LX-16A servo communication #
#     ##############################
#
#     Licensed under MIT License (MIT)
#
#     Copyright (c) 2018 Daniel Springwald | daniel@springwald.de
#
#     Permission is hereby granted, free of charge, to any person obtaining
#     a copy of this software and associated documentation files (the
#     "Software"), to deal in the Software without restriction, including
#     without limitation the rights to use, copy, modify, merge, publish,
#     distribute, sublicense, and/or sell copies of the Software, and to permit
#     persons to whom the Software is furnished to do so, subject to
#     the following conditions:
#
#     The above copyright notice and this permission notice shall be
#     included in all copies or substantial portions of the Software.
#
#     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#     OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#     THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#     FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#     DEALINGS IN THE SOFTWARE.

from serial import Serial
from time import sleep

SerialPort = Serial("/dev/ttyUSB0", baudrate=115200)
SerialPort.setDTR(1)

CMD_START_BYTE = 0x55
CMD_SERVO_MOVE_TIME_WRITE_BYTE = 1
CMD_READ_DATA_BYTE = 3
CMD_TEMP_READ_BYTE = 26
CMD_VOLT_READ_BYTE = 27
CMD_POS_READ_BYTE  = 28


TX_DELAY_TIME = 0.00002


def checksumWithLength(id, byteArry):
	check = id + len(byteArry)+2
	for val in byteArry:
		check = check + val
	check = bytes([(~(check))&0xff])
	return check[0]
	
def checksum(id, byteArry):
	check = id
	for val in byteArry:
		check = check + val
	check = bytes([(~(check))&0xff])
	return check[0]

def moveServo(id,speed,position):

	if(position < 0):
		position = 0
	if(position > 1000):
		position = 1000
	if(speed < 0):
		speed = 0
	if(speed > 10000):
		speed = 10000

	p = [position&0xff, position>>8]
	s = [speed&0xff, speed>>8]
    
	command = bytes([CMD_SERVO_MOVE_TIME_WRITE_BYTE, p[0], p[1], s[0], s[1]]);

	SerialPort.write(bytes([CMD_START_BYTE, CMD_START_BYTE, id, len(command)+2]))
	SerialPort.write(command)
	SerialPort.write(bytes([checksumWithLength(id, command)]))
    
	sleep(TX_DELAY_TIME)
	return True


def ReadTemperature(id):

	SerialPort.flushInput()

	command = bytes([CMD_READ_DATA_BYTE, CMD_TEMP_READ_BYTE]);
	
	SerialPort.write(bytes([CMD_START_BYTE, CMD_START_BYTE, id]))
	SerialPort.write(command)
	SerialPort.write(bytes([checksum(id, command)]))

	sleep(TX_DELAY_TIME)
	
	sleep(0.1)
	retry=0
	while retry<100:
		value =SerialPort.read(1)
		if value != '':
			for pos in range(0, 7):
				if pos == 5:
					tempture = int(ord(value))
					return tempture
				value=SerialPort.read(1)
		retry+=1
		sleep(0.1)


def ReadVolt(id):

	SerialPort.flushInput()
	
	command = bytes([CMD_READ_DATA_BYTE, CMD_VOLT_READ_BYTE]);
	
	SerialPort.write(bytes([CMD_START_BYTE, CMD_START_BYTE, id]))
	SerialPort.write(command)
	SerialPort.write(bytes([checksum(id, command)]))

	sleep(0.1)
	retry=0
	while retry<100:
		value=SerialPort.read(1)
		if value != '':
			for pos in range(0, 8):
				if pos == 5:
					volt1 = int(ord(value)) 
				if pos == 6:
					volt2 = int(ord(value))
					volt2 =  volt1 + 256*volt2 
					return volt2
				value=SerialPort.read(1)
		retry+=1
		sleep(0.1)

def ReadPos(id):

	SerialPort.flushInput()
	
	command = bytes([CMD_READ_DATA_BYTE, CMD_POS_READ_BYTE]);
	
	SerialPort.write(bytes([CMD_START_BYTE, CMD_START_BYTE, id]))
	SerialPort.write(command)
	SerialPort.write(bytes([checksum(id, command)]))
	
	sleep(0.1)
	retry=0
	while retry<100:
		value=SerialPort.read(1)
		if value != '':
			for pos in range(0, 8):
				if pos == 5:
					pos1 = int(ord(value)) 
				if pos == 6:
					pos2 = int(ord(value))
					pos2 =  pos1 + 256*pos2 
					return pos2
				value=SerialPort.read(1)
		retry+=1
		sleep(0.1)

moveServo(id=1,speed=10,position=20)
sleep(1)

#for pos in range(0, 5):
#	moveServo(id=1,speed=2000,position=585+100*pos)
#	sleep(0.1)

print (str(ReadTemperature(1))+"°C")
print (str(ReadVolt(1))+" mVolt")
print (str(ReadPos(1))+" pos")

