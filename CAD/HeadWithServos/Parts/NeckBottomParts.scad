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
use <..\Parts\KFL007Bearing35mm.scad>

bottomYPos = -115;
neckPipeXPos = 60;


module NeckBearring(drawHoles) {
    color([1,0.5,0.2]) translate([0,neckPipeXPos,bottomYPos-1-31.3]) KFL007Bearing35mm(drawHoles); // Bearring
}

module MakerBeamHoles() {
    width  = 160;
    depth = 130;
    depth2 = 150;
    width2  = 100;
    radius = 3.3;
    for(x = [-width/2 : width : width/2]) {
        for(y = [-depth/2 : depth / 4 : depth/2]) {
            translate([x,y,-20]) {
                cylinder(h=30, r=radius/2, $fn=resolutionLow(), center=true); // base body corner
            }
        }
    }
    if (true) {
        for(x = [-width2/2 : width2 / 2 : width2/2]) {
            for(y = [-depth2/2 : depth2 : depth2/2]) {
                translate([x,y,-20]) {
                    cylinder(h=30, r=radius/2, $fn=resolutionLow(), center=true); // base body corner
                }
            }
        }
    }
}


module NeckBase() {
    width  = 180;
    depth = 170;
    height = 5;
    
    zPos = -32;
    NeckBaseYPosMoveBackwards = 10;
    
    elipseHeight = 5;
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
          
            translate([0,0,-16]) scale([1,.7,1]) color([1,0.2,0.2]) cylinder(h=elipseHeight, r=(140)/2, $fn=resolutionHi(), center=true);// elipse body
        }
        union()
        {
            translate([0,0,-17]) NeckBearring(drawHoles=true);
            translate([0,neckPipeXPos+NeckBaseYPosMoveBackwards,bottomYPos+zPos]) MakerBeamHoles();
        }
    }
}

if (true) {
    //DrawInnerHead();
    //DrawMotorHolder(leftHolder=true, drawMotor=false);
    //DrawMotorHolder(leftHolder=false, drawMotor=false);
    NeckTop(drawPcbs=false);
    NeckPipe();
    //translate([0,0,-17]) NeckBearring(drawHoles=true);
}

NeckBase();

if (false) {
    difference() {
       NeckBase();
       translate([0,0,-300]) cube([500,500,300], center=true);
       translate([00,-235,0]) cube([500,500,400], center=true);
    }
}





