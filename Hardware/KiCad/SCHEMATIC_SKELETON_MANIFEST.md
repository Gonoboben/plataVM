# KiCad schematic skeleton manifest

Дата фиксации: 2026-07-14  
Дата обновления системных и top-листов: 2026-07-15  
Дата добавления `10_BFE_POWER` detailed hierarchy: 2026-07-15  
Дата проверки согласованности PCB-A BFE interfaces: 2026-07-15  
Дата добавления `20_CTRL_RESERVE` detailed hierarchy: 2026-07-15  
Дата проверки согласованности PCB-B CTRL_RESERVE interfaces: 2026-07-15  
Дата добавления `30_POWER_12V` detailed hierarchy: 2026-07-15  
Дата проверки согласованности PCB-C POWER_12V interfaces: 2026-07-15  
Дата добавления `40_POWER_5V` detailed hierarchy: 2026-07-15  
Дата проверки согласованности PCB-D POWER_5V interfaces: 2026-07-15  
Дата добавления `50_LIGHT_POWER` detailed hierarchy: 2026-07-15

Статус:

```text
ARCHITECTURE LEVEL A/B
PCB-A BFE_POWER interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
PCB-B CTRL_RESERVE interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
PCB-C POWER_12V interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
PCB-D POWER_5V interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
PCB-E LIGHT_POWER detailed hierarchy: ADDED — INTERFACE CHECK PENDING
```

## 1. Назначение

Этот manifest фиксирует хронологию и состояние KiCad workspace принятой многоплатной архитектуры PlataVM. На текущем уровне фиксируются functional boundaries, направления энергии, logical interfaces, safe states и controlled placeholders. Компоненты, footprints, physical connectors, BOM и PCB layout не выбираются.

Источники истины:

```text
Docs/SCHEMATIC_ARCHITECTURE.md
Docs/INTERBOARD_INTERFACES.md
Docs/NET_NAMING_RULES.md
Hardware/KiCad/BFE_INTERFACE_CONSISTENCY.md
Hardware/KiCad/CTRL_RESERVE_INTERFACE_CONSISTENCY.md
Hardware/KiCad/POWER_12V_INTERFACE_CONSISTENCY.md
Hardware/KiCad/POWER_5V_INTERFACE_CONSISTENCY.md
```

## 2. Многоплатная архитектура

```text
PCB-A_BFE_POWER
PCB-B_CTRL_RESERVE
PCB-C_POWER_12V
PCB-D_POWER_5V
PCB-E_LIGHT_POWER
INTERCONNECT passive only
```

Правила:

1. `PACK_BUS` создаётся на PCB-A.
2. `K_MAIN` не добавляется.
3. High-current power не проходит через PCB-B.
4. `INTERCONNECT` остаётся пассивным.
5. `EXT_KILL` не зависит от MCU firmware или external RS-485.
6. Ground domains не объединяются автоматически.
7. `5V_SYS_BUS` отделён от `5V_CRIT/3V3_CRIT` и EMG.
8. PCB-E остаётся одной функциональной платой; две зоны по три LED-канала являются локальным разбиением.

## 3. Detailed hierarchy packages

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

## 4. Interface consistency reports

```text
PCB-A: Hardware/KiCad/BFE_INTERFACE_CONSISTENCY.md
PCB-B: Hardware/KiCad/CTRL_RESERVE_INTERFACE_CONSISTENCY.md
PCB-C: Hardware/KiCad/POWER_12V_INTERFACE_CONSISTENCY.md
PCB-D: Hardware/KiCad/POWER_5V_INTERFACE_CONSISTENCY.md
```

Результат завершённых проверок:

```text
PASS WITH CONTROLLED PLACEHOLDERS
```

## 5. PCB-E_LIGHT_POWER detailed hierarchy

```text
51_LIGHT_INPUT_PROTECTION
52_LED_DRIVER_TEMPLATE
53_LED_DRIVER_1_3
54_LED_DRIVER_4_6
55_LIGHT_DIAGNOSTICS
56_LIGHT_CONNECTORS
```

Назначение:

```text
51 — PACK_BUS_LIGHT_IN branch input, protection/bulk-energy boundary and input diagnostics.
52 — reusable independent LED-driver control/regulation/protection/diagnostic contract.
53 — LED channels 1..3 in local thermal/power zone 1.
54 — LED channels 4..6 in local thermal/power zone 2.
55 — six-channel and board-level diagnostic aggregation toward PCB-B.
56 — logical LED output/return, harness, connector-class and testpoint boundaries.
```

## 6. PCB-E power and channel contract

```text
Input:        PACK_BUS_LIGHT_IN
Return:       POWER_GND
Local node:   LIGHT_PROTECTED_BUS
Load class:   six independent external LED modules
```

