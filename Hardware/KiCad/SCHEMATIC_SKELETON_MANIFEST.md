# KiCad schematic skeleton manifest

Дата фиксации: 2026-07-14  
Дата обновления системных и top-листов: 2026-07-15  
Дата добавления `10_BFE_POWER` detailed hierarchy: 2026-07-15  
Дата проверки согласованности PCB-A BFE interfaces: 2026-07-15  
Дата добавления `20_CTRL_RESERVE` detailed hierarchy: 2026-07-15  
Дата проверки согласованности PCB-B CTRL_RESERVE interfaces: 2026-07-15  
Дата добавления `30_POWER_12V` detailed hierarchy: 2026-07-15

Статус:

```text
ARCHITECTURE LEVEL A/B
PCB-A BFE_POWER interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
PCB-B CTRL_RESERVE interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
PCB-C POWER_12V detailed hierarchy: ADDED — INTERFACE CHECK PENDING
```

## 1. Назначение

Этот manifest фиксирует хронологию и текущее состояние KiCad workspace принятой многоплатной архитектуры PlataVM.

На текущем уровне фиксируются:

1. границы плат и функциональных листов;
2. направления энергии;
3. логические управляющие и диагностические интерфейсы;
4. безопасные состояния;
5. независимые аппаратные аварийные пути;
6. controlled placeholders для решений, требующих расчётов или дополнительных исходных данных.

На этом уровне не выбираются компоненты, footprints, физические разъёмы, BOM или PCB layout.

Источники истины:

```text
Docs/SCHEMATIC_ARCHITECTURE.md
Docs/INTERBOARD_INTERFACES.md
Docs/NET_NAMING_RULES.md
Hardware/KiCad/BFE_INTERFACE_CONSISTENCY.md
Hardware/KiCad/CTRL_RESERVE_INTERFACE_CONSISTENCY.md
```

## 2. Созданные KiCad-файлы

### Системный уровень

```text
Hardware/KiCad/PlataVM.kicad_pro
Hardware/KiCad/PlataVM.kicad_sch
Hardware/KiCad/00_SYSTEM_TOP.kicad_sch
Hardware/KiCad/01_EXTERNAL_BATTERIES_AND_HARNESS.kicad_sch
Hardware/KiCad/02_INTERBOARD_POWER_AND_CONTROL.kicad_sch
```

### PCB-A_BFE_POWER

```text
Hardware/KiCad/10_BFE_POWER_TOP.kicad_sch
Hardware/KiCad/11_BATTERY_INPUT_1.kicad_sch
Hardware/KiCad/12_BATTERY_INPUT_2.kicad_sch
Hardware/KiCad/13_MAIN_PATH_1.kicad_sch
Hardware/KiCad/14_MAIN_PATH_2.kicad_sch
Hardware/KiCad/15_DECK_BALANCE.kicad_sch
Hardware/KiCad/16_PACK_BUS_AND_DISCHARGE.kicad_sch
Hardware/KiCad/17_REMOTE_OFF_AND_EXT_KILL.kicad_sch
Hardware/KiCad/18_BATTERY_MEASUREMENTS.kicad_sch
Hardware/KiCad/19_BFE_CONNECTORS_TESTPOINTS.kicad_sch
```

### PCB-B_CTRL_RESERVE

```text
Hardware/KiCad/20_CTRL_RESERVE_TOP.kicad_sch
Hardware/KiCad/21_EMG_INPUT_CHARGE_ORING.kicad_sch
Hardware/KiCad/22_5V_CRIT_3V3_CRIT.kicad_sch
Hardware/KiCad/23_MCU_CORE.kicad_sch
Hardware/KiCad/24_WATCHDOG_SUPERVISOR.kicad_sch
Hardware/KiCad/25_RS485_ISOLATED.kicad_sch
Hardware/KiCad/26_EXT_KILL_INPUT_LOGIC.kicad_sch
Hardware/KiCad/27_CONTROL_IO.kicad_sch
Hardware/KiCad/28_SERVICE_DEBUG.kicad_sch
Hardware/KiCad/29_CTRL_CONNECTORS_TESTPOINTS.kicad_sch
```

