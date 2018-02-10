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
	
	_servos 	= None;
	servoCount = 0;
	_servoIds	= [];
	__targets	= None; 
	__values	= None;
	
	_released = False;

	def __init__(self, lX16AServos, servoIds):
		
		super().__init__(prio=-20)
		
		self.servoCount = len(servoIds);
		self._servoIds = servoIds;
		self._servos = lX16AServos;
		self.__targets = SharedInts(max_length=self.servoCount);
		self.__values = SharedInts(max_length=self.servoCount);
		
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
			
		for pos in range(0, self.servoCount):
			id = self._servoIds[pos];
			value = self._servos.ReadPos(id);
			target = self.__targets.get_value(pos);
			diff = target-value;
			zone = 3;
			if (True or diff < -zone or diff > zone):
				#print ("diff: " + str(diff))
				diff = max(-20, diff);
				diff = min(20, diff);
				self._servos.MoveServo(id, 0, value + diff);

		
	# resets the servo slowly and waits till it reached its reset position
	def ResetServo(self, id, pos):
		self.servos.MoveServo(self._servoIds[0],0,500);
		
	def MoveServo(self, id, pos):
		no = self.__getNumberForId(id);
		self.__targets.set_value(no, pos);

		
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
	tester.MoveServo(2,400);
	time.sleep(5);
	tester.MoveServo(2,700);
	time.sleep(5);
	print("done");
