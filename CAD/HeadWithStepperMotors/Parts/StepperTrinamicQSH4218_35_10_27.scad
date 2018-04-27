function resolutionLow() = ($exportQuality==true) ? 20 : 10;
function resolutionHi() = ($exportQuality==true) ? 300 : 50;

module StepperTrinamicQSH4218_35_10_27() {
    margin=1;
    
    size=42.3+margin;
    height=34;
    axisHeight=58;
    axisDiameter=5;
    
    holeDistance = 31;
    holeHeight=50;
    holeDiameter=2.5+margin;

    // Axis
    translate([0,0,axisHeight/2]) cylinder(h=axisHeight, r=axisDiameter/2, $fn=resolutionLow(), center=true); 

    // Body
    translate([0,0,height/2]) cube([size+margin,size,height],center=true);
    
    // Bottom
    translate([-holeDistance/2,+holeDistance/2,0]) cylinder(h=holeHeight, r=holeDiameter/2, $fn=resolutionLow(), center=true); 
    translate([+holeDistance/2,+holeDistance/2,0]) cylinder(h=holeHeight, r=holeDiameter/2, $fn=resolutionLow(), center=true); 
    translate([+holeDistance/2,-holeDistance/2,0]) cylinder(h=holeHeight, r=holeDiameter/2, $fn=resolutionLow(), center=true); 
    translate([-holeDistance/2,-holeDistance/2,0]) cylinder(h=holeHeight, r=holeDiameter/2, $fn=resolutionLow(), center=true); 
}

StepperTrinamicQSH4218_35_10_27();