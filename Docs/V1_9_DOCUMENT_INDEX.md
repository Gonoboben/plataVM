# Индекс документов PlataVM V1.9

## Нормативная база

```text
PROJECT_MASTER.md
ARCHITECTURE_BASELINE.md
SYSTEM_POWER_BUDGET_POLICY.md
SERVICE_OVERRIDE_POLICY.md
OPEN_QUESTIONS.md
PCB_D_OPEN_GATES_V1_9.md
```

## Packaging и интерфейсы

```text
MECHANICAL_ENVELOPE_V1_8.md
PCB_PACKAGING_BOUNDARY_V1_9.md
PCB_MODULE_AREA_BUDGET_V1_9.md
PHYSICAL_INTERFACE_COUNT_V1_9.md
PACKAGING_P1_REVIEW_CHECKLIST.md
PRE_KICAD_OUTLINE_GATE_V1_9.md
COMPONENT_HEIGHT_3D_GATE_V1_9.md
COMPONENT_HEIGHT_PLACEHOLDER_MAP_V1_9.md
PACKAGING_P1_3D_CLEARANCE_REVIEW_V1_9.md
INTERFACE_TOPOLOGY_DECISION_V1_9.md
PCB_D_COMPONENT_BOUNDING_BOXES_V1_9.md
```

## Расчёты и проверки

```text
BRANCH_CURRENT_PRECALC_V1_9.md
BASELINE_CONSISTENCY_V1_9.md
KICAD_VERSION_RECORD_V1_9.md
PCB_D_TWO_PHASE_BUCK_DESIGN_BASIS_V1_9.md
PCB_D_CONTROLLER_TRANSIENT_AMENDMENT_V1_9.md
PCB_D_CONTROLLER_CANDIDATE_MATRIX_V1_9.md
PCB_D_INPUT_PROTECTION_TRANSIENT_BOUNDARY_V1_9.md
PCB_D_INPUT_DAMPING_CALC_V1_9.md
PCB_D_PROTOTYPE_PARAMETER_SET_V1_9.md
PCB_D_PROTOTYPE_COMPONENT_CANDIDATES_V1_9.md
PCB_D_COMPONENT_SOURCE_RECORD_V1_9.md
PCB_D_OCP_TOLERANCE_CALC_V1_9.md
PCB_D_LOAD_TRANSIENT_TARGETS_V1_9.md
PCB_D_PROTOTYPE_LOSS_BOUNDARY_V1_9.md
PCB_D_DESIGN_BASIS_CONSISTENCY_V1_9.md
PCB_D_INPUT_PROTECTION_CONSISTENCY_V1_9.md
PCB_D_COMPONENT_SELECTION_CONSISTENCY_V1_9.md
../Hardware/KiCad/Boards/PRELIMINARY_OUTLINE_VALIDATION_V1_9.md
../Hardware/Mechanical/PACKAGING_P1_PLACEHOLDER.scad
../Hardware/Mechanical/PCB_D_POWER_STAGE_PLACEHOLDER.scad
```

## Трассируемость решения

```text
OWNER_DECISION_V1_9.md
V1_9_RELEASE_NOTES.md
adr/ADR-2026-07-21-service-override-v1-9.md
chronology/2026-07-21-service-override-v1-9.md
chronology/2026-07-21-kicad-10-board-verification.md
chronology/2026-07-21-component-height-placeholders-v1-9.md
chronology/2026-07-21-pcb-d-two-phase-design-basis.md
chronology/2026-07-21-pcb-d-input-protection.md
chronology/2026-07-21-pcb-d-prototype-components.md
```

## KiCad toolchain

```text
KiCad 10.0
pcbnew generator_version 10.0
board format 20260206
*.kicad_prl excluded from version control
```

## Текущий packaging status

```text
preliminary board outlines: PASS
functional/height placeholder maps: PASS
OpenSCAD assembly placeholder: CREATED
A↔B preliminary topology: 16 CTRL + 16 DIAG
CAN-FD preliminary order: PCB-B → PCB-D → PCB-E → PCB-C
PACKAGING-P1: CONDITIONAL PASS
actual component 3D fit: OPEN
connector selection: OPEN
thermal qualification: OPEN
```

## Текущий PCB-D status

```text
2-phase synchronous buck architecture: PRELIMINARY PASS
exact prototype controller: LM5143QRHARQ1
prototype MOSFET: BUK9Y6R0-60E
prototype inductors: XAL1010-332MED
prototype shunts: WSK25125L000FEA
prototype TVS: Littelfuse SMCJ18A
input capacitor class: 50-В X7R MLCC strategy; Ceff verification open
RC damping: EEH-ZK1V331P +0,10-Ом PWR263S-35 family
output capacitor starting set: 2×10SVPC330M + X7R tuning positions
fSW baseline: 400 кГц per phase
L baseline: 3,3 мкГн per phase
manual OCP tolerance: PRELIMINARY PASS; minimum margin 10,7 %
load-transient engineering targets: DEFINED
candidate loss boundary at 75 Вт: 2,9…6,0 Вт
PCB-D area/height fit: PRELIMINARY PASS
input transient boundary: PRELIMINARY DEFINED
R_DAMP exact orderable/pulse curve: OPEN
MLCC DC-bias effective capacitance: OPEN
LM5143DESIGN-CALC: OPEN
prototype converter-core schematic: NEXT
footprints/3D: OPEN
loop stability: OPEN
sealed-volume thermal test: OPEN
production BOM: NOT FROZEN
```