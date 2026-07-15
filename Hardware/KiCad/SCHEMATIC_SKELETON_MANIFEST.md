# KiCad schematic skeleton manifest

Дата фиксации: 2026-07-14  
Дата обновления системных и top-листов: 2026-07-15  
Дата добавления `10_BFE_POWER` detailed hierarchy: 2026-07-15  
Дата проверки согласованности PCB-A BFE interfaces: 2026-07-15  
Дата добавления `20_CTRL_RESERVE` detailed hierarchy: 2026-07-15  
Дата проверки согласованности PCB-B CTRL_RESERVE interfaces: 2026-07-15  
Дата добавления `30_POWER_12V` detailed hierarchy: 2026-07-15  
Дата проверки согласованности PCB-C POWER_12V interfaces: 2026-07-15

Статус:

```text
ARCHITECTURE LEVEL A/B
PCB-A BFE_POWER interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
PCB-B CTRL_RESERVE interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
PCB-C POWER_12V interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
```

## 1. Назначение

Этот manifest фиксирует хронологию и текущее состояние KiCad workspace принятой многоплатной архитектуры PlataVM.

На текущем уровне фиксируются:

1. границы плат и функциональных листов;
2. направления энергии;
3. точные логические управляющие и диагностические интерфейсы;
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
Hardware/KiCad/POWER_12V_INTERFACE_CONSISTENCY.md
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

### Оставшиеся top-листы

```text
40_POWER_5V_TOP
50_LIGHT_POWER_TOP
```

## 3. Зафиксированная архитектура

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

Отчёт:

```text
Hardware/KiCad/BFE_INTERFACE_CONSISTENCY.md
PASS WITH CONTROLLED PLACEHOLDERS
```

Hold-loop paths:

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

Отчёт:

```text
Hardware/KiCad/CTRL_RESERVE_INTERFACE_CONSISTENCY.md
PASS WITH CONTROLLED PLACEHOLDERS
```

Каноническая аппаратная цепь:

```text
EXT_KILL_HW_CHAIN
BAT1_HOLD_LOOP_OPEN_HW
BAT2_HOLD_LOOP_OPEN_HW
BAT1_MAIN_SW_OFF_HW
BAT2_MAIN_SW_OFF_HW
```

## 6. PCB-C_POWER_12V

Detailed hierarchy:

```text
31_POWER_12V_INPUT_PROTECTION
32_POWER_12V_CHANNEL_TEMPLATE
33_POWER_12V_CH1_CH7
34_POWER_12V_CH8_CH14
35_POWER_12V_DIAGNOSTICS
36_POWER_12V_CONNECTORS
```

Отчёт:

```text
Hardware/KiCad/POWER_12V_INTERFACE_CONSISTENCY.md
PASS WITH CONTROLLED PLACEHOLDERS
```

### Питание

```text
PACK_BUS_P12_IN
POWER_GND
P12_PROTECTED_BUS
```

### Каналы

```text
CH1..CH11  — normally MCU-controlled
CH12..CH14 — Always-On monitored during normal RUN
Nominal continuous requirement — 3 A per channel
```

Always-On не отменяет individual protection, monitoring, `P12_GROUP_SAFE_OFF` и `P12_GROUP_HARD_OFF`.

### Канонические control ports

```text
CTRL_B_TO_C_P12
P12_CH_EN[1..11]
P12_GROUP_SAFE_OFF
P12_GROUP_HARD_OFF
```

### Канонические diagnostic ports

```text
DIAG_C_TO_B_P12
P12_CH_FAULT_N[1..14]
P12_CH_ISENSE[1..14]
P12_BOARD_TEMP
P12_INPUT_VSENSE
P12_BOARD_FAULT_N
```

### Internal decomposition groups

```text
P12_CH_EN_1_7
P12_CH_EN_8_11
P12_CH_FAULT_N_1_7
P12_CH_FAULT_N_8_14
P12_CH_ISENSE_1_7
P12_CH_ISENSE_8_14
```

Эти группы являются локальным разложением листов PCB-C, а не альтернативными межплатными именами.

## 7. Safe-state правила PCB-C

1. CH1…CH11 default OFF при reset, brownout, lost firmware и disconnected control.
2. `P12_GROUP_HARD_OFF` имеет приоритет над normal enable и Always-On policy.
3. `P12_GROUP_SAFE_OFF` запрашивает controlled safe state.
4. CH12…CH14 выключаются при SAFE/HARD_OFF.
5. Diagnostic transport не может блокировать или задерживать HARD_OFF.
6. Отказ одного канала должен локализоваться, где это допускает upstream protection coordination.

## 8. Controlled placeholders

### PCB-A

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
P12_AON_CH12_14
P12_AON_POLICY_CH12_14
P12_BOARD_TEMP_SENSE_TBD
SIGNAL_GND_REFERENCE_TBD
P12_RETURN_GROUP_TBD
P12_OUTPUT_CONNECTOR_CLASS_TBD
P12_TP_LOW_ENERGY
P12_TP_POWER_GUARDED
```

## 9. Исходные данные, не блокирующие текущий уровень

До component selection для PCB-C потребуются:

1. назначение каждого CH1…CH14;
2. длительный, пусковой и аварийный ток каждой нагрузки;
3. inrush profile;
4. индуктивность/ёмкость нагрузки и кабеля;
5. duty cycle и последовательность включения;
6. допустимое падение напряжения;
7. длина и сечение проводников;
8. число одновременно нагруженных каналов;
9. thermal environment;
10. reverse-current и output-discharge requirements.

Эти данные не блокируют переход к Architecture A/B для PCB-D и PCB-E.

## 10. Что пока не делается

1. Не выбираются силовые и управляющие компоненты.
2. Не добавляется `K_MAIN`.
3. Не выбираются eFuse/high-side switches, fuses, sensors, TVS и suppression.
4. Не выбираются DC/DC, LED drivers, MCU, ADC, mux или internal serialized transport.
5. Не выбираются connectors, pin count, pinout, cables, wire gauge или busbar.
6. Не создаются реальные KiCad library symbols.
7. Не создаются footprints.
8. Не выполняется PCB layout.
9. Не создаётся BOM.
10. Не объединяются ground domains.
11. Не возвращается `.kicad_prl`.

## 11. Проверка пользователем в KiCad

Открыть:

```text
Hardware/KiCad/PlataVM.kicad_pro
```

Проверить текущие detailed sheets `10…36`:

1. отсутствие ошибок парсинга;
2. читаемость text zones;
3. видимость hierarchical labels;
4. сохранность bus labels с `[1..N]` после открытия/сохранения;
5. отсутствие `.kicad_prl` в Git changes;
6. независимость EXT_KILL от MCU/RS-485;
7. подчинение CH12…CH14 SAFE/HARD_OFF.

## 12. Следующий инженерный этап

```text
Start PCB-D_POWER_5V detailed hierarchy
```

Канонические подлисты:

```text
41_5V_DC_DC
42_5V_OUTPUT_TEMPLATE
43_5V_OUT1_OUT5
44_5V_OUT6_OUT10
45_5V_DIAGNOSTICS
46_5V_CONNECTORS
```

Компоненты, connectors, footprints, BOM и layout в следующий этап не входят.
