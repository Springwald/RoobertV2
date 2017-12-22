

module Stepper5VGear (margin) 
{
    faktor = margin == true ? 1.02 : 1;
    
    // stepper motor body
    bodyHeight = 19.2 * faktor;
    bodyRadius = 14 * faktor;
    translate([0,0,-bodyHeight]) cylinder(h=bodyHeight, r=bodyRadius,  $fn=100, center=false);   
    
    // static tower
    staticTowerRadius = 4.55* faktor;
    staticTowerMargin= 1.7* faktor;
    translate([-bodyRadius+staticTowerRadius+staticTowerMargin,0,0]) cylinder(h=1.6* faktor, r=staticTowerRadius, $fn=50, center=true); 
    
    // axis
    axisRadius = 2.5* faktor;
    translate([-bodyRadius+staticTowerRadius+staticTowerMargin,0,0]) cylinder(h=7, r=axisRadius, $fn=50, center=true); 
    intersection() 
    {
        cubeHeight = 6.2* faktor;
        translate([-bodyRadius+staticTowerRadius+staticTowerMargin,0,0]) cylinder(h=30* faktor, r=axisRadius, $fn=50, center=true); 
        translate([-bodyRadius+staticTowerRadius+staticTowerMargin,0,3.5 + cubeHeight/2]) cube([2.95* faktor,5* faktor,6.2* faktor],center=true);
    }
    
    // holder
    translate([0,35/2,-bodyHeight]) cylinder(h=22* faktor, r=2.05* faktor,  $fn=50, center=false);   
    translate([0,-35/2,-bodyHeight]) cylinder(h=22* faktor, r=2.05* faktor,  $fn=50, center=false);   
    
    // cable holder
    translate([bodyRadius,0,-bodyHeight/2]) cube([6.24* faktor,17.5* faktor,bodyHeight],center=true);
    
    // Print-Dummy-Base
    //baseHeight = 3;
    //translate([0,0,-bodyHeight+baseHeight/2])  cube([10,42,baseHeight],center=true);
}



color([1,0,1]) Stepper5VGear(false);
Stepper5VGear(true);