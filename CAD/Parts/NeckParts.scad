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

function resolutionLow() = ($exportQuality==true) ? 20 : 10;
function resolutionHi() = ($exportQuality==true) ? 300 : 50;

use <..\Parts\HeadParts.scad>
use <..\Parts\Stepper5VGear.scad>

bottomYPos = -100;
neckPipeXPos = 100;

innerNeckPipeDiameter = 33.8;
innerNeckPipeHeight=30;


module PCF8574() {
    radius = 2.7 /2;
    depth = 10;
    distanceX= 27;
    distanceZ=29.5;
    width=32;
    height=35;
    
    translate([distanceX / 2,  distanceZ / 2,-depth]) cylinder(h=depth * 2, r=radius, $fn=resolutionLow(), center=true); 
    translate([-distanceX / 2, distanceZ / 2,-depth]) cylinder(h=depth * 2, r=radius, $fn=resolutionLow(), center=true); 
    translate([-distanceX / 2,-distanceZ / 2,-depth]) cylinder(h=depth * 2, r=radius, $fn=resolutionLow(), center=true); 
    translate([distanceX / 2, -distanceZ / 2,-depth]) cylinder(h=depth * 2, r=radius, $fn=resolutionLow(), center=true); 
    
    cube([width,height,3],center=true);
}

module NeckPipeHole() {
    margin=2;
    translate([0,neckPipeXPos,-innerNeckPipeHeight/2]) {
        cylinder(innerNeckPipeHeight+50,r=innerNeckPipeDiameter/2-margin,$fn=resolutionHi(),center=true); 
    }
}

module NeckPipe() {
    translate([0,0,bottomYPos]) {
        difference() {
                translate([0,neckPipeXPos,-innerNeckPipeHeight/2]) cylinder(innerNeckPipeHeight,r=innerNeckPipeDiameter/2,$fn=resolutionHi(),center=true); 
                NeckPipeHole();
        }
    }
}

module NeckTop() {
    
    translate([0,0,bottomYPos]) {
        bottomWidth=204;
        bottomDepth=30;
        bottomHeight=5;
        difference() {
            union() {
                translate([0, 65.5+bottomDepth/2,-bottomHeight/2]) cube([bottomWidth,50+bottomDepth,bottomHeight],center=true);  // bottom
            }
            union() {
                MotorHolderSkrewHoles(true);
                MotorHolderSkrewHoles(false);
                NeckPipeHole();
            }
        }
        
        motorPcbX = 60;
        translate([motorPcbX, 75, 5]) Stepper5VGearPCB();
        translate([-motorPcbX, 75, 5]) Stepper5VGearPCB();
        PCF8574();
    }
}






DrawInnerHead();



NeckPipe();
NeckTop();
DrawMotorHolder(leftHolder=true, drawMotor=true);
DrawMotorHolder(leftHolder=false, drawMotor=true);



