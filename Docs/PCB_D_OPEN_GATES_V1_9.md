# PCB-D POWER_5V — открытые Gates после LM5143DESIGN-CALC, pin-map, symbol instantiation и native ERC V1.9

Дата: 2026-07-23  
Статус: `CALCULATION, PIN-MAP, SYMBOL-INSTANTIATION AND NATIVE ERC INTERNAL-TOPOLOGY GATES PASSED — OWNER, TEST AND PRODUCTION GATES OPEN`

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
| Q-P5-019A | Exact LM5143A-Q1 RHA-40 physical pin mapping and tie contract | CLOSED_PINMAP |
| Q-P5-019B | Exact KiCad symbol definition and converter-core instantiation | CLOSED_SYMBOL_GATE |
| Q-P5-019C | GitHub Actions official KiCad 10 native ERC, exact standalone-boundary classification | CLOSED_NATIVE_ERC_INTERNAL_TOPOLOGY |
| Q-P5-019C1 | Exact BUK9Y6R0-60E LFPAK56 and WSK2512 four-terminal physical pin mapping | CLOSED_EXACT_DISCRETE_PINMAP |

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
worst legal 20-А phase peak: 11,851 А
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

## 3. Exact pin-map result

```text
31 EN1
32 RES
33 DEMB
34 MODE
35 AGND
36 VDDA
37 RT
38 DITH
39 SYNCOUT
40 EN2
```

Single-output interleaved contract:

```text
MODE → VDDA
FB2 → AGND
FB1 → AGND for fixed 5 V
COMP1 ↔ COMP2
SS1 ↔ SS2
DEMB → VDDA for FPWM
EN1 = EN2 = EN_RUN
PG1 pin 24 = primary PGOOD
PG2 pin 7 = isolated testpoint only
VCC pins 15 and 16 = common VCC_BIAS
```

Validation:

```text
physical pins: 40
exposed pad: 1
pin-number/name uniqueness: PASS
single-output tie contract: PASS
PG1/PG2 role separation: PASS
machine-readable pin-map ERC: PASS
```

## 4. Exact symbol-instantiation result

Created:

```text
Hardware/KiCad/plataVM_symbols.kicad_sym
Tools/kicad/generate_pcb_d_converter_core.py
Tools/erc/pcb_d_kicad_symbol_gate.py
Hardware/KiCad/PCB_D_KICAD_SYMBOL_GATE_RESULT_V1_9.txt
```

Updated:

```text
Hardware/KiCad/41_5V_DC_DC.kicad_sch
Hardware/KiCad/PCB_D_CONVERTER_CORE_MANIFEST_V1_9.json
Tools/erc/pcb_d_converter_core_erc.py
```

Result:

```text
exact controller symbol instances: 1
controller pins including EP: 41
exact LFPAK56 MOSFET symbols: 4
exact WSK2512 Kelvin symbols: 2
schematic symbol instances: 50
split gate-resistor positions: 8
hierarchical interfaces: 11
CALC_TBD markers: 38
non-empty footprint assignments: 0
S-expression balance: PASS
UUID uniqueness: PASS
exact symbol Gate: PASS
```

Direct hardware boundaries now explicit:

```text
U_UVLO
U_EN_GATE
U_FAULT
U_ISENSE1
U_ISENSE2
U_ISUM
NT_AGND_PGND
```

Exact devices/values remain `CALC_TBD` where not yet calculated or measured.

## 5. Открыто после native ERC и exact discrete pin-map Gates

