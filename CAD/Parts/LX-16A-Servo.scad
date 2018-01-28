/*

 ##########################
 # LX-16A Servo and Mount #
 ##########################

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


$exportQuality = true;

function resolutionLow() = ($exportQuality==true) ? 30 : 10;
function resolutionHi() = ($exportQuality==true) ? 300 : 20;

LX16AHeight = 45.2;
LX16AWidth = 24.7;
LX16ADepth = 31;

LX16AOuterBodyDepth = LX16ADepth+2;
LX16AOuterBodyHeight = 30;

LX16AAxisDepth = 35.5;
LX16AAxisRadius = 6.3/2;

LX16AHoleDistanceX = 20.3;

LX16AidHolderDepth = 1.8;
LX16AlogoHolderDepth = 1;

LX16AmovementRadius = 12;

LX16AstretchHolderHeights = 20;

LX16AStegLengthModification = 0.7;

module LX16A() 
{
    // inner body
    color([0,1,0]) cube([LX16AWidth, LX16AHeight, LX16ADepth], center=true);
    
    // outer body
    difference()
    { 
        union() {
            translate([0, - LX16AHeight / 2 + LX16AOuterBodyHeight / 2, 0]) {
                cube([LX16AWidth, LX16AOuterBodyHeight, LX16AOuterBodyDepth], center=true);
            }
            // logo holder
            logoHolderHeight = 26+LX16AstretchHolderHeights;
            color([0,0,1]) translate([0, -LX16AHeight / 2 + logoHolderHeight / 2 , LX16AOuterBodyDepth/2 + LX16AlogoHolderDepth / 2]) cube([19.5, logoHolderHeight, LX16AlogoHolderDepth], center=true);
        }
        if (false) {
            translate([0, LX16AHeight / 2 - 10, 0]) {
                cylinder(h=LX16AHeight, r=movementRadius, $fn=resolutionHi(), center=true); 
                LX16AAxis();
            }
        }
    }
   
    // Id holder
    idHolderHeight = 18.8 + LX16AstretchHolderHeights;
    color([0,0,1]) translate([0, -LX16AHeight / 2 + idHolderHeight / 2 , -LX16AOuterBodyDepth/2 - LX16AidHolderDepth / 2]) cube([19.5, idHolderHeight, LX16AidHolderDepth], center=true);
    
    // cable hole
    cableHolerounded = false;
    if (cableHolerounded) {
        cableHoleHeight=5;
        cableHoleDepth=10;
        color([0,1,1]) translate([0,-LX16AHeight/2 + 21, -20]) cube([21, cableHoleHeight, cableHoleDepth], center=true);
        translate([0,-LX16AHeight/2 + 23, -20])
            difference() 
            {
                color([0,1,1]) cylinder(h=cableHoleDepth, r=21/2, $fn=resolutionLow(), center=true); 
                translate([0,-20,0]) cube([20, 40, cableHoleDepth], center=true);
            }
    } else {
        cableHoleHeight=20;
        cableHoleDepth=10;
        color([0,1,1]) translate([0,-LX16AHeight/2 + 27, -20]) cube([21, cableHoleHeight, cableHoleDepth], center=true);
    }
    
    // top screw holes
    screwHoleRadius = 0.8;
    translate([+LX16AHoleDistanceX/2,4.5,20]) cylinder(h=20, r=screwHoleRadius, $fn=resolutionLow(), center=true); 
    translate([-LX16AHoleDistanceX/2,4.5,20]) cylinder(h=20, r=screwHoleRadius, $fn=resolutionLow(), center=true);
    
    // bottom screw holes logo side
    screwHoleRadius = 0.8;
    translate([+LX16AHoleDistanceX/2,-16.3,10]) cylinder(h=20, r=screwHoleRadius, $fn=resolutionLow(), center=true); 
    translate([-LX16AHoleDistanceX/2,-16.3,10]) cylinder(h=20, r=screwHoleRadius, $fn=resolutionLow(), center=true);
    
    // bottom screw holes id side
    translate([+LX16AHoleDistanceX/2,-20.5,-10]) cylinder(h=20, r=screwHoleRadius, $fn=resolutionLow(), center=true); 
    translate([-LX16AHoleDistanceX/2,-20.5,-10]) cylinder(h=20, r=screwHoleRadius, $fn=resolutionLow(), center=true);
    
    translate([0, LX16AHeight / 2 - 10, 0]) {
        LX16AAxis();
    }
    
    translate([0, LX16AHeight / 2 - 10, 0]) {
        cylinder(h=LX16ADepth+10, r=12, $fn=resolutionLow(), center=true); 
        LX16AAxis();
    }
}

module LX16AScrewDriverTunnels() 
{
    margin = 1;
    height = 30;
    
    depthFront = LX16AOuterBodyDepth + LX16AidHolderDepth + LX16AlogoHolderDepth + margin ;
    
    // top screw holes
    screwDriverHoleRadius = 4;
    translate([+LX16AHoleDistanceX/2,4.5, depthFront/2  + height/2]) cylinder(h=height, r=screwDriverHoleRadius, $fn=resolutionLow(), center=true); 
    translate([-LX16AHoleDistanceX/2,4.5, depthFront/2  + height/2]) cylinder(h=height, r=screwDriverHoleRadius, $fn=resolutionLow(), center=true);
    
    // bottom screw holes logo side
    screwHoleRadius = 0.8;
    translate([+LX16AHoleDistanceX/2,-16.3,depthFront/2  + height/2]) cylinder(h=height, r=screwDriverHoleRadius, $fn=resolutionLow(), center=true); 
    translate([-LX16AHoleDistanceX/2,-16.3,depthFront/2  + height/2]) cylinder(h=height, r=screwDriverHoleRadius, $fn=resolutionLow(), center=true);
    
    // bottom screw holes id side
    translate([+LX16AHoleDistanceX/2,-20.5,-depthFront/2 - height/2 -margin]) cylinder(h=height, r=screwDriverHoleRadius, $fn=resolutionLow(), center=true); 
    translate([-LX16AHoleDistanceX/2,-20.5,-depthFront/2 - height/2 -margin]) cylinder(h=height, r=screwDriverHoleRadius, $fn=resolutionLow(), center=true);
}

module LX16AAxis() {
    
    // Axis
    cylinder(h=LX16AAxisDepth, r=LX16AAxisRadius, $fn=resolutionHi(), center=true); 
    
    // Servo Disc holder
    discHolderHeight=4;
    translate([0, 0, LX16AAxisDepth/2 - discHolderHeight/2]) cylinder(h=discHolderHeight, r=5, $fn=resolutionLow(), center=true); 
    
    // Servo Disk 
    discHeight = 2;
    discRadius = 10;
    translate([0, 0, LX16AAxisDepth/2 + discHeight/2]) cylinder(h=discHeight, r=discRadius, $fn=resolutionLow(), center=true); 
    
    mountingHoleSpacing = 14.0/2;
    holeHeight=10;
    holeRadius = 1.9;
    translate([+mountingHoleSpacing,0, LX16AAxisDepth/2+holeHeight/2]) cylinder(h=holeHeight, r=holeRadius, $fn=resolutionLow(), center=true); 
    translate([-mountingHoleSpacing,0, LX16AAxisDepth/2+holeHeight/2]) cylinder(h=holeHeight, r=holeRadius, $fn=resolutionLow(), center=true); 
    translate([0,+mountingHoleSpacing, LX16AAxisDepth/2+holeHeight/2]) cylinder(h=holeHeight, r=holeRadius, $fn=resolutionLow(), center=true); 
    translate([0,-mountingHoleSpacing, LX16AAxisDepth/2+holeHeight/2]) cylinder(h=holeHeight, r=holeRadius, $fn=resolutionLow(), center=true); 
    
    // Screw hole middle
    translate([0, 0, LX16AAxisDepth/2]) cylinder(h=20, r=3, $fn=resolutionLow(), center=true); 
}

module LX16ACubeHolder() {
    //rotate([90,0,0])
        difference() {
            union() {
                margin = 1;
                height = LX16AHeight * 0.65;
                translate([0,-LX16AHeight/2 + height/2 - margin/2, -LX16AidHolderDepth /2 + LX16AlogoHolderDepth/ 2]) 
                    cube([LX16AWidth + margin * 2, height + margin, LX16AOuterBodyDepth + LX16AidHolderDepth + LX16AlogoHolderDepth + margin * 2], center=true);
            }
            LX16A();
        }
        //LX16A();
}

module LX16ACircleHolder(inclusiveBottom) {
    marginBig = 4;
    marginSmall = 3;
    widthBig = 21;
    widthSmall = 12;
    discHolderHeight=10;
    difference() {
        union() {
            // Big 4 screw holder
            translate([0, 0, LX16AAxisDepth/2 + 2 + marginBig / 2]) cylinder(h=marginBig, r=widthBig/2, $fn=resolutionHi(), center=true); 
            
            // small 1 screw holder
            if(inclusiveBottom) {
                depthPlus = 4.5;
                translate([0, 0, - LX16AAxisDepth/2 + marginSmall / 2 - depthPlus/6 -1.75 + LX16AStegLengthModification ]) cylinder(h=marginSmall+depthPlus, r=widthSmall/2, $fn=resolutionHi(), center=true); 
            }
        }
        union () {
            LX16AAxis();
            
        }
    }   
}

module LX16ASkeletonHolder() {
    //rotate([90,0,0])
        difference() {
            union() {
                margin = 1;
                height = LX16AHeight * 0.65;
                translate([0,-LX16AHeight/2 + height/2 - margin/2, -LX16AidHolderDepth /2 + LX16AlogoHolderDepth/ 2]) 
                    cube([LX16AWidth + margin * 2, height + margin, LX16AOuterBodyDepth + LX16AidHolderDepth + LX16AlogoHolderDepth + margin * 2], center=true);
            }
            LX16A();
        }
        LX16A();
}

module LX16ACircleHolderSteg() {
    margin = 3;
    width = 22;
    width2 = 21;
    translate([0, LX16AHeight / 2 - 10, 0]) 
        color([0,0,1])
            difference() 
            {
                union() {
                    LX16ACircleHolder(inclusiveBottom= true);
                    // connection circle holder
                    translate([-width/2, 0, LX16AAxisDepth/2 + 3 + margin/2]) cube([width,width2,margin], center=true);
                    // connection middle
                    translate([-width + margin/ 2, 0, LX16AStegLengthModification/ 2]) cube([margin,width2,LX16AAxisDepth+ 9.5 - LX16AStegLengthModification], center=true);
                    // connection small axis
                    translate([-width/2, 0, -LX16AAxisDepth/2  - 3.25 + LX16AStegLengthModification]) cube([width,12,margin], center=true);
                }
                color([1,0,1]) LX16AAxis();
            }
}

//LX16ASkeletonHolder();

//LX16ACubeHolder();
//LX16AAxis();
//LX16A();


rotate([0,-90,0])
LX16ACircleHolderSteg();

//LX16AScrewDriverTunnels();

//translate([0, LX16AHeight / 2 - 10, 0]) {
//    color([0,0,1])
//        difference() 
//        {
//            LX16ACircleHolder(inclusiveBottom= true);
//            color([1,0,01]) LX16AAxis();
//        }
//}

