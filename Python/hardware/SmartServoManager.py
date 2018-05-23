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
#     # LX-16A servo communication #
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

import atexit

my_file = os.path.abspath(__file__)
my_path ='/'.join(my_file.split('/')[0:-1])

sys.path.insert(0,my_path + "/../libs" )

from MultiProcessing import *
from array import array
from SharedInts import SharedInts
from SharedFloats import SharedFloats
from LX16AServos import LX16AServos

class SmartServoManager(MultiProcessing):
	
	_lastUpdateTime	= time.time()
	_actualSpeedDelay = .006
	_maxStepsPerSpeedDelay = 1
	
	_ramp				= 10;
	
	_servos 			= None;
	servoCount 			= 0;
	_servoIds			= [];
	__targets			= None; 
	__values			= None; 
	
	__shared_ints__		= None
	
	_nextServoToReadPos = 0;
	
	_released = False;
	
	@property
	def allTargetsReached(self):
		return self.__shared_ints__.get_value(self.__targets_reached_int__)== 1
	@allTargetsReached.setter
	def allTargetsReached(self, value):
		if (value == True):
			self.__shared_ints__.set_value(self.__targets_reached_int__,1)
		else:
			self.__shared_ints__.set_value(self.__targets_reached_int__,0)

	def __init__(self, lX16AServos, servoIds, ramp=0, maxSpeed=1):
		
		super().__init__(prio=-20)
		
		self.servoCount = len(servoIds);
		self._servoIds = servoIds;
		self._servos = lX16AServos;
		self.__targets = SharedInts(max_length=self.servoCount);
		self.__values  = SharedInts(max_length=self.servoCount);
		
		self._ramp = ramp;
		self._maxStepsPerSpeedDelay = maxSpeed;

		self.__shared_ints__			= SharedInts(max_length=3)
		self.__targets_reached_int__	= self.__shared_ints__.get_next_key()
		
		self._processName = "SmartServoManager";
		
		# initial read of servo positions
		for pos in range(0, self.servoCount):
			id = self._servoIds[pos];
			value = self._servos.ReadPos(id);
			self.__values.set_value(pos, value);
			self.__targets.set_value(pos, value);
			#print(self.__values.get_value(pos));
			
		super().StartUpdating()
		
		
	def Update(self):
		#print("update start " + str(time.time()))
		if (super().updating_ended == True):
			return
		
		timeDiff = time.time() - self._lastUpdateTime
		if (timeDiff < self._actualSpeedDelay):
			time.sleep(self._actualSpeedDelay - timeDiff)
		allReached = True

		for i in range(0, self.servoCount):
			
			if (super().updating_ended == True):
				return
				
			id = self._servoIds[i];
			
			if (False and self._nextServoToReadPos == i):
			#if (id == 13 or id == 12):
				value = self._servos.ReadPos(id)
				self.__values.set_value(i, value);
				#print(str(i)+ " " + str(value))
			else:
				value = self.__values.get_value(i);

			diff = int(self.__targets.get_value(i) - value) 
			plus = 0
			
			tolerance = 10;
			
			if (diff < tolerance and diff > -tolerance):
				reachedThis = True
				#if (diff != 0):
				#	if (super().updating_ended == False):
				#		l = 1
						#newValue = int(self.__targets.get_value(i))
						#self._servos.MoveServo(id, self._ramp, newValue)
						#self.__values.set_value(i, newValue)
			else:
				reachedThis = False;
				
			diff = max(diff, -self._maxStepsPerSpeedDelay);
			diff = min(diff, self._maxStepsPerSpeedDelay);

			if (reachedThis == False):
				allReached = False
				newValue = int(value + diff) 
				if (super().updating_ended == False):
					self._servos.MoveServo(id, self._ramp, newValue);
					self.__values.set_value(i, newValue)

		self._nextServoToReadPos = self._nextServoToReadPos + 1
		if (self._nextServoToReadPos >= self.servoCount):
			self._nextServoToReadPos = 0

		self.allTargetsReached = allReached
		self._lastUpdateTime = time.time()
			
			
		#for pos in range(0, self.servoCount):
		#	id = self._servoIds[pos];
		#	value = self._servos.ReadPos(id);
		#	target = self.__targets.get_value(pos);
		#	diff = target-value;
		#	zone = 3;
		#	if (True or diff < -zone or diff > zone):
		#		#print ("diff: " + str(diff))
		#		diff = max(-10, diff);
		#		diff = min(10, diff);
		#		self._servos.MoveServo(id, 0, value + diff);

		
	def MoveServo(self, id, pos):
		no = self.__getNumberForId(id);
		self.__targets.set_value(no, pos);
		self.allTargetsReached = False;

		
	def __getNumberForId(self, id):
		for no in range(0, self.servoCount):
			if (id == self._servoIds[no]):
				return no;

	#def _readServoDirectly(self, id, pos):
	#	no = self.__getNumberForId(id);
	#	value = self._servos.ReadPos(id);
	#	self.__values.set_value(pos, value); # cache the value

	#def _moveServoDirectly(self, id, pos):
	#	no = self.__getNumberForId(id);
	#	self._servos.MoveServo(id,0,pos);
	
	def MoveToAndWait(self, positions):
		self.MoveToWithOutWait(positions);
		while (self.allTargetsReached == False):
			time.sleep(0.01);
			
	def MoveToWithOutWait(self, positions):
		for p in range(0,len(positions)):
			id = positions[p][0]
			value = positions[p][1]
			self.MoveServo(id, value)

	def Release(self):
		if (self._released == False):
			print("releasing " + self._processName)
			self._released = True;
			super().EndUpdating();
			print("super().EndUpdating() " + self._processName)
			time.sleep(self._actualSpeedDelay*10); 
			self._servos.ShutDown(self._servoIds);
			self. _servos.Release();

	def __del__(self):
		self.Release()

