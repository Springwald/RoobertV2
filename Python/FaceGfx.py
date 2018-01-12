#!/usr/bin/env python

#      Roobert - home robot project
#      ________            ______             _____ 
#      ___  __ \______________  /_______________  /_
#      __  /_/ /  __ \  __ \_  __ \  _ \_  ___/  __/
#      _  _, _// /_/ / /_/ /  /_/ /  __/  /   / /_  
#      /_/ |_| \____/\____//_.___/\___//_/    \__/
#
#     Project website: http://roobert.springwald.de
#
#     ################################
#     # Roobert face graphics module #
#     ################################
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

my_file = os.path.abspath(__file__)
my_path ='/'.join(my_file.split('/')[0:-1])

import time
from PIL import Image
from random import randrange, uniform
import pygame
from pygame.locals import *
import random

sys.path.insert(0,my_path + "/libs" )

from MultiProcessing import MultiProcessing
from SharedFloats import SharedFloats

program_path = my_path + ""

class FaceGfx(MultiProcessing):

	_released 	= False
	
	_visualize	= True

	screenWidth  = 1024
	screenHeight = 600
	
	_lastEyeX		= 0
	_lastEyeY		= 0
	
	speaking = False
	
	mouthGfx = None
	mouthAngle = 0
	mouthAngleTarget = 0
	mouthPosY = 0
	mouthPosYTarget = 0
	
	glassesGfx = None
	eyeBallGfx = None
	eyeWhiteGfx = None
	eyeBrowLeftGfx = None
	eyeBrowRightGfx = None
	i = 0
	lcd = None
	lastUpdate = time.time()
	delaySeconds = 1.0 / 10 #10 fps

	__shared_floats__			= SharedFloats(max_length=2)
	__eye_x_float__ 			= __shared_floats__.get_next_key()
	__eye_y_float__ 			= __shared_floats__.get_next_key()

	def __init__(self, visualize ):
		
		super().__init__(prio=20)
		
		self.program_path = program_path
		self._visualize = visualize
		
		image_filename = program_path + '/Gfx/Face-001.png'
		
		location= [0,0]
				
		os.putenv('SDL_FBDEV', '/dev/fb1')
		pygame.init()
		pygame.mixer.quit() # to prevent conflicts with speech output (audio device busy)

		screenInfo = pygame.display.Info()
		if (screenInfo.current_w > 900):
			self.lcd = pygame.display.set_mode((self.screenWidth,self.screenHeight))
		else:
			self.lcd = pygame.display.set_mode((self.screenWidth,self.screenHeight), FULLSCREEN, 16)
		
		self.LoadImages()
		
		self.eyeX = 0.5
		self.eyeY = 0.5

		pygame.display.update()
		pygame.mouse.set_visible(False)
		self.lcd.fill((255,194,0))

		pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
		self.image = pygame.image.load(image_filename)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location
		self.bg = pygame.image.load(image_filename)
		
		self.PaintMouth(False)
				
		super().StartUpdating()
		
	## multi process properties START ##
	
	@property
	def eyeX(self):
		return self.__shared_floats__.get_value(self.__eye_x_float__)
	@eyeX.setter
	def eyeX(self, value):
		self.__shared_floats__.set_value(self.__eye_x_float__,value)
		
	@property
	def eyeY(self):
		return self.__shared_floats__.get_value(self.__eye_y_float__)
	@eyeY.setter
	def eyeY(self, value):
		self.__shared_floats__.set_value(self.__eye_y_float__, value)
	
	## multi process properties END ##

	def LoadImage(self, filename, transparent):
		face_path = self.program_path + '/Gfx/Face/'
		png = pygame.image.load(face_path + filename)
		png.convert()
		if (transparent == True):
			return png
		surface = pygame.Surface(png.get_size())
		surface = surface.convert()
		surface.blit(png,(0,0))
		return surface

	def LoadImages(self):
		self.mouthGfx = self.LoadImage('mouth.png', False)
		self.glassesGfx = self.LoadImage( 'glasses.png', False)
		self.eyeBallGfx = self.LoadImage( 'eye_ball.png', True)
		self.eyeWhiteGfx  = self.LoadImage( 'eye_white.png',False)
		self.eyeBrowLeftGfx  = self.LoadImage( 'eyebrow_left.png', False)
		self.eyeBrowRightGfx  = self.LoadImage( 'eyebrow_right.png', False)
		
	def PaintEye(self,leftFactor):
		eyeCenterX = self.screenWidth * (0.5 + leftFactor * 0.158)
		eyeCenterY = self.screenHeight * 0.4
		
		eyeWhiteWidthHalf = self.screenWidth * 0.09
		eyeWhiteHeightHalf =  self.screenHeight * 0.09
		eyeBallWidthHalf = self.eyeBallGfx.get_width() / 2
		eyeBallHeightHalf = self.eyeBallGfx.get_height() / 2
		
		eyeBallPosX = eyeWhiteWidthHalf * (self.eyeX - 0.5)
		eyeBallPosY = eyeWhiteHeightHalf * (self.eyeY - 0.5)
		
		self.lcd.blit(self.eyeBallGfx, (eyeCenterX - eyeBallPosX - eyeBallWidthHalf, eyeCenterY + eyeBallPosY - eyeBallHeightHalf))
		
		eyeBrowY = self.screenHeight * 0.1
		eyeBrowGfx = self.eyeBrowRightGfx
		if (leftFactor > 0):
			eyeBrowGfx = self.eyeBrowLeftGfx
			
		self.lcd.blit(eyeBrowGfx, (eyeCenterX  - eyeBrowGfx.get_width() / 2 , eyeBrowY - eyeBrowGfx.get_height() / 2))
		
	def PaintMouth(self, moving):
		speedAngle = 2
		if (self.mouthAngle > self.mouthAngleTarget+speedAngle):
			self.mouthAngle = self.mouthAngle-speedAngle
		else:
			if (self.mouthAngle < self.mouthAngleTarget-speedAngle):
				self.mouthAngle = self.mouthAngle+speedAngle
			else:
				if (self.speaking == True):
					self.mouthAngleTarget = random.randint(-5, 5)
				else:
					self.mouthAngleTarget = 0
				
		# random mouth y pos
		speedY = 3
		if (self.mouthPosY > self.mouthPosYTarget + speedY):
			self.mouthPosY = self.mouthPosY-speedY
		else:
			if (self.mouthPosY < self.mouthPosYTarget - speedY):
				self.mouthPosY = self.mouthPosY+speedY
			else:
				if (self.speaking == True):
					self.mouthPosYTarget = random.randint(-10, 10)
				else:
					self.mouthPosYTarget = 0

		rotatedMouth = self.rot_center(self.mouthGfx, self.mouthAngle)
		self.lcd.blit(rotatedMouth, (self.screenWidth / 2 - self.mouthGfx.get_width() / 2, self.screenHeight * 0.7 + self.mouthPosY))

	def Update(self):
		if (super().updating_ended == True):
			return
		
		time.sleep(self.delaySeconds)
		
		toUpdate = False
		
		# eye-balls
		if (self._lastEyeX != self.eyeX or self._lastEyeY != self.eyeY):
			toUpdate = True
			self.lcd.blit(self.glassesGfx, ((self.screenWidth- self.glassesGfx.get_width()) / 2, self.screenHeight * 0.4 - self.glassesGfx.get_height() / 2))
			self.PaintEye(-1)
			self.PaintEye(1)
			self._lastEyeX = self.eyeX
			self._lastEyeY = self.eyeY

		#random mouth rotation
		if (self.speaking == True):
			toUpdate = True
			self.PaintMouth(True)
		
		if (toUpdate == True):
			pygame.display.update()
		else:
			time.sleep(0.5)
		
	def SetEyePos(self,eyePosX, eyePosY):
		if (eyePosX != self.eyeX or eyePosY != self.eyeY):
			self.changed = True
			self.eyeX =eyePosX
			self.eyeY =eyePosY
		
		
	def SetScreenBackLight(self, onOff):
		if (onOff == True):
			os.system("echo 0 | sudo tee /sys/class/backlight/rpi_backlight/bl_power")
		else:
			os.system("echo 1 | sudo tee /sys/class/backlight/rpi_backlight/bl_power")
		
	#def UpdateEndless(self):
	#	while self._ended == False:
	#		self.Update()
	#		time.sleep(0.02)
		

	def rot_center(self, image, angle):
		"""rotate an image while keeping its center and size"""
		orig_rect = image.get_rect()
		rot_image = pygame.transform.rotate(image, angle)
		rot_rect = orig_rect.copy()
		rot_rect.center = rot_image.get_rect().center
		rot_image = rot_image.subsurface(rot_rect).copy()
		return rot_image
		
	def Release(self):
		if (self._released == False):
			print("facegfx releasing")
			self._released = True
			super().EndUpdating()
			
	def __del__(self):
		self.Release()

if __name__ == "__main__":
	
	face = FaceGfx(True) 
	
	face.speaking = True
	#face.SetScreenBackLight(True)
	
	ended = False
	
	
	
	while ended == False:
		
		t = time.time()
		
		#face.Update()
		#face.SetScreenBackLight(False)
		
		d = time.time() -t
		#print(int(d * 1000))
		
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					ended = True 
					
		time.sleep(.01)
		
		newX = face.eyeX + 0.01
		if (newX > 1):
			newX =0
		face.SetEyePos(newX, newX)
		
					
		#face.SetScreenBackLight(True)
					
	face.Release()