### PCB-C_POWER_12V

```text
Hardware/KiCad/30_POWER_12V_TOP.kicad_sch
Hardware/KiCad/31_POWER_12V_INPUT_PROTECTION.kicad_sch
Hardware/KiCad/32_POWER_12V_CHANNEL_TEMPLATE.kicad_sch
Hardware/KiCad/33_POWER_12V_CH1_CH7.kicad_sch
Hardware/KiCad/34_POWER_12V_CH8_CH14.kicad_sch
Hardware/KiCad/35_POWER_12V_DIAGNOSTICS.kicad_sch
Hardware/KiCad/36_POWER_12V_CONNECTORS.kicad_sch
```

### Оставшиеся top-листы

```text
Hardware/KiCad/40_POWER_5V_TOP.kicad_sch
Hardware/KiCad/50_LIGHT_POWER_TOP.kicad_sch
```

### Отчёты

```text
Hardware/KiCad/BFE_INTERFACE_CONSISTENCY.md
Hardware/KiCad/CTRL_RESERVE_INTERFACE_CONSISTENCY.md
```

## 3. Зафиксированная многоплатная архитектура

```text
PCB-A_BFE_POWER
PCB-B_CTRL_RESERVE
PCB-C_POWER_12V
PCB-D_POWER_5V
PCB-E_LIGHT_POWER
INTERCONNECT passive only
```

Системные правила:

1. `PACK_BUS` создаётся на PCB-A.
2. `K_MAIN` не добавляется.
3. Высокие токи не проходят через PCB-B.
4. `INTERCONNECT` остаётся пассивным.
5. `EXT_KILL` не зависит от MCU firmware или внешнего RS-485.
6. `POWER_GND`, `SIGNAL_GND`, `ISO_GND`, `CHASSIS` не объединяются автоматически.
7. Две батарейные ветви остаются симметричными без отдельного ADR.

## 4. PCB-A_BFE_POWER

Detailed hierarchy:

```text
11_BATTERY_INPUT_1
12_BATTERY_INPUT_2
13_MAIN_PATH_1
14_MAIN_PATH_2
15_DECK_BALANCE
16_PACK_BUS_AND_DISCHARGE
17_REMOTE_OFF_AND_EXT_KILL
18_BATTERY_MEASUREMENTS
19_BFE_CONNECTORS_TESTPOINTS
```

Interface consistency report:

```text
Hardware/KiCad/BFE_INTERFACE_CONSISTENCY.md
PASS WITH CONTROLLED PLACEHOLDERS
```

Принятые hold-loop paths:

```text
BAT1_HOLD_RETURN_IN -> BAT1_EXT_KILL_NC_TBD -> BAT1_REMOTE_OFF_NC_TBD -> BAT1_SN176_NEG
BAT2_HOLD_RETURN_IN -> BAT2_EXT_KILL_NC_TBD -> BAT2_REMOTE_OFF_NC_TBD -> BAT2_SN176_NEG
```

## 5. PCB-B_CTRL_RESERVE

Detailed hierarchy:

```text
21_EMG_INPUT_CHARGE_ORING
22_5V_CRIT_3V3_CRIT
23_MCU_CORE
24_WATCHDOG_SUPERVISOR
25_RS485_ISOLATED
26_EXT_KILL_INPUT_LOGIC
27_CONTROL_IO
28_SERVICE_DEBUG
29_CTRL_CONNECTORS_TESTPOINTS
```

Interface consistency report:

```text
Hardware/KiCad/CTRL_RESERVE_INTERFACE_CONSISTENCY.md
PASS WITH CONTROLLED PLACEHOLDERS
```

