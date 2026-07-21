# Индекс документов PlataVM V1.9

## Нормативная база

```text
PROJECT_MASTER.md
ARCHITECTURE_BASELINE.md
SYSTEM_POWER_BUDGET_POLICY.md
SERVICE_OVERRIDE_POLICY.md
OPEN_QUESTIONS.md
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
PCB_D_DESIGN_BASIS_CONSISTENCY_V1_9.md
PCB_D_INPUT_PROTECTION_CONSISTENCY_V1_9.md
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
preferred prototype controller family: LM5143A-Q1
compatible 65-V alternate: LM5143-Q1
42-V alternate after measured proof: LM25143-Q1
fSW baseline: 400 кГц per phase
L baseline: 3,3 мкГн per phase
prototype sensing: 5 мОм Kelvin shunt per phase
MOSFET class: 60 В minimum
TVS prototype class: SMCJ18A
RC damping start: 330 мкФ + 0,10 Ом
estimated losses at 75 Вт: 3,4…5,4 Вт
PCB-D area/height fit: PRELIMINARY PASS
input transient boundary: PRELIMINARY DEFINED
final components/footprints: OPEN
measured transient clamp: OPEN
design-tool calculation: OPEN
loop stability: OPEN
sealed-volume thermal test: OPEN
```
