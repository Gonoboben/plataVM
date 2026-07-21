# PCB-D POWER_5V — prototype parameter set V1.9

Дата: 2026-07-21  
Статус: `SCHEMATIC INPUT SET WITH PROTOTYPE CANDIDATES — NO PRODUCTION BOM OR FOOTPRINT FREEZE`

## 1. Назначение

Канонический набор входов для:

- LM5143DESIGN-CALC;
- независимой ручной проверки;
- prototype converter-core schematic;
- transient и load-step simulation;
- preliminary footprints/3D;
- стендовых испытаний.

## 2. Converter configuration

```text
controller exact prototype orderable: LM5143QRHARQ1
controller family: LM5143A-Q1
configuration: single-output 2-phase
phase shift: 180°
VIN functional: 9,2…14,6 В
VIN DC calculation maximum: 16 В
VOUT: 5,0 В
IOUT continuous: 15 А
IOUT short: 20 А /1 с
repeat short: ≥10 с and I²t permission
fSW: 400 кГц per phase
operation mode: FPWM prototype baseline
```

Light-load mode remains outside the prototype baseline until phase-sharing, ripple and diagnostic behaviour are verified.

## 3. Prototype component set

```text
U_DCDC: LM5143QRHARQ1
Q_HS1/Q_LS1/Q_HS2/Q_LS2: BUK9Y6R0-60E,115
L1/L2: XAL1010-332MED
RSH1/RSH2: WSK25125L000FEA
D_TVS: Littelfuse SMCJ18A
C_DAMP: Panasonic EEH-ZK1V331P
R_DAMP: Bourns PWR263S-35 family, 0,10 Ом /1 % target
C_IN_MLCC: TDK C3225X7R1H226M250AC class
C_OUT_POLY: 2 × Panasonic 10SVPC330M
C_OUT_MLCC: Murata GRM32ER71A476KE15L class
```

`R_DAMP` exact order code and pulse curve remain open. All candidates remain prototype selections, not production BOM freeze.

## 4. Phase magnetics

```text
L1 = L2 = 3,3 мкГн ±20 %
selected: XAL1010-332MED
DCR: 3,7 typ /4,1 max мОм at 25 °C
Isat: 27,4 А class at 25 °C, 30-% drop criterion
Irms: 18,2 А at 20 °C rise class
shielded / AEC-Q class
```

Calculated maximum nominal phase ripple at 16 В:

```text
ΔIL ≈2,60 А p-p
```

Calculated phase peak:

```text
15-А total mode: ≈8,80 А
20-А total mode: ≈11,30 А
phase design capability: ≥13 А peak
```

Hot DCR, Isat and core loss curves remain mandatory inputs to thermal review.

## 5. Current sensing and OCP

```text
RSHUNT = 5 мОм ±1 %
selected: WSK25125L000FEA
quantity: 2
power: 1 Вт each
4-terminal Kelvin
```

Manual min/typ/max sweep:

```text
minimum phase peak threshold: 13,069 А
minimum equivalent total average threshold: 22,522 А
typical equivalent total average threshold: 26,596 А
maximum equivalent total average threshold: 31,158 А
worst-case legal 20-А phase peak: 11,808 А
minimum preliminary peak margin: 10,7 %
```

OCP remains a protective barrier above the legal `20 А /1 с` mode. It is not the precise system current limiter.

Exact slope compensation, propagation delay, RT tolerance, CS filtering and hiccup timing require official calculator and bench correlation.

## 6. MOSFET set

```text
quantity: 4 identical N-channel MOSFET
selected: BUK9Y6R0-60E,115
VDS: 60 В
logic-level gate class
RDS(on): 6-мОм class
package: LFPAK56
TJ max: 175 °C class
AEC-Q101
```

One type is used in all HS/LS positions for prototype manufacturability. Separate HS/LS optimization is allowed only after measured conduction/switching-loss review.

40-В MOSFET is not a prototype option.

## 7. Input transient protection

```text
D_TVS: Littelfuse SMCJ18A
polarity: unidirectional
VRWM: 18 В
VBR: 20…22,1 В
clamp class: 29,2 В
preferred measured peak: ≤32 В
engineering maximum acceptance: ≤36 В
```

TVS is placed at the PCB-D entry with a short dedicated POWER_GND return. Sustained overvoltage requires upstream branch OFF; TVS is not a continuous shunt regulator.

## 8. Input capacitor bank

