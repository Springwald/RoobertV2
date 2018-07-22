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
#     ##############################################
#     # Roobert hardware device factory and config #
#     ##############################################
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

from __future__ import division
import time, os, sys

my_file = os.path.abspath(__file__)
my_path ='/'.join(my_file.split('/')[0:-1])

sys.path.insert(0,my_path + "/" )

sys.path.insert(0,my_path + "/../DanielsRasPiPythonLibs/multitasking" )
sys.path.insert(0,my_path + "/../DanielsRasPiPythonLibs/hardware" )

from MultiProcessing import *
from array import array
from SharedInts import SharedInts
from SharedFloats import SharedFloats
from LX16AServos import LX16AServos
from SmartServoManager import SmartServoManager
from Arms import Arms

#from I2cIoExpanderPcf8574 import I2cIoExpanderPcf8574
#from RelaisI2C import RelaisI2C
#from Roomba import Roomba
#from PowerManagement import PowerManagement
#from RgbLeds import RgbLeds
#from HandAndArm import HandAndArm

import atexit

class HardwareDevices():

	#_roomba								= None
	#_body_leds							= None
	#_power_management					= None
	
	_arms								 = None
	
	#_handArmRight						= None
	#_handArmLeft						= None
	
	#_relais 							= None
	
	#power_relais_adress					= 0x39
	#power_relais_bit_arms_right 		= 5
	#power_relais_bit_arms_left 			= 7
	#power_relais_bit_sens3d_servos 		= 6
	
	_servoManager						= None
	
	__singleton							= None
	_released 							= False

	@staticmethod
	def singleton():
		if (HardwareDevices.__singleton == None):
			HardwareDevices.__singleton = HardwareDevices()
		return HardwareDevices.__singleton

	#@property
	#def roomba(self):
	#	if (self._roomba == None):
	#		self._roomba = Roomba()
	#	return self._roomba

	#@property
	#def body_leds(self):
	#	if (self._body_leds == None):
	#		self._body_leds = RgbLeds(self.power_management)
	#	return self._body_leds

	#@property
	#def relais(self):
	#	if (self._relais == None):
	#		self._relais = RelaisI2C(I2cIoExpanderPcf8574(address=self.power_relais_adress, useAsInputs=False))
	#	return self._relais

	#@property
	#def power_management(self):
	#	if (self._power_management == None):
	#		self._power_management = PowerManagement(self.roomba)
	#	return self._power_management

	#@property
	#def hand_arm_right(self):
	#	if (self._handArmRight == None):
	#		self._handArmRight = HandAndArm(rightArm = True, i2cAdress=0x40, busnum=1, power_relais = self.relais, relais_bit=self.power_relais_bit_arms_right)
	#	return self._handArmRight

	@property
	def arms(self):
		return self._arms

	def __init__(self):
		servos = LX16AServos();
		self._servoManager = SmartServoManager(lX16AServos=servos, ramp=0, maxSpeed=1)
		self._arms = Arms(self._servoManager)
		self._servoManager.Start()

	def Release(self):
		if (self._released == False):
			self._released = True
			print("releasing hardware devices")

			#if (self._body_leds != None):
			#	self._body_leds.Release()
				
			if (self._arms != None):
				self._arms.Release()
				
			#if (self._handArmLeft != None):
			#	self._handArmLeft.Release()
				
			#if (self._power_management != None):
			#	self._power_management.Release()
				
			#if (self._roomba != None):
			#	self._roomba.Release()

			#if (self._relais != None):
			#	self._relais.Release()

	def __del__(self):
		self.Release()

def exit_handler():
	devices.Release()


if __name__ == "__main__":
	
	devices = HardwareDevices.singleton()
	
	atexit.register(exit_handler)

	#print ("roomba: " + str(devices.roomba))
	#print ("body_leds: " + str(devices.body_leds))
	#print ("power_management: " + str(devices.power_management))
	
	#devices.arms.SetArm(gesture=Arms._strechSide, left=True);
	devices.arms.WaitTillTargetsReached();

	devices.Release()

