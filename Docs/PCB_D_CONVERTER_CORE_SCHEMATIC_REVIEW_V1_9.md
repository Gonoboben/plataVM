# PCB-D POWER_5V — converter-core schematic review V1.9

Дата: 2026-07-23  
Статус: `PRELIMINARY CONVERTER-CORE DEFINITION — EXACT PIN MAP AND SEMANTIC ERC PASS, NATIVE KICAD ERC OPEN`

## 1. Scope

Обновлён KiCad sheet:

```text
Hardware/KiCad/41_5V_DC_DC.kicad_sch
```

Лист фиксирует после расчётного и exact pin-map Gates:

- exact prototype controller orderable;
- verified LM5143A-Q1 RHA-40 pin numbers and roles;
- two-phase power-stage candidates;
- RT, soft-start и compensation starting values;
- common single-output ties;
- аппаратную enable/safety equation;
- явные `CALC_TBD` для неподтверждённых значений;
- input/output capacitor boundary;
- fault/measurement interfaces.

Лист ещё не является production schematic и не содержит утверждённых symbols, footprints, copper или layout.

## 2. Core connectivity

```text
PACK_BUS_P5_IN
 ├→ Q_HS1/Q_LS1 → PHASE1_SW → L1 → RSH1 ┐
 └→ Q_HS2/Q_LS2 → PHASE2_SW → L2 → RSH2 ┴→ 5V_SYS_BUS
```

Both phases:

```text
Q_HSx/Q_LSx = BUK9Y6R0-60E,115
Lx = XAL1010-332MED, 3,3 мкГн
RSHx = WSK25125L000FEA, 5 мОм /1 % Kelvin
```

## 3. Exact controller ties

```text
MODE pin 34 → VDDA
DEMB pin 33 → VDDA
DITH pin 38 → VDDA
FB1 pin 28 → AGND for fixed 5 В
FB2 pin 3 → AGND for single-output interleaved operation
COMP1 pin 29 ↔ COMP2 pin 2 = COMP_COMMON
SS1 pin 30 ↔ SS2 pin 1 = SS_COMMON
EN1 pin 31 = EN2 pin 40 = EN_RUN
VOUT1 pin 26 / VOUT2 pin 5 → 5V_SYS_BUS_SENSE
VCC pins 15/16 → VCC_BIAS
VCCX pin 6 → 5V_SYS_BUS after startup, subject to datasheet constraints
PG1 pin 24 → P5_PGOOD_OD
PG2 pin 7 → isolated testpad only; not aggregated
```

`AGND` here is the controller-local analog ground reference. It must not be silently renamed to generic system `POWER_GND`; the final AGND/PGND join is a controlled layout boundary around the controller exposed pad and decoupling network.

## 4. Confirmed prototype values

```text
R_RT = 54,9 кОм /1 %
C_SS = 510 нФ
C_RES = 470 нФ prototype start
R_COMP = 24,9 кОм /1 %
C_COMP = 3,3 нФ
C_HF = 220 пФ
```

## 5. Controlled CALC_TBD list

```text
U_UVLO exact supervisor/comparator
UVLO divider/reference/hysteresis values
hardware EN_RUN gate implementation
R_GATE_HS1/LS1/HS2/LS2
C_BOOT1/2 and D_BOOT1/2 exact values
RCS1/2 and CCS1/2
RC snubber values
actual input MLCC Ceff
actual output Ceff/ESR/ESL
```

DNP tuning remains explicit for snubbers and output/input capacitance.

## 6. Safety equation

```text
EN_RUN =
5V_SYS_EN
AND UVLO_OK
AND NOT P5_GROUP_SAFE_OFF
AND NOT P5_GROUP_HARD_OFF
```

Requirements:

- EN1 pin 31 and EN2 pin 40 are controlled together;
- SAFE/HARD_OFF path is hardware;
- local MCU, CAN-FD and SERVICE_OVERRIDE cannot bypass it;
- UVLO defaults to OFF on unpowered/invalid supervisor state.

## 7. Preliminary ERC

Machine-readable inputs:

```text
Hardware/KiCad/PCB_D_CONVERTER_CORE_MANIFEST_V1_9.json
Hardware/KiCad/LM5143A_Q1_RHA40_PINMAP_V1_9.json
```

Checkers:

```text
Tools/erc/pcb_d_converter_core_erc.py
Tools/erc/pcb_d_lm5143_pinmap_erc.py
```

Recorded results:

```text
phases: 2
physical controller pins: 40 + exposed pad
exact pin map: PASS
single-output interleaved ties: PASS
PG1/PG2 role separation: PASS
CALC_TBD markers: 19
controlled freeze policy: PASS
RESULT: PASS
```

Checked:

- required input/output boundary;
- exactly two interleaved phases;
- exact controller pin numbers and phase allocation;
- same prototype component set in both phases;
- common output sense;
- fixed-5-V configuration ties;
- required direct SAFE/HARD_OFF;
- no hidden production freeze;
- no use of forbidden power-domain substitutions;
- no high-current ownership transfer to PCB-B;
- unresolved values remain explicitly marked.

## 8. Native KiCad ERC status

Native KiCad ERC was not falsely claimed. The current environment does not contain `kicad-cli`/`eeschema`, and the sheet intentionally does not yet instantiate the exact controller and discrete symbols.

Therefore:

```text
exact physical pin-map contract: PASS
semantic/project ERC: PASS
S-expression structural check: PASS
KiCad symbol instantiation: OPEN
native KiCad application ERC: OPEN
```

Native ERC becomes mandatory immediately after exact symbol instantiation in owner KiCad 10.0. The PR must remain draft until that check is attached.

## 9. Production status

```text
calculation Gate: PASS
exact pin-map Gate: PASS
converter-core definition: CREATED
CALC_TBD visibility: PASS
semantic ERC: PASS
KiCad symbol/native ERC: OPEN
production schematic freeze: NOT GRANTED
production BOM: NOT FROZEN
footprints/3D: OPEN
sealed-volume thermal qualification: OPEN
```
