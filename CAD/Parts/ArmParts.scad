/*
  Roobert - home robot project
  ________            ______             _____ 
  ___  __ \______________  /_______________  /_
  __  /_/ /  __ \  __ \_  __ \  _ \_  ___/  __/
  _  _, _// /_/ / /_/ /  /_/ /  __/  /   / /_  
  /_/ |_| \____/\____//_.___/\___//_/    \__/

 Project website: http://roobert.springwald.de

 #############
 # arm parts #
 #############

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

use <LX-16A-Servo.scad>

module MakerBeamHole() {
    height = 40;
    radius = 3.3;
    radiusScrew= 6;
    translate([0,0,height/2]) cylinder(h=height, r=radius/2, $fn=resolutionLow(), center=true); 
    translate([0,0,-height/2])cylinder(h=height, r=radiusScrew/2, $fn=resolutionLow(), center=true); 
}


module Arm01_Shoulder () {
    holderMargin = 5;
    difference() {
        union() {
            rotate([90,90,-90])
                LX16ACubeHolder();
            color([1,0,0]) 
                translate([10,8.4,12 + holderMargin/2 +2]) 
                    cube([18.6,30.4,holderMargin],center=true);
        }
        union() {
            translate([10,0,14]) MakerBeamHole();
            translate([10,17,14]) MakerBeamHole();
        }
    }
}

module Arm02_Top () {
    difference() {
        union() {
            rotate([0,90,0])
                translate([0,-12.5,0]) 
                    LX16ACircleHolderSteg();
            LX16ACircleHolder(false);
        }
        union() {
            translate([0,0,-3]) 
                LX16AAxis();
        }
    }
}

module Arm03_Top () {
    difference() 
    {
        union() {
            rotate([- 90,0,0])
                translate([0,2.9,0]) {
                    LX16ACubeHolder();
                }
            LX16ACircleHolder(false);
        }
        translate([0,0,-3])
            union() {
                LX16AAxis();
                translate([0,0,-4.8]) LX16AAxisScrewDriverTunnels();
            }
    }
}

module Arm04_Middle () {
    union() {
        rotate([0,180,-90])
            LX16ACubeHolder();
        translate([-2,0,50])
            rotate([90,0,0])
                LX16ACubeHolder();
        difference() {
            translate([-4.25,0,23]) cube([22.1,26.75,8],center=true); 
            translate([5.5,0,23]) cube([22.1,21,21],center=true); 
        }
        
        // side strength
        //color([1,0,0]) translate([-2.5,-14.5,12]) cube([10,2,30],center=true); 
        //color([1,0,0]) translate([-2.5,14.5,12]) cube([10,2,30],center=true); 
        color([1,0,0]) translate([-4.5,-13.5,5]) rotate([90,-90,0]) BoneStrength(radius=10, length=45, startRound=false);
         color([1,0,0]) translate([-4.5,13.5,5]) rotate([-90,-90,0]) BoneStrength(radius=10, length=45, startRound=false);
    }
}

module Arm05_Middle () {
    difference() {
        union() {
            rotate([0,90,0])
                translate([40,-12.5,0]) 
                    LX16ACircleHolderSteg();
            rotate([0,0,90])
                translate([0,-12,8]) 
                    LX16ACubeHolder();
            difference() {
                translate([14.5,0,-16]) cube([30,26.75,10],center=true); 
                translate([5.5,0,-14.5]) cube([24,20.5,21],center=true); 
            }
        }
        union() {
            translate([0,0,-3]) {
                //LX16AAxis();
            }
        }
    }
}

module Arm06_Bottom_QDS_15RO_Servo () {
    slip=0.1;
    margin=2;
    depth=20+slip;
    width=41+slip;
    height=15;
    axisDepth=8;
    
    difference() 
    {
        union() {
            translate([0,0,height/2 + margin/2]) cube([width+margin*2,depth+margin*2,margin], center=true); // top
            translate([width/2+margin/2,0,0]) cube([margin,depth+margin*2,height], center=true); // left
            translate([-width/2-margin/2,0,0]) cube([margin,depth+margin*2,height], center=true); // right
            
            translate([0,depth/2+margin/2,0]) cube([width,margin,height], center=true); // front
            translate([0,-depth/2-margin/2,0]) cube([width,margin,height], center=true); // back
            
            //cube([41+margin*2,20+margin*2,margin], center=true);
            translate([0,0,-axisDepth-2.5]) LX16ACircleHolder(false);
        }
        union() {
            translate([0,0,-axisDepth-5]) LX16AAxis();
            translate([0,0,-axisDepth-12]) LX16AAxisScrewDriverTunnels();
            translate([0,-0,-3]) cube([16,50,height], center=true); // fan canal
            
            // screw holes
            holeRadius= 2.5/2;
            holeDistance=15;
            height1= height/2 - 10.5;
            height2= height/2 - 2.5;
            translate([25,holeDistance/2,height1]) rotate([0,90,0]) cylinder(h=50, r=holeRadius, $fn=resolutionLow(), center=true); 
            translate([25,-holeDistance/2,height1]) rotate([0,90,0]) cylinder(h=50, r=holeRadius, $fn=resolutionLow(), center=true); 
            translate([-25,holeDistance/2,height2]) rotate([0,90,0]) cylinder(h=50, r=holeRadius, $fn=resolutionLow(), center=true); 
            translate([-25,-holeDistance/2,height2]) rotate([0,90,0]) cylinder(h=50, r=holeRadius, $fn=resolutionLow(), center=true); 
        }
    }
}

module Arm06_Bottom () {
    
    innerWidth = 45.5;
    innerHeight = 20;
    innerDepth1= 36;
    
    centerX = -3;
    
    margin=2;
    height=0;
   
    //color([1,0,0]) translate([-4.25,0,innerDepth1/2-10]) cube([innerWidth,innerHeight, innerDepth1], center=true);
   
    
    difference() {
        union() {
             rotate([270,0,0]) rotate([0,90,0]) {
                LX16ACubeHolder();
                //LX16AAxis(moveUpToServoPos=true);
            }
            // filler
            fillerWidth=8.5;
            translate([-18.5-fillerWidth/2,0,-4.5]) cube([fillerWidth,innerHeight+6, innerDepth1], center=true);
            translate([centerX,0,3.7]) LX16ACircleHolder(false);
            
            // axis holder
            translate([-28.5,0,-LX16AxisPlus()]) rotate([0,90,0]) cylinder(h=5, r=3, $fn=resolutionHi(), center=true); 
            
            // side clip
            translate([-27,0,-6]) rotate([0,90,0]) color([0,1,0]) cylinder(h=3, r=14.5/2, $fn=resolutionHi(), center=true); 
            translate([-27,0,-9.75]) rotate([0,90,0]) color([0,1,0]) cylinder(h=3, r=14.5/2, $fn=resolutionHi(), center=true); 
        }
        union() {
            translate([centerX,0,-4.5]) {
                LX16AAxis(moveUpToServoPos=false);
                LX16AAxisScrewDriverTunnels();
            }
            
            // screw hole
            screwHoleRadius = 1.7;
            screwHoleXPos = -12.5;
            translate([screwHoleXPos,0,-LX16AxisPlus()]) rotate([0,90,0]) cylinder(h=40, r=screwHoleRadius, $fn=resolutionLow(), center=true); 
            translate([screwHoleXPos,0,-LX16AxisPlus()]) rotate([0,90,0]) cylinder(h=20, r=screwHoleRadius*2, $fn=resolutionLow(), center=true); 
            // small screw holes
            holeRadius= 1.5/2;
            holeDistance=15;
            height1= 24.5;
            //height2= height/2 - 2.5;
            translate([-25,holeDistance/2,-LX16AxisPlus()-10+height1]) rotate([0,90,0]) cylinder(h=50, r=holeRadius, $fn=resolutionLow(), center=true); 
            translate([-25,-holeDistance/2,-LX16AxisPlus()-10+height1]) rotate([0,90,0]) cylinder(h=50, r=holeRadius, $fn=resolutionLow(), center=true); 
           
//            translate([-25,holeDistance/2,height2]) rotate([0,90,0]) cylinder(h=50, r=holeRadius, $fn=resolutionLow(), center=true); 
//            translate([-25,-holeDistance/2,height2]) rotate([0,90,0]) cylinder(h=50, r=holeRadius, $fn=resolutionLow(), center=true); 
            
        }
    }
    
    
    
     
    
    

}

//Arm01_Shoulder();
//Arm02_Top ();
//Arm03_Top();
//Arm04_Middle();
//Arm05_Middle();
Arm06_Bottom();

