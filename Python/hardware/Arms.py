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
	
	_armHanging 			= [[1,185],[3,273],[5,501],[6,541],[7,495],[8,499]]
	
	_lookAtHand 			= [[1,226],[3,680],[5,346],[6,802],[7,830],[8,499]]
	_wink1 					= [[1,476],[3,770],[5,396],[6,866],[7,542],[8,499]]
	_wink2 					= [[1,459],[3,639],[5,396],[6,739],[7,601],[8,499]]
	_stretchSide			= [[1,335],[3,442],[5,542],[6,593],[7,770],[8,499]]
	
	#_rightCenteredValues	= [[1,370],[3,685],[5,510],[6,460],[7,495],[8,500]]

	
	def __init__(self, smartServoManager, leftHandOpen=480, leftHandClose=580, rightHandOpen=540, rightHandClose=430):
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
		
		# left arm
		self._servoManager.AddMasterServo(servoId=11, centeredValue=545);
		self._servoManager.AddSlaveServo(servoId=12, masterServoId=11, reverseToMaster=-1, centeredValue=459);
		self._servoManager.AddMasterServo(servoId=13, centeredValue=329);
		self._servoManager.AddSlaveServo(servoId=14, masterServoId=13, reverseToMaster=-1, centeredValue=700);
		self._servoManager.AddMasterServo(servoId=15, centeredValue=477);
		self._servoManager.AddMasterServo(servoId=16, centeredValue=486);
		self._servoManager.AddMasterServo(servoId=17, centeredValue=501);
		self._servoManager.AddMasterServo(servoId=18, centeredValue=503);

	def PrintRightArmValues(self):
		for id in range(1,8):
			self._servoManager.SetIsReadOnly(servoId=id, isReadOnly=True);
		self._servoManager.Start()
		while(True):
			self._servoManager.PrintReadOnlyServoValues()
			time.sleep(0.1)
			
	def PrintLeftArmValues(self):
		for id in range(11,18):
			self._servoManager.SetIsReadOnly(servoId=id, isReadOnly=True);
		self._servoManager.Start()
		while(True):
			self._servoManager.PrintReadOnlyServoValues(onlyMasterServos=False)
			time.sleep(0.1)
			

	def MirrorRightArmToLeftStart(self):
		for id in range(1,8):
			self._servoManager.SetIsReadOnly(servoId=id, isReadOnly=True);
		#self._servoManager.Start()

	def MirrorRightArmToLeftUpdate(self):
		for id in [1,3,5,6,7,8]:
			value = self._servoManager.ReadServo(id);
			#print (str(id) + ":" +str(value))
			value = -(value - self._servoManager.GetCenteredValue(id)) + self._servoManager.GetCenteredValue(id+10)
			self._servoManager.MoveServo(id+10, pos=value);

	def MirrorRightArmToLeftEnd(self):
		for id in range(1,8):
			self._servoManager.SetIsReadOnly(servoId=id, isReadOnly=False);

	def SetArm(self, gesture, left):
		for p in range(0,len(gesture)):
			id = gesture[p][0]
			value = gesture[p][1]
			if (left == True):
				id = id + 10;
				value = -(value - self._servoManager.GetCenteredValue(id-10)) + self._servoManager.GetCenteredValue(id)
				self._servoManager.MoveServo(id,value);
				#print ("left:" + str(id));
			else:
				self._servoManager.MoveServo(id,value);
				#print ("right:" + str(id))
	def WaitTillTargetsReached(self):
		while (self._servoManager.allTargetsReached == False):
			time.sleep(0.1);

	def SetHand(self, opened, left):
		if (left==True):
			if (opened==True):
				self._servoManager.MoveServo(18,self._leftHandOpen)
			else:
				self._servoManager.MoveServo(18,self._leftHandClose)
		else:
			if (opened==True):
				self._servoManager.MoveServo(8,self._rightHandOpen);
			else:
				self._servoManager.MoveServo(8,self._rightHandClose);

	def Release(self):
		if (self._released == False):
			self._released = True;
			self.SetArm(gesture=Arms._armHanging, left=False);
			self.SetArm(gesture=Arms._armHanging, left=True);
			self.SetHand(opened=True, left=False);
			self.SetHand(opened=True, left=True);
			self.WaitTillTargetsReached();

	def __del__(self):
		self.Release()

