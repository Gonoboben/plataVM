# PCB-D POWER_5V — converter-core schematic review V1.9

Дата: 2026-07-21  
Статус: `PRELIMINARY CONVERTER-CORE DEFINITION — SEMANTIC ERC PASS, NATIVE KICAD ERC OPEN`

## 1. Scope

Обновлён KiCad sheet:

```text
Hardware/KiCad/41_5V_DC_DC.kicad_sch
```

Лист фиксирует после расчётного Gate:

- exact prototype controller orderable;
- two-phase power-stage candidates;
- RT, soft-start и compensation starting values;
- common single-output ties;
- аппаратную enable/safety equation;
- явные `CALC_TBD` для неподтверждённых значений;
- input/output capacitor boundary;
- fault/measurement interfaces.

Лист ещё не является production schematic и не содержит утверждённых footprints/copper/layout.

## 2. Core connectivity

```text
PACK_BUS_P5_IN
 ├→ Q_HS1/Q_LS1 → SW1 → L1 → RSH1 ┐
 └→ Q_HS2/Q_LS2 → SW2 → L2 → RSH2 ┴→ 5V_SYS_BUS
```

Both phases:

```text
Q_HSx/Q_LSx = BUK9Y6R0-60E,115
Lx = XAL1010-332MED, 3,3 мкГн
RSHx = WSK25125L000FEA, 5 мОм /1 % Kelvin
```

## 3. Controller ties

```text
MODE → VDDA
DEMB → VDDA
DITH → VDDA
FB1 → POWER_GND
FB2 → POWER_GND
COMP1 ↔ COMP2
SS1 ↔ SS2
VOUT1/VOUT2 → 5V_SYS_BUS sense
VCCX → 5V_SYS_BUS after startup
```

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

- both EN channels are controlled together;
- SAFE/HARD_OFF path is hardware;
- local MCU, CAN-FD and SERVICE_OVERRIDE cannot bypass it;
- UVLO defaults to OFF on unpowered/invalid supervisor state.

## 7. Preliminary ERC

Machine-readable input:

```text
Hardware/KiCad/PCB_D_CONVERTER_CORE_MANIFEST_V1_9.json
```

Checker:

```text
Tools/erc/pcb_d_converter_core_erc.py
```

Executed command:

```text
python Tools/erc/pcb_d_converter_core_erc.py \
  Hardware/KiCad/PCB_D_CONVERTER_CORE_MANIFEST_V1_9.json
```

Result:

```text
phases: 2
CALC_TBD markers: 19
RESULT: PASS
```

Checked:

- required input/output boundary;
- exactly two interleaved phases;
- same prototype component set in both phases;
- common output sense;
- fixed-5-V configuration ties;
- required direct SAFE/HARD_OFF;
- no hidden production freeze;
- no use of forbidden power-domain substitutions;
- no high-current ownership transfer to PCB-B;
- unresolved values remain explicitly marked.

## 8. Native KiCad ERC status

Native KiCad ERC was not falsely claimed. The current environment does not contain `kicad-cli`/`eeschema`, and the sheet intentionally does not yet instantiate the exact 40-pin controller symbol and all discrete symbols.

Therefore:

```text
semantic/project ERC: PASS
S-expression structural check: PASS
native KiCad application ERC: OPEN
```

Native ERC becomes mandatory immediately after exact symbol/pin instantiation in owner KiCad 10.0. The PR must remain draft until that check is attached.

## 9. Production status

```text
calculation Gate: PASS
converter-core definition: CREATED
CALC_TBD visibility: PASS
semantic ERC: PASS
native KiCad ERC: OPEN
production schematic freeze: NOT GRANTED
production BOM: NOT FROZEN
footprints/3D: OPEN
sealed-volume thermal qualification: OPEN
```
