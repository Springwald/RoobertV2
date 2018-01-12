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

from hardware.PCF8574 import PCF8574
from hardware.I2cIoExpanderPcf8574 import I2cIoExpanderPcf8574
from NeckLeftRight import NeckLeftRight
from NeckUpDown import NeckUpDown
from SpeechOutput import SpeechOutput
#from HandAndArm import HandAndArm
from FaceGfx import FaceGfx
from Camera import Camera
#from Roomba import Roomba
#from RgbLeds import *
#from RelaisI2C import RelaisI2C
from hardware.HardwareDevices import HardwareDevices
from _thread import start_new_thread

import atexit

class Roobert:

	I2cIoExpanderPcf8574Adress		= 0x38
	MotorLeftRightAdress			= 0x0f
	MotorUpDownAdress				= 0x3e
	sens_3d_servo_adress			= 0x46
	
	_hardwareDevices 				= None
	
	FirstI2cIoExpanderPcf8574		= None
	_roomba							= None
	_faceGfx						= None
	_neckLeftRight					= None
	_neckUpDown						= None
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

		self.FirstI2cIoExpanderPcf8574 = I2cIoExpanderPcf8574(self.I2cIoExpanderPcf8574Adress, useAsInputs=True)
		endStop = self.FirstI2cIoExpanderPcf8574
		
		self._neckUpDown = NeckUpDown(I2cIoExpanderPcf8574(self.MotorUpDownAdress, useAsInputs=False), endStop)
		self._neckUpDown.targetPos =int(self._neckUpDown.MaxSteps * 0.65)
		
		self._neckLeftRight = NeckLeftRight(self.MotorLeftRightAdress, endStop)
		self._neckLeftRight.targetPos = int(self._neckLeftRight.MaxSteps *0.49)

		self._speechOutput = SpeechOutput()
				
		self._faceGfx = FaceGfx(self.showFace)
				
		#self._body_leds	= self._hardwareDevices.body_leds
		
		self._camera = Camera() 		

		
	def Release(self):
		if (self._released == False):
			self._released = True
			print ("shutting down roobert")
			
			# shut down other treads
			
			if (self._camera != None):
				self._camera.Release()
				
			if (self._faceGfx != None):
				self._faceGfx.Release()
				
			if (self._neckUpDown != None):
				self._neckUpDown.Release()
			if (self._neckLeftRight != None):
				self._neckLeftRight.Release()
				
			if (self._hardwareDevices != None):
				self._hardwareDevices.Release()
				
			self._ended = True
			
	def Update(self):
		if (self.showFace== True):
			self._faceGfx.speaking = self._speechOutput.speaking
			
	def RandomHeadMovement(self):
		if (self._neckLeftRight.targetReached==True):
			movementArea = int(self._neckLeftRight.MaxSteps / 2)
			self._neckLeftRight.targetPos =randrange(0,movementArea)
		if (self._neckUpDown.targetReached==True):
			movementArea = int(self._neckUpDown.MaxSteps / 2)
			self._neckUpDown.targetPos =randrange(0, movementArea)
			
	def Greet(self):
		print("greetings!");
		self._speechOutput.Speak("Guten Tag.")
		self._speechOutput.Speak("Mein Name ist Robert")
		self._hardwareDevices.hand_arm_right.gestureGreet()
		while (self._speechOutput.speaking==True):
			time.sleep(1)
		self._speechOutput.Speak("Ich freue mich, Sie kennen zu lernen")
		self._hardwareDevices.hand_arm_right.gesturePointForward()
		while (self._speechOutput.speaking==True):
			time.sleep(1)
		self._hardwareDevices.hand_arm_right.home()
			
	def drive_avoiding_obstacles(self):
		#print (self._sens3d.nearest)
		if (self._sens3d.nearest > 40):
			self._roomba.move(3)
			#time.sleep(0.5)
		else:
			if (self._sens3d.x_weight < 0.45):
				self._roomba.rotate(-20)
			else:
				if (self._sens3d.x_weight > 0.55):
					self._roomba.rotate(20)
				else:
					self._roomba.rotate(180 * self._rotate)
					self._rotate = self._rotate * -1
					
	def RotateDemoForPhoto(self):
		self._hardwareDevices.hand_arm_right.gesturePointForward();
		#self._hardwareDevices.roomba.rotate(10);
		
					
	def FollowFace(self):
		faceX = self._camera.posXFace
		faceY = self._camera.posYFace
		timeSinceLastFace = time.time() - self._lastFace 
		if (faceX != -1 and faceY != -1):
			# oh, there is a face
			if (timeSinceLastFace > 60):
				# see a face after a long time: say hello!
				start_new_thread(self.Greet,())
				#self.Greet()
				a=0
				
			self._lastFace = time.time()
			self._camera.ResetFace()
			diffX = (faceX - 0.5) 
			diffY = (faceY - 0.5) 
			if (math.fabs(diffX ) > 0.1):
				self._neckLeftRight.targetPos = self._neckLeftRight.targetPos - int(diffX * 100)
			if (math.fabs(diffY ) > 0.1):
				self._neckUpDown.targetPos = self._neckUpDown.targetPos - int(diffY * 100)
			
			self._faceGfx.SetEyePos(faceX,faceY)
		else:
			# there is no face
			if (timeSinceLastFace > 20):
				# long time no face seen
				self._faceGfx.SetEyePos(0.5,0.5)
			
	def __del__(self):
		self.Release()
		
def exit_handler():
	roobert.Release()

if __name__ == "__main__":
	
	roobert = Roobert()
	
	atexit.register(exit_handler)
	
	ended = False
	
	roobert.Update()
	#roobert._handArm.setArm(100,100,100)
	
	#roobert._speechOutput.Speak("Hallo")
	
	#roobert.Greet();
	
	while ended == False:
		
		time.sleep(0.5)
		
		roobert.Update()
		
		#roobert.RotateDemoForPhoto();
		
		#roobert.RandomHeadMovement()
		
		roobert.FollowFace()
		#roobert.drive_avoiding_obstacles()

		events = pygame.event.get()
	
		for event in events:
			if event.type == pygame.MOUSEBUTTONUP:
				ended = True 
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					ended = True 
				if event.key == pygame.K_TAB:
					#roobert.Greet()
					#start_new_thread(roobert.Greet,())
					a=0

        
        
        
        

    





