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
#     ###########################################
#     # demo behavoir e.g. for maker faire 2018 #
#     ###########################################
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

import atexit

class BehaveDemo:


	_hardwareDevices 				= None
	_faceGfx						= None
	_speechOutput					= None
	_camera							= None
	
	_ended							= False
	_released						= False

	showFace						= True
	_lastFace						= time.time() - 1000
	
	_rotate							= 1

	def __init__(self, hardwareDevices, speechOutput, faceGfx, camera):

		self._hardwareDevices = hardwareDevices
		self._speechOutput = speechOutput
		self._faceGfx = faceGfx
		self._camera = camera
		
		self._hardwareDevices.arms.SetArm(gesture=Arms._armHanging, left=True);
		self._hardwareDevices.arms.SetArm(gesture=Arms._armHanging, left=False);
		
	def Release(self):
		if (self._released == False):
			self._released = True
			self._ended = True
			
	def demo(self):
		ended = False;
		
		#self.Greet()
		
		while ended == False:
			
			self.Update()
			
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

	def Update(self):
		self.UpdateFace()
		self.FollowFace()

	def UpdateFace(self):
		if (self.showFace == True):
			self._faceGfx.speaking = self._speechOutput.IsSpeaking();

	def RandomHeadMovement(self):
		if (self._neckLeftRight.targetReached==True):
			movementArea = int(self._neckLeftRight.MaxSteps / 2)
			self._neckLeftRight.targetPos =randrange(0,movementArea)
		if (self._neckUpDown.targetReached==True):
			movementArea = int(self._neckUpDown.MaxSteps / 2)
			self._neckUpDown.targetPos =randrange(0, movementArea)
			
	def Greet(self):
		print("greetings!");
		self._hardwareDevices.arms.SetArm(gesture=Arms._stretchSide, left=True);
		self._speechOutput.Speak("Guten Tag.")
		while (self._speechOutput.IsSpeaking()==True):
			time.sleep(0.1)
		self._speechOutput.Speak("Mein Name ist Robert", wait=False)
		while (self._speechOutput.IsSpeaking()==True):
			time.sleep(0.1)
		self._hardwareDevices.arms.SetArm(gesture=Arms._armHanging, left=True);
		self._hardwareDevices.arms.WaitTillTargetsReached();
		while (self._speechOutput.IsSpeaking()==True):
			time.sleep(1)
		self._speechOutput.Speak("Ich freue mich, Sie kennen zu lernen")
		#self._hardwareDevices.hand_arm_right.gesturePointForward()
		while (self._speechOutput.IsSpeaking()==True):
			time.sleep(0.1)


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
			if (math.fabs(diffX) > 0.1):
				self._hardwareDevices.neck.SetLeftRight(self._hardwareDevices.neck.GetLeftRight() - int(diffX * 400))
			if (math.fabs(diffY) > 0.1):
				newY = self._hardwareDevices.neck.GetUpDown() - int(diffY * 300)
				print (newY)
				self._hardwareDevices.neck.SetUpDown(newY)
				
			
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
	
	demo = BehaveDemo()
	
	demo.demo()
	
	atexit.register(exit_handler)
	
	ended = False
	
	while ended == False:
		time.sleep(0.5)


    





