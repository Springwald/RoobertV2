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
use <..\..\Parts\LX-16A-Servo.scad>

bottomYPos = -100;
neckPipeXPos = 60;

innerNeckPipeDiameter = 35;
innerNeckPipeHeight=55;

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
    margin=2.5;
    translate([0,neckPipeXPos,-innerNeckPipeHeight/2]) {
        cylinder(innerNeckPipeHeight+50,r=innerNeckPipeDiameter/2-margin,$fn=resolutionHi(),center=true); 
    }
}

module NeckGearAdapter(margin) {
    height= 6;
    radius=20;
    color([0,1,1]) {
        translate([0,neckPipeXPos,-10-height/2]) {
            cylinder(height,r=radius+margin,$fn=6,center=true); 
        }   
    }
}

module NeckPipe() {
    distancerHeight = 5;
    distancerDiameter=innerNeckPipeDiameter+20;
    sideHoleHeight=35;
    sideHoleWidth=10;
    translate([0,0,bottomYPos]) {
        difference() {
            union() {
                translate([0,neckPipeXPos,-innerNeckPipeHeight/2])
                    cylinder(innerNeckPipeHeight,r=innerNeckPipeDiameter/2,$fn=resolutionHi(),center=true); 
                
            }
            union() {
                NeckPipeHole();
            }
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
                translate([-52,77,10]) rotate ([0,0,0]) I2CHub();
                translate([0,0,-bottomYPos]) MotorHolderSkrewHoles(leftHolder=true);
                translate([0,0,-bottomYPos]) MotorHolderSkrewHoles(leftHolder=false);
                MakerBeamAdapterTop();
           }
        }
        if (drawPcbs) {
            translate([-52,77,10]) rotate ([0,0,0]) I2CHub();
            MakerBeamAdapterTop();
        }
        
    }
}

module NeckServoConnector() {
    extraWidth=2;
    height = 30;
    translate([0,neckPipeXPos,-innerNeckPipeHeight/2+bottomYPos-innerNeckPipeHeight]) 
        cylinder(height,r=innerNeckPipeDiameter/2+ extraWidth,$fn=resolutionHi(),center=true); 
}


module MakerBeamAdapterTop() {
    color([0,0,1]) {
        translate([0,neckPipeXPos,0]) {
            translate([-25,0,0]) cylinder(30,r=3.1/2,$fn=resolutionLow(),center=true); 
            translate([+25,0,0]) cylinder(30,r=3.1/2,$fn=resolutionLow(),center=true); 
        }
    }
}


module MakerBeamAdapterBottom() {

    translate([0,neckPipeXPos,-200]) 
    {
        difference() {
        depth = 8.75;
        color([1,0,0]) {
            translate([0,0,0]) rotate([0,0,15])  cylinder(depth,r=12,$fn=resolutionHi(),center=true);
            margin=3;
            translate([0,0,margin/2]) cube([40,15,depth-margin],center=true);
         }
        union() {
            translate([0,0,-30]) LX16AAxis(moveUpToServoPos=false);
            translate([0,0,-9])LX16AAxisScrewDriverTunnels();
            translate([-15,0,0]) cylinder(30,r=3.1/2,$fn=resolutionLow(),center=true); 
            translate([+15,0,0]) cylinder(30,r=3.1/2,$fn=resolutionLow(),center=true); 
        }
    }
    }
    
}




//DrawInnerHead();

NeckPipe();
NeckTop(drawPcbs=true);
MakerBeamAdapterBottom();
//NeckServoConnector();
DrawMotorHolder(leftHolder=true, drawMotor=true);
DrawMotorHolder(leftHolder=false, drawMotor=true);



