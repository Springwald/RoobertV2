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
#     # neck motion control module #
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


from __future__ import division
import time, sys, os

my_file = os.path.abspath(__file__)
my_path ='/'.join(my_file.split('/')[0:-1])

sys.path.insert(0,my_path + "/../DanielsRasPiPythonLibs/multitasking")
sys.path.insert(0,my_path + "/../DanielsRasPiPythonLibs/hardware")

from MultiProcessing import *
from array import array
from SharedInts import SharedInts
from SharedFloats import SharedFloats
from LX16AServos import LX16AServos
from SmartServoManager import SmartServoManager

import atexit

clear = lambda: os.system('cls' if os.name=='nt' else 'clear')

class Neck():

	_servoManager 	= None
	_released 		= False
	_upDownId 		= 0
	_leftRightId 	= 0
	
	def __init__(self, smartServoManager):
		self._servoManager = smartServoManager
		self.DefineNeck()
		
	def DefineNeck(self):
		self._upDownId = 21
		self._leftRightId = 23
		self._servoManager.AddMasterServo(servoId=self._upDownId, centeredValue=501);
		self._servoManager.AddSlaveServo(servoId=self._upDownId+1, masterServoId=self._upDownId, reverseToMaster=-1, centeredValue=481);
		self._servoManager.AddMasterServo(servoId=self._leftRightId, centeredValue=500);

	def PrintValues(self):
		for id in range(23,24):
			self._servoManager.SetReadOnly(servoId=id, isReadOnly=True);
		self._servoManager.Start()
		while(True):
			self._servoManager.PrintReadOnlyServoValues()
			time.sleep(0.1)
				
	def WaitTillTargetsReached(self):
		while (self._servoManager.allTargetsReached == False):
			time.sleep(0.1)

	def SetUpDown(self, value):
		if (value > 300):
			value = 300
		if (value < -300):
			value = -300
		self._servoManager.MoveServo(self._upDownId, value+500)
		
	def SetLeftRight(self, value):
		if (value > 400):
			value = 400
		if (value < -400):
			value = -400
		self._servoManager.MoveServo(self._leftRightId, value+500)
		
	def GetUpDown(self):
		return self._servoManager.ReadServo(self._upDownId) - 500
		
	def GetLeftRight(self,):
		return self._servoManager.ReadServo(self._leftRightId) -500

	def Release(self):
		if (self._released == False):
			print("releasing neck")
			self._released = True;
			self.SetLeftRight(0);
			self.SetUpDown(0);
			self.WaitTillTargetsReached();

	def __del__(self):
		self.Release()

def exit_handler():
	tester.Release();
	servoManager.Release();
	servos.Release();

if __name__ == "__main__":

	atexit.register(exit_handler)

	ended = False;
	
	servos = LX16AServos()
	servoManager = SmartServoManager(lX16AServos=servos, ramp=0, maxSpeed=1)
	tester = Neck(servoManager)
	
	#tester.PrintValues();
	
	servoManager.Start()
	
	tester.SetUpDown(0)
	tester.SetLeftRight(0)
	tester.WaitTillTargetsReached()
	
	tester.SetLeftRight(-100)
	tester.WaitTillTargetsReached()
	tester.SetLeftRight(+100)
	tester.WaitTillTargetsReached()
	tester.SetLeftRight(0)
	tester.WaitTillTargetsReached()
	
	
	tester.SetUpDown(+100)
	tester.WaitTillTargetsReached()
	tester.SetUpDown(-100)
	tester.WaitTillTargetsReached()
	
	tester.SetUpDown(0)
	tester.SetLeftRight(0)
	tester.WaitTillTargetsReached()

	#time.sleep(2)
	
	
	#tester.MirrorRightArmToLeft();
	#tester.PrintRightArmValues()
	

	
	print("done")
	
	exit_handler()
	
