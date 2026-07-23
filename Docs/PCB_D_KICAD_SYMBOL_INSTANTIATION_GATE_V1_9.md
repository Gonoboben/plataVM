# PCB-D POWER_5V — exact KiCad symbol-instantiation Gate V1.9

Дата: 2026-07-23  
Статус: `EXACT SYMBOLS INSTANTIATED — NATIVE KICAD ERC OPEN`

## 1. Назначение

Преобразовать предварительный текстовый converter-core лист в реальный KiCad-10 S-expression с инстанцированными symbols и электрическими pin types, не переходя к production footprint/BOM/layout freeze.

Gate выполняется после:

```text
LM5143DESIGN-CALC: PASS
exact LM5143A-Q1 RHA-40 pin mapping: PASS
```

## 2. Созданные KiCad-артефакты

```text
Hardware/KiCad/41_5V_DC_DC.kicad_sch
Hardware/KiCad/plataVM_symbols.kicad_sym
Tools/kicad/generate_pcb_d_converter_core.py
Tools/erc/pcb_d_kicad_symbol_gate.py
Hardware/KiCad/PCB_D_KICAD_SYMBOL_GATE_RESULT_V1_9.txt
```

Формат:

```text
KiCad 10 native S-expression
schematic generator: plataVM_symbol_gate
symbol library generator: plataVM_symbol_gate
```

Third-party generator не маскируется под `eeschema`.

## 3. Exact controller symbol

Инстанцирован один symbol:

```text
Reference: U_DCDC
Value: LM5143QRHARQ1
Family: LM5143A-Q1
Package class: RHA VQFN-40
Physical pins: 40
Exposed pad: 1
```

Configuration-specific electrical typing сохраняет single-output interleaved mode:

```text
COMP1 = output
COMP2 = passive/high-impedance secondary EA node
SS1 = input
SS2 = passive/common soft-start node
PG1/PG2 = open-collector outputs
HO/HOL/LO/LOL = separate outputs
VCC pin 15 = power output
VCC pin 16 = passive common VCC pin
EP = passive AGND-side connection
```

Это предотвращает ложные ERC-конфликты между объединёнными `COMP1/COMP2` и `SS1/SS2`, не изменяя физический pin map.

## 4. Power-stage symbols

Инстанцированы:

```text
4 × BUK9Y6R0-60E,115 MOSFET symbols
2 × XAL1010-332MED inductors
2 × WSK25125L000FEA Kelvin shunts
2 × bootstrap diodes
2 × bootstrap capacitors
input/output equivalent capacitor groups
controller bias/decoupling positions
RT, SS, RES and compensation components
```

Ни одному symbol не назначен production footprint.

## 5. Split gate-drive correction

LM5143A-Q1 имеет отдельные outputs включения и выключения:

```text
HO1 / HOL1
LO1 / LOL1
HO2 / HOL2
LO2 / LOL2
```

Поэтому прежнее упрощение до четырсох общих независимых tuning positions:

```text
R_GH1_ON   R_GH1_OFF
R_GL1_ON   R_GL1_OFF
R_GH2_ON   R_GH2_OFF
R_GL2_ON   R_GL2_OFF
```

Все номиналы остаются `CALC_TBD` до gate-waveform, EMI и switching-loss measurement.

## 6. Current-sense implementation boundary

Для каждой фазы сохранена differential high-frequency filter position:

```text
PHASEx_L_OUT → R_CSx → CSx_FILTERED
CSx_FILTERED → C_CSx → 5V_SYS_BUS
VOUTx → 5V_SYS_BUS via Kelvin-sense routing class
```

Значения `R_CSx/C_CSx` остаются `CALC_TBD`. Фильтр не должен скрывать short-circuit onset или создавать недопустимую межфазную задержку.

## 7. Direct hardware safety boundary

Ранее `EN_RUN` существовал только как логический contract. Теперь на схеме явно инстанцированы placeholder blocks:

```text
U_UVLO    = UVLO_SUPERVISOR_TBD
U_EN_GATE = HW_ENABLE_GATE_TBD
```

Контракт:

```text
UVLO_OK = external PACK_BUS supervisor result

EN_RUN =
5V_SYS_EN
AND UVLO_OK
AND NOT P5_GROUP_SAFE_OFF
AND NOT P5_GROUP_HARD_OFF
```

`U_EN_GATE` питается от `PACK_BUS_P5_IN` boundary, а не от local MCU/CAN-FD. Exact supervisor, gate/transistor topology, resistor network and fail-safe polarity остаются `CALC_TBD`.

## 8. Diagnostic boundaries

Инстанцированы явные, но не замороженные diagnostic placeholders:

```text
U_FAULT    → P5_DC_DC_FAULT_N
U_ISENSE1  → P5_PHASE1_ISENSE
U_ISENSE2  → P5_PHASE2_ISENSE
U_ISUM     → 5V_SYS_TOTAL_ISENSE
```

`PG1 pin 24` остастся primary PGOOD. `PG2 pin 7` остаётся isolated testpoint и не включся в fault aggregate.

Diagnostic amplifier/logic parts, ranges, filters and accuracy remain `CALC_TBD`.

## 9. Grounding boundary

Exposed pad помещён на AGND-side net. Добавлен явный controlled join:

```text
NT_AGND_PGND
value = AGND_PGND_STAR_LAYOUT_TBD
```

Он фиксирует архитектурное требование контролируемой точки AGND/PGND, но не утверждает:

```text
land pattern
thermal-via count
copper geometry
star-point coordinates
hull thermal path
```

Hull thermal contact по-прежнему запрещсн.

## 10. Hierarchical interfaces

Сохранены и электрически привязаны 11 интерфейсов:

```text
PACK_BUS_P5_IN
POWER_GND
5V_SYS_EN
P5_GROUP_SAFE_OFF
P5_GROUP_HARD_OFF
5V_SYS_BUS
5V_SYS_VSENSE
5V_SYS_TOTAL_ISENSE
P5_DC_DC_FAULT_N
P5_PHASE1_ISENSE
P5_PHASE2_ISENSE
```

Floating hierarchical labels на symbol-core листе устранены.

## 11. Deterministic validation

Выполнено:

```text
controller pins including EP: 41
schematic symbol instances: 50
split gate-resistor positions: 8
hierarchical interfaces: 11
CALC_TBD markers: 38
S-expression balance: PASS
UUID uniqueness: PASS
exact controller pin/type contract: PASS
required converter-core references: PASS
forbidden architecture nets absent: PASS
non-empty footprint assignments: 0
RESULT: PASS
```

## 12. Native KiCad ERC CI

Добавлен workflow:

```text
.github/workflows/pcb-d-kicad-erc.yml
```

Он выполняет:

```text
semantic manifest ERC
exact pin-map ERC
exact symbol-instantiation Gate
reproducible generator diff
official KiCad 10 installation
kicad-cli sch erc --severity-error --exit-code-violations
ERC JSON artifact upload
```

Native ERC нельзя считать закрытым до фактического успешного GitHub Actions run и последующего owner KiCad 10 open/save review.

## 13. Freeze boundary

Закрыто:

```text
calculation Gate
exact pin mapping
KiCad symbol definition
KiCad symbol instantiation
symbol-core deterministic validation
```

Открыто:

```text
native KiCad ERC
owner KiCad 10 open/save
exact UVLO supervisor and hardware gate
exact CS/gate/bootstrap/snubber values
footprints and 3D
copper/layout
prototype BOM Gate
bench and thermal qualification
```

Production schematic/BOM/footprint freeze не выдан.

## 14. Следующий Gate

```text
GitHub Actions native KiCad ERC
→ исправить только подтверждённые parser/ERC errors
→ owner KiCad 10 open/save
→ exact UVLO and enable-gate calculation
→ exact CS/gate/bootstrap calculation
→ SW-node ringing measurement and snubber decision
```
