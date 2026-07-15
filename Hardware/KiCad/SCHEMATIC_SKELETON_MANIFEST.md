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

Статус:

```text
ARCHITECTURE LEVEL A/B
PCB-A BFE_POWER interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
PCB-B CTRL_RESERVE interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
PCB-C POWER_12V interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
PCB-D POWER_5V detailed hierarchy: ADDED — INTERFACE CHECK PENDING
```

## 1. Назначение

Этот manifest фиксирует хронологию и состояние KiCad workspace принятой многоплатной архитектуры PlataVM.

На текущем уровне фиксируются функциональные границы, направления энергии, logical interfaces, safe states и controlled placeholders. Компоненты, footprints, физические разъёмы, BOM и PCB layout не выбираются.

Источники истины:

```text
Docs/SCHEMATIC_ARCHITECTURE.md
Docs/INTERBOARD_INTERFACES.md
Docs/NET_NAMING_RULES.md
Hardware/KiCad/BFE_INTERFACE_CONSISTENCY.md
Hardware/KiCad/CTRL_RESERVE_INTERFACE_CONSISTENCY.md
Hardware/KiCad/POWER_12V_INTERFACE_CONSISTENCY.md
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
3. Высокие токи не проходят через PCB-B.
4. `INTERCONNECT` остаётся пассивным.
5. `EXT_KILL` не зависит от MCU firmware или external RS-485.
6. Ground domains не объединяются автоматически.
7. `5V_SYS_BUS` не является critical rail и не питается от EMG.

## 3. Созданные detailed hierarchy packages

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

### Оставшийся top-лист

```text
50_LIGHT_POWER_TOP
```

## 4. Interface consistency status

```text
PCB-A: Hardware/KiCad/BFE_INTERFACE_CONSISTENCY.md
PCB-B: Hardware/KiCad/CTRL_RESERVE_INTERFACE_CONSISTENCY.md
PCB-C: Hardware/KiCad/POWER_12V_INTERFACE_CONSISTENCY.md
```

Все три результата:

```text
PASS WITH CONTROLLED PLACEHOLDERS
```

## 5. PCB-D_POWER_5V detailed hierarchy

```text
41_5V_DC_DC
42_5V_OUTPUT_TEMPLATE
43_5V_OUT1_OUT5
44_5V_OUT6_OUT10
45_5V_DIAGNOSTICS
46_5V_CONNECTORS
```

Назначение:

```text
41 — PACK_BUS_P5_IN protection/conversion boundary, 5V_SYS enable and primary diagnostics.
42 — reusable single-output control/protection/diagnostic contract.
43 — 5V_OUT1..5V_OUT5, five normally controlled outputs.
44 — 5V_OUT6..5V_OUT7 controlled and 5V_OUT8..5V_OUT10 Always-On monitored.
45 — ten-output and 5V_SYS diagnostic aggregation toward PCB-B.
46 — logical output/return, harness, connector-class and testpoint boundaries.
```

## 6. PCB-D power contract

```text
Input:              PACK_BUS_P5_IN
Return:             POWER_GND
Converted rail:     5V_SYS_BUS
Board budget:       15 A continuous / 20 A short peak
Per-output ceiling: up to 3 A within total board budget
```

`5V_SYS_BUS`:

1. не питает `5V_CRIT` или `3V3_CRIT`;
2. не питается от `EMG_4S2P`;
3. предназначен только для PCB-D output domain;
4. выключается при board HARD_OFF;
5. требует отдельного converter thermal/EMC расчёта.

## 7. PCB-D output policy

```text
5V_OUT1..5V_OUT7   — normally controlled
5V_OUT8..5V_OUT10  — Always-On monitored during normal RUN
```

Always-On не отменяет:

```text
individual protection
P5_GROUP_SAFE_OFF
P5_GROUP_HARD_OFF
board-level protection
current/fault diagnostics
```

Индивидуальный лимит до 3 А не означает допустимость одновременной нагрузки 10 × 3 А. Суммарная нагрузка должна оставаться в пределах converter, copper и thermal budget.

## 8. Канонические PCB-D interfaces

### Control

```text
CTRL_B_TO_D_P5
5V_SYS_EN
P5_OUT_EN[1..7]
P5_GROUP_SAFE_OFF
P5_GROUP_HARD_OFF
```

### Diagnostics

```text
DIAG_D_TO_B_P5
P5_OUT_FAULT_N[1..10]
P5_OUT_ISENSE[1..10]
5V_SYS_VSENSE
5V_SYS_TOTAL_ISENSE
P5_BOARD_TEMP
P5_BOARD_FAULT_N
```

### Local decomposition groups

```text
P5_OUT_EN_1_5
P5_OUT_EN_6_7
P5_OUT_FAULT_N_1_5
P5_OUT_FAULT_N_6_10
P5_OUT_ISENSE_1_5
P5_OUT_ISENSE_6_10
5V_OUTPUTS_1_5
5V_OUTPUTS_6_10
```

Точное совпадение с `27_CONTROL_IO` будет проверено отдельным interface-consistency проходом.

## 9. Safe-state rules PCB-D

1. `5V_SYS_EN` defaults OFF при lost control, если иной startup policy не утверждён отдельно.
2. `P5_GROUP_HARD_OFF` имеет приоритет над converter/output enables и Always-On policy.
3. `P5_GROUP_SAFE_OFF` запрашивает controlled safe state выходов.
4. OUT8…OUT10 выключаются при SAFE/HARD_OFF.
5. Converter recovery не отменяет HARD_OFF.
6. Faulted output должен изолироваться без destabilization `5V_SYS_BUS`, где это допускает protection coordination.
7. Diagnostic transport не участвует в аппаратном выключении.

## 10. Controlled placeholders PCB-D

```text
P5_DC_DC_FAULT_N
P5_OUT_STATUS_TBD
P5_AON_OUT8_10
P5_AON_POLICY_OUT8_10
P5_BOARD_TEMP_SENSE_TBD
SIGNAL_GND_REFERENCE_TBD
P5_RETURN_GROUP_TBD
P5_OUTPUT_CONNECTOR_CLASS_TBD
P5_TP_LOW_ENERGY
P5_TP_POWER_GUARDED
```

Причины:

- converter topology и control IC не выбраны;
- magnetics, switching frequency, ripple and compensation не рассчитаны;
- output protection and backfeed topology не выбрана;
- Always-On implementation не выбрана;
- analog reference/transport не выбран;
- harness/return/connector mechanics требуют load data.

## 11. Данные, необходимые до component selection PCB-D

1. фактический диапазон `PACK_BUS_P5_IN`, включая minimum during discharge и maximum charge/transient;
2. load profile каждого `5V_OUT1…10`;
3. continuous, peak и inrush currents;
4. допустимые ripple, transient dip и recovery time;
5. simultaneous-load matrix;
6. cable length, wire resistance и allowable voltage drop;
7. backfeed/reverse current requirements;
8. output discharge requirements;
9. ambient/case temperature и cooling path;
10. EMI constraints и допустимая switching frequency range.

Эти данные не блокируют создание Architecture A/B для PCB-E_LIGHT_POWER.

## 12. Что пока не делается

1. Не выбираются DC/DC controller, MOSFETs, magnetics, capacitors или compensation.
2. Не выбираются load switches/eFuse/fuses/current sensors.
3. Не выбираются TVS, filters, suppression или backfeed protection.
4. Не выбираются ADC, mux, local controller или internal serialized transport.
5. Не выбираются connectors, pinout, cables, wire gauge или busbar.
6. Не создаются реальные KiCad library symbols.
7. Не создаются footprints.
8. Не выполняется PCB layout.
9. Не создаётся BOM.
10. Не объединяются ground domains.
11. Не возвращается `.kicad_prl`.

## 13. Проверка пользователем в KiCad

Проверить листы:

```text
40_POWER_5V_TOP
41_5V_DC_DC
42_5V_OUTPUT_TEMPLATE
43_5V_OUT1_OUT5
44_5V_OUT6_OUT10
45_5V_DIAGNOSTICS
46_5V_CONNECTORS
```

Проверить:

1. отсутствие parsing errors;
2. видимость hierarchical labels;
3. сохранность bus labels `[1..N]`;
4. явное отделение `5V_SYS_BUS` от `5V_CRIT/3V3_CRIT`;
5. подчинение OUT8…OUT10 SAFE/HARD_OFF;
6. отсутствие `.kicad_prl` в Git changes.

## 14. Следующий инженерный этап

```text
Run PCB-D_POWER_5V interface consistency check
```

После согласования PCB-D:

```text
Start PCB-E_LIGHT_POWER detailed hierarchy
```