def exit_handler():
	tester.Release()
	
def bigTest():
	ended = False;
	servos = LX16AServos();
	tester = SmartServoManager(lX16AServos=servos, servoIds= [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],ramp=0, maxSpeed=1);

	armHanging 		= [[1,151],[2,168],[3,455],[4,613],[5,471],[6,550]];
	wink1 			= [[1,374],[2,451],[3,693],[4,816],[5,565]];
	wink2 			= [[1,192],[2,678],[3,888],[4,872],[5,509]];
	strechSide		= [[1,299],[2,249],[3,663],[4,660],[5,848]];
	lookHand		= [[1,592],[2, 90],[3,361],[4,787],[5,795]];
	ghettoFist1		= [[1,105],[2,140],[3,525],[4,910],[5,116],[6,420]];
	ghettoFist2		= [[1,339],[2,138],[3,525],[4,753],[5,116],[6,420]];
	
	closeHand		= [[6,420]];
	openHand		= [[6,550]];
	
	lookRightHand	= [[13,500-150],[14,500+150],[15,500-250]];
	lookFront		= [[13,500],[14,500],[15,500]];
	
	#tester.MoveServo(4,613);
	
	
	#while(True):
	if (True):
	
		tester.MoveToAndWait(lookFront + armHanging);
		time.sleep(1);
	
		tester.MoveToAndWait(closeHand);
		tester.MoveToAndWait(openHand);

		tester.MoveToAndWait(strechSide + lookRightHand);
		time.sleep(2);
	
		for wink in range(0,2):
			tester.MoveToAndWait(wink1);
			tester.MoveToAndWait(wink2);

		tester.MoveToAndWait(armHanging);
		time.sleep(1);
			
		tester.MoveToAndWait(strechSide);
		time.sleep(2);
		
		tester.MoveToAndWait(armHanging);
		time.sleep(1);

	tester.MoveToAndWait(ghettoFist1);
	tester.MoveToAndWait(ghettoFist2);
	tester.MoveToAndWait(ghettoFist1);

	tester.MoveToAndWait(armHanging);
	time.sleep(2);
	
	tester.Release();
	print("done");
	
def SingleTest():
	ended = False;
	servos = LX16AServos();
	tester = SmartServoManager(lX16AServos=servos, servoIds= [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],ramp=0, maxSpeed=1);

	plus = 100;

	while(True):
		
		plus = - plus;
		
		tester.MoveServo(13,500+plus);
		tester.MoveServo(14,500-plus);
		tester.MoveServo(15,500+plus);
		while (tester.allTargetsReached == False):
			time.sleep(0.1);



if __name__ == "__main__":
	#SingleTest();
	bigTest();