| ID | Открытый параметр | Статус |
|---|---|---|
| Q-P5-009C | Exact hot-plug/turn-off transient waveforms and measured clamp | OPEN_MEASUREMENT |
| Q-P5-009D | Exact external UVLO supervisor/comparator and tolerance network | OPEN_CALC_COMPONENT |
| Q-P5-009E | Exact fail-safe hardware EN_RUN gate topology and polarity | OPEN_CALC_COMPONENT |
| Q-P5-010 | Final allowed 5V_SYS_BUS droop/overshoot from actual devices | OPEN_OWNER_DEVICE_DATA |
| Q-P5-011 | Actual single and simultaneous external load profiles | OPEN_OWNER_DEVICE_DATA |
| Q-P5-012B | Compare final 300/400/500/600-кГц efficiency/EMI result | OPEN_CALC_TEST |
| Q-P5-012C | Measured RT frequency over voltage and temperature | OPEN_TEST |
| Q-P5-013B | Exact CS filter, propagation delay and hiccup behaviour | OPEN_CALC_TEST |
| Q-P5-013C | Bench OCP onset, phase sharing and no-nuisance 20-А correlation | OPEN_TEST |
| Q-P5-014D | Exact MLCC DC-bias effective capacitance | OPEN_DATASHEET_CALC |
| Q-P5-014E | Eight exact split gate resistors, bootstrap and snubber values | OPEN_CALC_TEST |
| Q-P5-014F | PWR263S-35-R100FE pulse graph and hot-plug application verification | OPEN_DATASHEET_TEST |
| Q-P5-015 | Sealed-volume thermal result at +60 °C | OPEN_THERMAL_TEST |
| Q-P5-016B | Native Bode measurement over VIN/load/cap tolerance | OPEN_TEST |
| Q-P5-017B | Bode/load-step bench correlation | OPEN_TEST |
| Q-P5-018B | Exact MOSFET switching and inductor core losses | OPEN_CALC_TEST |
| Q-P5-019D | Owner KiCad 10 open/save, hierarchy-context, visual and ERC review | OPEN_OWNER_KICAD |
| Q-P5-019E | Exact diagnostic monitor/aggregate devices and ranges | OPEN_CALC_COMPONENT |
| Q-P5-019F | Exact AGND/PGND copper, EP and via implementation | OPEN_LAYOUT |

## 6. UVLO and hardware enable result

Required window:

```text
rising 8,8…9,0 В
falling 8,2…8,5 В
```

A passive divider remains rejected. The symbol-core now contains explicit placeholders:

```text
U_UVLO = external supervisor, CALC_TBD
U_EN_GATE = fail-safe hardware gate, CALC_TBD

EN_RUN = 5V_SYS_EN
AND UVLO_OK
AND NOT SAFE_OFF
AND NOT HARD_OFF
```

Both EN pins receive `EN_RUN`. Local MCU/CAN-FD and SERVICE_OVERRIDE cannot bypass the hardware path.

## 7. Gate-drive result

Separate controller outputs require separate tuning positions:

```text
HO1/HOL1 → R_GH1_ON/R_GH1_OFF
LO1/LOL1 → R_GL1_ON/R_GL1_OFF
HO2/HOL2 → R_GH2_ON/R_GH2_OFF
LO2/LOL2 → R_GL2_ON/R_GL2_OFF
```

All eight values remain open pending waveform/EMI/loss correlation.

## 8. Native ERC Gate result

Workflow:

```text
.github/workflows/pcb-d-kicad-erc.yml
```

Successful run:

```text
run id: 30028613180
head SHA: 0d741e46f0f817cbfa508ccfa0c92260a660f59b
job: exact-symbol-and-native-erc
KiCad: 10.0.4
conclusion: success
```

Successful steps:

```text
semantic manifest ERC
exact pin-map ERC
exact symbol Gate
reproducible generator byte parity
official KiCad 10 install
native kicad-cli sch erc capture
exact violation classification
JSON evidence artifact upload
```

Raw native result:

```text
exit code: 5
violations: 14
```

Exact classification:

```text
11 expected standalone root hierarchical boundaries
3 expected parent-driven U_EN_GATE control inputs
0 internal converter-core violations
0 residual geometry faults
```

The 14 raw violations are not hidden or described as zero-error ERC. They are exact standalone leaf-sheet boundary effects and are accepted only by the fixed allowlist. Any additional violation fails CI.

Evidence:

```text
artifact: pcb-d-kicad-native-erc
artifact id: 8575877765
digest: sha256:fb661e874e79b833e84e2a8c4dd4f13694ef71c5df1ba2c4c80002703d5edf26
```

Result:

```text
Q-P5-019C: CLOSED_NATIVE_ERC_INTERNAL_TOPOLOGY
owner KiCad 10 open/save and hierarchy-context review: OPEN
PR #45: remains draft
```

## 9. Thermal Gate

Still required:

```text
sealed enclosure
+60 °C internal design point
no hull thermal contact
15 А continuous until steady state
```

Measurements:

- four MOSFET temperatures;
- L1/L2 temperatures;
- controller temperature;
- input/output capacitor temperatures;
- phase sharing;
- output regulation;
- fault telemetry;
- conformal-coating impact.

## 10. Mechanical Gate

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

## 11. Next Gate

```text
owner KiCad 10 open/save and hierarchy-context visual/ERC review
→ verify that parent-sheet integration resolves the 14 expected standalone boundaries
→ exact UVLO/EN hardware calculation
→ exact CS/gate/bootstrap calculation
→ SW ringing and snubber decision
→ Bode/load-step/OCP bench correlation
→ footprint/3D candidate review
→ prototype BOM Gate
→ electrical/transient/load/thermal test plan
```
