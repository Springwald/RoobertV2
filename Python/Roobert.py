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
#     ##################################
#     # Roobert master control program #
#     ##################################
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

import os, sys
from os.path import abspath

import time
from random import randrange, uniform
import math
import pygame

from DanielsRasPiPythonLibs.hardware.PCF8574 import PCF8574
from DanielsRasPiPythonLibs.hardware.I2cIoExpanderPcf8574 import I2cIoExpanderPcf8574
from DanielsRasPiPythonLibs.speech.SpeechOutput import SpeechOutput

from Camera import Camera
from FaceGfx import FaceGfx
from Camera import Camera

from hardware.HardwareDevices import HardwareDevices
from hardware.Arms import Arms
from hardware.Neck import Neck
from _thread import start_new_thread

from BehaveDemo import BehaveDemo


import atexit

class Roobert:

	_hardwareDevices 				= None
	_faceGfx						= None
	_speechOutput					= None
	_camera							= None
	
	_body_leds						= None
	
	_ended							= False
	_released						= False

	showFace						= True
	_lastFace						= time.time() - 1000
	
	_rotate							= 1

	def __init__(self):

		self._hardwareDevices = HardwareDevices.singleton()
		self._speechOutput = SpeechOutput(soundcard="plughw:1", voice="-vmb-de6"); 
		self._faceGfx = FaceGfx(self.showFace)
		self._camera = Camera() 
		self._hardwareDevices.arms.SetArm(gesture=Arms._armHanging, left=True);
		self._hardwareDevices.arms.SetArm(gesture=Arms._armHanging, left=False);
		
	def Release(self):
		if (self._released == False):
			self._released = True
			print ("shutting down roobert")
			
			# shut down other treads
			
			if (self._camera != None):
				self._camera.Release()
				
			if (self._faceGfx != None):
				self._faceGfx.Release()

			if (self._hardwareDevices != None):
				self._hardwareDevices.Release()
				
			self._ended = True

	def __del__(self):
		self.Release()
		
def exit_handler():
	roobert.Release()

if __name__ == "__main__":
	
	roobert = Roobert()
	atexit.register(exit_handler)
	demo = BehaveDemo(roobert._hardwareDevices, roobert._speechOutput, roobert._faceGfx, roobert._camera)
	demo.demo()

    





