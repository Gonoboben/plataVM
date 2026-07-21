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

// Controller and current sensing.
envelope([31, 42, 0], [7, 7, 1.5], "CONTROLLER");
envelope([42, 17, 0], [7, 4, 1.5], "SHUNT_PHASE_1");
envelope([42, 57, 0], [7, 4, 1.5], "SHUNT_PHASE_2");

// Phase 1 half bridge, support and inductor.
envelope([31, 8, 0], [7, 6, 1.5], "HS_FET_1");
envelope([39, 8, 0], [7, 6, 1.5], "LS_FET_1");
envelope([31, 24, 0], [12, 8, 3], "GATE_SNUBBER_1");
envelope([49, 8, 0], [14, 10, 3], "LOCAL_CIN_1");
envelope([66, 8, 0], [13, 11, 11], "INDUCTOR_1");

// Phase 2 half bridge, support and inductor.
envelope([31, 68, 0], [7, 6, 1.5], "HS_FET_2");
envelope([39, 68, 0], [7, 6, 1.5], "LS_FET_2");
envelope([31, 54, 0], [12, 8, 3], "GATE_SNUBBER_2");
envelope([49, 68, 0], [14, 10, 3], "LOCAL_CIN_2");
envelope([66, 68, 0], [13, 11, 11], "INDUCTOR_2");

// Shared output capacitor banks.
envelope([83, 8, 0], [32, 16, 4], "OUTPUT_CERAMIC_BANK");
envelope([83, 28, 0], [34, 24, 16], "OUTPUT_POLYMER_BANK");

// Local MCU/CAN and provisional output-protection areas.
envelope([4, 70, 0], [18, 16, 5], "LOCAL_MCU_CAN");
envelope([26, 80, 0], [42, 10, 12], "OUTPUT_GROUP_1_5_PARTIAL");
envelope([72, 80, 0], [42, 10, 12], "OUTPUT_GROUP_6_10_PARTIAL");

// Reference outline for the preliminary 70 x 38 mm dual-phase power-stage cluster.
translate([29, 6, board_t])
    %cube([52, 74, 0.3]);
