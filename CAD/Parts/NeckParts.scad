/*
  Roobert - home robot project
  ________            ______             _____ 
  ___  __ \______________  /_______________  /_
  __  /_/ /  __ \  __ \_  __ \  _ \_  ___/  __/
  _  _, _// /_/ / /_/ /  /_/ /  __/  /   / /_  
  /_/ |_| \____/\____//_.___/\___//_/    \__/

 Project website: http://roobert.springwald.de

 ##############
 # neck parts #
 ##############

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

function resolutionLow() = ($exportQuality==true) ? 30 : 10;
function resolutionHi() = ($exportQuality==true) ? 300 : 50;

use <..\Parts\HeadParts.scad>

motorDistance = InnerFaceWidth+17;
bottomYPos = -100;

module NeckPipe() {
    innerPipeDiameter = 33.8;
    innerPipeHight=30;
    margin=2;
    difference() {
        cylinder(innerPipeHight,r=innerPipeDiameter/2,$fn=resolutionHi(),center=true); 
        cylinder(innerPipeHight+10,r=innerPipeDiameter/2-margin,$fn=resolutionHi(),center=true); 
    }
}

module NeckTop() {
    
    bottomWidth=204;
    bottomHeight=5;
    difference() {
        union() {
            translate([0, 65.5,bottomYPos-bottomHeight/2]) cube([bottomWidth,50,bottomHeight],center=true);  // bottom
        }
        MotorHolderSkrewHoles(true);
        MotorHolderSkrewHoles(false);
    }
}




NeckPipe();
NeckTop();
DrawMotorHolder(leftHolder=true, drawMotor=true);
DrawMotorHolder(leftHolder=false, drawMotor=true);



