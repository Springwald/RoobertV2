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
	
	_actionRunning					= False

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
		#self.FirstInfoAboutRoobert()
		
		while ended == False:
			
			self.UpdateFace()
			self.FollowFace()
			
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.MOUSEBUTTONUP:
					ended = True 
					
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
						ended = True 
						
					if event.key == pygame.K_KP0:
						self.Greet()
					
					if event.key == pygame.K_KP1:
						self.FirstInfoAboutRoobert()
						
					if event.key == pygame.K_KP7:
						self._hardwareDevices.BodyLeds.activeImageNo = 0
						self._hardwareDevices.BodyLeds.activeImageMode = 0
						
					if event.key == pygame.K_KP8:
						self._hardwareDevices.BodyLeds.activeImageNo = 1
						self._hardwareDevices.BodyLeds.activeImageMode = 1
						
					if event.key == pygame.K_KP9:
						self._hardwareDevices.BodyLeds.activeImageNo = 2
						self._hardwareDevices.BodyLeds.activeImageMode = 1
						
					if event.key == pygame.K_KP4:
						self._hardwareDevices.BodyLeds.activeImageNo = 3
						self._hardwareDevices.BodyLeds.activeImageMode = 1
						
					if event.key == pygame.K_KP5:
						self._hardwareDevices.BodyLeds.activeImageNo = 4
						self._hardwareDevices.BodyLeds.activeImageMode = 1
						
					if event.key == pygame.K_KP6:
						self._hardwareDevices.BodyLeds.activeImageNo = 5
						self._hardwareDevices.BodyLeds.activeImageMode = 1

	def UpdateFace(self):
		if (self.showFace == True):
			self._faceGfx.speaking = self._speechOutput.IsSpeaking();

	def Greet(self):
		
		self._actionRunning = True
		self.ResetNeck()
		
		# heart gif
		self._hardwareDevices.BodyLeds.activeImageNo = 0
		self._hardwareDevices.BodyLeds.activeImageMode = 0
		
		touchBody 		= [[1,212],[3,511],[5,138],[6,890],[7,702]]
		holdInFront 	= [[1,186],[3,398],[5,260],[6,718],[7,603]]
		pointToUser 	= [[1,213],[3,408],[5,641],[6,717],[7,755]]
		
		self.ResetArms()

		self._speechOutput.Speak("Guten Tag.", wait=True)
			
		self._hardwareDevices.arms.SetArm(gesture=touchBody, left=True);
		self._speechOutput.Speak("Mein Name ist Robert", wait=False)
		while (self._speechOutput.IsSpeaking()==True):
			time.sleep(0.1)
		
		self._hardwareDevices.arms.SetArm(gesture=holdInFront, left=True);	
		self._speechOutput.Speak("Ich freue mich, Sie kennen zu lernen", wait=False)
		time.sleep(1)
		self._hardwareDevices.arms.SetArm(gesture=pointToUser, left=True);
		self._hardwareDevices.arms.SetArm(gesture=pointToUser, left=False);

		while (self._speechOutput.IsSpeaking()==True):
			time.sleep(0.1)
			
		while (self._hardwareDevices.arms.WaitTillTargetsReached()==False):
			time.sleep(0.1)
			
		self.ResetArms()

		self._actionRunning = False
		
	def ResetArms(self):
		self._hardwareDevices.arms.SetArm(gesture=Arms._armHanging, left=True)
		self._hardwareDevices.arms.SetArm(gesture=Arms._armHanging, left=False)
		while (self._hardwareDevices.arms.WaitTillTargetsReached()==False):
			time.sleep(0.1)
			
	def ResetNeck(self):
		self._hardwareDevices.neck.SetUpDown(0)
		self._hardwareDevices.neck.SetLeftRight(0)
		self._faceGfx.SetEyePos(0.5,0.5)

	def FirstInfoAboutRoobert(self):
		
		self._actionRunning = True
		self.ResetNeck()
		
		pointToSide			= [[1,207],[3,297],[5,533],[6,741],[7,797]]
		pointToHead 		= [[1,204],[3,698],[5,395],[6,872],[7,781]]
		pointToBodyDisplay	= [[1,226],[3,374],[5,144],[6,842],[7,547]]
		pointToOtherArm1 	= [[1,126],[3,525],[5,237],[6,804],[7,546]]
		pointToOtherArm2 	= [[1,131],[3,481],[5,488],[6,896],[7,503]]
		
		self.ResetArms()
		
		# heart gif
		self._hardwareDevices.BodyLeds.activeImageNo = 0
		self._hardwareDevices.BodyLeds.activeImageMode = 0
		
		self._hardwareDevices.arms.SetArm(gesture=pointToSide, left=False)
		self._speechOutput.Speak("Ich kann ihnen gerne Details über mich erzählen.")
		
		self._hardwareDevices.arms.SetArm(gesture=pointToHead, left=True)
		self._hardwareDevices.arms.SetArm(gesture=Arms._armHanging, left=False)
		self._speechOutput.Speak("Mein Gesicht ist ein Bildschirm und wird von einem Raspberry Pei gesteuert")
		
		# banana gif
		self._hardwareDevices.BodyLeds.activeImageNo = 1
		self._hardwareDevices.BodyLeds.activeImageMode = 1
		self._hardwareDevices.arms.SetArm(gesture=pointToBodyDisplay, left=False);
		self._hardwareDevices.arms.SetArm(gesture=Arms._armHanging, left=True)
		self._speechOutput.Speak("In meinem Körper steckt eine weitere Anzeige mit 16 mal 16 Pixeln Auflösung")
		
		self._hardwareDevices.arms.SetArm(gesture=pointToOtherArm1, left=False);
		self._hardwareDevices.arms.SetArm(gesture=pointToOtherArm2, left=True);
		self._speechOutput.Speak("Jeder meiner Arme wird von 8 Servo Motoren angetrieben.")

		self._hardwareDevices.arms.SetArm(gesture=Arms._armHanging, left=True)
		self._hardwareDevices.arms.SetArm(gesture=Arms._armHanging, left=False)
		
		# heart gif
		self._hardwareDevices.BodyLeds.activeImageNo = 0
		self._hardwareDevices.BodyLeds.activeImageMode = 0
		
		self._actionRunning = False

	def FollowFace(self):
		
		if (self._actionRunning == True):
			self.ResetNeck()
			return
		
		faceX = self._camera.posXFace
		faceY = self._camera.posYFace
		timeSinceLastFace = time.time() - self._lastFace 
		if (faceX != -1 and faceY != -1):
			# oh, there is a face
			if (timeSinceLastFace > 60):
				# see a face after a long time: say hello!
				# start_new_thread(self.Greet,())
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
				self._hardwareDevices.neck.SetUpDown(newY)
				
			self._faceGfx.SetEyePos(faceX,faceY)
		else:
			# there is no face
			if (timeSinceLastFace > 20):
				# long time no face seen
				self._faceGfx.SetEyePos(0.5,0.5)
			if (timeSinceLastFace > 60):
				# long time no face seen
				self.ResetNeck()
			
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


    





