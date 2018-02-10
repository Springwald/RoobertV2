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
	_actualSpeedDelay = .002
	_maxStepsPerSpeedDelay = 20
	
	_servos 	= None;
	servoCount = 0;
	_servoIds	= [];
	__targets	= None; 
	__values	= None;
	
	__shared_ints__				= None
	
	_released = False;
	
	@property
	def allTargetsReached(self):
		#print (self.__shared_ints__.get_value(self.__targets_reached_int__)== 1)
		return self.__shared_ints__.get_value(self.__targets_reached_int__)== 1
	@allTargetsReached.setter
	def allTargetsReached(self, value):
		if (value == True):
			self.__shared_ints__.set_value(self.__targets_reached_int__,1)
		else:
			self.__shared_ints__.set_value(self.__targets_reached_int__,0)

	def __init__(self, lX16AServos, servoIds):
		
		super().__init__(prio=-20)
		
		self.servoCount = len(servoIds);
		self._servoIds = servoIds;
		self._servos = lX16AServos;
		self.__targets = SharedInts(max_length=self.servoCount);
		self.__values = SharedInts(max_length=self.servoCount);
		
		self.__shared_ints__			= SharedInts(max_length=3)
		self.__targets_reached_int__	= self.__shared_ints__.get_next_key()
		
		self._processName = "SmartServoManager";
		
		# initial read of servo positions
		for pos in range(0, self.servoCount):
			id = self._servoIds[pos];
			value = self._servos.ReadPos(id);
			self.__values.set_value(pos, value);
			self.__targets.set_value(pos, value);
			print(self.__values.get_value(pos));
			
		super().StartUpdating()
		
	def Update(self):
		#print("update start " + str(time.time()))
		if (super().updating_ended == True):
			return
		
		timeDiff = time.time() - self._lastUpdateTime
		if (timeDiff < self._actualSpeedDelay):
			time.sleep(self._actualSpeedDelay - timeDiff)
		#time.sleep(self._actualSpeedDelay)
		#timeDiff = time.time() - self._lastUpdateTime
		#timeDiff = min(timeDiff, self._actualSpeedDelay * 2)
		allReached = True
		#maxSpeed = self._maxStepsPerSecond * timeDiff
		
		for i in range(0, self.servoCount):
			reachedThis = True
			id = self._servoIds[i];
			value = self._servos.ReadPos(id);
			diff = int(self.__targets.get_value(i) - value) #self.__values.get_value(i))
			plus = 0
			
			tolerance = 20;
			
			if (diff > tolerance):
				plus = max(1, min(diff, self._maxStepsPerSpeedDelay))
				reachedThis = False
			if (diff < -tolerance):
				plus = min(-1, max(diff , -self._maxStepsPerSpeedDelay))
				reachedThis = False

			if (reachedThis == False):
				#print(str(value) + " > " + str(plus));
				#time.sleep(1);
				allReached = False
				newValue = int(value + plus) # self.__values.get_value(i) + plus
				#self.__values.set_value(i,newValue)
				#self.setServo(i,newValue)
				self._servos.MoveServo(id, 0, newValue);
				
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

		
	# resets the servo slowly and waits till it reached its reset position
	def ResetServo(self, id, pos):
		self.servos.MoveServo(self._servoIds[0],0,500);
		
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

	def Release(self):
		if (self._released == False):
			print("releasing " + self._processName)
			self._released = True;
			super().EndUpdating();
			self. _servos.Release();
			print("super().EndUpdating() " + self._processName)

	def __del__(self):
		self.Release()

def exit_handler():
	tester.Release()

if __name__ == "__main__":

	ended = False;
	servos = LX16AServos();
	tester = SmartServoManager(lX16AServos=servos, servoIds= [1,2,3,4,5]);
	
	for no in range(1, 5):
		tester.MoveServo(no, 500);
	while (tester.allTargetsReached == False):
		time.sleep(0.1);
	
	tester.MoveServo(1, 200);
	tester.MoveServo(2, 900);
	while (tester.allTargetsReached == False):
		time.sleep(0.1);
		
	tester.MoveServo(1, 200);
	tester.MoveServo(2, 150);
	while (tester.allTargetsReached == False):
		time.sleep(0.1);
		
	tester.MoveServo(1, 200);
	tester.MoveServo(2, 900);
	tester.MoveServo(3, 200);
	tester.MoveServo(4, 150);
	while (tester.allTargetsReached == False):
		time.sleep(0.1);
	
	for no in range(1, 5):
		tester.MoveServo(no, 500);
	while (tester.allTargetsReached == False):
		time.sleep(0.1);
	
	tester.Release();
	print("done");
