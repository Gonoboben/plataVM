# Главная концепция проекта ПДУ БНПА / PlataVM

Дата исходной фиксации: 2026-07-01  
Дата актуализации: 2026-07-21  
Статус:

```text
главный управляющий документ проекта
V1.7 owner-input-reviewed baseline
```

## 1. Назначение

Документ фиксирует верхнеуровневую концепцию PlataVM и является главным входом для схемы, PCB, BOM, прошивки, механики, испытаний и выпускной документации.

Подробности вынесены в:

```text
Docs/ARCHITECTURE_BASELINE.md
Docs/KBAT_ELECTRICAL_REQUIREMENTS.md
Docs/INTERBOARD_INTERFACES.md
Docs/SYSTEM_POWER_BUDGET_POLICY.md
Docs/MECHANICAL_ENVELOPE_V1_7.md
Docs/OPEN_QUESTIONS.md
```

## 2. Граница проекта

В проект входят:

1. две основные АКБ LiFePO4 4S24P, 12,8 В, 144 А·ч;
2. автономные BMS каждой основной АКБ;
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
15. MCU, внешний isolated RS-485 и внутренняя CAN-FD;
16. DECK_BALANCE;
17. DUAL_PACK_RUN и SINGLE_PACK_MODE;
18. общий power-budget manager;
19. цилиндрический корпус электроники и внутренняя компоновка;
20. схемы, PCB, BOM, firmware, GUI, тесты и документация.

## 3. Замороженная системная архитектура

### 3.1 Основные АКБ

```text
АКБ_1 cells → autonomous BMS → fuse → K_BAT1 → СН-176А-12 → BFE_1 ┐
                                                                                   ├→ PACK_BUS
АКБ_2 cells → autonomous BMS → fuse → K_BAT2 → СН-176А-12 → BFE_2 ┘
```

Принято:

1. обе исправные АКБ работают параллельно в `DUAL_PACK_RUN`;
2. اختلافия напряжений, токов и расчётного SoC используются для диагностики, но сами по себе не отключают исправную батарею;
3. BMS рассматривается как закрытый автономный двухполюсный защищённый источник;
4. raw-ветвь, внутренние точки и цифровое управление BMS не используются;
5. автоматический restart после восстановления BMS запрещён;
6. межблочное выравнивание выполняется только в `DECK_BALANCE`.

### 3.2 Главная шина

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

Высокие токи распределяются от PCB-A и не проходят через PCB-B или сигнальную backplane.

## 4. Корпуса основных АКБ

В каждом корпусе основной АКБ находятся только:

1. сборка 4S24P;
2. существующая автономная BMS;
3. силовой предохранитель;
4. F_CTRL у ответвления BAT_PROT+;
5. моностабильный K_BATx;
6. одна катушка continuous duty;
7. механически связанный K_BAT_AUX_NO;
8. LOCAL_START wiring;
9. минимальная пассивная suppression;
10. необходимая силовая проводка.

Не устанавливаются:

- MCU;
- дополнительная управляющая плата;
- CAN/RS-485/UART;
- обязательная цифровая телеметрия BMS;
- raw-доступ к ячейкам или внутренним точкам BMS;
- отдельный DC/DC для управляющей электроники.

## 5. СН-176А-12 и LOCAL_START

Рабочая распайка:

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
- включён параллельно K_BAT_AUX_NO.

Батарейная линия СН-176А-12 находится в owner-controlled scope. Её внешние ограничения учитываются в системном power budget независимо от исключения из текущей инженерной верификации.

## 6. K_BATx

K_BAT1/K_BAT2:

- одинаковые;
- однополюсные по положительному проводнику;
- SPST-NO;
- моностабильные;
- пружинный возврат в OPEN;
- одна катушка continuous duty;
- economizer preferred;
- электрический самоподхват через K_BAT_AUX_NO.

Функциональная цепь:

```text
BAT_PROT+ → F_CTRL → (LOCAL_START_NO ∥ K_BAT_AUX_NO)
→ K_BAT_COIL → pin 11
→ REMOTE_OFF_RUN_CONTACT
→ EXT_KILL series path
→ BAT_PROT−
```

Предварительная база:

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
| End-of-life contact resistance | ≤5 мОм |
| Operating temperature | −20…+60 °C |
| Mechanical life | ≥100 000 циклов |
| Electrical life | ≥10 000 операций |

Конкретная модель не выбирается до candidate table, паспортной проверки и стендовых испытаний.

## 7. REMOTE_OFF и EXT_KILL

REMOTE_OFF реализуется по принципу:

```text
energize-to-run relay
physical NO run contact
```

Логика:

```text
healthy critical power + healthy supervisor
→ relay energized
→ NO run contact CLOSED

loss of critical power / supervisor fault / OFF command
→ relay de-energized
→ NO run contact OPEN
→ K_BAT hold loop OPEN
```

Для двух АКБ используются два независимых run-contact.

EXT_KILL:

- включён в физический последовательный путь удержания;
- разрывает оба hold loop;
- запрещает MAIN_SW1/MAIN_SW2;
- независим от MCU, RS-485 и CAN-FD;
- имеет приоритет над LOCAL_START;
- после восстановления не вызывает автоматический restart.

