# PCB-B CTRL_RESERVE interface consistency

Дата проверки: 2026-07-15  
Область проверки:

```text
Docs/INTERBOARD_INTERFACES.md
Hardware/KiCad/02_INTERBOARD_POWER_AND_CONTROL.kicad_sch
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
```

## 1. Результат

```text
PCB-B CTRL_RESERVE interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
```

Проверка выполнена на уровне Architecture A/B. Она фиксирует логические имена, направления, безопасные состояния и аппаратные аварийные пути, но не выбирает компоненты, электрические уровни, физические разъёмы или упаковку сигналов.

## 2. Исправленные несовпадения PCB-B → PCB-A

| Старое имя на PCB-A | Каноническое имя | Получатель |
|---|---|---|
| `CTRL_MAIN_SW1_EN` | `BAT1_MAIN_SW_EN` | `13_MAIN_PATH_1` |
| `CTRL_MAIN_SW2_EN` | `BAT2_MAIN_SW_EN` | `14_MAIN_PATH_2` |
| `BALANCE_SW1_EN` | `BAT1_BALANCE_SW_EN` | `15_DECK_BALANCE` |
| `BALANCE_SW2_EN` | `BAT2_BALANCE_SW_EN` | `15_DECK_BALANCE` |
| `BAT1_REMOTE_OFF_OPEN_CMD` | `BAT1_HOLD_LOOP_OPEN_CMD` | `17_REMOTE_OFF_AND_EXT_KILL` |
| `BAT2_REMOTE_OFF_OPEN_CMD` | `BAT2_HOLD_LOOP_OPEN_CMD` | `17_REMOTE_OFF_AND_EXT_KILL` |
| `CTRL_BFE_FROM_CTRL` | `CTRL_B_TO_A` | `19_BFE_CONNECTORS_TESTPOINTS` |

`PACK_BUS_DISCHARGE_EN` уже совпадал и сохранён.

## 3. Аппаратный EXT_KILL

Каноническое агрегированное имя:

```text
EXT_KILL_HW_CHAIN
```

Старое документальное имя `EXT_KILL_HW` устранено из `Docs/INTERBOARD_INTERFACES.md`.

Четыре конечных действия теперь имеют совпадающие источники и получатели:

```text
26_EXT_KILL_INPUT_LOGIC: BAT1_HOLD_LOOP_OPEN_HW  -> 17_REMOTE_OFF_AND_EXT_KILL
26_EXT_KILL_INPUT_LOGIC: BAT2_HOLD_LOOP_OPEN_HW  -> 17_REMOTE_OFF_AND_EXT_KILL
26_EXT_KILL_INPUT_LOGIC: BAT1_MAIN_SW_OFF_HW     -> 13_MAIN_PATH_1
26_EXT_KILL_INPUT_LOGIC: BAT2_MAIN_SW_OFF_HW     -> 14_MAIN_PATH_2
```

Дополнительно:

```text
EXT_KILL_LATCHED      -> watchdog/supervisor and service observation
EXT_KILL_EVENT_STATUS -> MCU logging only
HARD_OFF_EVENT        -> EMG / KEEP_ALIVE behavior
EXT_KILL_RESET_AUTH   -> authorized manual reset request
```

MCU, RS-485 и service/debug не могут блокировать или задерживать аппаратное отключение.

## 4. Диагностика PCB-A → PCB-B

На `18_BATTERY_MEASUREMENTS` добавлены канонические внешние порты:

```text
BAT1_PRESENT
BAT2_PRESENT
BAT1_VSENSE
BAT2_VSENSE
BAT1_ISENSE
BAT2_ISENSE
PACK_BUS_VSENSE
BFE1_FAULT_N
BFE2_FAULT_N
BALANCE1_FAULT_N
BALANCE2_FAULT_N
PACK_BUS_DISCHARGE_FAULT_N
DIAG_A_TO_B
```

Внутренние source/skeleton names сохранены:

```text
BAT1_PRESENT_STATUS
BAT2_PRESENT_STATUS
DIAG_MAIN1_*
DIAG_MAIN2_*
DIAG_PACK_BUS_*
DIAG_BALANCE_*
DIAG_HOLD_LOOP_STATUS
```

