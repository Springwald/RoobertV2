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
    difference() {
        union() {
            rotate([90,90,-90])
                LX16ACubeHolder();
            color([1,0,0]) 
                translate([10,8.4,14]) 
                    cube([18.6,30.4,2],center=true);
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
    difference() {
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
                translate([0,0,5]) LX16AAxisScrewDriverTunnels();
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
                translate([14.5,0,-16]) cube([18.5,26.75,10],center=true); 
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

module Arm06_Bottom () {
    slip=0.1;
    margin=2;
    depth=20+slip;
    width=41+slip;
    height=15;
    
    difference() {
        union() {
            translate([0,0,height/2 + margin/2]) cube([width+margin*2,depth+margin*2,margin], center=true); // top
            translate([width/2+margin/2,0,0]) cube([margin,depth+margin*2,height], center=true); // left
            translate([-width/2-margin/2,0,0]) cube([margin,depth+margin*2,height], center=true); // right
            
            translate([0,depth/2+margin/2,0]) cube([width,margin,height], center=true); // front
            translate([0,-depth/2-margin/2,0]) cube([width,margin,height], center=true); // back
            
            //cube([41+margin*2,20+margin*2,margin], center=true);
            translate([0,0,-12]) LX16ACircleHolder(false);
        }
        union() {
            translate([0,0,-15]) LX16AAxis();
            translate([0,0,-9.5]) LX16AAxisScrewDriverTunnels();
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

//Arm01_Shoulder();
//Arm03_Top();
// Arm05_Middle();
Arm06_Bottom();

