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
Дата добавления `20_CTRL_RESERVE` detailed hierarchy: 2026-07-15

Статус:

```text
ARCHITECTURE LEVEL A/B — PCB-B CTRL_RESERVE detailed hierarchy added;
PCB-A BFE_POWER interfaces remain PASS WITH CONTROLLED PLACEHOLDERS
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
Hardware/KiCad/21_EMG_INPUT_CHARGE_ORING.kicad_sch
Hardware/KiCad/22_5V_CRIT_3V3_CRIT.kicad_sch
Hardware/KiCad/23_MCU_CORE.kicad_sch
Hardware/KiCad/24_WATCHDOG_SUPERVISOR.kicad_sch
Hardware/KiCad/25_RS485_ISOLATED.kicad_sch
Hardware/KiCad/26_EXT_KILL_INPUT_LOGIC.kicad_sch
Hardware/KiCad/27_CONTROL_IO.kicad_sch
Hardware/KiCad/28_SERVICE_DEBUG.kicad_sch
Hardware/KiCad/29_CTRL_CONNECTORS_TESTPOINTS.kicad_sch
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
9. Detailed hierarchy пакет уровня Architecture A/B для `20_CTRL_RESERVE_TOP` и подлистов `21…29`.
10. Безопасные границы: батареи, PACK_BUS, HARD_OFF, EXT_KILL, critical/reserve domain, земли и межплатные интерфейсы.

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

## 6. `20_CTRL_RESERVE` detailed hierarchy

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

Назначение подлистов:

```text
21 — PACK_BUS critical input, reserve/EMG source selection, charge/ORing and KEEP_ALIVE boundary.
22 — 5V_CRIT / 3V3_CRIT critical-domain rail generation and monitored power state.
23 — MCU normal-control, logging and logical interface boundary.
24 — watchdog, power supervisor, fault manager, reset and safe-state containment.
25 — external isolated RS-485 half-duplex boundary.
26 — external EXT_KILL input, latch and independent hardware fanout to PCB-A.
27 — commands and diagnostics between PCB-B and PCB-A/C/D/E.
28 — SWD, service UART, boot/config and authorized service-reset boundary.
29 — logical connector classes and controlled low-energy testpoints.
```

Зафиксированные ограничения PCB-B:

```text
PACK_BUS is created on PCB-A; no K_MAIN is introduced.
Only the limited PACK_BUS_CRIT_IN branch enters PCB-B.
High-current CH / 5V_SYS / LED currents do not pass through PCB-B.
EXT_KILL_HW_CHAIN does not depend on MCU firmware or external RS-485.
REMOTE_OFF and EXT_KILL retain priority over LOCAL_START.
BMS or critical-power recovery must not automatically energize K_BAT1/K_BAT2.
POWER_GND, SIGNAL_GND, ISO_GND and CHASSIS remain separate until an explicit decision.
```

Не определено на этом этапе:

```text
MCU part number and pin allocation
charger / ORing / critical DC/DC topology
watchdog / supervisor / fault-manager components
RS-485 transceiver / isolator / isolated supply
parallel vs muxed vs serialized interboard diagnostics
physical connectors, pin count and pinout
footprints, BOM and PCB layout
```

## 7. Controlled placeholders

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
EXT_KILL_RETURN_TBD
CHASSIS_RS485_SHIELD_TBD
BOOT_CONFIG_TBD
CTRL_TP_LOW_ENERGY
CTRL_TP_SAFETY_OBSERVE_ONLY
```

Причина: это локальные symbol-skeleton точки или намеренно не назначенные/service placeholders, а не финальные межлистовые электрические интерфейсы.

## 8. Что пока не делается

1. Не выбирается `K_BATx`.
2. Не добавляется `K_MAIN`.
3. Не выбираются `MAIN_SWx`.
4. Не выбираются датчики тока.
5. Не выбираются DC/DC, charger/ORing, LED-драйверы, MCU и eFuse/high-side switches.
6. Не выбираются RS-485 transceiver, isolator, watchdog, supervisor и fault-manager components.
7. Не создаются реальные KiCad library symbols.
8. Не создаются footprints.
9. Не выполняется PCB layout.
10. Не объединяются автоматически `POWER_GND`, `SIGNAL_GND`, `ISO_GND` и `CHASSIS`.
11. Не назначаются физические межплатные или внешние разъёмы.
12. Не фиксируется окончательный pin-count.
13. Не выбираются номиналы `F_BATx`, `F_CTRLx`, R_BAL, suppression и PACK_BUS discharge.
14. Не выбирается технология `REMOTE_OFF_NC / EXT_KILL_NC`.
15. Не выбираются topology/current sensor/ADC frontend/thermal solutions.
16. Не создаётся BOM.
17. Не возвращается `.kicad_prl`.

## 9. Проверка пользователем

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
20_CTRL_RESERVE_TOP
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

Проверить:

1. листы открываются без ошибки парсинга;
2. текстовые группы читаются;
3. hierarchical labels видны;
4. KiCad не удаляет labels при сохранении;
5. `.kicad_prl` не попадает в Git changes;
6. EXT_KILL не зависит от MCU/RS-485 по описанию листов;
7. ни один подлист PCB-B не проводит высокие токи внешних нагрузок.

## 10. Следующий инженерный этап

Рекомендуемый следующий шаг:

```text
Run PCB-B_CTRL_RESERVE interface consistency check
```

Проверить необходимо:

```text
20/21/22/23/24/25/26/27/28/29
against:
02_INTERBOARD_POWER_AND_CONTROL
13_MAIN_PATH_1
14_MAIN_PATH_2
15_DECK_BALANCE
16_PACK_BUS_AND_DISCHARGE
17_REMOTE_OFF_AND_EXT_KILL
18_BATTERY_MEASUREMENTS
19_BFE_CONNECTORS_TESTPOINTS
```

После согласования интерфейсных имён отдельным решением можно переходить к следующему text-only symbol-skeleton или topology pass. Выбор компонентов, footprints, BOM и layout в этот этап не входит.
