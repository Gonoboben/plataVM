# Архитектура принципиальной схемы ПДУ БНПА / PlataVM

Дата актуализации: 2026-07-16  
Статус:

```text
V1.6 ACCEPTED SCHEMATIC ARCHITECTURE
CAN-FD internal transport; direct hard safety lines; no component freeze
```

## 1. Назначение

Документ задаёт функциональное разбиение принципиальной схемы, иерархию листов KiCad, границы плат и обязательные межплатные контракты. Конкретные модели компонентов, footprints, разъёмы и PCB layout выбираются отдельными расчётными этапами.

## 2. Многоплатная система

ПДУ состоит из пяти функциональных PCB-модулей и пассивного INTERCONNECT:

1. `PCB-A_BFE_POWER` — два Battery Front-End, объединение в PACK_BUS, измерения, электронные ключи, DECK_BALANCE и конечные аппаратные отключения;
2. `PCB-B_CTRL_RESERVE` — central MCU, critical power, EMG, watchdog/supervisor, fault manager, внешний isolated RS-485, внутренняя CAN-FD и аппаратные safe-control outputs;
3. `PCB-C_POWER_12V` — 14 защищённых 12 В каналов, local control/ADC и CAN-FD node;
4. `PCB-D_POWER_5V` — 5V_SYS converter, 10 защищённых выходов, local control/ADC и CAN-FD node;
5. `PCB-E_LIGHT_POWER` — шесть независимых LED drivers, local PWM/current control и CAN-FD node;
6. `INTERCONNECT` — только пассивные силовые шины, жгуты, экраны и/или passive backplane.

Высокие токи не проходят через PCB-B. Центральный `K_MAIN` отсутствует.

## 3. Каноническая структура питания

```text
АКБ_1 → BMS → fuse → K_BAT1 → СН-176А-12 → PCB-A / BFE_1 ┐
                                                               ├→ PACK_BUS
АКБ_2 → BMS → fuse → K_BAT2 → СН-176А-12 → PCB-A / BFE_2 ┘

PACK_BUS
├→ PACK_BUS_CRIT_IN  → PCB-B
├→ PACK_BUS_P12_IN   → PCB-C
├→ PACK_BUS_P5_IN    → PCB-D
└→ PACK_BUS_LIGHT_IN → PCB-E
```

Каждая силовая ветвь имеет отдельный рассчитанный проводник/шину и локальную защиту. Сигнальная backplane не является силовой шиной.

## 4. Каноническая структура управления

```text
PCB-B ↔ PCB-A
  direct critical control, direct measurements, EXT_KILL hardware chain

PCB-B ↔ PCB-C/D/E
  CAN_INT_H / CAN_INT_L for normal commands and telemetry
  + direct SAFE/HARD_OFF lines
  + direct board-fault summary lines

PCB-B ↔ верхний уровень
  isolated RS-485
```

Внутренняя CAN-FD не заменяет EXT_KILL, HARD_OFF или локальные аппаратные защиты.

## 5. PCB-A_BFE_POWER

### 5.1 На плате размещаются

1. `BAT1+ / BAT1−` и `BAT2+ / BAT2−` после СН-176А-12;
2. входная TVS/EMI-защита обеих ветвей;
3. измерение напряжения и тока каждой ветви;
4. `MAIN_SW1`, `MAIN_SW2`;
5. `BALANCE_SW1/R_BAL1`, `BALANCE_SW2/R_BAL2`;
6. объединение исправных ветвей в `PACK_BUS`;
7. измерение `PACK_BUS_VSENSE` и при необходимости общего тока;
8. `PACK_BUS_DISCHARGE`;
9. два независимых energize-to-run REMOTE_OFF relay contacts;
10. конечные аппаратные действия EXT_KILL для MAIN_SW и hold loops;
11. силовые выходы PACK_BUS к PCB-B/C/D/E;
12. разъёмы и защищённые test points.

### 5.2 REMOTE_OFF на PCB-A

Используется физический `NO` run-contact, который замкнут только при healthy critical control:

```text
REMOTE_OFF relay energized → run contact CLOSED
relay de-energized          → run contact OPEN → hold loop OPEN
```

Имя `REMOTE_OFF_NC` не используется для физического контакта. Логическая функция может быть active-low, но физическая fail-open реализация — energize-to-run NO.

### 5.3 PCB-A ↔ PCB-B direct nets

Управление:

```text
BAT1_MAIN_SW_EN
BAT2_MAIN_SW_EN
BAT1_BALANCE_SW_EN
BAT2_BALANCE_SW_EN
BAT1_HOLD_LOOP_OPEN_CMD
BAT2_HOLD_LOOP_OPEN_CMD
PACK_BUS_DISCHARGE_EN
EXT_KILL_HW_CHAIN
```

Диагностика:

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

### 5.4 На PCB-A не размещаются

