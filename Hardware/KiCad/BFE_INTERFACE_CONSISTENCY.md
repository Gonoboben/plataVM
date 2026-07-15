# PCB-A BFE_POWER interface consistency report

Date: 2026-07-15

Scope:

```text
Hardware/KiCad/10_BFE_POWER_TOP.kicad_sch
Hardware/KiCad/11_BATTERY_INPUT_1.kicad_sch
Hardware/KiCad/12_BATTERY_INPUT_2.kicad_sch
Hardware/KiCad/13_MAIN_PATH_1.kicad_sch
Hardware/KiCad/14_MAIN_PATH_2.kicad_sch
Hardware/KiCad/15_DECK_BALANCE.kicad_sch
Hardware/KiCad/16_PACK_BUS_AND_DISCHARGE.kicad_sch
Hardware/KiCad/17_REMOTE_OFF_AND_EXT_KILL.kicad_sch
Hardware/KiCad/18_BATTERY_MEASUREMENTS.kicad_sch
Hardware/KiCad/19_BFE_CONNECTORS_TESTPOINTS.kicad_sch
```

Status:

```text
PASS WITH CONTROLLED PLACEHOLDERS
```

This report checks text-only hierarchical labels and interface names before adding real KiCad library symbols. It does not select components, footprints, connector families, pin count, wire gauge, sensor topology, DC/DC, MCU, PCB layout or BOM part numbers.

## 1. Corrections made in this pass

### 1.1 Hold-loop return names

Before this pass, sheet 17 used return names:

```text
BAT1_SN176_NEG_RETURN
BAT2_SN176_NEG_RETURN
```

The battery input sheets use:

```text
BAT1_SN176_NEG
BAT2_SN176_NEG
```

To remove the interface break, sheet 17 now returns hold-loop paths to the same accepted battery negative names:

```text
BAT1_HOLD_RETURN_IN -> BAT1_EXT_KILL_NC_TBD -> BAT1_REMOTE_OFF_NC_TBD -> BAT1_SN176_NEG
BAT2_HOLD_RETURN_IN -> BAT2_EXT_KILL_NC_TBD -> BAT2_REMOTE_OFF_NC_TBD -> BAT2_SN176_NEG
```

### 1.2 Balance tap source names

Sheet 15 consumes:

```text
BALANCE_TAP_BAT1
BALANCE_TAP_BAT2
```

Sheets 11 and 12 now explicitly expose these taps from the corresponding battery input boundaries.

### 1.3 Measurement aggregation completeness

Sheet 18 now explicitly receives:

```text
BAT1_PRESENT_STATUS
BAT2_PRESENT_STATUS
DIAG_BALANCE_I
DIAG_BALANCE_TEMP
DIAG_BALANCE_STATUS
```

This keeps presence/status and balance observability connected to the measurement aggregation boundary.

## 2. Accepted cross-sheet interface pairs

### 2.1 Battery input to main paths

```text
11_BATTERY_INPUT_1: BAT1_TO_MAIN_PATH -> 13_MAIN_PATH_1: BAT1_TO_MAIN_PATH
12_BATTERY_INPUT_2: BAT2_TO_MAIN_PATH -> 14_MAIN_PATH_2: BAT2_TO_MAIN_PATH
```

### 2.2 Battery input to hold-loop actuators

```text
11_BATTERY_INPUT_1: BAT1_HOLD_RETURN_IN -> 17_REMOTE_OFF_AND_EXT_KILL: BAT1_HOLD_RETURN_IN
12_BATTERY_INPUT_2: BAT2_HOLD_RETURN_IN -> 17_REMOTE_OFF_AND_EXT_KILL: BAT2_HOLD_RETURN_IN
11_BATTERY_INPUT_1: BAT1_SN176_NEG -> 17_REMOTE_OFF_AND_EXT_KILL: BAT1_SN176_NEG
12_BATTERY_INPUT_2: BAT2_SN176_NEG -> 17_REMOTE_OFF_AND_EXT_KILL: BAT2_SN176_NEG
```