Время:

```text
t_OFF ≥ max(250 мс; 5 × t_release_max)
t_release_system target ≤100 мс
```

`HARD_OFF_FAILED` и `WELDED_CONTACT` блокируют повторный запуск.

## 8. PCB-A_BFE_POWER

PCB-A выполняет:

1. два симметричных Battery Front-End;
2. измерение токов и напряжений батарейных ветвей;
3. MAIN_SW1/MAIN_SW2;
4. BALANCE_SW1/BALANCE_SW2;
5. формирование PACK_BUS;
6. PACK_BUS discharge;
7. final hardware actions EXT_KILL;
8. распределение силовых ветвей PCB-B/C/D/E.

PCB-A не содержит главный MCU и не заменяет контакторы K_BATx.

## 9. PCB-B_CTRL_RESERVE

PCB-B содержит:

1. центральный MCU семейства STM32G4;
2. 5V_CRIT/3V3_CRIT;
3. EMG_4S2P charge/ORing/KEEP_ALIVE;
4. watchdog и supervisor;
5. fault manager;
6. внешний isolated RS-485 half-duplex;
7. внутренний CAN-FD master/control node;
8. direct hardware safety/fault interfaces;
9. единственную контролируемую точку SIGNAL_GND–POWER_GND;
10. service/debug.

PCB-B не проводит суммарные токи пользовательских нагрузок.

## 10. PCB-C_POWER_12V

Принято:

- 14 каналов CH1…CH14;
- CH1…CH11 normally controlled;
- CH12…CH14 Always-On monitored в RUN;
- 3 А continuous и 5 А peak до 1 с на канал;
- hardware board rating 30 А continuous;
- индивидуальная защита и current diagnostics;
- локальный MCU/I/O/ADC;
- normal commands/telemetry по CAN-FD;
- direct P12_GROUP_SAFE_OFF и P12_GROUP_HARD_OFF;
- direct P12_BOARD_FAULT_N.

## 11. PCB-D_POWER_5V

Принято:

- PACK_BUS → 5V_SYS_BUS;
- preliminary topology — two-phase synchronous buck;
- 15 А continuous / 20 А short на 5V_SYS_BUS;
- 10 выходов до 3 А;
- OUT1…OUT7 controlled;
- OUT8…OUT10 Always-On monitored;
- индивидуальная защита и current diagnostics;
- локальный MCU/I/O/ADC;
- normal commands/telemetry по CAN-FD;
- direct P5_GROUP_SAFE_OFF, P5_GROUP_HARD_OFF и P5_BOARD_FAULT_N.

`5V_SYS_BUS` не питает PCB-B critical domain и не питается от EMG.

## 12. PCB-E_LIGHT_POWER

Принято:

- шесть независимых LED-driver channels;
- две симметричные зоны 2×3;
- functional input 8…16 В;
- локальное регулирование тока;
- local PWM generation;
- PWM 3,3 В active-high;
- default 1 кГц, configurable 100…1000 Гц;
- normal setpoints/telemetry по CAN-FD;
- direct LIGHT_GROUP_HARD_OFF;
- direct LIGHT_BOARD_FAULT_N;
- default safe state — все LED OFF;
- отдельный automatic brightness limit в SINGLE_PACK_MODE отсутствует.

## 13. Внешняя и внутренняя связь

Внешняя связь:

```text
isolated RS-485
half-duplex
115200 bit/s preliminary
8N1
addressed binary protocol
CRC-16
sequence number
heartbeat / timeout
```

Внутренняя связь PCB-B↔PCB-C/D/E:

```text
CAN_INT_H
CAN_INT_L
```

По CAN-FD передаются normal commands, configuration, setpoints, per-channel telemetry и service data.

Отдельными проводами остаются SAFE/HARD_OFF и board-fault summary.

CAN-FD не заменяет аппаратную безопасность.

## 14. Земли, корпус и экраны

Используются отдельные сети:

```text
POWER_GND
SIGNAL_GND
ISO_GND
CHASSIS
```

Принято:

1. SIGNAL_GND соединяется с POWER_GND в одной контролируемой точке PCB-B;
2. ISO_GND остаётся DC-isolated;
3. экраны подключаются к CHASSIS у ввода;
4. optional HF coupling ISO_GND–CHASSIS допускается только после EMC review;
5. безымянный общий GND, скрывающий домены, запрещён.

## 15. DECK_BALANCE

DECK_BALANCE:

- выполняется только на палубе;
- требует две доступные батареи;
- требует отключённые тяжёлые нагрузки;
- nominal current 2 А;
- hard limit 3 А;
- preliminary finish: abs(ΔU) ≤50 мВ и abs(I) ≤0,2 А в течение 60 с;
- разрешён только при подтверждённой температуре батарей 0…45 °C;
- запрещён в SINGLE_PACK_MODE.

Тайм-аут и no-progress criterion остаются расчётно-испытательными параметрами.

## 16. DUAL_PACK_RUN

Условия:

```text
обе батареи доступны
обе ветви подключены
нет battery isolation fault
не DECK_BALANCE
```

Системный предел PACK_BUS:

```text
40 А continuous
44 А short
warning at 34 А
```

Локальные ratings плат и каналов действуют дополнительно.

## 17. SINGLE_PACK_MODE

`SINGLE_PACK_MODE` — деградированный, но функциональный режим одной основной АКБ.

Системный предел:

```text
20 А continuous
22 А short
warning at 17 А
```

Правила:

1. сам вход в режим не выключает свет, 12 В или 5 В нагрузки;
2. сам вход не создаёт фиксированный список запрещённых функций;
3. DECK_BALANCE запрещён;
4. отдельное снижение яркости отсутствует;
5. GUI показывает активную батарею, причину режима, ток и остаточный бюджет;
6. восстановление второй BMS не подключает батарею автоматически;
7. возврат к DUAL_PACK_RUN требует нового LOCAL_START и проверки безопасного параллельного подключения.

## 18. Power-budget command policy

Для активного режима:

```text
85 % continuous limit → warning
100 % continuous limit → reject new noncritical load command
```

Дополнительно:

- учитывается фактический суммарный ток PACK_BUS;
- яркость автоматически не меняется;
- уже включённые пользовательские нагрузки обычным software budget manager не сбрасываются;
- hardware protection, SAFE_OFF, HARD_OFF и EXT_KILL имеют приоритет;
- service override разрешён только в диагностическом режиме с журналированием;
- service override не отменяет аппаратные защиты.

До отдельного решения внешние CH/5V_OUT/LED считаются некритическими для admission control, а PCB-B critical domain — критическим.

## 19. HARD_OFF

### 19.1 Штатный

```text
запретить новые команды
→ отключить тяжёлые нагрузки и электронные силовые тракты
→ сохранить журнал
→ разорвать hold loops K_BAT1/K_BAT2
→ подтвердить отпускание контакторов
→ проверить токи батарейных ветвей
→ проконтролировать разряд PACK_BUS
→ завершить работу critical domain от EMG
```

### 19.2 Аварийный

```text
EXT_KILL / critical hardware fault
→ независимо от firmware запретить MAIN_SW1/MAIN_SW2
→ разорвать оба hold loop
→ заблокировать restart
→ сохранить fault code от EMG, если critical domain остаётся работоспособным
```

## 20. Условия эксплуатации

Принято:

```text
operating temperature: −20…+60 °C
storage temperature: −30…+70 °C
high humidity
possible condensation
marine atmosphere
conformal coating required
```

Внутренний корпус штатно сухой. Вибрационный, ударный и pressure profile остаются открытыми.

## 21. Корпус электроники

Подтверждён внешний envelope:

```text
цилиндр
наружный диаметр 130 мм
длина 1000 мм
один торец заварен
второй торец — съёмная крышка с разъёмами
```

Сервисная концепция:

- доступ со стороны крышки;
- продольный извлекаемый carrier/tray;
- глухой торец не требует обслуживания;
- PCB-A около батарейных вводов;
- PCB-C/D/E около соответствующих выходных жгутов;
- PCB-B в наименее шумной зоне;
- силовые шины и CAN/direct hard lines трассируются раздельно.

Внутренний диаметр, материал, полезная длина, pressure rating, connector map, carrier и thermal interface пока не определены.

## 22. KiCad workspace

Владелец подтвердил, что текущий root project и листы 00…56 открываются нормально.

Перед schematic freeze обязательны:

1. повторный parsing review release commit;
2. запись версии KiCad;
3. ERC;
4. отсутствие `.kicad_prl` в репозитории.

## 23. Неизменяемые ограничения

Запрещено без нового ADR:

1. добавлять `K_MAIN`;
2. проводить высокие токи через PCB-B;
3. делать EXT_KILL зависимым от MCU, RS-485 или CAN-FD;
4. добавлять активную дополнительную электронику в основные АКБ;
5. использовать батарейный соединитель для цифровой связи;
6. объединять 5V_SYS_BUS с 5V_CRIT/3V3_CRIT;
7. питать пользовательские силовые нагрузки от EMG;
8. превращать INTERCONNECT в обязательную активную плату;
9. автоматически запускать K_BATx после BMS recovery;
10. выбирать конкретные part numbers без закрытых входных данных, расчёта и проверки.

## 24. Текущий инженерный рубеж

Owner-level решения V1.7 закрыли:

- стартовый общий power budget;
- SINGLE_PACK_MODE;
- warning/block policy;
- базовые environmental requirements;
- внешний механический envelope;
- текущую owner verification KiCad workspace.

Следующие блокеры полного Gate G-R:

1. BMS BAT_PROT fault/recovery tests;
2. K_BATx и REMOTE_OFF relay candidate selection/tests;
3. internal dimensions, pressure/vibration и 3D packaging;
4. physical CAN-FD/hard-line pin count и connector selection;
5. short-limit timing, filters/hysteresis и реальные load profiles.

Разрешено продолжать расчёты и component selection по узлам, для которых входные данные закрыты и которые не зависят от перечисленных блокеров.
