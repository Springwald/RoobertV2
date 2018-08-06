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


$exportQuality = true;

function resolutionLow() = ($exportQuality==true) ? 30 : 10;
function resolutionHi() = ($exportQuality==true) ? 200 : 20;

module NeoPixelDiffuser(countX=8, countZ=8, plateheight= 0.5)  // plateheight= bold: 0.5, thin: 0.3
{
    height = 5;
    singleWidth=8.2;
    width = singleWidth*countX;
    depth = singleWidth*countZ;
    stegWidth = 2.1;
    margin = 1;
    borderWidth=stegWidth/2;
    
    // plate 
    cube([width,depth,plateheight],center=true);
    
    // inner bars
    for (x = [1:1:countX-1]) 
    {
        translate([0,-width/2+x*singleWidth,height/2-margin/2]) cube([width,stegWidth,height-margin],center=true);        
    }
    for (z = [1:1:countZ-1]) 
    {
        translate([-depth/2+z*singleWidth,0,height/2-margin/2]) cube([stegWidth,depth,height-margin],center=true);        
    }
    
    // outer borders
    for (a = [-1:2:1]) {
        translate([0,(-width/2+borderWidth/2)*a,height/2]) cube([width,borderWidth,height],center=true);     
        translate([(-width/2+borderWidth/2)*a,0,height/2]) cube([borderWidth,width,height],center=true);     
    }
}

NeoPixelDiffuser(countX=16, countZ=16, plateheight=0.3);