### 2.3 Battery input to measurement aggregation

```text
11_BATTERY_INPUT_1: BAT1_MEAS_TAPS -> 18_BATTERY_MEASUREMENTS: BAT1_MEAS_TAPS
12_BATTERY_INPUT_2: BAT2_MEAS_TAPS -> 18_BATTERY_MEASUREMENTS: BAT2_MEAS_TAPS
11_BATTERY_INPUT_1: BAT1_PRESENT_STATUS -> 18_BATTERY_MEASUREMENTS: BAT1_PRESENT_STATUS
12_BATTERY_INPUT_2: BAT2_PRESENT_STATUS -> 18_BATTERY_MEASUREMENTS: BAT2_PRESENT_STATUS
```

### 2.4 Battery input to deck balance

```text
11_BATTERY_INPUT_1: BALANCE_TAP_BAT1 -> 15_DECK_BALANCE: BALANCE_TAP_BAT1
12_BATTERY_INPUT_2: BALANCE_TAP_BAT2 -> 15_DECK_BALANCE: BALANCE_TAP_BAT2
```

### 2.5 Main paths to PACK_BUS

```text
13_MAIN_PATH_1: BFE1_SW_OUT -> 16_PACK_BUS_AND_DISCHARGE: BFE1_SW_OUT
14_MAIN_PATH_2: BFE2_SW_OUT -> 16_PACK_BUS_AND_DISCHARGE: BFE2_SW_OUT
```

### 2.6 Main path diagnostics to measurement aggregation

```text
13_MAIN_PATH_1: DIAG_MAIN1_I     -> 18_BATTERY_MEASUREMENTS: DIAG_MAIN1_I
13_MAIN_PATH_1: DIAG_MAIN1_VIN   -> 18_BATTERY_MEASUREMENTS: DIAG_MAIN1_VIN
13_MAIN_PATH_1: DIAG_MAIN1_VOUT  -> 18_BATTERY_MEASUREMENTS: DIAG_MAIN1_VOUT
13_MAIN_PATH_1: DIAG_MAIN1_FAULT -> 18_BATTERY_MEASUREMENTS: DIAG_MAIN1_FAULT

14_MAIN_PATH_2: DIAG_MAIN2_I     -> 18_BATTERY_MEASUREMENTS: DIAG_MAIN2_I
14_MAIN_PATH_2: DIAG_MAIN2_VIN   -> 18_BATTERY_MEASUREMENTS: DIAG_MAIN2_VIN
14_MAIN_PATH_2: DIAG_MAIN2_VOUT  -> 18_BATTERY_MEASUREMENTS: DIAG_MAIN2_VOUT
14_MAIN_PATH_2: DIAG_MAIN2_FAULT -> 18_BATTERY_MEASUREMENTS: DIAG_MAIN2_FAULT
```

### 2.7 PACK_BUS diagnostics to measurement aggregation

```text
16_PACK_BUS_AND_DISCHARGE: DIAG_PACK_BUS_V            -> 18_BATTERY_MEASUREMENTS: DIAG_PACK_BUS_V
16_PACK_BUS_AND_DISCHARGE: DIAG_PACK_BUS_DISCH_STATUS -> 18_BATTERY_MEASUREMENTS: DIAG_PACK_BUS_DISCH_STATUS
```

### 2.8 Hold-loop diagnostics to measurement aggregation

```text
17_REMOTE_OFF_AND_EXT_KILL: DIAG_HOLD_LOOP_STATUS -> 18_BATTERY_MEASUREMENTS: DIAG_HOLD_LOOP_STATUS
```

### 2.9 Balance diagnostics to measurement aggregation

```text
15_DECK_BALANCE: DIAG_BALANCE_I      -> 18_BATTERY_MEASUREMENTS: DIAG_BALANCE_I
15_DECK_BALANCE: DIAG_BALANCE_TEMP   -> 18_BATTERY_MEASUREMENTS: DIAG_BALANCE_TEMP
15_DECK_BALANCE: DIAG_BALANCE_STATUS -> 18_BATTERY_MEASUREMENTS: DIAG_BALANCE_STATUS
```

