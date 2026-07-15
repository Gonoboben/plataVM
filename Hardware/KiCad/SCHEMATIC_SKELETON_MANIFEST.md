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

Статус:

```text
ARCHITECTURE LEVEL B/C0 — PCB-A BFE_POWER net groups refined; first text-only symbol skeleton zones added
```

## 1. Назначение

Этот пакет создаёт стартовый KiCad workspace для принятой многоплатной `SCHEMATIC ARCHITECTURE` и постепенно переводит листы от архитектурных текстовых границ к будущим схемным символам.

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
7. Первый text-only symbol skeleton проход для `11_BATTERY_INPUT_1`, `12_BATTERY_INPUT_2`, `17_REMOTE_OFF_AND_EXT_KILL`.
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

## 5. Level B net groups

### 11/12 — BAT input boundaries

```text
BAT1_SN176_POS
BAT1_SN176_NEG
BAT1_HOLD_RETURN_IN
BAT1_SN176_RESERVE
BAT1_TO_MAIN_PATH
BAT1_MEAS_TAPS
BAT1_PRESENT_STATUS

BAT2_SN176_POS
BAT2_SN176_NEG
BAT2_HOLD_RETURN_IN
BAT2_SN176_RESERVE
BAT2_TO_MAIN_PATH
BAT2_MEAS_TAPS
BAT2_PRESENT_STATUS
```

### 17 — REMOTE_OFF / EXT_KILL hold-loop logic

```text
BAT1_HOLD_RETURN_IN -> BAT1_EXT_KILL_NC_TBD -> BAT1_REMOTE_OFF_NC_TBD -> BAT1_SN176_NEG_RETURN
BAT2_HOLD_RETURN_IN -> BAT2_EXT_KILL_NC_TBD -> BAT2_REMOTE_OFF_NC_TBD -> BAT2_SN176_NEG_RETURN
```

Rules:

```text
BAT1/BAT2 hold loops не объединяются по силовому возврату.
EXT_KILL может иметь общий источник команды, но не должен зависеть от MCU firmware.
REMOTE_OFF_OPEN_CMD размыкает удерживающую цепь, а не подаёт SET/RESET.
Восстановление BMS не вызывает автоматический рестарт K_BATx.
```

### 16 — PACK_BUS / discharge

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
BAT1_TO_MAIN_PATH
MAIN_SW1_INPUT
MAIN_SW1_OUTPUT
BFE1_SW_OUT
CTRL_MAIN_SW1_EN
MAIN_SW1_SAFE_OFF
EXT_KILL_HW_CHAIN
DIAG_MAIN1_I
DIAG_MAIN1_VIN
DIAG_MAIN1_VOUT
DIAG_MAIN1_FAULT

BAT2_TO_MAIN_PATH
MAIN_SW2_INPUT
MAIN_SW2_OUTPUT
BFE2_SW_OUT
CTRL_MAIN_SW2_EN
MAIN_SW2_SAFE_OFF
EXT_KILL_HW_CHAIN
DIAG_MAIN2_I
DIAG_MAIN2_VIN
DIAG_MAIN2_VOUT
DIAG_MAIN2_FAULT
```

### 18 — measurements aggregation

```text
BAT1_MEAS_TAPS
BAT2_MEAS_TAPS
DIAG_MAIN1_I / DIAG_MAIN1_VIN / DIAG_MAIN1_VOUT / DIAG_MAIN1_FAULT
DIAG_MAIN2_I / DIAG_MAIN2_VIN / DIAG_MAIN2_VOUT / DIAG_MAIN2_FAULT
DIAG_PACK_BUS_V
DIAG_PACK_BUS_DISCH_STATUS
DIAG_HOLD_LOOP_STATUS
DIAG_BALANCE_STATUS
DIAG_BFE_TO_CTRL
```

### 15 — deck balance

```text
BALANCE_TAP_BAT1
BALANCE_TAP_BAT2
BALANCE_PATH_TBD
BALANCE_ARM
BALANCE_SW1_EN
BALANCE_SW2_EN
BALANCE_ABORT
EXT_KILL_HW_CHAIN
DIAG_BALANCE_I
DIAG_BALANCE_TEMP
DIAG_BALANCE_STATUS
```

### 19 — connector/testpoint groups

```text
PACK_BUS_TO_CRIT
PACK_BUS_TO_P12
PACK_BUS_TO_P5
PACK_BUS_TO_LIGHT
CTRL_BFE_FROM_CTRL
DIAG_BFE_TO_CTRL
EXT_KILL_HW_CHAIN
BFE_TP_LOW_ENERGY
BFE_TP_POWER_GUARDED
BFE_FAULT_INJECTION_TP
```

## 6. Symbol skeleton pass `11/12/17`

Этот проход не добавляет реальные библиотечные символы KiCad и не создаёт BOM. Он добавляет текстовые зоны будущей установки символов и фиксирует имена будущих placeholders.

### 11_BATTERY_INPUT_1

```text
J_BAT1_SN176_TBD — future 12-pin connector placeholder.
Pins 1..5  -> BAT1_SN176_POS.
Pins 6..10 -> BAT1_SN176_NEG.
Pin 11     -> BAT1_HOLD_RETURN_IN.
Pin 12     -> BAT1_SN176_RESERVE.
LOCAL_START1 remains external to PCB-A and outside SN-176A-12.
```

### 12_BATTERY_INPUT_2

```text
J_BAT2_SN176_TBD — future 12-pin connector placeholder.
Pins 1..5  -> BAT2_SN176_POS.
Pins 6..10 -> BAT2_SN176_NEG.
Pin 11     -> BAT2_HOLD_RETURN_IN.
Pin 12     -> BAT2_SN176_RESERVE.
LOCAL_START2 remains external to PCB-A and outside SN-176A-12.
```

### 17_REMOTE_OFF_AND_EXT_KILL

```text
K17A_BAT1_EXT_KILL_NC_TBD
K17B_BAT1_REMOTE_OFF_NC_TBD
K17C_BAT2_EXT_KILL_NC_TBD
K17D_BAT2_REMOTE_OFF_NC_TBD
```

These are functional NC actuator placeholders only. The final implementation technology is still TBD.

## 7. Что пока не делается

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
12. Не добавляются реальные KiCad library symbols в BOM.

## 8. Проверка пользователем

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

## 9. Следующий инженерный этап

```text
BFE symbol skeletons continuation
```

Порядок:

```text
16_PACK_BUS_AND_DISCHARGE
→ 13_MAIN_PATH_1 / 14_MAIN_PATH_2
→ 18_BATTERY_MEASUREMENTS
→ 15_DECK_BALANCE
→ 19_BFE_CONNECTORS_TESTPOINTS
```
