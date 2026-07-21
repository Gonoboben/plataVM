# PCB-D POWER_5V — открытые Gates после LM5143DESIGN-CALC V1.9

Дата: 2026-07-21  
Статус: `CALCULATION GATE PASSED — NATIVE ERC, TEST AND PRODUCTION GATES OPEN`

## 1. Закрыто предварительно

| Gate | Результат | Статус |
|---|---|---|
| Q-P5-009A | Prototype controller voltage class 65 В | CLOSED_PRELIMINARY |
| Q-P5-009B | SMCJ18A transient-protection class | CLOSED_PRELIMINARY |
| Q-P5-012A | fSW baseline 400 кГц | CLOSED_PRELIMINARY |
| Q-P5-013A | Prototype 5-мОм Kelvin shunts | CLOSED_PRELIMINARY |
| Q-P5-014A | Prototype controller/MOSFET/inductor/shunt/TVS/capacitor candidates | CLOSED_PRELIMINARY |
| Q-P5-014B | Manual OCP tolerance compatibility with 20 А /1 с | CLOSED_PRELIMINARY |
| Q-P5-014C | Exact prototype R_DAMP orderable PWR263S-35-R100FE | CLOSED_PRELIMINARY |
| Q-P5-017A | Preliminary load-step targets | CLOSED_PRELIMINARY |
| Q-P5-018A | Candidate loss feasibility at 75 Вт | CLOSED_PRELIMINARY |
| LM5143DESIGN-CALC | Official-family calculator configuration and input/output record | CLOSED_CALCULATION |
| Q-P5-016A | Nominal and tolerance-sweep compensation model | CLOSED_PRELIMINARY |

## 2. Calculator result

```text
configuration: LM5143A-Q1, single-output, 2 phases, 180°, FPWM
VIN: 9,2 /12,8 /16 В
VOUT: 5 В
IOUT: 15 А continuous; 20 А /1 с
fSW: 400 кГц/phase
RT: 54,9 кОм /1 %
L1/L2: 3,3 мкГн ±20 %
RSH1/RSH2: 5 мОм ±1 % Kelvin
CSS: 510 нФ starting value
```

OCP comparison:

```text
calculator nominal total-average OCP:
  27,454 А at VINmin
  26,867 А at VINnom
  26,566 А at VINmax

manual minimum total-average OCP: 22,522 А
worst legal 20-А phase peak with conservative RT sweep: 11,851 А
minimum phase threshold: 13,069 А
minimum preliminary margin: 10,28 %
```

Compensation starting set:

```text
RCOMP = 24,9 кОм /1 %
CCOMP = 3,3 нФ
CHF = 220 пФ
nominal crossover ≈29,18 кГц
nominal phase margin ≈73,55°
modeled crossover corners ≈18,31…39,14 кГц
modeled minimum phase margin ≈56,21°
```

These are prototype calculation results, not production guarantees.

## 3. Открыто после calculator Gate

| ID | Открытый параметр | Статус |
|---|---|---|
| Q-P5-009C | Exact hot-plug/turn-off transient waveforms and measured clamp | OPEN_MEASUREMENT |
| Q-P5-009D | Exact external UVLO supervisor/comparator and tolerance network | OPEN_CALC_COMPONENT |
| Q-P5-010 | Final allowed 5V_SYS_BUS droop/overshoot from actual devices | OPEN_OWNER_DEVICE_DATA |
| Q-P5-011 | Actual single and simultaneous external load profiles | OPEN_OWNER_DEVICE_DATA |
| Q-P5-012B | Compare final 300/400/500/600-кГц efficiency/EMI result | OPEN_CALC_TEST |
| Q-P5-012C | Measured RT frequency over voltage and temperature | OPEN_TEST |
| Q-P5-013B | Exact CS filter, propagation delay and hiccup behaviour | OPEN_CALC_TEST |
| Q-P5-013C | Bench OCP onset, phase sharing and no-nuisance 20-А correlation | OPEN_TEST |
| Q-P5-014D | Exact MLCC DC-bias effective capacitance | OPEN_DATASHEET_CALC |
| Q-P5-014E | Exact gate resistors, bootstrap and snubber values | OPEN_CALC_TEST |
| Q-P5-014F | PWR263S-35-R100FE pulse graph and hot-plug application verification | OPEN_DATASHEET_TEST |
| Q-P5-015 | Sealed-volume thermal result at +60 °C | OPEN_THERMAL_TEST |
| Q-P5-016B | Native Bode measurement over VIN/load/cap tolerance | OPEN_TEST |
| Q-P5-017B | Bode/load-step bench correlation | OPEN_TEST |
| Q-P5-018B | Exact MOSFET switching and inductor core losses | OPEN_CALC_TEST |
| Q-P5-019 | Exact controller/discrete symbols and native KiCad ERC | OPEN_SCHEMATIC_ERC |

## 4. UVLO result

Required operating window:

```text
rising 8,8…9,0 В
falling 8,2…8,5 В
```

LM5143A-Q1 EN thresholds do not permit this narrow hysteresis from one passive divider. Therefore:

```text
passive EN divider: REJECTED
external supervisor/comparator: CALC_TBD
nominal target: 8,9 В rising /8,35 В falling
hardware-qualified UVLO_OK required for both EN inputs
```

The exact device and resistor network remain outside production freeze.

## 5. Prototype converter-core status

Created:

```text
Hardware/KiCad/41_5V_DC_DC.kicad_sch
Hardware/KiCad/PCB_D_CONVERTER_CORE_MANIFEST_V1_9.json
Tools/erc/pcb_d_converter_core_erc.py
```

The sheet contains:

- selected prototype candidates;
- confirmed RT/SS/compensation starting values;
- explicit `CALC_TBD` values for UVLO, CS filters, gate resistors, bootstrap and snubbers;
- DNP/tuning options;
- direct SAFE/HARD_OFF equation;
- no production BOM status;
- no footprint freeze.

Validation:

```text
S-expression structural check: PASS
machine-readable semantic ERC: PASS
native KiCad application ERC: OPEN
```

The current sheet is a preliminary converter-core definition. Production schematic freeze is not granted.

## 6. Thermal Gate

Prototype component selection and calculation do not close:

```text
sealed enclosure
+60 °C internal design point
no hull thermal contact
15 А continuous until steady state
```

Required measurements:

- four MOSFET temperatures;
- L1/L2 temperatures;
- controller temperature;
- input/output capacitor temperatures;
- phase sharing;
- output regulation;
- fault telemetry;
- conformal-coating impact.

## 7. Mechanical Gate

Required before footprint freeze:

```text
manufacturer land patterns
STEP/3D models
RHA exposed-pad/via pattern
LFPAK56 courtyard and gate-loop feasibility
XAL1010 solder and clearance review
D²PAK R_DAMP area
8 × input-MLCC placement
connector and harness mating volume
inter-level L1/L2 clearance
```

## 8. Next Gate

```text
exact LM5143A-Q1 and discrete symbol/pin instantiation
→ owner KiCad 10.0 open
→ native KiCad ERC
→ exact UVLO/CS/gate/bootstrap/snubber calculation
→ Bode/load-step/OCP bench correlation
→ exact footprint/3D candidate review
→ prototype BOM Gate
→ electrical/transient/load/thermal test plan
```
