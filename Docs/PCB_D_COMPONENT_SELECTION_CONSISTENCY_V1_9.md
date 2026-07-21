# PCB-D POWER_5V — consistency review prototype component selection V1.9

Дата: 2026-07-21  
Статус: `CONSISTENCY PASS — SCHEMATIC AND THERMAL GATES OPEN`

## 1. Проверенные документы

```text
ARCHITECTURE_BASELINE.md
SYSTEM_POWER_BUDGET_POLICY.md
PCB_D_TWO_PHASE_BUCK_DESIGN_BASIS_V1_9.md
PCB_D_CONTROLLER_TRANSIENT_AMENDMENT_V1_9.md
PCB_D_INPUT_PROTECTION_TRANSIENT_BOUNDARY_V1_9.md
PCB_D_INPUT_DAMPING_CALC_V1_9.md
PCB_D_PROTOTYPE_PARAMETER_SET_V1_9.md
PCB_D_PROTOTYPE_COMPONENT_CANDIDATES_V1_9.md
PCB_D_OCP_TOLERANCE_CALC_V1_9.md
PCB_D_LOAD_TRANSIENT_TARGETS_V1_9.md
PCB_D_PROTOTYPE_LOSS_BOUNDARY_V1_9.md
PCB_D_COMPONENT_BOUNDING_BOXES_V1_9.md
```

## 2. Electrical boundary

| Boundary | Required | Candidate result |
|---|---:|---|
| Controller VIN class | 65 В | LM5143QRHARQ1, PASS |
| MOSFET VDS | ≥60 В | BUK9Y6R0-60E, PASS |
| Inductance | 3,3 мкГн ±20 % | XAL1010-332MED, PASS |
| Inductor DCR | ≤8 мОм target | 4,1 мОм max at 25 °C, PASS |
| Inductor current | ≥15 А Isat class | 27,4 А 30-% drop at 25 °C, PASS with hot curve open |
| Shunt | 5 мОм ±1 %, ≥1 Вт, Kelvin | WSK25125L000FEA, PASS |
| TVS | 18-В standoff class | SMCJ18A, PASS |
| Input capacitor | ≥35 В | 50-В MLCC class + 35-В hybrid, PASS |
| Output polymer | ≥10 В | 10SVPC330M, PASS prototype |

## 3. OCP compatibility

Manual tolerance sweep:

```text
minimum peak threshold per phase: 13,069 А
maximum 20-А-mode phase peak: 11,808 А
minimum margin: about 10,7 %
```

Result:

```text
20 А /1 с legal mode: preliminary no-nuisance OCP PASS
true converter OCP: remains above system short mode
```

OCP is not used as the precise system current limiter.

## 4. Input capacitor correction

The current candidate set does not restore the rejected 25-В input capacitor class.

```text
MLCC: 50 В
C_DAMP: 35 В
TVS clamp class: 29,2 В
```

Voltage hierarchy remains consistent.

## 5. Effective input capacitance

Eight 1210 MLCC positions are introduced conceptually:

```text
6 populated
2 DNP
```

Nominal quantity alone does not close the requirement. Gate remains:

```text
Ceff total at 16 В, temperature, tolerance and aging ≥100 мкФ
```

No false claim of `8 ×22 =176 мкФ effective` is permitted.

## 6. Damping resistor status

PWR263S-35 family proves availability of a high-pulse D²PAK resistor class down to 0,02 Ом. However exact 0,10-Ом /1-% order code and pulse curve must be verified before BOM freeze.

Therefore:

```text
R_DAMP family: ACCEPTED
R_DAMP exact orderable: OPEN
```

This is intentionally not hidden as a completed exact part selection.

## 7. Mechanical fit

Existing PCB-D envelope:

```text
125 ×94 мм
component height ≤23 мм
power-stage placeholder 70 ×38 ×13 мм
```

Selected tall parts:

```text
XAL1010: about 10-mm class
EEH-ZK1V331P: 10,2 мм
10SVPC330M: 6,9 мм
```

Result:

```text
height fit: PRELIMINARY PASS
real footprint/STEP fit: OPEN
```

R_DAMP and eight input-MLCC positions may increase input-protection area. Board area must be rechecked during schematic placement before footprint freeze.

## 8. Thermal consistency

Candidate loss boundary:

```text
2,9…6,0 Вт at 75 Вт output
η estimate 92,6…96,3 %
```

This overlaps the earlier feasibility range and does not close the sealed-volume thermal Gate.

No hull contact or external heatsink was introduced.

## 9. Safety architecture

Not changed:

- no `K_MAIN`;
- high current does not pass through PCB-B;
- `5V_SYS_BUS` remains separated from `5V_CRIT/3V3_CRIT`;
- `P5_GROUP_SAFE_OFF` and `P5_GROUP_HARD_OFF` remain direct hardware lines;
- CAN-FD and local MCU do not constitute the only disable path;
- `SERVICE_OVERRIDE` cannot bypass hardware OCP or hard-off;
- PCB-D is not powered by EMG;
- `P5_BOARD_FAULT_N` remains required.

## 10. Manufacturability

Prototype choices improve manufacturability by:

- using one MOSFET type in all four positions;
- using two identical inductors;
- using identical 5-мОм shunts;
- including DNP capacitor tuning positions;
- using wettable-flank controller package;
- retaining standard power packages.

Open manufacturing risks:

- exact RHA thermal-pad and via process;
- LFPAK56 land pattern verification;
- XAL1010 solder profile and voiding;
- hybrid/polymer capacitor vibration support;
- D²PAK R_DAMP area and copper heat spreading;
- conformal-coating keepouts around capacitor vents/test points.

## 11. Official calculator limitation

`LM5143DESIGN-CALC` was identified and its supported device list verified, but the tool was not executed in this environment.

Therefore no claim is made for:

- tool-generated compensation;
- tool-generated efficiency;
- tool-generated BOM;
- tool-generated OCP values;
- tool-generated stability margins.

Manual calculations remain independent preliminary inputs.

## 12. Result

```text
exact controller orderable: PASS
prototype MOSFET: PASS
prototype inductor: PASS
prototype shunt: PASS
prototype TVS: PASS
prototype damping capacitor: PASS
output capacitor starting set: PASS
input MLCC footprint strategy: PASS
OCP manual tolerance: PASS
architecture continuity: PASS
R_DAMP exact code/pulse curve: OPEN
calculator output: OPEN
prototype schematic: OPEN
3D/footprint fit: OPEN
sealed thermal qualification: OPEN
production BOM: NOT FROZEN
```