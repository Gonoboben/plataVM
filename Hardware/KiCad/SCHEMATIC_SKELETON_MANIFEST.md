# KiCad schematic skeleton manifest

Дата фиксации: 2026-07-14  
Дата обновления `00_SYSTEM_TOP`: 2026-07-15  
Дата обновления `01_EXTERNAL_BATTERIES_AND_HARNESS`: 2026-07-15  
Дата обновления `02_INTERBOARD_POWER_AND_CONTROL`: 2026-07-15  
Дата обновления PCB top-листов `10/20/30/40/50`: 2026-07-15  
Дата добавления `10_BFE_POWER` detailed hierarchy: 2026-07-15  
Дата проверки согласованности PCB-A BFE interfaces: 2026-07-15  
Дата добавления `20_CTRL_RESERVE` detailed hierarchy: 2026-07-15  
Дата проверки согласованности PCB-B CTRL_RESERVE interfaces: 2026-07-15

Статус:

```text
ARCHITECTURE LEVEL A/B
PCB-A BFE_POWER interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
PCB-B CTRL_RESERVE interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
```

## 1. Назначение

Этот manifest фиксирует хронологию и текущее состояние стартового KiCad workspace принятой многоплатной `SCHEMATIC ARCHITECTURE`.

На текущем уровне фиксируются:

1. границы плат;
2. detailed hierarchy;
3. точные логические имена межплатных интерфейсов;
4. направления управления и диагностики;
5. безопасные состояния;
6. независимые аппаратные аварийные пути;
7. controlled placeholders для ещё не принятых электрических и механических решений.

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
7. Две батарейные ветви остаются симметричными, если отдельный ADR не утверждает иное.

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

Назначение:

```text
11/12 — BFE-side boundaries of AKB_1 / AKB_2 through SN-176A-12.
13/14 — MAIN_SW1 / MAIN_SW2 functional power paths.
15    — controlled deck-side balancing boundary.
16    — PACK_BUS creation, fanout and discharge.
17    — REMOTE_OFF_NC / EXT_KILL_NC final hold-loop actuators.
18    — voltage/current/status measurement aggregation.
19    — connector grouping and service testpoints.
```

## 5. Проверка согласованности PCB-A

Отчёт:

```text
Hardware/KiCad/BFE_INTERFACE_CONSISTENCY.md
```

Результат:

```text
PASS WITH CONTROLLED PLACEHOLDERS
```

Исправления первого прохода:

```text
BAT1_SN176_NEG_RETURN -> BAT1_SN176_NEG
BAT2_SN176_NEG_RETURN -> BAT2_SN176_NEG
BALANCE_TAP_BAT1 added on 11_BATTERY_INPUT_1
BALANCE_TAP_BAT2 added on 12_BATTERY_INPUT_2
BAT1_PRESENT_STATUS / BAT2_PRESENT_STATUS aggregated on 18_BATTERY_MEASUREMENTS
DIAG_BALANCE_I / DIAG_BALANCE_TEMP aggregated on 18_BATTERY_MEASUREMENTS
```

Принятые hold-loop paths:

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

Назначение:

```text
21 — PACK_BUS critical input, EMG source, charge/ORing and KEEP_ALIVE boundary.
22 — 5V_CRIT / 3V3_CRIT critical-domain rail generation.
23 — MCU normal-control, logging and logical interface boundary.
24 — watchdog, supervisor, fault manager, reset and safe-state containment.
25 — external isolated RS-485 half-duplex boundary.
26 — external EXT_KILL input, latch and independent hardware fanout.
27 — control/diagnostics between PCB-B and PCB-A/C/D/E.
28 — SWD, service UART, boot/config and authorized EXT_KILL reset boundary.
29 — logical connector classes and controlled low-energy testpoints.
```

## 7. Проверка согласованности PCB-B

Отчёт:

```text
Hardware/KiCad/CTRL_RESERVE_INTERFACE_CONSISTENCY.md
```

Результат:

```text
PASS WITH CONTROLLED PLACEHOLDERS
```

Исправлены PCB-B → PCB-A names:

```text
CTRL_MAIN_SW1_EN          -> BAT1_MAIN_SW_EN
CTRL_MAIN_SW2_EN          -> BAT2_MAIN_SW_EN
BALANCE_SW1_EN            -> BAT1_BALANCE_SW_EN
BALANCE_SW2_EN            -> BAT2_BALANCE_SW_EN
BAT1_REMOTE_OFF_OPEN_CMD  -> BAT1_HOLD_LOOP_OPEN_CMD
BAT2_REMOTE_OFF_OPEN_CMD  -> BAT2_HOLD_LOOP_OPEN_CMD
CTRL_BFE_FROM_CTRL        -> CTRL_B_TO_A
DIAG_BFE_TO_CTRL          -> DIAG_A_TO_B
```

