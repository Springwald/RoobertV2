/*

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


use <.\bend.scad>

$exportQuality = true;

function resolutionLow() = ($exportQuality==true) ? 30 : 10;
function resolutionHi() = ($exportQuality==true) ? 300 : 20;

faceHeight=220;
faceWidth=150;

module HalfHead(cutHalf=false) {
    
    difference() {
        scale([1.1,1,1]) {
            translate([-44.5,160,-152])
            rotate([-9,-.6,0]) {
                import("raw/head1.stl", convexity=3);
            }
        }
        union() {
            translate([0,200,0]) cube([400,400,400], center=true);
            rotate([90,0,0]) 
            { 
                scale([1 * faceWidth /faceHeight ,1,1]) {
                    difference() {
                        cube([1000,1000,100],center=true);
                        cylinder(h = 1000, r1 = faceHeight/2, r2 = faceHeight/2, $fn=resolutionHi(), center = true);
                    }
                }
            }
        }
    }
}

module FrontHead() 
{  
    HalfHead(cutHalf=false);
    mirror([1,0,0]) HalfHead(cutHalf=false);
    
    content = "GAITO";
    font = "Liberation Sans";
    translate ([-74,-15,-30])
    parabolic_bend([20, 150, 2], 0.007) {
            rotate([0,-90,0])
            {
            linear_extrude(height = 10) {
            text(content, font = font, size = 14);
            }
        }
    }
    
    rotate([90,0,0]) 
    { 
        scale([1 * faceWidth /faceHeight ,1,1]) {
            cylinder(h = 10, r1 = faceHeight/2, r2 = faceHeight/2, $fn=resolutionHi(), center = true);
        }
    }
}




//use <..\Parts\ArmPartsStronger.scad>

withSupport = true;
all=true;
rightArm = false;

FrontHead();
