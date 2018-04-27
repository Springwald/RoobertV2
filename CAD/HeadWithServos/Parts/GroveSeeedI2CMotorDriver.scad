function resolutionLow() = ($exportQuality==true) ? 20 : 10;
function resolutionHi() = ($exportQuality==true) ? 300 : 50;

module GroveSeedI2CMotorDriver() {
    width = 64.2;
    height = 44;
    
    holeDistanceX1 = 60;
    holeDistanceX2 = 40;
    
    holeDistanceY1 = 40;
    holeDistanceY2 = 20;
    
    holeDiameter = 2.3;
    holeHeight = 20;
    
    // Body
    translate([0,0,0]) cube([width,height,3],center=true);
    
    translate([0,0,-holeHeight/2]) { 
        // holes
        for (x = [-holeDistanceX2/2:holeDistanceX2/2:holeDistanceX2/2]) {
            translate([x,+holeDistanceY1/2,0]) cylinder(h=holeHeight, r=holeDiameter/2, $fn=resolutionLow(), center=true); 
            translate([x,-holeDistanceY1/2,0]) cylinder(h=holeHeight, r=holeDiameter/2, $fn=resolutionLow(), center=true); 
        }
        for (y = [-holeDistanceY2/2:holeDistanceY2:holeDistanceY2/2]) {
            translate([+holeDistanceX1/2,y,0]) cylinder(h=holeHeight, r=holeDiameter/2, $fn=resolutionLow(), center=true); 
            translate([-holeDistanceX1/2,y,0]) cylinder(h=holeHeight, r=holeDiameter/2, $fn=resolutionLow(), center=true); 
        }
    }
    
}

GroveSeedI2CMotorDriver();