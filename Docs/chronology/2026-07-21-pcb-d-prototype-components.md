# Хронология: выбор компонентов прототипа PCB-D POWER_5V

Дата: 2026-07-21  
База этапа: merge PR #43, commit `9ee73cf43f02a248cb81fffde2a2887105dc9a1e`

## 1. Причина этапа

После transient review были определены классы, но оставались открыты:

```text
exact controller orderable
MOSFET candidate
inductor candidate
5-мОм Kelvin shunt
TVS orderable
35-В damping capacitor
input/output capacitor strategy
OCP tolerance
load-step targets
candidate loss boundary
```

## 2. Prototype candidates

```text
U_DCDC: LM5143QRHARQ1
Q1…Q4: BUK9Y6R0-60E,115
L1/L2: XAL1010-332MED
RSH1/RSH2: WSK25125L000FEA
D_TVS: Littelfuse SMCJ18A
C_DAMP: Panasonic EEH-ZK1V331P
R_DAMP: Bourns PWR263S-35 family, 0,10 Ом target
C_IN: 22 мкФ /50 В X7R /1210 class, 8 positions
C_OUT: 2 ×10SVPC330M + 47-мкФ X7R tuning bank
```

`R_DAMP` exact code and pulse curve remain open. The set is prototype-only and does not freeze production BOM.

## 3. OCP result

Manual tolerance sweep:

```text
minimum phase peak threshold: 13,069 А
minimum equivalent total-average threshold: 22,522 А
worst-case legal 20-А phase peak: 11,808 А
minimum preliminary margin: 10,7 %
maximum equivalent threshold: about 31,158 А
```

Result:

```text
5-мОм shunt: MANUAL PRELIMINARY PASS
LM5143DESIGN-CALC and bench correlation: OPEN
```

## 4. Capacitor strategy

Input bank:

```text
8 ×1210 footprints
6 populated +2 DNP
22 мкФ /50 В X7R class
Ceff total at 16 В/tolerance/temp/aging ≥100 мкФ
```

Nominal capacitance is not accepted as effective capacitance.

Output bank:

```text
2 ×330 мкФ /10 В low-ESR polymer
4 ×47 мкФ /10 В X7R populated
2 ×47 мкФ DNP
```

## 5. Load-transient targets

```text
0↔3 А: ±5 %, settle <500 мкс
0↔6 А: ±8 %, settle <1 мс
0↔15 А validation: 4,25…5,75 В, recover <2 мс
15→20 А /1 с: no nuisance OCP, droop target ≤5 %
enable staggering: 5 мс preliminary
phase margin: ≥50° target
```

These remain engineering targets until actual external-device profiles are received.

## 6. Candidate loss boundary

```text
75-Вт output loss estimate: 2,9…6,0 Вт
estimated efficiency feasibility: 92,6…96,3 %
```

Sealed +60 °C thermal qualification remains open.

## 7. Architecture continuity

Not changed:

- no `K_MAIN`;
- no high-current path through PCB-B;
- two-phase 400-кГц /3,3-мкГн topology;
- 15-А continuous and 20-А/1-с mode;
- 60-В MOSFET minimum;
- SMCJ18A input boundary;
- 35-В minimum input capacitor policy;
- hard SAFE/HARD_OFF independent of MCU/CAN-FD;
- no hull thermal contact;
- PCB-D outline and level allocation.

## 8. Created documents

```text
Docs/PCB_D_PROTOTYPE_COMPONENT_CANDIDATES_V1_9.md
Docs/PCB_D_OCP_TOLERANCE_CALC_V1_9.md
Docs/PCB_D_LOAD_TRANSIENT_TARGETS_V1_9.md
Docs/PCB_D_PROTOTYPE_LOSS_BOUNDARY_V1_9.md
Docs/PCB_D_COMPONENT_SELECTION_CONSISTENCY_V1_9.md
```

Updated:

```text
Docs/PCB_D_PROTOTYPE_PARAMETER_SET_V1_9.md
Docs/V1_9_DOCUMENT_INDEX.md
```

## 9. Next Gate

```text
official LM5143DESIGN-CALC
→ exact compensation/OCP/RT/SS values
→ converter-core schematic
→ ERC
→ preliminary footprints and 3D
→ prototype BOM
→ transient/load/thermal bench plan
```