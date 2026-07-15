# KiCad schematic skeleton manifest

Дата фиксации: 2026-07-14  
Дата обновления `00_SYSTEM_TOP`: 2026-07-15  
Дата обновления `02_INTERBOARD_POWER_AND_CONTROL`: 2026-07-15  
Дата обновления `01_EXTERNAL_BATTERIES_AND_HARNESS`: 2026-07-15  
Дата обновления PCB top-листов `10/20/30/40/50`: 2026-07-15  
Дата добавления `10_BFE_POWER` detailed hierarchy: 2026-07-15  
Дата Level B прохода по `11/12/17`: 2026-07-15  
Дата Level B прохода по `13/14/15/16/18/19`: 2026-07-15  
Дата symbol-skeleton прохода по `11/12/17`: 2026-07-15  
Дата symbol-skeleton прохода по `13/14/15/16/18/19`: 2026-07-15

Статус:

```text
ARCHITECTURE LEVEL B/C0 — PCB-A BFE_POWER net groups refined; text-only symbol skeleton zones added for all BFE sub-sheets
```

## 1. Назначение

Этот пакет создаёт стартовый KiCad workspace для принятой многоплатной `SCHEMATIC ARCHITECTURE`. Он фиксирует структуру, имена групп и зоны будущей детализации, но не выбирает компоненты, footprints или part numbers.

Источник истины:

```text
Docs/SCHEMATIC_ARCHITECTURE.md
Docs/INTERBOARD_INTERFACES.md
Docs/NET_NAMING_RULES.md
```

## 2. Созданные KiCad-файлы

```text
Hardware/KiCad/PlataVM.kicad_pro
Hardware/KiCad/PlataVM.kicad_sch
Hardware/KiCad/00_SYSTEM_TOP.kicad_sch
Hardware/KiCad/01_EXTERNAL_BATTERIES_AND_HARNESS.kicad_sch
Hardware/KiCad/02_INTERBOARD_POWER_AND_CONTROL.kicad_sch
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
Hardware/KiCad/20_CTRL_RESERVE_TOP.kicad_sch
Hardware/KiCad/30_POWER_12V_TOP.kicad_sch
Hardware/KiCad/40_POWER_5V_TOP.kicad_sch
Hardware/KiCad/50_LIGHT_POWER_TOP.kicad_sch
```

## 3. Что уже зафиксировано

1. Корневой проект `PlataVM.kicad_pro`.
2. Корневой лист `PlataVM.kicad_sch`.
3. Системные листы `00`, `01`, `02`.
4. Top-листы PCB-A/PCB-B/PCB-C/PCB-D/PCB-E.
5. Detailed hierarchy пакет для `10_BFE_POWER_TOP`.
6. Level B net groups для всех подлистов PCB-A `11…19`.
7. Text-only symbol skeleton zones для всех подлистов PCB-A `11…19`.
8. Безопасные границы: батареи, PACK_BUS, HARD_OFF, EXT_KILL, земли и межплатные интерфейсы.

## 4. `10_BFE_POWER` detailed hierarchy

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

Назначение подлистов:

```text
11/12 — BFE-side boundaries of AKB_1 / AKB_2 through SN-176A-12.
13/14 — MAIN_SW1 / MAIN_SW2 functional power paths.
15    — controlled deck-side balancing boundary.
16    — PACK_BUS creation, fanout and discharge.
17    — REMOTE_OFF_NC / EXT_KILL_NC final hold-loop actuators.
18    — voltage/current/status measurement groups.
19    — connector grouping and service testpoints.
```

## 5. Level B/C0 text-only symbol skeleton zones

### 11/12 — BAT input boundaries

```text
J_BAT1_SN176_TBD
J_BAT2_SN176_TBD
```

Pin grouping:

```text
Pins 1..5  -> BATx_SN176_POS
Pins 6..10 -> BATx_SN176_NEG
Pin 11     -> BATx_HOLD_RETURN_IN
Pin 12     -> BATx_SN176_RESERVE
```