- central MCU;
- внешний RS-485;
- внутренний CAN-FD node как обязательный safety path;
- каналы CH1…CH14;
- 5V_SYS converter;
- LED drivers;
- активная электроника внутри корпусов основных АКБ.

## 6. PCB-B_CTRL_RESERVE

### 6.1 На плате размещаются

1. central MCU семейства STM32G4, package TBD;
2. watchdog и supervisor;
3. fault manager и аппаратные блокировки;
4. `RESERVE_BRANCH`, EMG charge/control и KEEP_ALIVE;
5. `5V_CRIT`, `3V3_CRIT`;
6. внешний isolated RS-485;
7. внутренний CAN-FD controller/transceiver;
8. hard SAFE/HARD_OFF outputs к PCB-C/D/E;
9. board-fault summary inputs от PCB-C/D/E;
10. вход EXT_KILL и аппаратное формирование `EXT_KILL_HW_CHAIN`;
11. SWD/UART service и test points;
12. единственная управляемая точка `SIGNAL_GND–POWER_GND`;
13. CHASSIS/shield entry network;
14. optional внешний CAN/CAN-FD footprint в статусе DNP, электрически отделённый от обязательной внутренней CAN-FD.

### 6.2 На плате не размещаются

- суммарные токи 12 В каналов;
- суммарный ток 5V_SYS_BUS;
- LED power stages;
- основные токи BAT1/BAT2/PACK_BUS кроме ограниченного critical branch.

### 6.3 Critical power rule

`5V_CRIT` и `3V3_CRIT` не являются источником `5V_SYS_BUS`. Потеря healthy critical control должна открыть energize-to-run REMOTE_OFF relay contacts.

## 7. PCB-C_POWER_12V

На плате:

1. вход `PACK_BUS_P12_IN` и POWER_GND;
2. входная защита и локальная bulk capacitance;
3. CH1…CH11 controlled;
4. CH12…CH14 Always-On monitored в RUN;
5. 3 А continuous / 5 А peak до 1 с на канал;
6. individual high-side switch/eFuse, current sense и fault protection;
7. local MCU/I/O/ADC и CAN-FD transceiver;
8. direct `P12_GROUP_SAFE_OFF` и `P12_GROUP_HARD_OFF` inputs;
9. direct `P12_BOARD_FAULT_N` output;
10. внешние разъёмы и test points.

Normal channel commands and detailed diagnostics are CAN-FD data objects. Hard-off does not depend on CAN-FD.

## 8. PCB-D_POWER_5V

На плате:

1. вход `PACK_BUS_P5_IN` и POWER_GND;
2. input protection/inrush/bulk network;
3. preliminary two-phase synchronous buck 15 А continuous / 20 А short;
4. 10 protected outputs up to 3 А each within total budget;
5. OUT1…OUT7 controlled;
6. OUT8…OUT10 Always-On monitored в RUN;
7. local MCU/I/O/ADC и CAN-FD transceiver;
8. direct `P5_GROUP_SAFE_OFF` и `P5_GROUP_HARD_OFF` inputs;
9. direct `P5_BOARD_FAULT_N` output;
10. thermal monitoring and external output connectors.

`5V_SYS_BUS` не питает PCB-B critical domain и не питается от EMG.

## 9. PCB-E_LIGHT_POWER

На плате:

1. вход `PACK_BUS_LIGHT_IN` и POWER_GND;
2. branch input protection and bulk network;
3. шесть независимых LED driver channels;
4. две симметричные thermal/power zones 2×3;
5. local MCU/current-control/PWM generation;
6. CAN-FD transceiver;
7. direct `LIGHT_GROUP_HARD_OFF` input;
8. direct `LIGHT_BOARD_FAULT_N` output;
9. per-channel current/open/short diagnostics;
10. external LED connectors and thermal sensors.

CAN-FD передаёт brightness setpoints и diagnostics. Шесть высокочастотных PWM-линий не проходят через межплатный жгут. Локальный PWM: 3,3 В active-high, default 1 кГц, configurable 100…1000 Гц.

Default safe state — все LED OFF.

## 10. INTERCONNECT

INTERCONNECT включает:

1. отдельные PACK_BUS power branches;
2. POWER_GND returns;
3. critical power branch;
4. CAN_INT_H/CAN_INT_L differential pair;
5. direct SAFE/HARD_OFF lines;
6. direct board-fault summary lines;
7. EXT_KILL hardware chain;
8. CHASSIS/shield connections;
9. service/test wiring.

INTERCONNECT остаётся пассивным. CAN-FD выполняется как линейная шина с termination на двух физических концах; node order определяется после 3D-компоновки.

## 11. Ground/chassis policy

1. `POWER_GND`, `SIGNAL_GND`, `ISO_GND`, `CHASSIS` — разные nets;
2. одна точка `SIGNAL_GND–POWER_GND` на PCB-B через net-tie/configurable element;
3. экраны подключаются к CHASSIS у ввода;
4. ISO_GND отделён по DC;
5. optional HF coupling ISO_GND–CHASSIS после EMC review;
6. безымянный `GND` запрещён в межплатных контрактах.