Они не являются альтернативными межплатными net names: это локальные входы будущего измерительного/диагностического frontend.

На `27_CONTROL_IO` добавлены совпадающие входы и `BFE_FAULT_SUMMARY_N` для fault manager.

## 5. Внутренние интерфейсы PCB-B

Закрыты следующие пары:

```text
21 KEEP_ALIVE_SOURCE       -> 22 KEEP_ALIVE_SOURCE
21 EMG_CHARGE_STATUS       -> 23 EMG_CHARGE_STATUS
21 EMG_FAULT_N             -> 24 EMG_FAULT_N
23 MCU_RUN_STATUS          -> 24 MCU_RUN_STATUS
24 CONTROLLED_SHUTDOWN_REQ -> 23 CONTROLLED_SHUTDOWN_REQ
24 FAULT_LATCHED_STATUS    -> 23 FAULT_LATCHED_STATUS
24 WATCHDOG_FAULT_N        -> 23 WATCHDOG_FAULT_N
25 RS485_LINK_STATUS       -> 23 RS485_LINK_STATUS
23 RS485_LOGIC             <-> 25 RS485_LOGIC
28 EXT_KILL_RESET_AUTH     -> 26 EXT_KILL_RESET_AUTH
```

`22_5V_CRIT_3V3_CRIT` теперь получает объединённый `KEEP_ALIVE_SOURCE`; source selection и charge/ORing остаются ответственностью листа 21.

## 6. Групповые межплатные имена

Согласованы с `02_INTERBOARD_POWER_AND_CONTROL`:

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
EXT_KILL_HW_CHAIN
```

Внешние PCB-B boundaries:

```text
RS485_ISOLATED
EXT_KILL_IN_RAW
EMG_4S2P_EXTERNAL
SERVICE_DEBUG
```

## 7. Controlled placeholders

Следующие точки могут оставаться single-ended или функционально сгруппированными до следующего этапа:

```text
RESERVE_BRANCH
EMG_BUS
MAIN_SW1_SAFE_OFF
MAIN_SW2_SAFE_OFF
BALANCE_ARM
BALANCE_ABORT
EXT_KILL_RETURN_TBD
EMG_4S2P_EXTERNAL
CHASSIS_RS485_SHIELD_TBD
BOOT_CONFIG_TBD
CTRL_TP_LOW_ENERGY
CTRL_TP_SAFETY_OBSERVE_ONLY
```

Причины:

1. `RESERVE_BRANCH` и `EMG_BUS` — внутренние pre-ORing функциональные точки листа 21; межлистовой источник после ORing называется `KEEP_ALIVE_SOURCE`.
2. `MAIN_SWx_SAFE_OFF`, `BALANCE_ARM`, `BALANCE_ABORT` — локальные symbol-skeleton interlock points, а не утверждённые межплатные порты.
3. `EXT_KILL_RETURN_TBD` требует решения по физической контактной схеме, line supervision и fail-safe disconnect behavior.
4. EMG, RS-485 shield/chassis, boot/config и testpoint packaging требуют отдельного электрического и механического решения.

## 8. Что не изменено

- `K_MAIN` не добавлен.
- `PACK_BUS` остаётся созданным на PCB-A.
- High-current load power не проходит через PCB-B.
- `K_BATx` остаются monostable normally-open contactors в корпусах АКБ.
- Восстановление BMS или critical power не включает `K_BATx` автоматически.
- `REMOTE_OFF` и `EXT_KILL` имеют приоритет над `LOCAL_START`.
- `POWER_GND`, `SIGNAL_GND`, `ISO_GND`, `CHASSIS` не объединены.
- Реальные KiCad library symbols не добавлены.
- Компоненты, footprints, BOM и PCB layout не выбирались.
- `.kicad_prl` не возвращён.

## 9. Следующий этап

```text
Start PCB-C_POWER_12V detailed hierarchy
```

После создания листов `31…36` необходимо выполнить отдельную проверку точных control/diagnostic names PCB-B ↔ PCB-C.
