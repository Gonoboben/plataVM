# Главная концепция проекта ПДУ БНПА / PlataVM

Дата исходной фиксации: 2026-07-01  
Дата актуализации: 2026-07-21  
Статус:

```text
главный управляющий документ проекта
V1.9 guarded-service and preliminary-packaging baseline
```

## 1. Назначение

Документ фиксирует верхнеуровневую концепцию PlataVM и является главным входом для схемы, PCB, BOM, firmware, GUI, механики, испытаний и выпускной документации.

Подробности:

```text
Docs/ARCHITECTURE_BASELINE.md
Docs/KBAT_ELECTRICAL_REQUIREMENTS.md
Docs/INTERBOARD_INTERFACES.md
Docs/SYSTEM_POWER_BUDGET_POLICY.md
Docs/SERVICE_OVERRIDE_POLICY.md
Docs/MECHANICAL_ENVELOPE_V1_8.md
Docs/PCB_PACKAGING_BOUNDARY_V1_9.md
Docs/PCB_MODULE_AREA_BUDGET_V1_9.md
Docs/PHYSICAL_INTERFACE_COUNT_V1_9.md
Docs/BRANCH_CURRENT_PRECALC_V1_9.md
Docs/OPEN_QUESTIONS.md
```

## 2. Граница проекта

В проект входят:

1. две основные АКБ LiFePO4 4S24P, 12,8 В, 144 А·ч;
2. автономные BMS;
3. K_BAT1/K_BAT2 и LOCAL_START;
4. две линии СН-176А-12 длиной 1 м;
5. PCB-A_BFE_POWER;
6. PCB-B_CTRL_RESERVE;
7. PCB-C_POWER_12V;
8. PCB-D_POWER_5V;
9. PCB-E_LIGHT_POWER;
10. пассивный INTERCONNECT;
11. PACK_BUS и распределённый BATTERY_DISCONNECT/HARD_OFF;
12. POWER_12V_BUS, 5V_SYS_BUS, LIGHT_POWER_BRANCH;
13. RESERVE_BRANCH / EMG_4S2P / KEEP_ALIVE;
14. 5V_CRIT / 3V3_CRIT;
15. внешний isolated RS-485 и внутренняя CAN-FD;
16. DECK_BALANCE;
17. DUAL_PACK_RUN и SINGLE_PACK_MODE;
18. power-budget manager;
19. guarded SERVICE_OVERRIDE;
20. многоуровневая электронная сборка в envelope 100 × 250 × 80 мм;
21. physical interface count и последующий выбор connector classes;
22. схемы, PCB, BOM, firmware, GUI, тесты и документация.

## 3. Замороженная системная архитектура

### 3.1 Основные АКБ

```text
АКБ_1 cells → autonomous BMS → fuse → K_BAT1 → СН-176А-12 → BFE_1 ┐
                                                                                   ├→ PACK_BUS
АКБ_2 cells → autonomous BMS → fuse → K_BAT2 → СН-176А-12 → BFE_2 ┘
```

Принято:

1. обе исправные АКБ работают параллельно в DUAL_PACK_RUN;
2. различия напряжений, токов и расчётного SoC используются для диагностики и сами по себе не отключают исправную АКБ;
3. BMS — закрытый автономный двухполюсный защищённый источник;
4. raw-ветвь, внутренние точки и digital control BMS не используются;
5. automatic restart после восстановления BMS запрещён;
6. межблочное выравнивание выполняется только в DECK_BALANCE.

### 3.2 PACK_BUS

```text
PACK_BUS
├→ PCB-B / PACK_BUS_CRIT_IN
├→ PCB-C / PACK_BUS_P12_IN
├→ PCB-D / PACK_BUS_P5_IN
└→ PCB-E / PACK_BUS_LIGHT_IN
```

Центральный `K_MAIN` и отдельная `MAIN_INPUT_BUS` отсутствуют.

### 3.3 Многоплатное разбиение

```text
PCB-A_BFE_POWER
PCB-B_CTRL_RESERVE
PCB-C_POWER_12V
PCB-D_POWER_5V
PCB-E_LIGHT_POWER
INTERCONNECT — пассивный
```

Высокие токи распределяются от PCB-A и не проходят через PCB-B или signal backplane.

## 4. Корпуса основных АКБ

Внутри каждой основной АКБ остаются только:

