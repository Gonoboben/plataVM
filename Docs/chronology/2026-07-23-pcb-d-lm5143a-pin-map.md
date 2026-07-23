# 2026-07-23 — PCB-D LM5143A-Q1 exact RHA-40 pin-map Gate

## Исходное состояние

```text
repository: Gonoboben/plataVM
base main: c513dbb3c9da57b8b5a26e755accc94e893e3ef3
working branch: agent/pcb-d-lm5143design-calc-v1-9
PR: #45 draft
preceding Gate: LM5143DESIGN-CALC calculation PASS
```

## Цель этапа

Закрыть exact physical pin mapping выбранного prototype controller `LM5143QRHARQ1` до создания реального KiCad symbol и native ERC.

Особое внимание требовалось к выводам 31…40, поскольку LM5143A-Q1 RHA-40 нельзя подменять pinout другого корпуса или более раннего семейства.

## Результат

Зафиксирован exact RHA-40 mapping:

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

Полный mapping 1…40 + exposed pad сохранён в machine-readable record.

Single-output interleaved contract:

```text
MODE -> VDDA
FB2 -> AGND
FB1 -> AGND for fixed 5 V
COMP1 <-> COMP2
SS1 <-> SS2
DEMB -> VDDA for FPWM
EN1 = EN2 = EN_RUN
PG1 = primary PGOOD
PG2 = isolated testpad only
```

## Добавлено

```text
Docs/PCB_D_LM5143A_Q1_PIN_MAPPING_GATE_V1_9.md
Hardware/KiCad/LM5143A_Q1_RHA40_PINMAP_V1_9.json
Hardware/KiCad/LM5143A_Q1_RHA40_PINMAP_ERC_RESULT_V1_9.txt
Tools/erc/pcb_d_lm5143_pinmap_erc.py
```

## Обновлено

```text
Hardware/KiCad/41_5V_DC_DC.kicad_sch
Hardware/KiCad/PCB_D_CONVERTER_CORE_MANIFEST_V1_9.json
Hardware/KiCad/PCB_D_CONVERTER_CORE_ERC_RESULT_V1_9.txt
Tools/erc/pcb_d_converter_core_erc.py
Docs/V1_9_DOCUMENT_INDEX.md
Docs/PCB_D_OPEN_GATES_V1_9.md
```

## Проверки

```text
physical pins: 40
exposed pad: 1
pin-number/name uniqueness: PASS
single-output interleaved ties: PASS
VCC pins 15/16 common-net rule: PASS
PG1/PG2 role separation: PASS
EN1/EN2 hardware EN_RUN contract: PASS
converter-core semantic ERC: PASS
```

## Ограничения

Не выполнены и не заявлены:

```text
actual KiCad symbol instantiation
owner KiCad 10.0 open/save
native KiCad ERC
production footprint freeze
production BOM freeze
copper/layout freeze
```

PR остаётся draft до native KiCad verification.

## Архитектурная непрерывность

- `K_MAIN` не добавлен;
- high-current path остаётся локальным на PCB-D и не проходит через PCB-B;
- `5V_SYS_BUS` не объединён с `5V_CRIT/3V3_CRIT`;
- SAFE/HARD_OFF остаются direct hardware inputs;
- local MCU/CAN-FD не являются единственным shutdown path;
- thermal contact с корпусом не добавлен;
- production BOM, footprint и layout не заморожены.

## Следующий Gate

```text
exact KiCad symbol from verified pin map
→ instantiate controller and discrete converter-core symbols
→ owner KiCad 10.0 open/save
→ native ERC
→ exact UVLO/CS/gate/bootstrap/snubber calculation
```
