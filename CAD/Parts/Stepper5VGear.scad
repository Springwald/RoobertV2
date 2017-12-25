

function resolutionLow() = ($exportQuality==true) ? 50 : 10;
function resolutionHi() = ($exportQuality==true) ? 200 : 50;

module Stepper5VGear (margin, axisrotation) 
{
    faktor = margin == true ? 1.02 : 1;
    
    // stepper motor body
    bodyHeight = 19.2 * faktor;
    bodyRadius = 14 * faktor;
    translate([0,0,-bodyHeight]) cylinder(h=bodyHeight, r=bodyRadius,  $fn=resolutionHi(), center=false);   
    
    // static tower
    staticTowerRadius = 4.55* faktor;
    staticTowerMargin= 1.7* faktor;
    translate([-bodyRadius+staticTowerRadius+staticTowerMargin,0,0]) cylinder(h=1.6* faktor, r=staticTowerRadius, $fn=resolutionLow(), center=true); 
    
    // axis
    
        axisRadius = 2.5* faktor;
        translate([-bodyRadius+staticTowerRadius+staticTowerMargin,0,0]) cylinder(h=7, r=axisRadius, $fn=resolutionLow(), center=true); 
        
        intersection() 
        {
            cubeHeight = 6.2* faktor;
            translate([-bodyRadius+staticTowerRadius+staticTowerMargin,0,0]) cylinder(h=30* faktor, r=axisRadius, $fn=resolutionLow(), center=true); 
            translate([-bodyRadius+staticTowerRadius+staticTowerMargin,0,3.5 + cubeHeight/2]) rotate([0,0,axisrotation]) cube([2.95* faktor,5* faktor,6.2* faktor],center=true);
        }

    
    // holder
    translate([0,35/2,-bodyHeight-2]) cylinder(h=22* faktor, r=2.05* faktor,  $fn=resolutionLow(), center=false);   
    translate([0,-35/2,-bodyHeight-2]) cylinder(h=22* faktor, r=2.05* faktor,  $fn=resolutionLow(), center=false);   
    
    // cable holder
    translate([bodyRadius,0,-bodyHeight/2]) cube([8* faktor,17.5* faktor,bodyHeight],center=true);
    
    // Print-Dummy-Base
    //baseHeight = 3;
    //translate([0,0,-bodyHeight+baseHeight/2])  cube([10,42,baseHeight],center=true);
}


module Stepper5VGearPCB() 
{
    radius = 2.7 /2;
    depth = 10;
    distanceX= 27;
    distanceZ=29.5;
    width=32;
    height=35;
    
    translate([distanceX / 2,  distanceZ / 2,-depth]) cylinder(h=depth * 2, r=radius, $fn=resolutionLow(), center=true); 
    translate([-distanceX / 2, distanceZ / 2,-depth]) cylinder(h=depth * 2, r=radius, $fn=resolutionLow(), center=true); 
    translate([-distanceX / 2,-distanceZ / 2,-depth]) cylinder(h=depth * 2, r=radius, $fn=resolutionLow(), center=true); 
    translate([distanceX / 2, -distanceZ / 2,-depth]) cylinder(h=depth * 2, r=radius, $fn=resolutionLow(), center=true); 
    
    cube([width,height,3],center=true);
}



//color([1,0,1]) Stepper5VGear(false);
//Stepper5VGear(true,90);

Stepper5VGearPCB();
