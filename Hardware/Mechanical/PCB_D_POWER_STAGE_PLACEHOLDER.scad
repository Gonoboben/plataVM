// PlataVM PCB-D POWER_5V component-envelope model
// Version: V1.9
// Purpose: two-phase buck bounding-box and height review only.
// No final parts, footprints, mounting holes, copper, connectors or production geometry.

$fn = 48;

board_x = 125;
board_y = 94;
board_t = 1.6;
height_limit = 23;

module board() {
    cube([board_x, board_y, board_t]);
}

module envelope(pos, size, label="") {
    translate([pos[0], pos[1], board_t + pos[2]])
        %cube(size);
}

module height_limit_plane() {
    translate([0, 0, board_t + height_limit])
        %cube([board_x, board_y, 0.2]);
}

board();
height_limit_plane();

// Input protection and bulk input region.
envelope([4, 8, 0], [18, 22, 12], "INPUT_PROTECTION");
envelope([4, 34, 0], [22, 18, 12], "INPUT_BULK");

// Reference outline for the preliminary 70 x 38 mm dual-phase power-stage cluster.
translate([28, 8, board_t])
    %cube([70, 38, 0.3]);

// Phase 1 row inside the 70 x 38 mm cluster.
envelope([30, 10, 0], [14, 10, 3], "LOCAL_CIN_1");
envelope([46, 10, 0], [7, 6, 1.5], "HS_FET_1");
envelope([54, 10, 0], [7, 6, 1.5], "LS_FET_1");
envelope([64, 9, 0], [13, 11, 11], "INDUCTOR_1");
envelope([80, 12, 0], [7, 4, 1.5], "SHUNT_PHASE_1");

// Phase 2 row inside the 70 x 38 mm cluster.
envelope([30, 34, 0], [14, 10, 3], "LOCAL_CIN_2");
envelope([46, 36, 0], [7, 6, 1.5], "HS_FET_2");
envelope([54, 36, 0], [7, 6, 1.5], "LS_FET_2");
envelope([64, 33, 0], [13, 11, 11], "INDUCTOR_2");
envelope([80, 38, 0], [7, 4, 1.5], "SHUNT_PHASE_2");

// Shared controller and gate/snubber support volumes.
envelope([89, 20, 0], [7, 7, 1.5], "CONTROLLER");
envelope([46, 19, 0], [12, 8, 3], "GATE_SNUBBER_1");
envelope([46, 27, 0], [12, 8, 3], "GATE_SNUBBER_2");

// Shared output capacitor banks.
envelope([83, 50, 0], [32, 16, 4], "OUTPUT_CERAMIC_BANK");
envelope([83, 68, 0], [34, 24, 16], "OUTPUT_POLYMER_BANK");

// Local MCU/CAN and provisional output-protection areas.
envelope([4, 70, 0], [18, 16, 5], "LOCAL_MCU_CAN");
envelope([28, 56, 0], [42, 14, 12], "OUTPUT_GROUP_1_5_PARTIAL");
envelope([28, 74, 0], [42, 14, 12], "OUTPUT_GROUP_6_10_PARTIAL");
