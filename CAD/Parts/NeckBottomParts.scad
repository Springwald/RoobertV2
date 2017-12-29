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
use <..\Parts\StepperTrinamicQSH4218_35_10_27.scad>
use <..\Parts\KFL007Bearing35mm.scad>

bottomYPos = -115;
neckPipeXPos = 60;


module NeckMotorGear() {
    translate([-15,-15,0]) {
        scale([3.25,3.25,1]) 
            linear_extrude(height = 12, center = true, convexity = 100)
            import("NeckMotorGear.dxf");
    }
}

module NeckMotor() {
    translate([0,neckPipeXPos+69.5,bottomYPos-51]) 
    {
        // Motor
        StepperTrinamicQSH4218_35_10_27();
        
        // Gear
        translate([0,0,51]) {
            NeckMotorGear();
        }
    }
}

module NeckBearring(drawHoles) {
    color([1,0.5,0.2]) translate([0,neckPipeXPos,bottomYPos-1-31.3]) KFL007Bearing35mm(drawHoles); // Bearring
}

module MakerBeamHoles() {
    width  = 145;
    depth = 155;
    radius = 3.1;
    for(x = [-width/2 : width : width/2]) {
        for(y = [-depth/2 : depth / 5 : depth/2]) {
            translate([x,y,-20]) {
                cylinder(h=30, r=radius/2, $fn=resolutionLow(), center=true); // base body corner
            }
        }
    }
    for(x = [-width/2 : 30 : width/2]) {
        for(y = [-depth/2 : depth : depth/2]) {
            if (y < 10 || (x > 20 || x < -20))  {
                translate([x,y,-20]) {
                    cylinder(h=30, r=radius/2, $fn=resolutionLow(), center=true); // base body corner
                }
            }
        }
    }
}

module NeckBaseMicroSwitch() {
    holeRadius = 3.1/2;
    height = 43;
    difference() 
    {
        translate([10,6.5,2]) cube([20,8,height],center=true);  // microswitch holder
        
        translate([9,14,22]) rotate([-90,0,90]) color([0.6,0,.8]) {
            translate([0,8,-9.5 / 2]) rotate ([0,90,0]) cylinder(30,r=holeRadius,$fn=resolutionLow(),center=true);
            translate([0,8,9.5 / 2])  rotate ([0,90,0]) cylinder(30,r=holeRadius,$fn=resolutionLow(),center=true);
            cube([6.2,16,22],center=true); 
        }
    }
}

module NeckBase() {
    width  = 160;
    depth = 170;
    height = 5;
    
    zPos = -32;
    NeckBaseYPosMoveBackwards = 10;
    
    elipseHeight = 20;
    cornerRound = 20;
        
    difference() 
    {
        translate([0,neckPipeXPos,bottomYPos+zPos])  {
            
            translate([0,NeckBaseYPosMoveBackwards,-20]) cube([width-cornerRound,depth,height],center=true); // base body
            translate([0,NeckBaseYPosMoveBackwards,-20]) cube([width,depth-cornerRound,height],center=true); // base body
            
            translate([width/2-cornerRound/2,NeckBaseYPosMoveBackwards + depth/2 - cornerRound/2,-20]) cylinder(h=height, r=cornerRound/2, $fn=resolutionHi(), center=true); // base body corner
            translate([-width/2+cornerRound/2,NeckBaseYPosMoveBackwards + depth/2 - cornerRound/2,-20]) cylinder(h=height, r=cornerRound/2, $fn=resolutionHi(), center=true); // base body corner
            translate([-width/2+cornerRound/2,NeckBaseYPosMoveBackwards - depth/2 + cornerRound/2,-20]) cylinder(h=height, r=cornerRound/2, $fn=resolutionHi(), center=true); // base body corner
            translate([width/2-cornerRound/2,NeckBaseYPosMoveBackwards - depth/2 + cornerRound/2,-20]) cylinder(h=height, r=cornerRound/2, $fn=resolutionHi(), center=true); // base body corner
        
                       
            translate([0,0,-9]) scale([1,.6,1]) color([1,0.2,0.2]) cylinder(h=elipseHeight, r=(width-20)/2, $fn=resolutionHi(), center=true);// elipse body
            
            translate([0,-60,0]) NeckBaseMicroSwitch();
        }
        union()
        {
            NeckMotor();
            NeckBearring(drawHoles=true);
            translate([0,neckPipeXPos+NeckBaseYPosMoveBackwards,bottomYPos+zPos]) MakerBeamHoles();
        }
    }
    
    
}

if (true) {
    DrawInnerHead();
    DrawMotorHolder(leftHolder=true, drawMotor=false);
    DrawMotorHolder(leftHolder=false, drawMotor=false);
    NeckGear();
    NeckTop(drawPcbs=false);
    NeckBase();
    NeckBearring(drawHoles=false);
}

NeckPipe();
NeckMotor();