1. сборка 4S24P;
2. автономная BMS;
3. силовой предохранитель;
4. F_CTRL;
5. моностабильный K_BATx;
6. одна катушка continuous duty;
7. K_BAT_AUX_NO;
8. LOCAL_START wiring;
9. passive suppression;
10. силовая проводка.

Не устанавливаются MCU, дополнительная управляющая плата, CAN/RS-485/UART, обязательная digital telemetry BMS, raw-доступ и отдельный control DC/DC.

## 5. СН-176А-12 и LOCAL_START

| Контакты | Назначение |
|---|---|
| 1–5 | BAT+ |
| 6–10 | BAT− |
| 11 | REMOTE_OFF / K_BAT_HOLD_RETURN |
| 12 | RESERVE |

LOCAL_START:

- отдельный двухконтактный разъём;
- normally open;
- пружинно-возвратный;
- без фиксации;
- параллельно K_BAT_AUX_NO.

Батарейная линия СН-176А-12 находится в owner-controlled scope. Её внешние ограничения учитываются системой.

## 6. K_BATx

K_BAT1/K_BAT2:

- одинаковые;
- однополюсные по плюсу;
- SPST-NO;
- моностабильные;
- пружинный возврат OPEN;
- одна катушка continuous duty;
- economizer preferred;
- electrical self-hold через K_BAT_AUX_NO.

```text
BAT_PROT+ → F_CTRL → (LOCAL_START_NO ∥ K_BAT_AUX_NO)
→ K_BAT_COIL → pin 11
→ REMOTE_OFF_RUN_CONTACT
→ EXT_KILL series path
→ BAT_PROT−
```

| Параметр | Требование |
|---|---:|
| BAT_PROT calculation range | 0…16 В DC |
| Guaranteed pull-in | 9…16 В |
| Guaranteed hold | 7,5…16 В |
| Inrush | ≤2 А / 150 мс |
| Hold current | target ≤0,15 А; limit ≤0,25 А |
| Hold power | target ≤2 Вт; limit ≤4 Вт |
| Main contact continuous | ≥30 А; target class ≥50 А |
| DC breaking capacity | ≥30 А при 16 В DC |
| Initial contact resistance | ≤2 мОм |
| End-of-life resistance | ≤5 мОм |
| Operating temperature | −20…+60 °C |
| Mechanical life | ≥100 000 циклов |
| Electrical life | ≥10 000 операций |

Конкретная модель выбирается после candidate review и испытаний.

## 7. REMOTE_OFF и EXT_KILL

REMOTE_OFF:

```text
healthy critical power + healthy supervisor
→ energize-to-run relay energized
→ physical NO run contact CLOSED

loss of critical power / supervisor fault / OFF command
→ relay de-energized
→ NO run contact OPEN
→ hold loop OPEN
```

Для двух АКБ используются два независимых run-contact.

EXT_KILL:

- физически разрывает оба hold loop;
- запрещает MAIN_SW1/MAIN_SW2;
- независим от MCU, RS-485 и CAN-FD;
- имеет приоритет над LOCAL_START;
- не допускает automatic restart.

```text
t_OFF ≥ max(250 мс; 5 × t_release_max)
t_release_system target ≤100 мс
```

`HARD_OFF_FAILED` и `WELDED_CONTACT` блокируют restart.

## 8. PCB-A_BFE_POWER

PCB-A выполняет:

1. два симметричных BFE;
2. измерение токов и напряжений батарейных ветвей;
3. MAIN_SW1/MAIN_SW2;
4. BALANCE_SW1/BALANCE_SW2;
5. формирование PACK_BUS;
6. PACK_BUS discharge;
7. final hardware actions EXT_KILL;
8. распределение силовых ветвей PCB-B/C/D/E.

PCB-A не содержит главный MCU и не заменяет K_BATx.

Preliminary area budget:

```text
PCB-A target 94 × 110 мм
preliminary maximum 100 × 120 мм
component height ≤23 мм
```

## 9. PCB-B_CTRL_RESERVE

PCB-B содержит:

1. центральный STM32G4-family MCU;
2. 5V_CRIT/3V3_CRIT;
3. EMG_4S2P charge/ORing/KEEP_ALIVE;
4. watchdog/supervisor;
5. fault manager;
6. внешний isolated RS-485;
7. внутренний CAN-FD control node;
8. direct hardware safety/fault interfaces;
9. controlled SIGNAL_GND–POWER_GND point;
10. service/debug;
11. guarded SERVICE_OVERRIDE state machine и журналирование.

