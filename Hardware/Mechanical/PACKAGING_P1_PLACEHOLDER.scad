// PlataVM PACKAGING-P1 placeholder model
// Version: V1.9
// Purpose: board-envelope and height-budget review only
// No final components, connectors, mounting holes or production geometry.

$fn = 64;

assembly_x = 250;
assembly_y = 100;
assembly_z = 80;
board_t = 1.6;

z_l0 = 3;
z_l1 = 32;
z_l2 = 61;

h_l0 = 23;
h_l1 = 23;
h_l2 = 16;

module board_block(x, y, z, sx, sy, h, name="") {
    translate([x, y, z]) {
        cube([sx, sy, board_t]);
        translate([0, 0, board_t])
            %cube([sx, sy, h]);
    }
}

module assembly_envelope() {
    %cube([assembly_x, assembly_y, assembly_z]);
}

module mounting_axis(x, y) {
    translate([x, y, 0])
        %cylinder(h=assembly_z, d=10);
}

assembly_envelope();

// L0: PCB-A + PCB-C = 240 mm
board_block(0, 3, z_l0, 110, 94, h_l0, "PCB-A");
board_block(110, 3, z_l0, 130, 94, h_l0, "PCB-C");

// L1: PCB-D + PCB-E = 235 mm
board_block(0, 3, z_l1, 125, 94, h_l1, "PCB-D");
board_block(125, 3, z_l1, 110, 94, h_l1, "PCB-E");

// L2: PCB-B = 180 mm
board_block(0, 3, z_l2, 180, 94, h_l2, "PCB-B");

// Generic mounting/tool-access axes. Coordinates are preliminary only.
mounting_axis(7.5, 10.5);
mounting_axis(7.5, 89.5);
mounting_axis(102.5, 10.5);
mounting_axis(102.5, 89.5);
mounting_axis(117.5, 10.5);
mounting_axis(117.5, 89.5);
mounting_axis(232.5, 10.5);
mounting_axis(232.5, 89.5);

// Reference planes for level separation.
translate([0, 0, z_l0 + board_t + h_l0])
    %cube([assembly_x, assembly_y, 0.2]);
translate([0, 0, z_l1 + board_t + h_l1])
    %cube([assembly_x, assembly_y, 0.2]);
translate([0, 0, z_l2 + board_t + h_l2])
    %cube([assembly_x, assembly_y, 0.2]);
