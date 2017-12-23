/*
  Roobert - home robot project
  ________            ______             _____ 
  ___  __ \______________  /_______________  /_
  __  /_/ /  __ \  __ \_  __ \  _ \_  ___/  __/
  _  _, _// /_/ / /_/ /  /_/ /  __/  /   / /_  
  /_/ |_| \____/\____//_.___/\___//_/    \__/

 Project website: http://roobert.springwald.de

 ######################
 # head monitor mount #
 ######################

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

InnerFaceWidth=180;
InnerFaceHeight=150;
InnerFaceDepth=20;
InnerFaceDemoRotation=0;

motorDistance = InnerFaceWidth+17;

motorHolderAngle = 30;

MonitorLCDDepth=7;

cameraPos = [0,12,67];

use <Stepper5VGear.scad>

module Camera() 
{
    depth = 30;
    depthPCB=10;
    depthPCB2=20;
    translate([0,-.5,-20]) cube([26,5,20],center=true); // pcb
    translate([0,-2-(depthPCB2/2-5),0]) cube([26,depthPCB2,25],center=true); // cable hole
    translate([0,0,-2.5]) cube([9.2,depth,9.2],center=true); // camera
    translate([-7.5,depth/2,7]) rotate([90,0,0]) cylinder(depth,r=1,$fn=resolutionLow(),center=true); // Led
    translate([-7.5,depthPCB-7,7]) rotate([90,0,0]) cylinder(6,r=3,$fn=resolutionLow(),center=true); // Led hole
    translate([0,0,7]) cube([8,4 +(depthPCB-5),11],center=true); // clip hole
}

module CameraBox() 
{
    depth = 5;
    translate([0,depth,0]) color([0,0,1]) cube([29,depth,29],center=true); // camera box   
}

module MonitorLCD() {
    width=166;
    height=105;
    depth= MonitorLCDDepth;
    translate([-width/2,-depth,-height/2]) cube([width,depth*20,height],center=false);
}

module MonitorPCB() {
    width=167;
    height=125;
    depth= 50;
    sticks = 12;
    difference() {
        translate([-width/2,MonitorLCDDepth,-height/2]) cube([width,depth*2,height],center=false);
        translate([-width/2+sticks,MonitorLCDDepth,-height/2]) cube([width-sticks*2,depth*2,height],center=false);
    }
}

module MonitorScrewHoles() 
{
    depth=50;
    radius=1.7;
    distX = 157;
    distY = 115;
    translate([-distX/2,0,distY/2]) rotate([90,0,0]) cylinder(depth,r=radius,$fn=resolutionLow(),center=true); // 1
    translate([distX/2,0,distY/2]) rotate([90,0,0]) cylinder(depth,r=radius,$fn=resolutionLow(),center=true); // 2
    translate([-distX/2,0,-distY/2]) rotate([90,0,0]) cylinder(depth,r=radius,$fn=resolutionLow(),center=true); // 3
    translate([distX/2,0,-distY/2]) rotate([90,0,0]) cylinder(depth,r=radius,$fn=resolutionLow(),center=true); // 4
}

module HDMIPort() {
    width=30;
    height=23;
    depth=14;
    margin=3;
    posY = 115/2-33;
    translate([InnerFaceWidth/2-width/2,MonitorLCDDepth-margin,posY]) rotate([0,0,0]) cube([width,depth,height],center=false);
}

module USBPort() {
    width=30;
    height=12;
    depth=11;
    margin=3;
    posY = 115/2-46;
    translate([InnerFaceWidth/2-width/2,MonitorLCDDepth-margin,posY]) rotate([0,0,0]) cube([width,depth,height],center=false);
}

module GroveUltraSonicSensor() {

    sensorDiameter = 16;
    sensorHeight= 30;
    sensorDistance=22;
    
    // Sensors
    translate ([sensorDistance/2,-sensorHeight/2,0]) rotate([90,0,0])  cylinder(sensorHeight, r=sensorDiameter/2, $fn=resolutionHi(), center=true);
    translate ([-sensorDistance/2,-sensorHeight/2,0]) rotate([90,0,0])  cylinder(sensorHeight, r=sensorDiameter/2, $fn=resolutionHi(), center=true);
    
    //PCB
    cube([50,20,25],center=true);
    
    // Cable adapter
    translate ([0,-11,-10]) cube([12,8,20],center=true);
}

module GrovePIRMotionSensor() {
    
    sensorDiameter = 16;
    sensorHeight= 30;

    // Sensors    
    translate ([-16,-9.5,0]) rotate([90,0,0])  cylinder(sensorHeight, r=sensorDiameter/2, $fn=resolutionHi(), center=true);
    
    //PCB
    cube([47,20,24],center=true);
    
    // Cable adapter
    translate ([18,19.5-11,-2]) cube([11,60,17],center=true);
}

module GLVL53L0XV2_TimeOfLightSensor() {

    holeHeight = 40;

    // Sensor  
    translate ([0,-15,-1]) cube([13,30,9],center=true);
    
    // Holes
    translate ([-10,-9.5,0]) rotate([90,0,0])  cylinder(holeHeight, r=3.5/2, $fn=resolutionLow(), center=true);
    translate ([10,-9.5,0]) rotate([90,0,0])  cylinder(holeHeight, r=3.5/2, $fn=resolutionLow(), center=true);
    
    //PCB
    cube([26,20,11],center=true);
    
    // Cable adapter
    //translate ([18,19.5-11,-2]) cube([11,60,17],center=true);
}


module InnerFace() {
    additionalTopHeight = 7;
    width=180;
    height=150 + additionalTopHeight;
    margin= 14;
    difference() 
    {
        translate([-width/2,0,-height/2+additionalTopHeight/2]) cube([width,InnerFaceDepth,height],center=false);
        //translate([0,15,height/2-margin]) cube([width-margin*3,InnerFaceDepth,20],center=true);
    }
}

module HeadSphere(radius) 
{
    intersection() 
    {
        rotate([10,0,0]) scale ([0.9,1.1,0.72]) sphere(radius, $fn=resolutionHi(), center=true);
        translate ([0,0,190]) rotate([10,0,0]) scale([3,2.5,2])  sphere(radius, $fn=resolutionHi(), center=true);
    }
}

module InnerHead() {
    intersection() {
        difference() {
            union() {
                difference() {
                    InnerFace();
                union() {
                    MonitorLCD();
                    MonitorPCB();
                    MonitorScrewHoles();
                    HDMIPort();
                    USBPort();
                    translate([-40,22,67]) GroveUltraSonicSensor();
                    translate([40,24,67]) rotate([0,0,0]) GrovePIRMotionSensor();
                    translate([0,15,-60]) GLVL53L0XV2_TimeOfLightSensor();
                }
            }
            translate(cameraPos) rotate([0,0,180]) CameraBox();
            }
            translate(cameraPos) rotate([0,0,180]) Camera();
        }
        HeadSphere(131);
    }
    
   
    
    
}

module OneMotor(left, axisAngle) {
    rotate([0, 90,0]) {
        if (left) {
             Stepper5VGear(10,axisAngle);
        } else {
            mirror([0,0,1])Stepper5VGear(10,axisAngle);
        }
    }
}

MotorHolderWidth = 7;

module MotorHolder(left, drawMotor) 
{
    //rotate ([0,90,0]) cylinder(1000,r=1,$fn=resolution,center=true);
    
    x = left ? -motorDistance/2 : motorDistance/2 ;
    
    MotorHolderHeight = 200;
    MotorHolderDepth = 42;
    
    translate([x,0,-7.7]) 
    {
        difference() 
        {
            
            union() 
            {
                translate([0,0,-MotorHolderHeight/2]) cube([MotorHolderWidth,MotorHolderDepth,MotorHolderHeight],center=true); 
                rotate([0,90,0]) cylinder(MotorHolderWidth,r=MotorHolderDepth/2,$fn=resolutionHi(),center=true);
            }
            translate([left ? 4.5 : -4.5,0,0]) 
            {    
                OneMotor(left, 90-motorHolderAngle);
            }
        }
        if (drawMotor) {
            translate([left ? 4.5 : -4.5,0,0]) 
            {    
                OneMotor(left, 90-motorHolderAngle);
            }
        }
    }
}

motorHolderTranslation = [0,10,-5];
motorHolderRotation = [motorHolderAngle-InnerFaceDemoRotation,0,0];

module DrawInnerHead() {
    rotate([InnerFaceDemoRotation,0,0]) 
    {
        difference() 
        {
            InnerHead();
            translate(motorHolderTranslation) 
            {
                rotate (motorHolderRotation) 
                {
                    MotorHolder(false, true);
                    MotorHolder(true, true);  
                }
            }
        }
    }
}
    
bottomYPos = -100;

module DrawMotorHolder(leftHolder, drawMotor) {
    difference() {
        rotate([InnerFaceDemoRotation,0,0]) 
        {
            // motor holder and outer head 
            translate(motorHolderTranslation) 
            {
                rotate (motorHolderRotation) 
                {
                    MotorHolder(leftHolder, drawMotor);
                }
            }
        }
        dummySize = 400;
        translate([-dummySize/2,-dummySize/2,bottomYPos-dummySize]) cube([dummySize,dummySize,dummySize],center=false); // Height cut
    }
    bottomWidth=25;
    bottomHeight=5;
    move = leftHolder==false ? (motorDistance+MotorHolderWidth)/2 - bottomWidth: -(motorDistance+MotorHolderWidth)/2 ;
    translate([move, 40.6,bottomYPos]) cube([bottomWidth,50,bottomHeight],center=false);  // bottom
}

DrawInnerHead();

// DrawMotorHolder(leftHolder=true, drawMotor=true);
// DrawMotorHolder(leftHolder=false, drawMotor=true);


