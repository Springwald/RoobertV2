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

import atexit

my_file = os.path.abspath(__file__)
my_path ='/'.join(my_file.split('/')[0:-1])

sys.path.insert(0,my_path + "/../libs" )

from MultiProcessing import *
from array import array
from SharedInts import SharedInts
from SharedFloats import SharedFloats
from LX16AServos import LX16AServos
from SmartServoManager import SmartServoManager

class Arms():

	_servos = None;
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

	def __init__(self, leftHandOpen, leftHandClose, rightHandOpen, rightHandClose):
		self._servos = LX16AServos();
		self._servoManager = SmartServoManager(lX16AServos=self._servos, servoIds= [1,2,3,4,5,6,7,8,9,10,11,12],ramp=0, maxSpeed=35);
		self._leftHandOpen = leftHandOpen;
		self._leftHandClose = leftHandClose;
		self._rightHandOpen = rightHandOpen;
		self._rightHandClose = rightHandClose;
		
		self.SetArm(gesture=Arms._armHanging, left=False);
		self.SetHand(opened=True, left=False);
		self.SetArm(gesture=Arms._armHanging, left=True);
		self.SetHand(opened=True, left=True);
		self.WaitTillTargetsReached();
		
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
				self._servoManager.MoveServo(12,self._leftHandOpen);
			else:
				self._servoManager.MoveServo(12,self._leftHandClose);
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
			self._servos.Release();

	def __del__(self):
		self.Release()

def exit_handler():
	tester.Release()

if __name__ == "__main__":

	ended = False;
	tester = Arms(leftHandOpen=480, leftHandClose=560, rightHandOpen=540, rightHandClose=450);
	tester.SetHand(opened=False, left= True);
	tester.SetHand(opened=False, left= False);
	tester.WaitTillTargetsReached();
	time.sleep(1);
	tester.SetHand(opened=True, left= True);
	tester.SetHand(opened=True, left= False);
	tester.WaitTillTargetsReached();
	time.sleep(1);
	
	
	tester.SetArm(gesture=Arms._strechSide, left=True);
	tester.WaitTillTargetsReached();
	
	tester.SetArm(gesture=Arms._lookHand, left=False);
	tester.WaitTillTargetsReached();
	
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
