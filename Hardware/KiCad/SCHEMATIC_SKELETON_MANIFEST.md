# KiCad schematic skeleton manifest

Дата фиксации: 2026-07-14  
Дата текущего обновления: 2026-07-15

## 1. Текущий статус

```text
ARCHITECTURE LEVEL A/B
PCB-A BFE_POWER interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
PCB-B CTRL_RESERVE interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
PCB-C POWER_12V interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
PCB-D POWER_5V interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
PCB-E LIGHT_POWER interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
```

Все пять PCB-модулей имеют detailed hierarchy Architecture A/B. Компоненты, реальные KiCad library symbols, footprints, физические разъёмы, BOM и PCB layout не выбирались.

Источники истины:

```text
Docs/SCHEMATIC_ARCHITECTURE.md
Docs/INTERBOARD_INTERFACES.md
Docs/NET_NAMING_RULES.md
Hardware/KiCad/BFE_INTERFACE_CONSISTENCY.md
Hardware/KiCad/CTRL_RESERVE_INTERFACE_CONSISTENCY.md
Hardware/KiCad/POWER_12V_INTERFACE_CONSISTENCY.md
Hardware/KiCad/POWER_5V_INTERFACE_CONSISTENCY.md
Hardware/KiCad/LIGHT_POWER_INTERFACE_CONSISTENCY.md
```

## 2. Принятая архитектура

```text
PCB-A_BFE_POWER
PCB-B_CTRL_RESERVE
PCB-C_POWER_12V
PCB-D_POWER_5V
PCB-E_LIGHT_POWER
INTERCONNECT passive only
```

Неизменяемые правила текущего baseline:

1. `PACK_BUS` создаётся на PCB-A.
2. `K_MAIN` не добавляется.
3. High-current load power не проходит через PCB-B.
4. `INTERCONNECT` не содержит обязательной активной электроники.
5. `EXT_KILL` действует без зависимости от MCU firmware и external RS-485.
6. `POWER_GND`, `SIGNAL_GND`, `ISO_GND`, `CHASSIS` не объединяются автоматически.
7. `5V_SYS_BUS` отделён от `5V_CRIT/3V3_CRIT` и EMG.
8. PCB-E остаётся одной функциональной платой; зоны 1..3 и 4..6 являются локальным разбиением.

## 3. Detailed hierarchy

### PCB-A_BFE_POWER

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

### PCB-B_CTRL_RESERVE

