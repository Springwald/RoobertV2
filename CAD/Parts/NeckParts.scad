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
neckPipeXPos = 60;

innerNeckPipeDiameter = 33.8;
innerNeckPipeHeight=50;

module I2CHub() {
     color([0.5,.5,.5]) {
        radius = 2.7 /2;
        depth = 20;
        distanceX=20;
        distanceZ=20;
        width=40;
        height=21;
        
        translate([distanceX / 2,  distanceZ / 2,-depth/2]) cylinder(h=depth * 2, r=radius, $fn=resolutionLow(), center=true); 
        translate([distanceX / 2, -distanceZ / 2,-depth/2]) cylinder(h=depth * 2, r=radius, $fn=resolutionLow(), center=true); 
        translate([-width / 2,0,-depth/2]) cylinder(h=depth * 2, r=radius, $fn=resolutionLow(), center=true); 
        cube([width,height,3],center=true);
    }
}

module PCF8574() {
    color([1,0,0]) {
        radius = 2.7 /2;
        depth = 20;
        distanceX= 35;
        distanceZ=20;
        width=50;
        height=16;
        
        translate([distanceX / 2,  distanceZ / 2,-depth/2]) cylinder(h=depth * 2, r=radius, $fn=resolutionLow(), center=true); 
        translate([-distanceX / 2, distanceZ / 2,-depth/2]) cylinder(h=depth * 2, r=radius, $fn=resolutionLow(), center=true); 
        translate([-distanceX / 2,-distanceZ / 2,-depth/2]) cylinder(h=depth * 2, r=radius, $fn=resolutionLow(), center=true); 
        translate([distanceX / 2, -distanceZ / 2,-depth/2]) cylinder(h=depth * 2, r=radius, $fn=resolutionLow(), center=true); 
        
        cube([width,height,3],center=true);
    }
}

module NeckPipeHole() {
    margin=2;
    translate([0,neckPipeXPos,-innerNeckPipeHeight/2]) {
        cylinder(innerNeckPipeHeight+50,r=innerNeckPipeDiameter/2-margin,$fn=resolutionHi(),center=true); 
    }
}

module NeckGearAdapter() {
    height= 6;
    radius=20;
    color([0,1,1]) {
        translate([0,neckPipeXPos,-10-height/2]) {
            cylinder(height,r=radius,$fn=6,center=true); 
        }   
    }
}

module NeckPipe() {
    distancerHeight = 5;
    distancerDiameter=innerNeckPipeDiameter+20;
    translate([0,0,bottomYPos]) {
        difference() {
            union() {
                translate([0,neckPipeXPos,-innerNeckPipeHeight/2]) cylinder(innerNeckPipeHeight,r=innerNeckPipeDiameter/2,$fn=resolutionHi(),center=true); 
                color([1,0,1]) translate([0,neckPipeXPos,-distancerHeight*1.5]) cylinder(distancerHeight,r=distancerDiameter/2,$fn=resolutionHi(),center=true); 
                NeckGearAdapter();
            }
            NeckPipeHole();
        }
    }
}

module NeckTop(drawPcbs) {
    
    translate([0,0,bottomYPos]) {
        bottomWidth=204;
        bottomDepth=35;
        bottomHeight=5;
        difference() {
            intersection() {
                translate([0, 30.5+bottomDepth/2,-bottomHeight/2]) cube([bottomWidth,50+bottomDepth,bottomHeight],center=true);  // bottom
                r = 260;
                translate([0,530-r,0]) cylinder(30,r=r,$fn=resolutionHi(),center=true);  // round back
            }
            union() {
                MotorHolderSkrewHoles(true);
                MotorHolderSkrewHoles(false);
                NeckPipeHole();
                
                motorPcbX = 60;
                translate([motorPcbX, 70, 5]) color([1,0,0]) Stepper5VGearPCB();
                translate([-motorPcbX, 70, 5]) color([1,0,0]) Stepper5VGearPCB();
                translate([0+45,35,3]) PCF8574();
                translate([+-45,35,3]) PCF8574();
                translate([-30,72,10]) rotate ([0,0,90]) I2CHub();
                translate([0,0,-bottomYPos]) MotorHolderSkrewHoles(leftHolder=true);
                translate([0,0,-bottomYPos]) MotorHolderSkrewHoles(leftHolder=false);
            }
        }
        if (drawPcbs) {
            motorPcbX = 60;
            translate([motorPcbX, 70, 5]) color([1,0,0]) Stepper5VGearPCB();
            translate([-motorPcbX, 70, 5]) color([1,0,0]) Stepper5VGearPCB();
            translate([0+45,35,3]) PCF8574();
            translate([+-45,35,3]) PCF8574();
            translate([-30,72,10]) rotate ([0,0,90]) I2CHub();
        }
        
    }
}



DrawInnerHead();



NeckPipe();
NeckTop(drawPcbs=true);
DrawMotorHolder(leftHolder=true, drawMotor=true);
DrawMotorHolder(leftHolder=false, drawMotor=true);



