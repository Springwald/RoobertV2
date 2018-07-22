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
#     ########
#     # Arms #
#     ########
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

class Arms():

	_servoManager = None;
	_released = False;
	
	_armHanging 	= [[1,151],[2,168],[3,455],[4,613],[5,471]];
	_wink1 		= [[1,374],[2,451],[3,693],[4,816],[5,565]];
	_wink2 		= [[1,192],[2,678],[3,888],[4,872],[5,509]];
	_strechSide	= [[1,299],[2,249],[3,663],[4,660],[5,848]];
	_lookHand	= [[1,592],[2, 90],[3,361],[4,787],[5,795]];
	_ghettoFist1	= [[1,105],[2,140],[3,525],[4,910],[5,116]];
	_ghettoFist2	= [[1,339],[2,138],[3,525],[4,753],[5,116]];
	
	_leftServoCorrection = [-50,20,0,0,0,50];
	
	def __init__(self, smartServoManager, leftHandOpen=480, leftHandClose=560, rightHandOpen=540, rightHandClose=450):
		self._servoManager = smartServoManager
		self._leftHandOpen = leftHandOpen
		self._leftHandClose = leftHandClose
		self._rightHandOpen = rightHandOpen
		self._rightHandClose = rightHandClose
		self.DefineArms()
		
		#self.SetArm(gesture=Arms._armHanging, left=False);
		#self.SetHand(opened=True, left=False);
		#self.SetArm(gesture=Arms._armHanging, left=True);
		#self.SetHand(opened=True, left=True);
		#self.WaitTillTargetsReached();
		
	def DefineArms(self):
		# right arm
		self._servoManager.AddMasterServo(servoId=1, centeredValue=370);
		self._servoManager.AddSlaveServo(servoId=2, masterServoId=1, reverseToMaster=-1, centeredValue=608);
		self._servoManager.AddMasterServo(servoId=3, centeredValue=685);
		self._servoManager.AddSlaveServo(servoId=4, masterServoId=3, reverseToMaster=-1, centeredValue=352);
		self._servoManager.AddMasterServo(servoId=5, centeredValue=510);
		self._servoManager.AddMasterServo(servoId=6, centeredValue=460);
		self._servoManager.AddMasterServo(servoId=7, centeredValue=495);
		self._servoManager.AddMasterServo(servoId=8, centeredValue=500);

	def PrintRightArmValues(self):
		self._servoManager.SetReadOnly(servoId=1, isReadOnly=True);
		self._servoManager.SetReadOnly(servoId=2, isReadOnly=True);
		self._servoManager.SetReadOnly(servoId=3, isReadOnly=True);
		self._servoManager.SetReadOnly(servoId=4, isReadOnly=True);
		self._servoManager.SetReadOnly(servoId=5, isReadOnly=True);
		self._servoManager.SetReadOnly(servoId=6, isReadOnly=True);
		self._servoManager.SetReadOnly(servoId=7, isReadOnly=True);
		self._servoManager.SetReadOnly(servoId=8, isReadOnly=True);
		self._servoManager.Start()
		while(True):
			out = ""
			# print all readonly servos
			for a in range(0, self._servoManager.servoCount):
				id = self._servoManager._servoIds[a]
				if (self._servoManager._isReadOnly[a]==True):
					p = self._servoManager.ReadServo(id)
					#if (p != -1):
					out = out  + str(id) + ": " + str(p) + "\r\n"
					
			# print only the master servos in in copy format
			
			## push to screen
			clear()
			print(out)
			time.sleep(0.1)

	def SetArm(self, gesture, left):
		for p in range(0,len(gesture)):
			id = gesture[p][0]
			value = gesture[p][1]
			if (left == True):
				id = id + 6;
				value = 1000-value + self._leftServoCorrection[p];
			self._servoManager.MoveServo(id,value);
			
	def WaitTillTargetsReached(self):
		while (self._servoManager.allTargetsReached == False):
			time.sleep(0.1);

	def SetHand(self, opened, left):
		if (left==True):
			if (opened==True):
				self._servoManager.MoveServo(12,self._leftHandOpen)
			else:
				self._servoManager.MoveServo(12,self._leftHandClose)
		else:
			if (opened==True):
				self._servoManager.MoveServo(6,self._rightHandOpen);
			else:
				self._servoManager.MoveServo(6,self._rightHandClose);

	def Release(self):
		if (self._released == False):
			self._released = True;
			self.SetArm(gesture=Arms._armHanging, left=False);
			self.SetArm(gesture=Arms._armHanging, left=True);
			self.SetHand(opened=True, left=False);
			self.SetHand(opened=True, left=True);
			self.WaitTillTargetsReached();
			self._servoManager.Release();

	def __del__(self):
		self.Release()

def exit_handler():
	tester.Release()

if __name__ == "__main__":

	ended = False;
	
	servos = LX16AServos()
	servoManager = SmartServoManager(lX16AServos=servos, ramp=0, maxSpeed=1)
	tester = Arms(servoManager)
	tester.PrintRightArmValues()
	
	plus = 100
	servoManager.Start()
	while(True):
		plus = - plus
		#tester._servoManager.MoveServo(1,400+plus)
		tester._servoManager.MoveServo(3,600+plus)
		while (tester._servoManager.allTargetsReached == False):
			time.sleep(0.1)
	
	
	
	tester.SetHand(opened=False, left= True);
	tester.SetHand(opened=False, left= False);
	tester.WaitTillTargetsReached();
	time.sleep(1);
	tester.SetHand(opened=True, left= True);
	tester.SetHand(opened=True, left= False);
	tester.WaitTillTargetsReached();
	time.sleep(1);
	
	#while(True):
	#	time.sleep(1)
	#	print("sleep")

	
	tester.SetArm(gesture=Arms._strechSide, left=True);
	tester.WaitTillTargetsReached();
	
	#tester.SetArm(gesture=Arms._lookHand, left=False);
	#tester.WaitTillTargetsReached();
	
	tester.SetArm(gesture=Arms._strechSide, left=True);
	tester.SetArm(gesture=Arms._strechSide, left=False);
	tester.WaitTillTargetsReached();
	
	tester.SetArm(gesture=Arms._wink1, left=True);
	tester.WaitTillTargetsReached();
	tester.SetArm(gesture=Arms._wink2, left= True);
	tester.WaitTillTargetsReached();
	tester.SetArm(gesture=Arms._wink1, left=True);
	tester.WaitTillTargetsReached();
	tester.SetArm(gesture=Arms._wink2, left= True);
	tester.WaitTillTargetsReached();
	
	tester.SetHand(opened=False, left= True);
	tester.SetArm(gesture=Arms._ghettoFist1, left= True);
	tester.WaitTillTargetsReached();
	tester.SetArm(gesture=Arms._ghettoFist2, left= True);
	tester.WaitTillTargetsReached();
	
	
	
	
	tester.Release();
	
	print("done");