### 2.10 PACK_BUS fanout to connector/testpoint grouping

```text
16_PACK_BUS_AND_DISCHARGE: PACK_BUS_TO_CRIT  -> 19_BFE_CONNECTORS_TESTPOINTS: PACK_BUS_TO_CRIT
16_PACK_BUS_AND_DISCHARGE: PACK_BUS_TO_P12   -> 19_BFE_CONNECTORS_TESTPOINTS: PACK_BUS_TO_P12
16_PACK_BUS_AND_DISCHARGE: PACK_BUS_TO_P5    -> 19_BFE_CONNECTORS_TESTPOINTS: PACK_BUS_TO_P5
16_PACK_BUS_AND_DISCHARGE: PACK_BUS_TO_LIGHT -> 19_BFE_CONNECTORS_TESTPOINTS: PACK_BUS_TO_LIGHT
```

### 2.11 BFE diagnostics to external control connector group

```text
18_BATTERY_MEASUREMENTS: DIAG_BFE_TO_CTRL -> 19_BFE_CONNECTORS_TESTPOINTS: DIAG_BFE_TO_CTRL
```

## 3. Controlled placeholders that are intentionally not paired yet

The following labels are allowed to remain single-ended until real generic symbols or connector groups are added:

```text
BAT1_SN176_RESERVE
BAT2_SN176_RESERVE
BAT1_EXT_KILL_NC_TBD
BAT1_REMOTE_OFF_NC_TBD
BAT2_EXT_KILL_NC_TBD
BAT2_REMOTE_OFF_NC_TBD
MAIN_SW1_INPUT
MAIN_SW1_OUTPUT
MAIN_SW2_INPUT
MAIN_SW2_OUTPUT
PACK_BUS_NODE
BALANCE_PATH_TBD
BFE_TP_LOW_ENERGY
BFE_TP_POWER_GUARDED
BFE_FAULT_INJECTION_TP
```

Reason: these are local symbol-skeleton points or intentionally unassigned/service placeholders, not finalized inter-sheet electrical interfaces.

## 4. External control interfaces still aggregated

The PCB-B to PCB-A control interface is intentionally still represented as an aggregate connector group on sheet 19:

```text
CTRL_BFE_FROM_CTRL
```

The detailed consumers on BFE sheets are:

```text
CTRL_MAIN_SW1_EN
MAIN_SW1_SAFE_OFF
CTRL_MAIN_SW2_EN
MAIN_SW2_SAFE_OFF
PACK_BUS_DISCHARGE_EN
BALANCE_ARM
BALANCE_SW1_EN
BALANCE_SW2_EN
BALANCE_ABORT
BAT1_REMOTE_OFF_OPEN_CMD
BAT2_REMOTE_OFF_OPEN_CMD
EXT_KILL_HW_CHAIN
```

This is acceptable at the current stage because physical interboard connectors and final pin-count are still not selected. The next PCB-B or connector-detail pass must expand `CTRL_BFE_FROM_CTRL` into these named lines or explicitly define a safe multiplexing/interface scheme.

## 5. Safety constraints preserved

```text
No K_MAIN added.
PACK_BUS is still created on PCB-A.
High current is not routed through PCB-B_CTRL_RESERVE.
K_BATx remains external monostable contactor.
PCB-A only interrupts K_BATx hold-loop return.
EXT_KILL hardware path must not depend on MCU firmware.
BAT1 and BAT2 hold-loop returns remain separated.
BMS recovery must not auto-restart K_BATx.
```

## 6. Result

```text
PCB-A BFE_POWER interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
```

Next recommended step:

```text
Start PCB-B_CTRL_RESERVE detailed hierarchy
```

Rationale: PCB-A now has enough stable interface names to map MCU/control/diagnostic responsibility on PCB-B without changing PCB-A architecture.