Каждый канал сохраняет независимые:

```text
PWM control
current regulation
fault reporting
current diagnostics
regulated LED output
```

Разбиение `1..3` и `4..6` является локальной тепловой/компоновочной зоной внутри одной PCB-E.

## 7. Канонические PCB-E interfaces

### Control

```text
CTRL_B_TO_E_LIGHT
LIGHT_BRANCH_EN
LED_PWM[1..6]
LIGHT_GROUP_HARD_OFF
```

### Diagnostics

```text
DIAG_E_TO_B_LIGHT
LED_FAULT_N[1..6]
LED_ISENSE[1..6]
LIGHT_INPUT_VSENSE
LIGHT_BOARD_TEMP
LIGHT_BOARD_FAULT_N
```

### Local decomposition

```text
LED_PWM_1_3
LED_PWM_4_6
LED_FAULT_N_1_3
LED_FAULT_N_4_6
LED_ISENSE_1_3
LED_ISENSE_4_6
LED_OUTPUTS_1_3
LED_OUTPUTS_4_6
```

Точное совпадение PCB-B ↔ PCB-E будет проверено отдельным interface-consistency проходом.

## 8. Safe-state rules PCB-E

1. Default safe state — все шесть LED outputs OFF.
2. `LIGHT_GROUP_HARD_OFF` имеет приоритет над `LIGHT_BRANCH_EN` и всеми PWM.
3. Lost firmware, reset, unpowered/disconnected control не должны включать свет.
4. Single-channel fault должен локализоваться, если thermal/group protection не требует wider shutdown.
5. Diagnostic transport не участвует в аппаратном выключении.
6. Restart/retry policy не может отменять active HARD_OFF.

## 9. Controlled placeholders PCB-E

```text
LIGHT_INPUT_FAULT_N
LIGHT_INPUT_PRESENT
LED_CH_STATUS_TBD
LIGHT_ZONE1_TEMP_SENSE_TBD
LIGHT_ZONE2_TEMP_SENSE_TBD
SIGNAL_GND_REFERENCE_TBD
LIGHT_RETURN_GROUP_TBD
LIGHT_OUTPUT_CONNECTOR_CLASS_TBD
LIGHT_TP_LOW_ENERGY
LIGHT_TP_POWER_GUARDED
```

Причины:

- driver topology и conversion ratio не выбраны;
- LED voltage/current tolerances требуют подтверждения;
- PWM electrical level/frequency/dimming range не определены;
- thermal sensor placement и cooling path не определены;
- diagnostic transport/reference не выбран;
- harness/return/connector mechanics требуют load and environmental data.

## 10. Данные, необходимые до component selection PCB-E

1. подтверждённый диапазон Vf и рабочий ток каждой LED-матрицы;
2. допустимая точность и ripple LED current;
3. PWM frequency, electrical level, minimum pulse/dimming range;
4. режимы одновременной работы шести каналов;
5. required startup/shutdown sequencing;
6. open-load/short-load/reverse-connection behavior;
7. входной диапазон `PACK_BUS_LIGHT_IN` включая transients;
8. кабельная длина, сопротивление и допустимое падение;
9. thermal environment, heat transfer and maximum component/PCB temperatures;
10. EMI constraints и требования к lighting artifacts/flicker.

Эти данные не блокируют Architecture A/B и interface-consistency, но блокируют выбор driver topology и компонентов.

## 11. Общие controlled placeholders

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

## 12. Что пока не делается

1. Не выбираются силовые и управляющие components.
2. Не добавляется `K_MAIN`.
3. Не выбираются LED-driver/controller topology, switches, magnetics, sensors, TVS или filters.
4. Не выбираются ADC, mux, local controllers или internal serialized transport.
5. Не выбираются connectors, pinout, cables, wire gauge или busbars.
6. Не создаются реальные KiCad library symbols.
7. Не создаются footprints.
8. Не выполняется PCB layout.
9. Не создаётся BOM.
10. Ground domains не объединяются.
11. `.kicad_prl` не возвращается.

## 13. Проверка пользователем в KiCad

Проверить detailed sheets `10…56`:

1. отсутствие parsing errors;
2. видимость hierarchical labels;
3. сохранность bus labels `[1..N]`;
4. независимость EXT_KILL от MCU/RS-485;
5. подчинение всех outputs SAFE/HARD_OFF;
6. отделение `5V_SYS_BUS` от critical domain;
7. симметричность LED zones 1..3 и 4..6;
8. отсутствие `.kicad_prl` в Git changes.

## 14. Следующий инженерный этап

```text
Run PCB-E_LIGHT_POWER interface consistency check
```

После согласования PCB-E:

```text
Run system-wide interface consistency audit
```
