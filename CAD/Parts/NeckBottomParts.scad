/*
  Roobert - home robot project
  ________            ______             _____ 
  ___  __ \______________  /_______________  /_
  __  /_/ /  __ \  __ \_  __ \  _ \_  ___/  __/
  _  _, _// /_/ / /_/ /  /_/ /  __/  /   / /_  
  /_/ |_| \____/\____//_.___/\___//_/    \__/

 Project website: http://roobert.springwald.de

 #####################
 # neck bottom parts #
 #####################

 Licensed under MIT License (MIT)

 Copyright (c) 2018 Daniel Springwald | daniel@springwald.de

 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to permit
 persons to whom the Software is furnished to do so, subject to
 the following conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 DEALINGS IN THE SOFTWARE.

*/

function resolutionLow() = ($exportQuality==true) ? 20 : 10;
function resolutionHi() = ($exportQuality==true) ? 300 : 50;

use <..\Parts\HeadParts.scad>
use <..\Parts\NeckParts.scad>
use <..\Parts\Stepper5VGear.scad>

bottomYPos = -115;
neckPipeXPos = 60;






module NeckMotorGear() {
    top = -115;
        translate([-15,-15,0]) {
            scale([3.25,3.25,1]) 
                linear_extrude(height = 12, center = true, convexity = 100)
                import("NeckMotorGear.dxf");
    }

}

module NeckMotor() {
    translate([0,neckPipeXPos+69.5,bottomYPos]) 
    {
        // Axis
        cylinder(h=30, r=2.5, $fn=resolutionLow(), center=true); 
    
        // Gear
        NeckMotorGear();
    }
}

//DrawInnerHead();

NeckGear();

NeckPipe();
NeckTop(drawPcbs=false);
DrawMotorHolder(leftHolder=true, drawMotor=true);
DrawMotorHolder(leftHolder=false, drawMotor=true);

NeckMotor();



