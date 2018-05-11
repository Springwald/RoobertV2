function resolutionLow() = ($exportQuality==true) ? 20 : 10;
function resolutionHi() = ($exportQuality==true) ? 300 : 50;

module KFL007Bearing35mm (drawHoles) {
    margin = 2;
    
    holeDistance = 95;
    holeDiameter = 13;
    holeScrewDiameter = 6;
    
    axisHeight = 31.3;
    axisOuterDiameter = 35+2*4;
    axisInnerDiameter = 35;
    
    bodyDiameter= 80+margin;
    bodyHeight = 10;
    bodyWidth = 122;
    bodyBarWidth1 = 22+margin;
    bodyBarWidth2 = 45+margin;
    bodyBarDepth = 20+margin;
    
    // Body
    difference() {
        union() {
             // Axis
            translate([0,0,axisHeight/2]) cylinder(h=axisHeight, r=axisOuterDiameter/2, $fn=resolutionHi(), center=true);
            
            // Body cylinder
            translate([0,0,bodyHeight/2]) cylinder(h=bodyHeight, r=bodyDiameter/2, $fn=resolutionHi(), center=true); 
            
            // Body bar
            intersection() {
                union() {
                    translate([-bodyDiameter/2- bodyBarDepth/2,0,bodyHeight/2]) rotate([0,0,90]) rotate([90,45,0]) cylinder(bodyBarDepth,bodyBarWidth1* 0.7,bodyBarWidth2* 0.7,$fn=4, center=true);   
                   translate([bodyDiameter/2+bodyBarDepth/2,0,bodyHeight/2]) rotate([0,0,-90]) rotate([90,45,0]) cylinder(bodyBarDepth,bodyBarWidth1*0.7,bodyBarWidth2*0.7,$fn=4, center=true);   
                    translate([0,0,bodyHeight/2]) cube([bodyDiameter,bodyBarWidth2,bodyHeight], center=true);
                }
                translate([0,0,bodyHeight/2]) cube([500,bodyBarWidth2,bodyHeight], center=true);
            }
            
            /* intersection() {
                translate([0,0,bodyHeight/2]) cube([bodyWidth,bodyBarWidth,bodyHeight], center=true);
                translate([holeDistance/2,0,bodyHeight/2]) cylinder(h=20, r=15, $fn=resolutionHi(), center=true); 
            }
            intersection() {
                translate([0,0,bodyHeight/2]) cube([bodyWidth,bodyBarWidth,bodyHeight], center=true);
                translate([-holeDistance/2,0,bodyHeight/2]) cylinder(h=20, r=15, $fn=resolutionHi(), center=true); 
            }
            //translate([-10,0,bodyHeight/2]) cube([bodyWidth-20,bodyBarWidth,bodyHeight], center=true);*/
        }
        union() {
            // Holes
            translate([+holeDistance/2,0,0]) cylinder(h=80, r=holeDiameter/2, $fn=resolutionHi(), center=true); 
            translate([-holeDistance/2,0,0]) cylinder(h=80, r=holeDiameter/2, $fn=resolutionHi(), center=true); 
            translate([0,0,10]) cylinder(h=60, r=axisInnerDiameter/2, $fn=resolutionHi(), center=true);  // inner axis hole
            translate([0,0,-14]) cylinder(h=40, r=10+axisInnerDiameter/2, $fn=resolutionHi(), center=true);  // inner axis  bottom hole
        }
    }
    
    if (drawHoles) {
         translate([+holeDistance/2,0,0]) cylinder(h=80, r=holeScrewDiameter/2, $fn=resolutionHi(), center=true); 
         translate([-holeDistance/2,0,0]) cylinder(h=80, r=holeScrewDiameter/2, $fn=resolutionHi(), center=true); 
         translate([0,0,10]) cylinder(h=60, r=axisInnerDiameter/2, $fn=resolutionHi(), center=true);  // inner axis hole
         translate([0,0,-14]) cylinder(h=40, r=10+axisInnerDiameter/2, $fn=resolutionHi(), center=true);  // inner axis  bottom hole
    }
}

KFL007Bearing35mm(false);