def exit_handler():
	tester.Release()
	servoManager.Release()
	servos.Release()
	

if __name__ == "__main__":

	atexit.register(exit_handler)

	ended = False;
	
	servos = LX16AServos()
	servoManager = SmartServoManager(lX16AServos=servos, ramp=0, maxSpeed=1)
	tester = Arms(servoManager)
	#tester.MirrorRightArmToLeft();
	
	#tester.PrintRightArmValues()
	tester.PrintLeftArmValues();
	
	
	servoManager.Start();
	#time.sleep(1);
	#tester.SetArm(gesture=Arms._rightCenteredValues, left=True);
	#tester.WaitTillTargetsReached();
	
	
	
	
	
	#while(True):
	#	print()
	
	while(True):
		tester.SetArm(gesture=Arms._armHanging, left=False);
		tester.SetArm(gesture=Arms._armHanging, left=True);
		tester.WaitTillTargetsReached();
		tester.SetArm(gesture=Arms._lookAtHand, left=False);
		tester.WaitTillTargetsReached();
		
		for i in range(1,4):
			tester.SetArm(gesture=Arms._wink2, left=False);
			tester.WaitTillTargetsReached();
			tester.SetArm(gesture=Arms._wink1, left=False);
			tester.WaitTillTargetsReached();
			
		tester.SetArm(gesture=Arms._armHanging, left=True);
		tester.WaitTillTargetsReached();
		tester.SetArm(gesture=Arms._lookAtHand, left=True);
		tester.WaitTillTargetsReached();
		for i in range(1,4):
			tester.SetArm(gesture=Arms._wink2, left=True);
			tester.WaitTillTargetsReached();
			tester.SetArm(gesture=Arms._wink1, left=True);
			tester.WaitTillTargetsReached();
			

	#plus = 100
	#servoManager.Start()
	#while(True):
		#plus = - plus
		##tester._servoManager.MoveServo(1,400+plus)
		#tester._servoManager.MoveServo(3,600+plus)
		#while (tester._servoManager.allTargetsReached == False):
			#time.sleep(0.1)
	
	
	
	#tester.SetHand(opened=False, left= True);
	#tester.SetHand(opened=False, left= False);
	#tester.WaitTillTargetsReached();
	#time.sleep(1);
	#tester.SetHand(opened=True, left= True);
	#tester.SetHand(opened=True, left= False);
	#tester.WaitTillTargetsReached();
	#time.sleep(1);
	
	##while(True):
	##	time.sleep(1)
	##	print("sleep")

	
	#tester.SetArm(gesture=Arms._strechSide, left=True);
	#tester.WaitTillTargetsReached();
	
	##tester.SetArm(gesture=Arms._lookHand, left=False);
	##tester.WaitTillTargetsReached();
	
	#tester.SetArm(gesture=Arms._strechSide, left=True);
	#tester.SetArm(gesture=Arms._strechSide, left=False);
	#tester.WaitTillTargetsReached();
	
	#tester.SetArm(gesture=Arms._wink1, left=True);
	#tester.WaitTillTargetsReached();
	#tester.SetArm(gesture=Arms._wink2, left= True);
	#tester.WaitTillTargetsReached();
	#tester.SetArm(gesture=Arms._wink1, left=True);
	#tester.WaitTillTargetsReached();
	#tester.SetArm(gesture=Arms._wink2, left= True);
	#tester.WaitTillTargetsReached();
	
	#tester.SetHand(opened=False, left= True);
	#tester.SetArm(gesture=Arms._ghettoFist1, left= True);
	#tester.WaitTillTargetsReached();
	#tester.SetArm(gesture=Arms._ghettoFist2, left= True);
	#tester.WaitTillTargetsReached();
	
	
	
	
	
	print("done");
