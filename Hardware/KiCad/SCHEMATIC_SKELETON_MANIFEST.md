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
Дата проверки согласованности PCB-A BFE interfaces: 2026-07-15

Статус:

```text
ARCHITECTURE LEVEL B/C0 — PCB-A BFE_POWER interfaces checked: PASS WITH CONTROLLED PLACEHOLDERS
```

## 1. Назначение

Этот пакет создаёт стартовый KiCad workspace для принятой многоплатной `SCHEMATIC ARCHITECTURE`. Он фиксирует структуру, имена групп и зоны будущей детализации, но не выбирает компоненты, footprints или part numbers.

Источник истины:

```text
Docs/SCHEMATIC_ARCHITECTURE.md
Docs/INTERBOARD_INTERFACES.md
Docs/NET_NAMING_RULES.md
Hardware/KiCad/BFE_INTERFACE_CONSISTENCY.md
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
Hardware/KiCad/BFE_INTERFACE_CONSISTENCY.md
```

## 3. Что уже зафиксировано

1. Корневой проект `PlataVM.kicad_pro`.
2. Корневой лист `PlataVM.kicad_sch`.
3. Системные листы `00`, `01`, `02`.
4. Top-листы PCB-A/PCB-B/PCB-C/PCB-D/PCB-E.
5. Detailed hierarchy пакет для `10_BFE_POWER_TOP`.
6. Level B net groups для всех подлистов PCB-A `11…19`.
7. Text-only symbol skeleton zones для всех подлистов PCB-A `11…19`.
8. Проверка согласованности PCB-A BFE interfaces: `PASS WITH CONTROLLED PLACEHOLDERS`.
9. Безопасные границы: батареи, PACK_BUS, HARD_OFF, EXT_KILL, земли и межплатные интерфейсы.

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

## 5. Проверка согласованности PCB-A BFE interfaces

Отдельный отчёт:

```text
Hardware/KiCad/BFE_INTERFACE_CONSISTENCY.md
```

Результат:

```text
PASS WITH CONTROLLED PLACEHOLDERS
```

Исправлено в рамках проверки:

```text
BAT1_SN176_NEG_RETURN -> BAT1_SN176_NEG
BAT2_SN176_NEG_RETURN -> BAT2_SN176_NEG
BALANCE_TAP_BAT1 добавлен как источник на 11_BATTERY_INPUT_1
BALANCE_TAP_BAT2 добавлен как источник на 12_BATTERY_INPUT_2
BAT1_PRESENT_STATUS / BAT2_PRESENT_STATUS заведены в 18_BATTERY_MEASUREMENTS
DIAG_BALANCE_I / DIAG_BALANCE_TEMP заведены в 18_BATTERY_MEASUREMENTS
```

Принятая цепь hold-loop после проверки:

```text
BAT1_HOLD_RETURN_IN -> BAT1_EXT_KILL_NC_TBD -> BAT1_REMOTE_OFF_NC_TBD -> BAT1_SN176_NEG
BAT2_HOLD_RETURN_IN -> BAT2_EXT_KILL_NC_TBD -> BAT2_REMOTE_OFF_NC_TBD -> BAT2_SN176_NEG
```

## 6. Controlled placeholders

Следующие labels могут оставаться single-ended до появления реальных generic KiCad symbols или connector-group детализации:

```text
BAT1_SN176_RESERVE
BAT2_SN176_RESERVE
BAT1_EXT_KILL_NC_TBD
BAT1_REMOTE_OFF_NC_TBD
BAT2_EXT_KILL_NC_TBD
BAT2_REMOTE_OFF_NC_TBD
MAIN_SW1_INPUT
MAIN_SW1_OUTPUT
MAIN_SW2_INPUT
MAIN_SW2_OUTPUT
PACK_BUS_NODE
BALANCE_PATH_TBD
BFE_TP_LOW_ENERGY
BFE_TP_POWER_GUARDED
BFE_FAULT_INJECTION_TP
```

Причина: это локальные symbol-skeleton точки или намеренно не назначенные/service placeholders, а не финальные межлистовые электрические интерфейсы.

## 7. Что пока не делается

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

## 8. Проверка пользователем

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

## 9. Следующий инженерный этап

Рекомендуемый следующий шаг:

```text
Start PCB-B_CTRL_RESERVE detailed hierarchy
```

Причина: PCB-A теперь имеет стабильные имена для питания, hold-loop, PACK_BUS, диагностики, балансировки и connector/testpoint boundaries. Можно безопаснее раскладывать ответственность PCB-B по MCU, watchdog/supervisor, EMG/KEEP_ALIVE, control outputs, diagnostics inputs и isolated RS-485.