### 17 — REMOTE_OFF / EXT_KILL hold-loop final actuators

```text
K17A_BAT1_EXT_KILL_NC_TBD
K17B_BAT1_REMOTE_OFF_NC_TBD
K17C_BAT2_EXT_KILL_NC_TBD
K17D_BAT2_REMOTE_OFF_NC_TBD
```

Functional chain:

```text
BAT1_HOLD_RETURN_IN -> BAT1_EXT_KILL_NC_TBD -> BAT1_REMOTE_OFF_NC_TBD -> BAT1_SN176_NEG_RETURN
BAT2_HOLD_RETURN_IN -> BAT2_EXT_KILL_NC_TBD -> BAT2_REMOTE_OFF_NC_TBD -> BAT2_SN176_NEG_RETURN
```

### 16 — PACK_BUS / discharge

```text
NODE16_PACK_BUS_JOIN_TBD
J16_PACK_BUS_FANOUT_TBD
SW16_PACK_BUS_DISCHARGE_TBD
```

Net groups:

```text
BFE1_SW_OUT
BFE2_SW_OUT
PACK_BUS_NODE
PACK_BUS_TO_CRIT
PACK_BUS_TO_P12
PACK_BUS_TO_P5
PACK_BUS_TO_LIGHT
PACK_BUS_DISCHARGE_EN
DIAG_PACK_BUS_V
DIAG_PACK_BUS_DISCH_STATUS
```

### 13/14 — MAIN paths

```text
SENSE13_MAIN1_TBD
MAIN_SW1_TBD
SAFE_OFF13_TBD
SENSE14_MAIN2_TBD
MAIN_SW2_TBD
SAFE_OFF14_TBD
```

### 18 — measurements aggregation

```text
AFE18_BAT_INPUTS_TBD
AFE18_MAIN_PATHS_TBD
AFE18_SYSTEM_STATUS_TBD
```

### 15 — deck balance

```text
BAL15_PATH_TBD
BAL15_SWITCHES_TBD
BAL15_DIAG_TBD
```

### 19 — connector/testpoint groups

```text
J19_PACK_BUS_FANOUT_TBD
J19_CTRL_DIAG_TBD
TP19_SERVICE_TBD
```

## 6. Что пока не делается

1. Не выбирается `K_BATx`.
2. Не выбираются `MAIN_SWx`.
3. Не выбираются датчики тока.
4. Не выбираются DC/DC, LED-драйверы, MCU и eFuse/high-side switches.
5. Не создаются реальные KiCad library symbols.
6. Не создаются footprints.
7. Не выполняется PCB layout.
8. Не объединяются автоматически `POWER_GND`, `SIGNAL_GND`, `ISO_GND` и `CHASSIS`.
9. Не назначаются физические межплатные разъёмы.
10. Не фиксируется окончательный pin-count.
11. Не выбираются номиналы `F_BATx`, `F_CTRLx`, R_BAL, suppression и PACK_BUS discharge.
12. Не выбирается технология `REMOTE_OFF_NC / EXT_KILL_NC`.
13. Не выбираются topology/current sensor/ADC frontend/thermal solutions.
14. Не создаётся BOM.

## 7. Проверка пользователем

После checkout ветки открыть:

```text
Hardware/KiCad/PlataVM.kicad_pro
```

Минимальная проверка:

```text
10_BFE_POWER_TOP
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

Проверить:

1. листы открываются без ошибки парсинга;
2. текстовые группы читаются;
3. hierarchical labels видны;
4. KiCad не удаляет labels при сохранении;
5. `.kicad_prl` не попадает в Git changes.

## 8. Следующий инженерный этап

Следующий шаг после проверки:

```text
Resolve cross-sheet interface consistency for PCB-A BFE_POWER, then decide whether to create real generic KiCad placeholder symbols or move to PCB-B_CTRL_RESERVE hierarchy.
```
