# KiCad schematic skeleton manifest

Дата фиксации: 2026-07-14  
Дата обновления `00_SYSTEM_TOP`: 2026-07-15  
Дата обновления `02_INTERBOARD_POWER_AND_CONTROL`: 2026-07-15  
Дата обновления `01_EXTERNAL_BATTERIES_AND_HARNESS`: 2026-07-15  
Дата обновления PCB top-листов `10/20/30/40/50`: 2026-07-15  
Дата добавления `10_BFE_POWER` detailed hierarchy: 2026-07-15  
Дата Level B прохода по `11/12/17`: 2026-07-15

Статус:

```text
ARCHITECTURE LEVEL B — BFE input boundaries and hold-loop logic refined
```

## 1. Назначение

Этот пакет создаёт стартовый KiCad workspace для принятой многоплатной `SCHEMATIC ARCHITECTURE`. Он не выбирает компоненты, footprints или part numbers.

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
6. Level B проход по критичным BFE-листам `11`, `12`, `17`.
7. Безопасные границы: батареи, PACK_BUS, HARD_OFF, EXT_KILL, земли и межплатные интерфейсы.

## 4. `10_BFE_POWER` detailed hierarchy

Подлисты PCB-A:

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

## 5. Level B уточнение `11/12/17`

В этом проходе уточнены net names и safe-state logic без выбора компонентов.

### 11_BATTERY_INPUT_1

```text
BAT1_SN176_POS
BAT1_SN176_NEG
BAT1_HOLD_RETURN_IN
BAT1_TO_MAIN_PATH
BAT1_MEAS_TAPS
BAT1_PRESENT_STATUS
```

### 12_BATTERY_INPUT_2

```text
BAT2_SN176_POS
BAT2_SN176_NEG
BAT2_HOLD_RETURN_IN
BAT2_TO_MAIN_PATH
BAT2_MEAS_TAPS
BAT2_PRESENT_STATUS
```

### 17_REMOTE_OFF_AND_EXT_KILL

```text
BAT1_HOLD_RETURN_IN
BAT1_SN176_NEG_RETURN
BAT2_HOLD_RETURN_IN
BAT2_SN176_NEG_RETURN
BAT1_REMOTE_OFF_OPEN_CMD
BAT2_REMOTE_OFF_OPEN_CMD
EXT_KILL_HW_CHAIN
DIAG_HOLD_LOOP_STATUS
```

Логика hold-loop:

```text
BAT1_HOLD_RETURN_IN -> BAT1_EXT_KILL_NC -> BAT1_REMOTE_OFF_NC -> BAT1_SN176_NEG return
BAT2_HOLD_RETURN_IN -> BAT2_EXT_KILL_NC -> BAT2_REMOTE_OFF_NC -> BAT2_SN176_NEG return
```

Правила:

```text
- BAT1/BAT2 hold loops не объединяются по силовому возврату.
- EXT_KILL может иметь общий источник команды, но не должен зависеть от MCU firmware.
- REMOTE_OFF_OPEN_CMD размыкает удерживающую цепь, а не подаёт SET/RESET.
- Восстановление BMS не вызывает автоматический рестарт K_BATx.
```

## 6. Что пока не делается

1. Не выбирается `K_BATx`.
2. Не выбираются `MAIN_SWx`.
3. Не выбираются датчики тока.
4. Не выбираются DC/DC, LED-драйверы, MCU и eFuse/high-side switches.
5. Не создаются footprints.
6. Не выполняется PCB layout.
7. Не объединяются автоматически `POWER_GND`, `SIGNAL_GND`, `ISO_GND` и `CHASSIS`.
8. Не назначаются физические межплатные разъёмы.
9. Не фиксируется окончательный pin-count.
10. Не выбираются номиналы `F_BATx`, `F_CTRLx`, R_BAL, suppression и PACK_BUS discharge.
11. Не выбирается технология `REMOTE_OFF_NC / EXT_KILL_NC`.

## 7. Проверка пользователем

После checkout ветки открыть:

```text
Hardware/KiCad/PlataVM.kicad_pro
```

Минимальная проверка:

```text
11_BATTERY_INPUT_1
12_BATTERY_INPUT_2
17_REMOTE_OFF_AND_EXT_KILL
```

Проверить:

1. листы открываются без ошибки парсинга;
2. текстовые группы читаются;
3. hierarchical labels видны;
4. KiCad не удаляет labels при сохранении;
5. `.kicad_prl` не попадает в Git changes.

## 8. Следующий инженерный этап

После проверки этого пакета следующий шаг:

```text
BFE Level B continuation
```

Порядок:

```text
16_PACK_BUS_AND_DISCHARGE
→ 13_MAIN_PATH_1 / 14_MAIN_PATH_2
→ 18_BATTERY_MEASUREMENTS
→ 15_DECK_BALANCE
→ 19_BFE_CONNECTORS_TESTPOINTS
```