```text
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

### PCB-C_POWER_12V

```text
30_POWER_12V_TOP
31_POWER_12V_INPUT_PROTECTION
32_POWER_12V_CHANNEL_TEMPLATE
33_POWER_12V_CH1_CH7
34_POWER_12V_CH8_CH14
35_POWER_12V_DIAGNOSTICS
36_POWER_12V_CONNECTORS
```

### PCB-D_POWER_5V

```text
40_POWER_5V_TOP
41_5V_DC_DC
42_5V_OUTPUT_TEMPLATE
43_5V_OUT1_OUT5
44_5V_OUT6_OUT10
45_5V_DIAGNOSTICS
46_5V_CONNECTORS
```

### PCB-E_LIGHT_POWER

```text
50_LIGHT_POWER_TOP
51_LIGHT_INPUT_PROTECTION
52_LED_DRIVER_TEMPLATE
53_LED_DRIVER_1_3
54_LED_DRIVER_4_6
55_LIGHT_DIAGNOSTICS
56_LIGHT_CONNECTORS
```

## 4. Канонические межплатные группы

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

## 5. PCB-A / PCB-B safety contract

```text
EXT_KILL_HW_CHAIN
BAT1_HOLD_LOOP_OPEN_HW
BAT2_HOLD_LOOP_OPEN_HW
BAT1_MAIN_SW_OFF_HW
BAT2_MAIN_SW_OFF_HW
```

`REMOTE_OFF` и `EXT_KILL` имеют приоритет над `LOCAL_START`. Восстановление BMS или critical power не запускает `K_BAT1/K_BAT2` автоматически.

## 6. PCB-C control and diagnostics

```text
P12_CH_EN[1..11]
P12_GROUP_SAFE_OFF
P12_GROUP_HARD_OFF
P12_CH_FAULT_N[1..14]
P12_CH_ISENSE[1..14]
P12_INPUT_VSENSE
P12_BOARD_TEMP
P12_BOARD_FAULT_N
```

CH12..CH14 — Always-On monitored during normal RUN, но выключаются при SAFE/HARD_OFF.

## 7. PCB-D control and diagnostics

```text
5V_SYS_EN
P5_OUT_EN[1..7]
P5_GROUP_SAFE_OFF
P5_GROUP_HARD_OFF
P5_OUT_FAULT_N[1..10]
P5_OUT_ISENSE[1..10]
5V_SYS_VSENSE
5V_SYS_TOTAL_ISENSE
P5_BOARD_TEMP
P5_BOARD_FAULT_N
```

OUT8..OUT10 — Always-On monitored during normal RUN, но выключаются при SAFE/HARD_OFF. `5V_SYS_BUS` имеет preliminary budget 15 A continuous / 20 A short peak.

## 8. PCB-E control and diagnostics

```text
LIGHT_BRANCH_EN
LED_PWM[1..6]
LIGHT_GROUP_HARD_OFF
LED_FAULT_N[1..6]
LED_ISENSE[1..6]
LIGHT_INPUT_VSENSE
LIGHT_BOARD_TEMP
LIGHT_BOARD_FAULT_N
```

Default safe state — все шесть LED outputs OFF. `LIGHT_GROUP_HARD_OFF` имеет приоритет над branch enable и PWM.

## 9. Controlled placeholders

### PCB-A

```text
BAT1_SN176_RESERVE
BAT2_SN176_RESERVE
BAT1_EXT_KILL_NC_TBD
BAT1_REMOTE_OFF_NC_TBD
BAT2_EXT_KILL_NC_TBD
BAT2_REMOTE_OFF_NC_TBD
MAIN_SW1_SAFE_OFF
MAIN_SW2_SAFE_OFF
BALANCE_ARM
BALANCE_ABORT
```

### PCB-B

```text
RESERVE_BRANCH
EMG_BUS
EXT_KILL_RETURN_TBD
EMG_4S2P_EXTERNAL
CHASSIS_RS485_SHIELD_TBD
BOOT_CONFIG_TBD
```

### PCB-C

```text
P12_INPUT_FAULT_N
P12_INPUT_PRESENT
P12_CH_STATUS_TBD
P12_AON_POLICY_CH12_14
P12_BOARD_TEMP_SENSE_TBD
SIGNAL_GND_REFERENCE_TBD
P12_RETURN_GROUP_TBD
P12_OUTPUT_CONNECTOR_CLASS_TBD
```

### PCB-D

```text
P5_DC_DC_FAULT_N
P5_OUT_STATUS_TBD
P5_AON_POLICY_OUT8_10
P5_BOARD_TEMP_SENSE_TBD
SIGNAL_GND_REFERENCE_TBD
P5_RETURN_GROUP_TBD
P5_OUTPUT_CONNECTOR_CLASS_TBD
```

### PCB-E

```text
LIGHT_INPUT_FAULT_N
LIGHT_INPUT_PRESENT
LED_CH_STATUS_TBD
LIGHT_ZONE1_TEMP_SENSE_TBD
LIGHT_ZONE2_TEMP_SENSE_TBD
SIGNAL_GND_REFERENCE_TBD
LIGHT_RETURN_GROUP_TBD
LIGHT_OUTPUT_CONNECTOR_CLASS_TBD
```

## 10. Данные, необходимые до component selection

1. фактический `PACK_BUS` operating/transient range;
2. load profiles, inrush, duty cycle и simultaneous-use matrix для CH1..CH14 и 5V_OUT1..10;
3. LED Vf/current tolerances, PWM frequency/level/dimming range и thermal conditions;
4. EMG energy/hold-up/charge requirements;
5. EXT_KILL physical contact topology, active level, line supervision и disconnect behavior;
6. ground/chassis/shield bonding policy;
7. internal interboard transport choice;
8. physical connector/harness/mechanical/environmental requirements.

Эти данные не требовались для Architecture A/B, но блокируют component selection и реальные схемотехнические topology calculations.

## 11. Запрещённые действия текущего этапа

1. Не выбирать MCU, DC/DC, LED drivers, eFuse/high-side switches, sensors, watchdog, isolators или transceivers.
2. Не добавлять `K_MAIN`.
3. Не создавать реальные KiCad library symbols и footprints.
4. Не создавать BOM или PCB layout.
5. Не выбирать physical connectors, pinout, cables и wire gauge.
6. Не объединять ground domains.
7. Не возвращать `.kicad_prl`.

## 12. Проверка пользователем в KiCad

Открыть `Hardware/KiCad/PlataVM.kicad_pro` и проверить листы `10…56`:

1. отсутствие parsing errors;
2. видимость hierarchical labels;
3. сохранность bus labels `[1..N]` после save;
4. независимость EXT_KILL от MCU/RS-485;
5. подчинение Always-On outputs SAFE/HARD_OFF;
6. отделение `5V_SYS_BUS` от critical domain;
7. симметричность LED zones;
8. отсутствие `.kicad_prl` в Git changes.

## 13. Следующий этап

```text
Run system-wide interface consistency audit
```
