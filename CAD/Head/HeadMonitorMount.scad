/*
  Roobert - home robot project
  ________            ______             _____ 
  ___  __ \______________  /_______________  /_
  __  /_/ /  __ \  __ \_  __ \  _ \_  ___/  __/
  _  _, _// /_/ / /_/ /  /_/ /  __/  /   / /_  
  /_/ |_| \____/\____//_.___/\___//_/    \__/

 Project website: http://roobert.springwald.de

 ######################
 # head monitor mount #
 ######################

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

resolution      = debug ? 50 : 100;
resolutionLow   = debug ? 10 : 20;

InnerFaceWidth=180;
InnerFaceHeight=150;
MonitorLCDDepth=7;
    
module MonitorLCD() {
    width=166;
    height=105;
    depth= MonitorLCDDepth;
    translate([-width/2,-depth,-height/2]) cube([width,depth*20,height],center=false);
}

module MonitorPCB() {
    width=167;
    height=125;
    depth= 50;
    translate([-width/2,MonitorLCDDepth,-height/2]) cube([width,depth*2,height],center=false);
}

module MonitorScrewHoles() 
{
    depth=50;
    radius=1.7;
    distX = 157;
    distY = 115;
    translate([-distX/2,0,distY/2]) rotate([90,0,0]) cylinder(depth,r=radius,$fn=resolutionLow,center=true); // 1
    translate([distX/2,0,distY/2]) rotate([90,0,0]) cylinder(depth,r=radius,$fn=resolutionLow,center=true); // 2
    translate([-distX/2,0,-distY/2]) rotate([90,0,0]) cylinder(depth,r=radius,$fn=resolutionLow,center=true); // 3
    translate([distX/2,0,-distY/2]) rotate([90,0,0]) cylinder(depth,r=radius,$fn=resolutionLow,center=true); // 4
}

module HDMIPort() {
    width=30;
    height=17;
    depth=8;
    margin=3;
    posY = 115/2-30;
    translate([InnerFaceWidth/2-width/2,MonitorLCDDepth-margin,posY]) rotate([0,0,0]) cube([width,depth*2,height],center=false);
}

module USBPort() {
    width=30;
    height=12;
    depth=8;
    margin=3;
    posY = 115/2-46;
    translate([InnerFaceWidth/2-width/2,MonitorLCDDepth-margin,posY]) rotate([0,0,0]) cube([width,depth*2,height],center=false);
}

module InnerFace() {
    width=180;
    height=150;
    translate([-width/2,0,-height/2])  cube([width,10,height],center=false);
}

difference() {
    InnerFace();
    union() {
        MonitorLCD();
        MonitorPCB();
        MonitorScrewHoles();
        HDMIPort();
        USBPort();
    }
}