```text
MLCC class: 22 мкФ /50 В /X7R /1210
candidate: C3225X7R1H226M250AC class
footprints: 8
initially populated: 6
DNP tuning: 2
required Ceff total at 16 В/tolerance/temp/aging: ≥100 мкФ
combined ripple capability: ≥6 А RMS at +60 °C
```

Nominal sum is not accepted as effective capacitance. Exact DC-bias curves must be included before schematic/BOM freeze.

## 9. RC damping branch

```text
C_DAMP: EEH-ZK1V331P
Cd = 330 мкФ /35 В

R_DAMP target = 0,10 Ом /1 %
family = PWR263S-35
Rd tuning = 0,068…0,15 Ом
single-pulse energy ≥50 мДж minimum
target pulse margin ≥100 мДж
series power inductor = DNP for first prototype
```

The resistor is in series with `C_DAMP` only and does not carry the 15-А continuous input current after capacitor charge.

## 10. Output capacitor bank

```text
2 × 10SVPC330M, 330 мкФ /10 В
4 × 47 мкФ /10 В X7R /1210 populated
2 × 47 мкФ /10 В X7R /1210 DNP options
additional local 1…10 мкФ and 100 нФ decoupling
```

Loop calculation uses actual Ceff/ESR/ESL and not nominal capacitance.

## 11. Load-transient targets

```text
Tier A: 0↔3 А, ±5 %, settle to ±2 % <500 мкс
Tier B: 0↔6 А, ±8 %, settle to ±2 % <1 мс
Tier C: 0↔15 А validation, 4,25…5,75 В, recover to ±5 % <2 мс
Tier D: 15→20 А for 1 с, steady droop target ≤5 %, no nuisance OCP
enable staggering start: 5 мс
phase margin target: ≥50°, preferred ≥60°
crossover initial target: 20…40 кГц
```

These are engineering targets pending actual external-device load profiles.

## 12. UVLO and soft-start targets

```text
UVLO rising: 8,8…9,0 В target
UVLO falling: 8,2…8,5 В target
soft start: 10…20 мс target
```

Exact resistor/capacitor values are generated after official controller calculation and schematic review.

## 13. Hardware safety inputs

```text
P5_GROUP_SAFE_OFF
P5_GROUP_HARD_OFF
P5_BOARD_FAULT_N
```

SAFE/HARD_OFF must disable PWM/gate drive independently of local MCU, CAN-FD, SERVICE_OVERRIDE and normal command path.

## 14. Prototype observability

```text
TP_P5_IN_RAW
TP_P5_IN_CLAMPED
TP_P5_POWER_GND
TP_PHASE1_SW
TP_PHASE2_SW
TP_PHASE1_ISENSE_P/N
TP_PHASE2_ISENSE_P/N
TP_5V_SYS_BUS
TP_COMP/FB as layout permits
TP_PGOOD
TEMP_Q_HS1/Q_LS1/Q_HS2/Q_LS2
TEMP_L1/L2
TEMP_CIN/COUT/CONTROLLER
```

High-dV/dt and current-sense points must be physically separated.

## 15. Preliminary loss boundary

```text
75-Вт output candidate-set loss: 2,9…6,0 Вт
estimated feasibility efficiency: 92,6…96,3 %
```

Exact MOSFET switching loss, inductor core loss and sealed-volume temperature remain open.

## 16. Open design-tool inputs

```text
exact gate-drive configuration
actual Qg/Qgd/Coss curves
exact hot inductor curves
MLCC DC-bias Ceff curves
output capacitor Ceff/ESR/ESL
exact R_DAMP orderable/pulse curve
exact CS filter
RT resistor and frequency tolerance
slope compensation
compensation network
spread-spectrum policy
EMI filter decision
```

## 17. Manual acceptance before schematic

```text
input transient boundary: PASS
controller exact prototype orderable: PASS
prototype MOSFET/inductor/shunt/TVS: PASS
capacitor starting sets: PASS
manual OCP tolerance: PASS
manual load-step targets: PASS
candidate loss feasibility: PASS
exact R_DAMP: OPEN
LM5143DESIGN-CALC output: OPEN
loop compensation: OPEN
footprint/3D fit: OPEN
thermal qualification: OPEN
production BOM: NOT FROZEN
```

## 18. Next use

```text
LM5143DESIGN-CALC
→ independent calculation comparison
→ converter-core schematic
→ ERC
→ preliminary footprint/3D review
→ prototype BOM and bench test plan
```