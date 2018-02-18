/*
  Roobert - home robot project
  ________            ______             _____ 
  ___  __ \______________  /_______________  /_
  __  /_/ /  __ \  __ \_  __ \  _ \_  ___/  __/
  _  _, _// /_/ / /_/ /  /_/ /  __/  /   / /_  
  /_/ |_| \____/\____//_.___/\___//_/    \__/

 Project website: http://roobert.springwald.de

 ##################
 # BusLinker case #
 ##################

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



buslinkerWidth=41;
buslinkerHeigth=15;
buslinkerDepth=26;

module BusLinker() {
    union() {
        // pcb
        cube([buslinkerWidth,buslinkerDepth,buslinkerHeigth],center=true);
        // usb
        translate([buslinkerWidth/2,6.5,-1.5]) cube([22,13,12],center=true);
        // power cord
        translate([buslinkerWidth/2,-7,-1.5]) cube([22,9,12],center=true);
    }
}

module BusLinkerHolder() {
    margin = 3;
    holderDepth=10;
    difference() {
        union() {
            // case
            cube([buslinkerWidth+margin*2,buslinkerDepth+margin*2,buslinkerHeigth+margin],center=true); 
            // Makerbeam holder
            translate([0,margin+buslinkerDepth/2 + holderDepth/2,-buslinkerHeigth/2]) 
                difference() 
                {
                    translate([0,0,0]) cube([buslinkerWidth+margin*2,holderDepth,margin],center=true); 
                    translate([12,0,0]) MakerBeamHole();
                    translate([-12,0,0]) MakerBeamHole();
                }
        }
        union() {
            translate([0,0,margin]) BusLinker();
        }
    }
}

module MakerBeamHole() {
    height = 40;
    radius = 3.3;
    translate([0,0,0]) cylinder(h=height, r=radius/2, $fn=resolutionLow(), center=true); 
}

//BusLinker();
BusLinkerHolder();