Каноническая аппаратная цепь:

```text
EXT_KILL_HW_CHAIN
```

Четыре конечных действия:

```text
BAT1_HOLD_LOOP_OPEN_HW
BAT2_HOLD_LOOP_OPEN_HW
BAT1_MAIN_SW_OFF_HW
BAT2_MAIN_SW_OFF_HW
```

Канонические PCB-A diagnostic outputs:

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
```

Закрытые internal PCB-B boundaries:

```text
KEEP_ALIVE_SOURCE
EMG_CHARGE_STATUS
EMG_FAULT_N
MCU_RUN_STATUS
CONTROLLED_SHUTDOWN_REQ
FAULT_LATCHED_STATUS
WATCHDOG_FAULT_N
RS485_LINK_STATUS
RS485_LOGIC
EXT_KILL_RESET_AUTH
HARD_OFF_EVENT
```

## 8. Канонические групповые интерфейсы

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

## 9. Controlled placeholders

PCB-A local placeholders:

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
MAIN_SW1_SAFE_OFF
MAIN_SW2_SAFE_OFF
PACK_BUS_NODE
BALANCE_PATH_TBD
BALANCE_ARM
BALANCE_ABORT
BFE_TP_LOW_ENERGY
BFE_TP_POWER_GUARDED
BFE_FAULT_INJECTION_TP
```

PCB-B local/external placeholders:

```text
RESERVE_BRANCH
EMG_BUS
EXT_KILL_RETURN_TBD
EMG_4S2P_EXTERNAL
CHASSIS_RS485_SHIELD_TBD
BOOT_CONFIG_TBD
CTRL_TP_LOW_ENERGY
CTRL_TP_SAFETY_OBSERVE_ONLY
```

Эти labels не являются альтернативными утверждёнными межплатными net names. Они обозначают локальные functional zones, pre-ORing nodes, service/test boundaries или ещё не определённые физические возвраты и упаковку интерфейса.

## 10. Что пока не делается

1. Не выбирается `K_BATx`.
2. Не добавляется `K_MAIN`.
3. Не выбираются `MAIN_SWx`.
4. Не выбираются датчики тока и ADC frontend.
5. Не выбираются charger/ORing, DC/DC, LDO и critical power components.
6. Не выбираются MCU, clock, memory или pin allocation.
7. Не выбираются watchdog, supervisor, latch и fault-manager components.
8. Не выбираются RS-485 transceiver, isolator, isolated supply, termination или TVS.
9. Не выбираются eFuse/high-side switches, LED-драйверы или channel protection.
10. Не создаются реальные KiCad library symbols.
11. Не создаются footprints.
12. Не выполняется PCB layout.
13. Не создаётся BOM.
14. Не назначаются физические межплатные или внешние разъёмы.
15. Не фиксируется окончательный pin-count.
16. Не выбираются wire gauge, cable, busbar или passive backplane mechanics.
17. Не объединяются `POWER_GND`, `SIGNAL_GND`, `ISO_GND`, `CHASSIS`.
18. Не возвращается `.kicad_prl`.

## 11. Проверка пользователем в KiCad

После checkout ветки открыть:

```text
Hardware/KiCad/PlataVM.kicad_pro
```

Минимальная проверка текущего пакета:

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
7. четыре конечных EXT_KILL actions присутствуют;
8. ни один подлист PCB-B не проводит высокие токи внешних нагрузок;
9. `POWER_GND`, `SIGNAL_GND`, `ISO_GND`, `CHASSIS` остаются раздельными.

## 12. Следующий инженерный этап

```text
Start PCB-C_POWER_12V detailed hierarchy
```

Канонические подлисты следующего этапа:

```text
31_POWER_12V_INPUT_PROTECTION
32_POWER_12V_CHANNEL_TEMPLATE
33_POWER_12V_CH1_CH7
34_POWER_12V_CH8_CH14
35_POWER_12V_DIAGNOSTICS
36_POWER_12V_CONNECTORS
```

На следующем этапе по-прежнему запрещены преждевременный выбор eFuse/high-side switches, connectors, footprints, BOM и PCB layout.
