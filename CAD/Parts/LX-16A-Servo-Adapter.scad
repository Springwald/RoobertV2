/*


 ########################
 # LX-16A Servo Adapter #
 ########################

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

include <LX-16A-Servo.scad>

module MakerBeamHole() {
    height = 40;
    radius = 3.3;
    radiusScrew= 6;
    translate([0,0,height/2]) cylinder(h=height, r=radius/2, $fn=resolutionLow(), center=true); 
    translate([0,0,-height/2])cylinder(h=height, r=radiusScrew/2, $fn=resolutionLow(), center=true); 
}


module DoubleHolderOuterPart(frame=true) {
    margin = 3;
    width = 22;
    width2 = 25;
    widthStabilizer = 2.5;
    marginStabilizer = 2;
    innerWidth3 = (frame==true) ? width2 : width2-4;
    

    translate([0, LX16AHeight / 2 - 10, 0]) 
        difference() 
        {
            union() {
                LX16ACircleHolder(inclusiveBottom=false);
                // connection circle holder
                translate([-width/2, 0, LX16AAxisDepth/2 + 3 + margin/2]) cube([width,width2-4,margin], center=true);
                // connection middle
                translate([-width + margin/ 2, 0, LX16AStegLengthModification/ 2]) cube([margin,innerWidth3,LX16AAxisDepth+ 9.5 - LX16AStegLengthModification], center=true);
            
                color([0,1,0]) 
                    translate([-5.75,0, LX16AAxisDepth/2  + 6.5 - LX16AStegLengthModification])
                        rotate([0,0,180])
                            BoneStrength(radius=11, length=32.5, startRound=false, scaler=1);

                
                // connection middle stabilizer
                if (frame) {
                     translate([-width + marginStabilizer/ 2 + margin,width2/2 - widthStabilizer/2, LX16AStegLengthModification/ 2]) cube([marginStabilizer,widthStabilizer,LX16AAxisDepth+ 9.5 - LX16AStegLengthModification], center=true);
                    translate([-width + marginStabilizer/ 2 + margin, -width2/2 +widthStabilizer/2, LX16AStegLengthModification/ 2]) cube([marginStabilizer,widthStabilizer,LX16AAxisDepth+ 9.5 - LX16AStegLengthModification], center=true);
                }
               
            }
            color([1,0,1]) LX16AAxis();
            translate([0,0,14])LX16AAxisScrewDriverTunnels();

           
        }
}

module DoubleHolderOuter(hole=true, frame=true) {
    translate([0,0,-1]) {
        difference() {
            union() {
                DoubleHolderOuterPart(frame);
                translate([0,0,-36]) mirror([0,0,1]) DoubleHolderOuterPart(frame);
            }
            // Cable hole
            if (hole==true) { 
                translate([-20,12.5,-20]) rotate([0,90,0]) cylinder(h=20, r=5.9, $fn=resolutionHi(), center=true); 
            }
           
        }
    }
}

module DoubleHolderInner(hole=true) {
    holderMargin = 5;
    difference() {
        union() {
            LX16ACubeHolder();
            translate([0,0,-38]) rotate([0,180,0]) LX16ACubeHolder();
        }
        // Cable hole
        if (hole==true) translate([-10,-0.5,-20]) rotate([0,90,0]) cylinder(h=20, r=5.9, $fn=resolutionHi(), center=true); 
    }
}


 DoubleHolderOuter(frame=true, hole=true);
//DoubleHolderInner();