Каноническая аппаратная цепь:

```text
EXT_KILL_HW_CHAIN
```

Конечные действия:

```text
BAT1_HOLD_LOOP_OPEN_HW
BAT2_HOLD_LOOP_OPEN_HW
BAT1_MAIN_SW_OFF_HW
BAT2_MAIN_SW_OFF_HW
```

Канонические grouped interfaces:

```text
PWR_A_TO_B_CRIT
CTRL_B_TO_A
DIAG_A_TO_B
CTRL_B_TO_C_P12
DIAG_C_TO_B_P12
CTRL_B_TO_D_P5
DIAG_D_TO_B_P5
CTRL_B_TO_E_LIGHT
DIAG_E_TO_B_LIGHT
```

## 6. PCB-C_POWER_12V detailed hierarchy

```text
31_POWER_12V_INPUT_PROTECTION
32_POWER_12V_CHANNEL_TEMPLATE
33_POWER_12V_CH1_CH7
34_POWER_12V_CH8_CH14
35_POWER_12V_DIAGNOSTICS
36_POWER_12V_CONNECTORS
```

Назначение:

```text
31 — PACK_BUS_P12_IN branch input, local protection/bulk-energy boundary and input diagnostics.
32 — reusable single-channel functional contract for control, protection, safe states and diagnostics.
33 — CH1..CH7, seven independent MCU-controlled channels.
34 — CH8..CH11 controlled and CH12..CH14 Always-On monitored.
35 — 14-channel and board-level diagnostic aggregation toward PCB-B.
36 — logical output/return, harness, connector-class and testpoint boundaries.
```

## 7. Зафиксированные требования PCB-C

### Питание

```text
Input:  PACK_BUS_P12_IN
Return: POWER_GND
Local protected node: P12_PROTECTED_BUS
```

PCB-C получает отдельную силовую ветвь непосредственно от PCB-A. Ни один ток CH1…CH14 не проходит через PCB-B.

### Каналы

```text
CH1..CH11  — normally MCU-controlled
CH12..CH14 — Always-On monitored during normal RUN
Nominal continuous requirement — 3 A per channel
```

Always-On не отменяет:

1. индивидуальную защиту;
2. токовую и fault-диагностику;
3. групповое `SAFE_OFF`;
4. групповое `HARD_OFF`;
5. отключение при board-level protection.

### Канонические управляющие функции

```text
P12_CH_EN[1..11]
P12_GROUP_SAFE_OFF
P12_GROUP_HARD_OFF
```

В текущих text-only листах массивы временно представлены сохраняющими идентичность группами:

```text
P12_CH_EN_1_7
P12_CH_EN_8_11
```

Точное представление `[1..11]` против отдельных nets будет проверено отдельным interface-consistency проходом.

### Канонические диагностические функции

```text
P12_CH_FAULT_N[1..14]
P12_CH_ISENSE[1..14]
P12_BOARD_TEMP
P12_INPUT_VSENSE
P12_BOARD_FAULT_N
DIAG_C_TO_B_P12
```

Внутренние группы:

```text
P12_CH_FAULT_N_1_7
P12_CH_FAULT_N_8_14
P12_CH_ISENSE_1_7
P12_CH_ISENSE_8_14
P12_CH_FAULT_N_1_14
P12_CH_ISENSE_1_14
```

## 8. Safe-state и fault-containment правила PCB-C

1. `P12_GROUP_HARD_OFF` имеет приоритет над нормальными enable-командами.
2. `P12_GROUP_SAFE_OFF` блокирует каналы по принятой safe-state последовательности.
3. Reset, brownout, потеря firmware и disconnected control должны оставлять CH1…CH11 в OFF.
4. CH12…CH14 выключаются при SAFE/HARD_OFF несмотря на статус Always-On.
5. Отказ одного канала не должен отключать остальные, если это не требуется upstream branch protection.
6. Диагностика не является обязательным звеном аппаратного HARD_OFF.
7. Выбор защиты должен учитывать индуктивные нагрузки, ёмкостной inrush, reverse current и repetitive fault cycling.