PCB-B не проводит суммарные токи пользовательских нагрузок.

Preliminary area budget:

```text
PCB-B target 94 × 180 мм
preliminary maximum 100 × 220 мм
component height ≤16 мм
```

## 10. PCB-C_POWER_12V

- CH1…CH11 normally controlled;
- CH12…CH14 Always-On monitored;
- 3 А continuous / 5 А peak до 1 с на канал;
- board hardware rating 30 А continuous;
- local protection/current diagnostics;
- local MCU/I/O/ADC;
- normal commands/telemetry по CAN-FD;
- direct P12_GROUP_SAFE_OFF, P12_GROUP_HARD_OFF и P12_BOARD_FAULT_N.

Preliminary area budget:

```text
PCB-C target 94 × 130 мм
preliminary maximum 100 × 145 мм
component height ≤23 мм
```

## 11. PCB-D_POWER_5V

- PACK_BUS → 5V_SYS_BUS;
- preliminary two-phase synchronous buck;
- 15 А continuous / 20 А short на 5 В;
- 10 outputs до 3 А;
- OUT1…OUT7 controlled;
- OUT8…OUT10 Always-On monitored;
- local protection/current diagnostics;
- local MCU/I/O/ADC и CAN-FD;
- direct P5 safe/hard/fault lines;
- thermal contact с корпусом запрещён;
- cooling only by low-loss design, PCB copper and internal natural convection.

`5V_SYS_BUS` не питает critical domain и не питается от EMG.

Preliminary area/current budget:

```text
PCB-D target 94 × 125 мм
preliminary maximum 100 × 140 мм
component height ≤23 мм
PACK_BUS_P5_IN connector class = 15 А preliminary
```

Расчёт при 75 Вт output, 9,2 В input и η=88 %:

```text
I_IN ≈9,26 А
```

При 100 Вт short:

```text
I_IN ≈12,35 А
```

## 12. PCB-E_LIGHT_POWER

- 6 independent LED channels;
- две зоны 2×3;
- functional input 8…16 В;
- local current regulation и PWM;
- PWM 3,3 В active-high, default 1 кГц, 100…1000 Гц configurable;
- normal setpoints/telemetry по CAN-FD;
- direct LIGHT_GROUP_HARD_OFF и LIGHT_BOARD_FAULT_N;
- default safe state — all LED OFF;
- separate automatic brightness limit отсутствует;
- thermal contact с корпусом запрещён.

Preliminary area/current budget:

```text
PCB-E target 94 × 110 мм
preliminary maximum 100 × 130 мм
component height ≤23 мм
PACK_BUS_LIGHT_IN connector class = 25 А preliminary
```

При 180 Вт, 9,2 В и η=88 %:

```text
I_IN ≈22,23 А
```

Полная световая мощность при низком напряжении не проходит SINGLE_PACK continuous budget 20 А без учёта других ветвей.

## 13. Связь

Внешняя:

```text
isolated RS-485
half-duplex
115200 bit/s preliminary
8N1
addressed binary protocol
CRC-16
sequence number
heartbeat/timeout
```

Внутренняя PCB-B↔PCB-C/D/E:

```text
CAN_INT_H
CAN_INT_L
```

CAN-FD несёт normal commands, configuration, setpoints и telemetry. SAFE/HARD_OFF и board-fault summary остаются direct hardware lines.

## 14. Preliminary physical interface classes

### 14.1 A↔B

```text
critical power: 2 logical poles
control/diagnostics: 32 signal positions target
```

Допускается split:

```text
16-position CTRL
16-position DIAG
```

### 14.2 B↔C/D/E

Стандартизированный signal class:

```text
8 positions each
CAN_H
CAN_L
CAN_REF_GND
SAFE or reserve
HARD_OFF
BOARD_FAULT_N
RESERVE_1
RESERVE_2
```

### 14.3 A→C/D/E power

```text
A→C: 2 high-current poles, 30 А class
A→D: 2 power poles, 15 А class preliminary
A→E: 2 high-current poles, 25 А class preliminary
```

### 14.4 Service/debug

```text
10 positions preliminary
```

Конкретные connector families и final pinout не выбраны.

## 15. Ground, chassis и shields

