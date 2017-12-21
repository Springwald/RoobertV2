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

debug = false;

resolution      = debug ? 50 : 200;
resolutionLow   = debug ? 10 : 20;

InnerFaceWidth=180;
InnerFaceHeight=150;
MonitorLCDDepth=7;

cameraPos = [0,12,67];

module Camera() 
{
    depth = 30;
    depthPCB=10;
    translate([0,-2,0]) cube([26,depthPCB,25],center=true); // pcb
    translate([0,0,-2.5]) cube([9.2,depth,9.2],center=true); // camera
    translate([-7.5,0,7]) rotate([90,0,0]) cylinder(depth,r=1,$fn=resolutionLow,center=true); // Led
    translate([-7.5,depthPCB-7,7]) rotate([90,0,0]) cylinder(6,r=3,$fn=resolutionLow,center=true); // Led hole
    translate([0,0,7]) cube([8,4 +(depthPCB-5),11],center=true); // clip hole
}

module CameraBox() 
{
    depth = 5;
    translate([0,depth,0]) color([0,0,1]) cube([29,depth,29],center=true); // camera box   
}

    
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
    additionalTopHeight = 7;
    width=180;
    height=150 + additionalTopHeight;
    margin= 14;
    difference() 
    {
        translate([-width/2,0,-height/2+additionalTopHeight/2]) cube([width,15,height],center=false);
        translate([0,15,height/2-margin]) cube([width-margin*3,15,20],center=true);
    }
}

module HeadSphere(radius) 
{
    intersection() 
    {
        rotate([10,0,0]) scale ([0.9,1.1,0.72]) sphere(radius, $fn=resolution, center=true);
        translate ([0,0,190]) rotate([10,0,0]) scale([3,2.5,2])  sphere(radius, $fn=resolution, center=true);
    }
}

intersection() {
    difference() {
        union() {
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
        translate(cameraPos) rotate([0,0,180]) CameraBox();
        }
        translate(cameraPos) rotate([0,0,180]) Camera();
    }
    HeadSphere(130);
}