## 9. Controlled placeholders PCB-C

```text
P12_INPUT_FAULT_N
P12_INPUT_PRESENT
P12_CH_STATUS_TBD
P12_AON_POLICY_CH12_14
P12_BOARD_TEMP_SENSE_TBD
SIGNAL_GND_REFERENCE_TBD
P12_RETURN_GROUP_TBD
P12_OUTPUT_CONNECTOR_CLASS_TBD
P12_TP_LOW_ENERGY
P12_TP_POWER_GUARDED
```

Причины:

1. тип и координация input/channel protection не выбраны;
2. способ формирования Always-On enable не выбран;
3. датчик температуры и его размещение не определены;
4. способ передачи analog diagnostics и reference ground не определён;
5. физическая схема возвратов, проводники, разъёмы и testpoints требуют нагрузочных и механических данных.

## 10. Исходные данные, пока не требуемые для architecture hierarchy

Следующие данные не блокируют создание Level A/B, но обязательны до component selection и расчёта силовой части:

1. назначение каждого CH1…CH14;
2. длительный, пусковой и аварийный ток каждой нагрузки;
3. длительность и форма inrush;
4. индуктивность/ёмкость нагрузки и кабеля;
5. duty cycle и допустимая последовательность включения;
6. максимально допустимое падение напряжения;
7. длина, сечение и тип проводников;
8. допустимое число одновременно нагруженных каналов;
9. ambient/case temperature и тепловой путь;
10. требования к output discharge и reverse current blocking.

## 11. Что пока не делается

1. Не выбирается `K_BATx` и не добавляется `K_MAIN`.
2. Не выбираются `MAIN_SWx`.
3. Не выбираются PCB-C eFuse/high-side switches, fuses или current sensors.
4. Не выбираются TVS, reverse protection, bulk capacitors или suppression.
5. Не выбираются ADC, mux, local controller или serialized diagnostics.
6. Не выбираются физические разъёмы, pin count, pinout, кабели, wire gauge или busbar.
7. Не создаются реальные KiCad library symbols.
8. Не создаются footprints.
9. Не выполняется PCB layout.
10. Не создаётся BOM.
11. Не объединяются `POWER_GND`, `SIGNAL_GND`, `ISO_GND`, `CHASSIS`.
12. Не возвращается `.kicad_prl`.

## 12. Проверка пользователем в KiCad

После checkout ветки открыть:

```text
Hardware/KiCad/PlataVM.kicad_pro
```

Проверить листы:

```text
30_POWER_12V_TOP
31_POWER_12V_INPUT_PROTECTION
32_POWER_12V_CHANNEL_TEMPLATE
33_POWER_12V_CH1_CH7
34_POWER_12V_CH8_CH14
35_POWER_12V_DIAGNOSTICS
36_POWER_12V_CONNECTORS
```

Минимальная проверка:

1. листы открываются без ошибки парсинга;
2. текстовые зоны читаются;
3. hierarchical labels видны;
4. KiCad не удаляет labels при сохранении;
5. CH12…CH14 явно остаются subject to SAFE/HARD_OFF;
6. высокие токи не проходят через PCB-B;
7. `.kicad_prl` не появляется в Git changes.

## 13. Следующий инженерный этап

```text
Run PCB-C_POWER_12V interface consistency check
```

Проверить:

```text
30/31/32/33/34/35/36
against:
02_INTERBOARD_POWER_AND_CONTROL
27_CONTROL_IO
Docs/INTERBOARD_INTERFACES.md
```

После согласования PCB-C можно переходить к `40_POWER_5V` detailed hierarchy. Компоненты, connectors, footprints, BOM и layout в interface-consistency этап не входят.
