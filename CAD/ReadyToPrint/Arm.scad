/*
  Roobert - home robot project
  ________            ______             _____ 
  ___  __ \______________  /_______________  /_
  __  /_/ /  __ \  __ \_  __ \  _ \_  ___/  __/
  _  _, _// /_/ / /_/ /  /_/ /  __/  /   / /_  
  /_/ |_| \____/\____//_.___/\___//_/    \__/

 Project website: http://roobert.springwald.de

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

use <..\Parts\ArmParts.scad>

withSupport = true;
all=true;
rightArm = false;

function mirr() = (rightArm==true) ? 0 : 1;

// Arm01_Shoulder
if (withSupport == false || all) 
    color([1,1,1]) // White
       translate([10,40,23.6]) 
            mirror([0,mirr(),0])
                rotate([-90,0,0]) Arm01_Shoulder();

// Arm02_Top
if (withSupport == true || all) 
    color([1,0,0]) // red
        translate([0,0,23.75]) rotate([0,180,90]) Arm02_Top();

// Arm03_Top
if (withSupport == true || all) 
    color([0,1,0]) // green
        translate([30,0,23.75]) rotate([0,180,0]) Arm03_Top();

// Arm04_Middle
if (withSupport == true || all) 
    color([0.5,0.5,1]) // blue
        translate([-40,-20,18.5]) 
            mirror([0,mirr(),0])
                rotate([0,0,180]) Arm04_Middle();

// Arm05_Middle
if (withSupport == true || all) 
    color([1,1,0]) // yellow
        translate([-43,20,35.6]) 
            rotate([0,90,0]) Arm05_Middle();

// Arm06_Bottom
if (withSupport == true || all)
    color([0.5,0,0.5]) // purple
        translate([15,-40,11.75]) 
            rotate([0,180,0])
                Arm06_Bottom();