```text
POWER_GND
SIGNAL_GND
ISO_GND
CHASSIS
```

1. SIGNAL_GND–POWER_GND соединяются в одной controlled point PCB-B;
2. ISO_GND остаётся DC-isolated;
3. shields terminate to CHASSIS at entry;
4. optional HF ISO_GND–CHASSIS только после EMC review;
5. generic unnamed GND, скрывающий domains, запрещён.

## 16. DECK_BALANCE

- только на палубе;
- две доступные АКБ;
- heavy loads OFF;
- nominal 2 А;
- hard limit 3 А;
- finish: abs(ΔU) ≤50 мВ и abs(I) ≤0,2 А в течение 60 с;
- temperature 0…45 °C;
- запрещён в SINGLE_PACK_MODE.

## 17. DUAL_PACK_RUN

```text
40 А continuous
44 А short ≤1 с
warning at 34 А
minimum short repeat interval 10 с
I²t / thermal accumulator
```

Локальные ratings действуют дополнительно.

## 18. SINGLE_PACK_MODE

```text
20 А continuous
22 А short ≤1 с
warning at 17 А
minimum short repeat interval 10 с
I²t / thermal accumulator
```

Режим деградированный, но функциональный:

1. вход не выключает свет, 12 В или 5 В нагрузки;
2. фиксированный список запрещённых функций отсутствует;
3. DECK_BALANCE запрещён;
4. brightness автоматически не меняется;
5. GUI показывает батарею, ток, budget и accumulator;
6. recovery второй BMS не подключает батарею автоматически;
7. возврат требует LOCAL_START и проверки безопасного параллельного подключения.

## 19. Power-budget admission control

```text
low-pass = 100 мс
warning ON >85 % for 250 мс
warning OFF <80 % for 2 с
block new noncritical command at predicted ≥100 %
re-enable below 90 % for 2 с
```

Already-enabled loads software budget manager не сбрасывает. Hardware protection, SAFE/HARD_OFF и EXT_KILL имеют приоритет.

## 20. Load classification и profiles

Critical:

```text
5V_CRIT / 3V3_CRIT
supervisor
fault manager
communication
journal retention
```

Noncritical for admission control:

```text
CH1…CH14
5V_OUT1…5V_OUT10
LED1…LED6
```

Для каждой нагрузки:

```text
I_NOM
I_PEAK
T_PEAK
I_INRUSH
```

Unknown profile:

```text
conservative channel maximum
LOAD_PROFILE_UNKNOWN
```

## 21. Guarded SERVICE_OVERRIDE

Выбран вариант B.

Режим:

- доступен только в SERVICE_MODE;
- требует сервисной авторизации;
- требует двойного подтверждения;
- разрешает одну выбранную внешнюю некритическую нагрузку;
- создаёт одноразовое окно 60 с;
- автоматически отключает выбранный output не позднее 60 с;
- не изменяет short limit ≤1 с;
- блокирует predicted current выше short limit;
- полностью журналируется;
- отменяется при reset, communication loss, mode/battery-state change, hardware fault, SAFE/HARD_OFF или EXT_KILL.

Если overridden output держит ток выше continuous limit более 1 с, отключается именно он. Остальные нагрузки не участвуют в обычном software shedding.

Override не применяется к батарейным ключам, critical rails, REMOTE_OFF, safety commands или DECK_BALANCE.

## 22. Механический envelope

Owner-defined available volume:

```text
internal cylinder Ø130 мм × 1000 мм
one welded end
removable connector lid
```

PCB assembly:

```text
maximum width 100 мм
preliminary maximum length 250 мм
maximum total height 80 мм
multilevel
removed together with lid
boards fixed by screws to standoffs
```

Винты, стойки и крышечная механика — owner-controlled. PCB содержат mounting-hole zones и keepout.

Отдельный mandatory carrier/tray не вводится.

## 23. Preliminary packaging candidate PACKAGING-P1

```text
L0: PCB-A + PCB-C
L1: PCB-D + PCB-E
L2: PCB-B
```

Формальная проверка:

```text
L0 length = 110 + 130 = 240 мм <250 мм
L1 length = 125 + 110 = 235 мм <250 мм
L2 length = 180 мм <250 мм
height budget = 79 мм <80 мм
```

Размеры являются area budget и не являются final board outlines.

## 24. Mounting-hole policy

До выбора винтов и стоек:

```text
MOUNT_HOLE_TBD
NO FINAL DRILL
MECHANICAL KEEPOUT ONLY
```

Каждая плата получает не менее четырёх mounting-hole zones, tool access и дополнительные опоры тяжёлых компонентов.

## 25. Вибрационная фиксация

- solder/screws are primary retention;
- heavy components require separate mechanical support;
- polyethylene hot-melt adhesive — auxiliary strain relief/anti-vibration only;
- не используется как единственная опора, около hot components или с нарушением insulation/repairability;
- совместимость с −20…+60 °C и conformal coating проверяется.

## 26. Тепловая архитектура

Запрещены thermal pads, heat spreaders и carrier-to-hull contact.

```text
component
→ PCB copper / internal local heatsink
→ internal air
→ natural convection inside sealed enclosure
```

Thermal verification:

- sealed volume;
- no hull contact;
- ambient +60 °C;
- maximum allowed system load;
- short cycle 1 с / 10 с.

Предварительные потери:

```text
PCB-D at 75 Вт:
6,52…10,23 Вт при η 92…88 %

PCB-E at 180 Вт:
15,65…24,55 Вт при η 92…88 %
```

Потери PCB-E являются существенным thermal blocker. До подтверждения actual LED power и driver efficiency continuous rating не считается термически доказанным.

При превышении температуры корректируются потери, topology/components, площадь/число PCB, внутренняя компоновка или continuous rating.

## 27. Корпус и pressure scope

Pressure-hull material, wall thickness, lid strength and qualification не входят в PCB scope. Корпус принимается owner-provided and qualified.

Герметичность не устраняет external differential pressure; mechanical responsibility остаётся у владельца/изготовителя корпуса.

## 28. HARD_OFF

### Штатный

```text
запретить новые команды
→ отключить heavy loads и electronic power paths
→ сохранить журнал
→ разорвать hold loops
→ подтвердить K_BAT OPEN
→ проверить токи
→ проконтролировать PACK_BUS discharge
→ завершить critical-domain work from EMG
```

### Аварийный

```text
EXT_KILL / critical hardware fault
→ запретить MAIN_SW1/MAIN_SW2
→ разорвать оба hold loop
→ блокировать restart
→ сохранить fault code from EMG if possible
```

## 29. KiCad workspace

Владелец подтвердил, что root project и листы 00…56 открываются нормально. Перед schematic freeze обязательны KiCad version record, ERC release commit и отсутствие `.kicad_prl`.

## 30. Неизменяемые ограничения

Без нового ADR запрещено:

1. добавлять K_MAIN;
2. проводить high current через PCB-B;
3. делать EXT_KILL зависимым от firmware/RS-485/CAN-FD;
4. добавлять active electronics в main battery housings;
5. использовать battery connector для digital communication;
6. объединять 5V_SYS_BUS с 5V_CRIT/3V3_CRIT;
7. питать user power loads от EMG;
8. превращать INTERCONNECT в mandatory active board;
9. automatically restart K_BATx после BMS recovery;
10. использовать корпус как heat sink без нового решения владельца;
11. позволять SERVICE_OVERRIDE обходить аппаратные защиты;
12. замораживать PCB outlines/mounting holes без component-height и 3D review;
13. выбирать part numbers без закрытых входов и расчёта.

## 31. Текущий инженерный рубеж

Закрыты V1.9:

- PCB assembly envelope;
- multilevel mounting/service concept;
- thermal-path restriction;
- short timing/cooldown/I²t;
- filtering/hysteresis;
- critical/noncritical classification;
- load-profile fallback;
- guarded SERVICE_OVERRIDE;
- preliminary packaging candidate;
- module area budgets;
- logical physical interface count;
- preliminary PCB-D/PCB-E branch current classes.

Остаются:

1. BMS BAT_PROT tests;
2. K_BATx/REMOTE_OFF candidate selection and tests;
3. preliminary KiCad board outlines and mounting-hole zones;
4. component-height/3D clearance review;
5. A↔B connector 32 vs 16+16 decision;
6. physical CAN-FD node order and termination;
7. PCB-B critical branch current calculation;
8. refinement PCB-D/PCB-E efficiency and ripple calculations;
9. connector class comparison and selection;
10. thermal calculations/tests without hull contact;
11. release ERC.

Разрешено продолжать расчёты и component selection по узлам с закрытыми входными данными.