## 12. Иерархия листов KiCad

### 12.1 Корень

```text
PlataVM.kicad_pro
PlataVM.kicad_sch
00_SYSTEM_TOP.kicad_sch
01_EXTERNAL_BATTERIES_AND_HARNESS.kicad_sch
02_INTERBOARD_POWER_AND_CONTROL.kicad_sch
```

### 12.2 PCB-A

```text
10_BFE_POWER_TOP.kicad_sch
11_BATTERY_INPUT_1.kicad_sch
12_BATTERY_INPUT_2.kicad_sch
13_MAIN_PATH_1.kicad_sch
14_MAIN_PATH_2.kicad_sch
15_DECK_BALANCE.kicad_sch
16_PACK_BUS_AND_DISCHARGE.kicad_sch
17_REMOTE_OFF_AND_EXT_KILL.kicad_sch
18_BATTERY_MEASUREMENTS.kicad_sch
19_BFE_CONNECTORS_TESTPOINTS.kicad_sch
```

### 12.3 PCB-B

```text
20_CTRL_RESERVE_TOP.kicad_sch
21_EMG_INPUT_CHARGE_ORING.kicad_sch
22_5V_CRIT_3V3_CRIT.kicad_sch
23_MCU_CORE.kicad_sch
24_WATCHDOG_SUPERVISOR.kicad_sch
25_RS485_ISOLATED.kicad_sch
26_EXT_KILL_INPUT_LOGIC.kicad_sch
27_CONTROL_IO.kicad_sch
28_SERVICE_DEBUG.kicad_sch
29_CTRL_CONNECTORS_TESTPOINTS.kicad_sch
```

Внутренняя CAN-FD добавляется в функциональные границы `23_MCU_CORE`, `27_CONTROL_IO` и `29_CTRL_CONNECTORS_TESTPOINTS`; отдельный новый PCB-модуль не создаётся.

### 12.4 PCB-C

```text
30_POWER_12V_TOP.kicad_sch
31_POWER_12V_INPUT_PROTECTION.kicad_sch
32_POWER_12V_CHANNEL_TEMPLATE.kicad_sch
33_POWER_12V_CH1_CH7.kicad_sch
34_POWER_12V_CH8_CH14.kicad_sch
35_POWER_12V_DIAGNOSTICS.kicad_sch
36_POWER_12V_CONNECTORS.kicad_sch
```

### 12.5 PCB-D

```text
40_POWER_5V_TOP.kicad_sch
41_5V_DC_DC.kicad_sch
42_5V_OUTPUT_TEMPLATE.kicad_sch
43_5V_OUT1_OUT5.kicad_sch
44_5V_OUT6_OUT10.kicad_sch
45_5V_DIAGNOSTICS.kicad_sch
46_5V_CONNECTORS.kicad_sch
```

### 12.6 PCB-E

```text
50_LIGHT_POWER_TOP.kicad_sch
51_LIGHT_INPUT_PROTECTION.kicad_sch
52_LED_DRIVER_TEMPLATE.kicad_sch
53_LED_DRIVER_1_3.kicad_sch
54_LED_DRIVER_4_6.kicad_sch
55_LIGHT_DIAGNOSTICS.kicad_sch
56_LIGHT_CONNECTORS.kicad_sch
```

## 13. Reference designator ranges

| Плата | Диапазон |
|---|---:|
| PCB-A | 100–199 |
| PCB-B | 200–299 |
| PCB-C | 300–399 |
| PCB-D | 400–499 |
| PCB-E | 500–599 |

## 14. KiCad alignment required

Текущий architecture skeleton должен быть обновлён следующим отдельным schematic PR:

1. добавить CAN_INT_H/CAN_INT_L logical boundaries на PCB-B/C/D/E;
2. оставить per-channel names как data-object contracts, а не отдельные обязательные межплатные pins;
3. оставить direct SAFE/HARD_OFF и board-fault summary pins;
4. заменить физическую семантику `REMOTE_OFF_NC` на energize-to-run NO run-contact;
5. добавить единственную ground net-tie point на PCB-B;
6. выполнить повторный system interface consistency audit.

До этого текущие листы считаются Architecture A/B skeleton, а не frozen physical pinout.

## 15. Запрещённые изменения

1. добавление центрального K_MAIN;
2. пропуск высоких токов через PCB-B;
3. зависимость EXT_KILL от firmware/CAN-FD/RS-485;
4. объединение ground domains без net-tie policy;
5. активные компоненты в INTERCONNECT;
6. активная электроника в корпусах основных АКБ;
7. выбор components/footprints до закрытия соответствующих расчётов;
8. автоматический restart после BMS recovery.
