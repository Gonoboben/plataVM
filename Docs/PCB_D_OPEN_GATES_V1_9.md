# PCB-D POWER_5V — открытые Gates после выбора prototype components V1.9

Дата: 2026-07-21  
Статус: `PROTOTYPE COMPONENT SET SELECTED — DESIGN AND TEST GATES OPEN`

## 1. Закрыто предварительно

| Gate | Результат | Статус |
|---|---|---|
| Q-P5-009A | Prototype controller voltage class 65 В | CLOSED_PRELIMINARY |
| Q-P5-009B | SMCJ18A transient-protection class | CLOSED_PRELIMINARY |
| Q-P5-012A | fSW baseline 400 кГц | CLOSED_PRELIMINARY |
| Q-P5-013A | Prototype 5-мОм Kelvin shunts | CLOSED_PRELIMINARY |
| Q-P5-014A | Prototype controller/MOSFET/inductor/shunt/TVS/capacitor candidates | CLOSED_PRELIMINARY |
| Q-P5-014B | Manual OCP tolerance compatibility with 20 А /1 с | CLOSED_PRELIMINARY |
| Q-P5-017A | Preliminary load-step targets | CLOSED_PRELIMINARY |
| Q-P5-018A | Candidate loss feasibility at 75 Вт | CLOSED_PRELIMINARY |

## 2. Открыто до converter-core schematic

| ID | Открытый параметр | Статус |
|---|---|---|
| Q-P5-009C | Exact hot-plug/turn-off transient waveforms and measured clamp | OPEN_MEASUREMENT |
| Q-P5-010 | Final allowed 5V_SYS_BUS droop/overshoot from actual devices | OPEN_OWNER_DEVICE_DATA |
| Q-P5-011 | Actual single and simultaneous external load profiles | OPEN_OWNER_DEVICE_DATA |
| Q-P5-012B | Compare final 300/400/500/600-кГц efficiency/EMI result | OPEN_CALC_TEST |
| Q-P5-013B | Exact CS filter, slope compensation, propagation delay and hiccup behaviour | OPEN_CALC |
| Q-P5-014C | Exact R_DAMP orderable and pulse curve | OPEN_CANDIDATE |
| Q-P5-014D | Exact MLCC DC-bias effective capacitance | OPEN_DATASHEET_CALC |
| Q-P5-014E | Exact gate resistors, bootstrap and snubber values | OPEN_CALC_TEST |
| Q-P5-015 | Sealed-volume thermal result at +60 °C | OPEN_THERMAL_TEST |
| Q-P5-016 | Loop compensation and stability over VIN/load/cap tolerance | OPEN_CALC_TEST |
| Q-P5-017B | Bode/load-step bench correlation | OPEN_TEST |
| Q-P5-018B | Exact MOSFET switching and inductor core losses | OPEN_CALC_TEST |

## 3. Official design-tool Gate

Required output:

```text
LM5143DESIGN-CALC project/input record
exact controller configuration
RT value and frequency tolerance
UVLO divider
soft-start capacitor
current-limit and slope-compensation result
compensation network
crossover and phase margin
MOSFET loss estimate
inductor and capacitor checks
preliminary schematic/BOM output
```

The official tool has not been executed in the current environment.

## 4. Prototype schematic permission

A converter-core schematic may be created with:

- selected prototype candidates;
- clearly marked `CALC_TBD` values for compensation/CS filters/RT/SS;
- DNP/tuning options;
- no production BOM status;
- no footprint freeze until exact land-pattern review;
- mandatory ERC and independent calculation review.

Production schematic freeze is not granted.

## 5. Thermal Gate

Prototype component selection does not close:

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

## 6. Mechanical Gate

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

## 7. Next Gate

```text
LM5143DESIGN-CALC
→ converter-core schematic
→ ERC
→ exact footprint/3D candidate review
→ prototype BOM
→ electrical/transient/load/thermal test plan
```