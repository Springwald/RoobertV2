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
#     ##################################
#     # Roobert RGB LED control module #
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


import time
import os, sys
from PIL import Image
from neopixel import *

my_file = os.path.abspath(__file__)
my_path ='/'.join(my_file.split('/')[0:-1])

sys.path.insert(0,my_path + "/../DanielsRasPiPythonLibs/multitasking")
sys.path.insert(0,my_path + "/../DanielsRasPiPythonLibs/hardware")
sys.path.insert(0,my_path + "/../DanielsRasPiPythonLibs/gfx")

from MultiProcessing import MultiProcessing
from AnimationImage import AnimationImage

class RgbLeds(MultiProcessing):

	# LED strip configuration:
	LED_COUNT      = 64*4    # Number of LED pixels.
	LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
	LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
	LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
	LED_BRIGHTNESS = 127    # Set to 0 for darkest and 255 for brightest
	LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
	
	_strip 			= None
	_program_path 	= None
	_released		= False
	_dimmer			 = 1
	
	Images			= []
	
	_pulse_phase	= 1
	_pulse_step		= 0
	
	_blocksWidth 	= 2
	_blockHeight	= 2
	
	
	_width			= 8 * _blocksWidth
	_height			= 8 * _blockHeight
	
	_aniFrameNo		= 0
	
	__activeImageNo		= MultiProcessing.get_next_key() 
	__activeImageMode	= MultiProcessing.get_next_key() 
	
	@property
	def activeImageNo(self):
		return self.GetSharedValue(self.__activeImageNo)
	@activeImageNo.setter
	def activeImageNo(self, value):
		self.SetSharedValue(self.__activeImageNo, value)
		
	@property
	def activeImageMode(self):
		return self.GetSharedValue(self.__activeImageMode)
	@activeImageMode.setter
	def activeImageMode(self, value):
		self.SetSharedValue(self.__activeImageMode, value)

	def __init__(self, imageFilenames):
		super().__init__(prio=20)
		
		print ("init RgbLeds")
		
		# Create NeoPixel object with appropriate configuration.
		self._strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS)
		# Intialize the library (must be called once before other functions).
		self._strip.begin()
		
		for i in range(len(imageFilenames)):
			self.Images.append(AnimationImage(imageFilenames[i]));

		self.activeImageNo = 0
		self.activeImageMode = 0

		super().StartUpdating()
		
	def colorWipe(self, color, wait_ms=0.1):
		#Wipe color across display a pixel at a time.
		for i in range(self._strip.numPixels()):
			self._strip.setPixelColor(i, color)
			self._strip.show()
			time.sleep(wait_ms/1000.0)
			
	def speed(self):
		col = Color (0,0,0)
		for m in range(0, 25):
			for i in range(self._strip.numPixels()):
				self._strip.setPixelColor(i, col)
			self._strip.show()
		col = Color (200,200,255)
		for m in range(0, 1):
			for i in range(self._strip.numPixels()):
				self._strip.setPixelColor(i, col)
			self._strip.show()
		
			
	def theaterChase(self, color, wait_ms=50, iterations=10):
		"""Movie theater light style chaser animation."""
		strip = self._strip
		for j in range(iterations):
			for q in range(3):
				for i in range(0, strip.numPixels(), 3):
					strip.setPixelColor(i+q, color)
				strip.show()
				time.sleep(wait_ms/1000.0)
				for i in range(0, strip.numPixels(), 3):
					strip.setPixelColor(i+q, 0)
	
	def wheel(self,pos):
		"""Generate rainbow colors across 0-255 positions."""
		if pos < 85:
			return Color(pos * 3, 255 - pos * 3, 0)
		elif pos < 170:
			pos -= 85
			return Color(255 - pos * 3, 0, pos * 3)
		else:
			pos -= 170
			return Color(0, pos * 3, 255 - pos * 3)
					
	def rainbowCycle(self, wait_ms=20, iterations=5):
		"""Draw rainbow that uniformly distributes itself across all pixels."""
		strip = self._strip
		for j in range(256*iterations):
			for i in range(strip.numPixels()):
				strip.setPixelColor(i, self.wheel(((int(i * 256 / strip.numPixels()) + j) & 255)))
			strip.show()
			time.sleep(wait_ms/1000.0)

	def showImage(self, imgframes, frame=0): 
		y = 0
		x = 0
		xPlus = 0
		yPlus = 0
		img = imgframes[frame]
		for neoPos in range(0, self._height * self._width):
			width, height = img.size
			imgX = width / self._width * (x+xPlus)  #(x + xPlus)  #
			imgY = height * (y+yPlus) / self._height  #y 
			RGB = img.getpixel((imgX, imgY))
			R,G,B,A = RGB
			#color =  Color(int(B * self._dimmer), int(R * self._dimmer),int(G * self._dimmer))
			color =  Color(int(G * self._dimmer), int(R * self._dimmer),int(B * self._dimmer))
			#color =  Color(G, R, B)
			self._strip.setPixelColor(neoPos, color) #pixels[0,0])
			if (y % 2 ==0):
				x = x + 1
				if (x > 7):
					x = 7;
					y = y + 1
					if (y >= self._height):
						y = 0
						xPlus = xPlus + 8
			else:
				x = x - 1
				if (x < 0):
					x = 0
					y = y + 1
					if (y >= self._height):
						y = 0
						xPlus = xPlus + 8
			#pos = pos + 3
		self._strip.show()
		
		
	def Off(self):
		number =0
		for y in range(8):
			for x in range(8):
				self._strip.setPixelColor(number, 0) 
				self._strip.show()
				number = number + 1
							
	def Update(self):
		if self.activeImageMode == 0:
			self.DimmImage(self.Images[self.activeImageNo])
		if self.activeImageMode == 1:
			self.AnimateImage(self.Images[self.activeImageNo]);
		
	def AnimateImage(self, image):
		if (super().updating_ended == True):
			return

		if (self._aniFrameNo >= len(image.Frames)):
			self._aniFrameNo = 0
			
		self._dimmer = 1
		self.showImage(image.Frames, self._aniFrameNo)
		time.sleep(image.Delay)
		
		self._aniFrameNo = self._aniFrameNo+1
		
	def DimmImage(self, image):
		if (super().updating_ended == True):
			return
		steps = 20
		delay = 0.05
		
		self._pulse_step = self._pulse_step + self._pulse_phase
		if (self._pulse_step > steps or self._pulse_step < 1):
			self._pulse_phase = - self._pulse_phase

		self._dimmer = 0.5 * self._pulse_step / steps 
		self.showImage(image.Frames)
		
		time.sleep(delay)

	def Release(self):
		if (self._released == False):
			self._released = True
			print("RGB LEDs releasing")
			super().EndUpdating()
			self.Off()

	def __del__(self):
		self.Release()

if __name__ == "__main__":


	leds = RgbLeds([my_path + '/../Gfx/Body/hearth2.gif', my_path + '/../../RoobertGifs/e8nZC.gif']) 

	ended = False
	


	for a in range(15):
		time.sleep(1)
	
	#while ended == False:
	#	time.sleep(1)
		#print("hu")
	#	a=1
		#leds.speed()
		#leds.Update()
		#leds.colorWipe(Color(0,0,255),10)
		#leds.theaterChase(Color(0,0,255),50)
		#leds.rainbowCycle(wait_ms=10, iterations=5)
		
	#time.sleep(13)
		
	leds.Release()
		


