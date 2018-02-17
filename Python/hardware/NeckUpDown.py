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
#     ########################################
#     # neck left/right motor control module #
#     ########################################
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
from GroveI2CMotorDriver import GroveI2CMotorDriver
from I2cIoExpanderPcf8574 import I2cIoExpanderPcf8574
from StepperMotorControl import StepperMotorControl


class NeckUpDown(StepperMotorControl):

	_motorName                = "neck up/down"

	_i2cIoExpanderPcf8574Motor   = None      	# the I2cIoExpanderPcf8574 to control the 2 motors
	_i2cIoExpanderPcf8574EndStop = None      	# the I2cIoExpanderPcf8574 the endstop is connected to
	_endStopBit                  = 64         	# the bit of the I2cIoExpanderPcf8574 to read the motor endstop (1,2,4,8...)
    
	MaxSteps                     =  340         # how many motor steps can the motor maximum move 
    
	_isClosedCircle              = False      	# is 0 to maxSteps a full round to the same endstop
    
	_fastestSpeedDelay           = 0.005        # how fast can the stepper motor go
	_slowestSpeedDelay           = _fastestSpeedDelay * 4 
	_actualSpeedDelay            = _slowestSpeedDelay
    
	_rampSpeedup                 = 1.05         # how fast is the speed of for motor ramping
	_rampSafeArea                = 30           # prevent to come nearer than this to the endstop
    
	_stepData						= [0b00011000, 0b00100100, 0b01000010, 0b10000001]  # the stepper motor step bits (4 bits for each motor)
	_stepDataOff					= 0

	_released						 = False

	def __init__(self, i2cIoExpanderPcf8574Motor=None, i2cIoExpanderPcf8574EndStop=None):
		super().__init__()
		self._i2cIoExpanderPcf8574Motor=i2cIoExpanderPcf8574Motor
		self._i2cIoExpanderPcf8574EndStop = i2cIoExpanderPcf8574EndStop
		super().start()

	def _endStop(self):
		#print (self._i2cIoExpanderPcf8574EndStop.getBit(self._endStopBit))
		return self._i2cIoExpanderPcf8574EndStop.getBit(self._endStopBit)

	def _updateMotorSteps(self):
		if (super()._releasedMotor == True):
			return
		lastStepDataPos = self.lastStepDataPos
		actualStepDataPos = self.actualStepDataPos
		#print("actualStepDataPos = " + str(actualStepDataPos) + " of " + str(len(self._stepData)))
		if (lastStepDataPos != actualStepDataPos): # stepper has to move
			#print("actualStepDataPos " + self._motorName + ":" + str(actualStepDataPos))
			if (actualStepDataPos > len(self._stepData)-1):
				actualStepDataPos = len(self._stepData)-1
				print("actualStepDataPos >= "+ str(len(self._stepData)))
			else:
				if (actualStepDataPos < 0):
					actualStepDataPos = 0
					print("actualStepDataPos < 0")
			self._i2cIoExpanderPcf8574Motor.setByte(self._stepData[actualStepDataPos])
			self.lastStepDataPos = actualStepDataPos
			self.lastStepDataPosChange = time.time()
			
	def Release(self):
		if (self._released == False):
			super().ReleaseStepperMotor()
			self._released = True
			self._i2cIoExpanderPcf8574Motor.setByte(self._stepDataOff)

	def __del__(self):
		self.Release()

if __name__ == "__main__":
	endStop = I2cIoExpanderPcf8574(0x38, useAsInputs=True)
	motor = I2cIoExpanderPcf8574(0x3e, useAsInputs=False)

	controller = NeckUpDown(motor, endStop)

	for i in range(1, 2):
		
		controller.targetPos = 0
		while controller.targetReached == False:
			#print("wait for target "+ str(controller._targetPos))
			#controller.ManualUpdate()
			time.sleep(0.1)

		controller.targetPos = controller.MaxSteps
		while controller.targetReached == False:
			#print("wait for target "+ str(controller._targetPos))
			#controller.ManualUpdate()
			time.sleep(0.1)

			
	controller.Release()

