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
from Neck import Neck
from RgbLeds import RgbLeds

import atexit

class HardwareDevices():

	_bodyLeds							= None

	_arms								= None
	_neck								= None
	
	_servoManager						= None
	_servos								= None
	
	__singleton							= None
	_released 							= False

	@staticmethod
	def singleton():
		if (HardwareDevices.__singleton == None):
			HardwareDevices.__singleton = HardwareDevices()
		return HardwareDevices.__singleton

	@property
	def arms(self):
		return self._arms 
		
	@property
	def neck(self):
		return self._neck 
	
	@property
	def BodyLeds(self):
		return self._bodyLeds 

	def __init__(self):
		self._servos = LX16AServos();
		self._servoManager = SmartServoManager(lX16AServos=self._servos, ramp=0, maxSpeed=1)
		self._arms = Arms(self._servoManager)
		self._neck = Neck(self._servoManager)
		self._servoManager.Start()
		self._neck.SetLeftRight(0)
		self._neck.SetUpDown(0)
		
		self._bodyLeds = RgbLeds([
					my_path + '/../Gfx/Body/hearth2.gif', 
					my_path + '/../../RoobertGifs/e8nZC.gif',
					my_path + '/../../RoobertGifs/U9LwW86.gif',
					my_path + '/../../RoobertGifs/Spin_Toad.gif',
					my_path + '/../../RoobertGifs/haleye.gif',
					my_path + '/../../RoobertGifs/Yoshi_render.gif'
					])

	def Release(self):
		if (self._released == False):
			self._released = True
			print("releasing hardware devices")

			if (self._bodyLeds != None):
				self._bodyLeds.Release()
				
			if (self._arms != None):
				self._arms.Release()
				
			if (self._neck != None):
				self._neck.Release()
				
			if (self._servoManager != None):
				self._servoManager.Release()
				
			if (self._servos != None):
				self._servos.Release()
				

	def __del__(self):
		self.Release()

def exit_handler():
	devices.Release()


if __name__ == "__main__":
	
	devices = HardwareDevices.singleton()
	
	atexit.register(exit_handler)

	devices.arms.WaitTillTargetsReached();
	
	time.sleep(5)

	devices.Release()

