# PCB-D POWER_5V — prototype parameter set V1.9

Дата: 2026-07-21  
Статус: `CALCULATION/SCHEMATIC INPUT SET — NO BOM OR FOOTPRINT FREEZE`

## 1. Назначение

Документ собирает в одном месте текущие численные входы для:

- официального LM5143DESIGN-CALC;
- ручной проверки;
- prototype schematic core;
- transient simulation;
- component candidate search;
- последующего KiCad implementation.

## 2. Converter configuration

```text
controller family: LM5143A-Q1 preferred
configuration: single-output 2-phase
phase shift: 180°
VIN functional: 9,2…14,6 В
VIN DC calculation maximum: 16 В
VOUT: 5,0 В
IOUT continuous: 15 А
IOUT short: 20 А
short duration: 1 с
repeat: ≥10 с and I²t permission
fSW: 400 кГц per phase
operation mode: FPWM preferred for controlled ripple/current sharing
```

Light-load mode remains a later firmware/efficiency decision; it must not interfere with diagnostics or hard-off behavior.

## 3. Phase magnetics

```text
L1 = L2 = 3,3 мкГн ±20 %
Isat hot ≥15 А
Irms hot ≥10 А
DCR 25 °C target ≤8 мОм
shielded construction
AEC-Q200 preferred
bounding box ≤13 × 11 × 11 мм
```

Calculated maximum phase ripple at 16 В:

```text
ΔIL ≈2,60 А p-p
```

Calculated phase peak:

```text
15-А total mode: ≈8,80 А
20-А total mode: ≈11,30 А
phase design capability: ≥13 А peak
```

## 4. Current sensing

```text
2 × Kelvin shunt
RSHUNT = 5 мОм ±1 %
power ≥1 Вт continuous
low TCR
4-terminal preferred
```

Current-limit design must be checked against exact LM5143A-Q1 min/typ/max threshold, slope compensation, propagation delay and tolerances.

## 5. MOSFET class

```text
quantity: 4 N-channel MOSFET
VDS: 60 В minimum
RDS(on) 25 °C target ≤3 мОм at actual gate drive
hot RDS(on) design target ≤6 мОм
Qg target ≤40 нКл
package target: 5 × 6 мм
height target ≤1,5 мм
TJ max ≥150 °C; 175 °C preferred
AEC-Q101 preferred
```

40-В MOSFET is not a prototype option.

## 6. Input transient protection

```text
TVS class: SMCJ18A
polarity: unidirectional
VRWM: 18 В
VBR: 20…22,1 В
nominal datasheet clamp class: 29,2 В
controller/MOSFET measured peak target: ≤32 В preferred
engineering maximum acceptance target: ≤36 В
```

TVS exact manufacturer/orderable remains open.

## 7. Input capacitor bank

Main switching bank:

```text
effective ceramic capacitance at bias ≥100 мкФ
voltage rating ≥35 В for prototype
combined ripple capability ≥6 А RMS at +60 °C
local HF ceramics at each half-bridge
```

25-В input capacitors are rejected for the prototype because the SMCJ18A clamp class is approximately 29,2 В. Any future reduction of voltage class requires a separate measured transient and derating review.

## 8. RC damping branch

```text
Cd = 330 мкФ initial
Cd voltage rating ≥35 В
Rd = 0,10 Ом initial
Rd tuning range = 0,068…0,15 Ом
Rd pulse energy ≥50 мДж minimum
recommended pulse margin ≥100 мДж
series input inductor = DNP for first prototype
```

The resistor is in series with Cd only, not with the 15-А main current path.

## 9. Output capacitor bank

Initial design-tool/manual set:

```text
4 × 47 мкФ X7R minimum
2 × 220…330 мкФ low-ESR polymer class
additional 1…10 мкФ local decoupling
100 нФ local decoupling
```

Not frozen:

- exact effective capacitance;
- ESR/ESL;
- polymer voltage/current class;
- allowed droop/overshoot;
- simultaneous load step;
- compensation values.

## 10. UVLO and soft start targets

Preliminary functional targets:

```text
UVLO rising target: 8,8…9,0 В
UVLO falling target: 8,2…8,5 В
soft-start target: 10…20 мс
```

These targets:

- permit operation at the accepted 9,2-В lower boundary;
- avoid chatter on short dips;
- do not override BMS/system undervoltage actions;
- reduce input inrush and 5V_SYS_BUS overshoot.

Exact resistor/capacitor values are generated only after exact controller variant and design-tool calculation.

## 11. Hardware safety inputs

Required independent gating:

```text
P5_GROUP_SAFE_OFF
P5_GROUP_HARD_OFF
```

Both must disable PWM/gate drive without relying on:

- local MCU;
- CAN-FD;
- SERVICE_OVERRIDE;
- normal software command path.

`P5_BOARD_FAULT_N` reports local protection/diagnostic state to PCB-B.

## 12. Prototype observability

Required test points:

```text
TP_P5_IN_RAW
TP_P5_IN_CLAMPED
TP_P5_POWER_GND
TP_PHASE1_SW
TP_PHASE2_SW
TP_PHASE1_ISENSE_P/N
TP_PHASE2_ISENSE_P/N
TP_5V_SYS_BUS
TP_COMP/FB as permitted by layout
TP_PGOOD
TP_TEMP_FET1/FET2/IND1/IND2/CAP_BANK
```

High-dV/dt and current-sense test points must be separated physically.

## 13. Design-tool inputs still required

```text
exact LM5143A-Q1 orderable/package
controller gate-drive voltage/configuration
MOSFET candidates and full Qg/Qgd/Coss curves
inductor candidates and hot DCR/Isat curves
input capacitor effective C/ESR/ESL
output capacitor effective C/ESR/ESL
load-step targets
target crossover/phase margin
spread-spectrum policy
EMI filter decision
```

## 14. Manual acceptance before schematic

```text
input transient boundary documented: PASS
controller voltage class selected: PASS
phase electrical sizing: PASS
RC damping start values: PASS
35-В input capacitor class: PASS
exact OCP calculation: OPEN
loop compensation: OPEN
exact component candidates: OPEN
thermal qualification: OPEN
```

## 15. Next use

This parameter set is the canonical input for the next step:

```text
LM5143DESIGN-CALC run
→ exact prototype candidate table
→ schematic converter core
→ simulation/test plan
```
