# Межплатные интерфейсы PlataVM

Дата актуализации: 2026-07-16  
Статус:

```text
V1.6 LOGICAL/TRANSPORT BASELINE
CAN-FD for normal PCB-B↔PCB-C/D/E traffic; direct hardware safe lines retained
```

## 1. Назначение

Документ задаёт силовые, управляющие, диагностические и коммуникационные связи между PCB-A…PCB-E. Физические разъёмы и окончательный pinout выбираются после 3D-компоновки и подсчёта контактов.

## 2. Базовые правила

1. Силовые токи не проходят через `PCB-B_CTRL_RESERVE`.
2. `PACK_BUS` и `POWER_GND` распределяются от PCB-A отдельными рассчитанными ветвями.
3. INTERCONNECT не содержит активных компонентов.
4. PCB-C/D/E получают локальное питание, защиту и локальные I/O/ADC.
5. Нормальные команды и подробная телеметрия PCB-B↔PCB-C/D/E передаются по внутренней CAN-FD.
6. `SAFE_OFF`, `HARD_OFF`, EXT_KILL и критические fault summary не зависят от CAN-FD.
7. PCB-A↔PCB-B сохраняет прямые critical control/measurement paths.
8. Внешний isolated RS-485 не используется как внутренняя шина.
9. `POWER_GND`, `SIGNAL_GND`, `ISO_GND` и `CHASSIS` не объединяются произвольно.
10. Отсоединение любого межплатного разъёма должно переводить соответствующую силовую функцию в безопасное состояние.

## 3. Силовое распределение от PCB-A

| Получатель | Питание | Возврат | Назначение | HARD_OFF |
|---|---|---|---|---|
| PCB-B | `PACK_BUS_CRIT_IN` | `POWER_GND` | critical power / EMG charge path | critical domain переходит на EMG |
| PCB-C | `PACK_BUS_P12_IN` | `POWER_GND` | 14 каналов 12 В | OFF |
| PCB-D | `PACK_BUS_P5_IN` | `POWER_GND` | DC/DC и внешние 5 В | OFF |
| PCB-E | `PACK_BUS_LIGHT_IN` | `POWER_GND` | LED-драйверы | OFF |

Силовые ветви выполняются отдельными шинами/жгутами и не используют сигнальную backplane как токонесущий элемент.

## 4. PCB-A_BFE_POWER ↔ PCB-B_CTRL_RESERVE

### 4.1 Прямое управление B→A

| Сигнал | Назначение | Safe state |
|---|---|---|
| `BAT1_MAIN_SW_EN` | разрешение MAIN_SW1 | OFF |
| `BAT2_MAIN_SW_EN` | разрешение MAIN_SW2 | OFF |
| `BAT1_BALANCE_SW_EN` | BALANCE_SW1 | OFF |
| `BAT2_BALANCE_SW_EN` | BALANCE_SW2 | OFF |
| `BAT1_HOLD_LOOP_OPEN_CMD` | штатное открытие hold loop АКБ_1 | OPEN при активной команде |
| `BAT2_HOLD_LOOP_OPEN_CMD` | штатное открытие hold loop АКБ_2 | OPEN при активной команде |
| `PACK_BUS_DISCHARGE_EN` | управляемый разряд PACK_BUS | OFF |
| `EXT_KILL_HW_CHAIN` | независимый аппаратный HARD_OFF | оба MAIN_SW OFF, оба hold loop OPEN |

### 4.2 Прямая диагностика A→B

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

Аналоговые каналы сопровождаются явной reference net и не маршрутизируются как неопределённые одиночные сигналы.

### 4.3 Аппаратный EXT_KILL

Канонические конечные действия:

```text
BAT1_HOLD_LOOP_OPEN_HW
BAT2_HOLD_LOOP_OPEN_HW
BAT1_MAIN_SW_OFF_HW
BAT2_MAIN_SW_OFF_HW
```

MCU может регистрировать событие, но не участвует в обязательном пути отключения.

## 5. Внутренняя CAN-FD PCB-B↔PCB-C/D/E

### 5.1 Назначение

CAN-FD переносит:

- normal enable/configuration commands;
- per-channel current/voltage/temperature telemetry;
- channel fault details;
- board state, counters and service data;
- firmware/service diagnostics.

CAN-FD не переносит единственный экземпляр команды HARD_OFF и не является условием работы EXT_KILL.

### 5.2 Логические линии физического уровня

Предварительные net names:

```text
CAN_INT_H
CAN_INT_L
CAN_INT_SHIELD / CHASSIS reference as defined by harness
```

Топология — линейная шина с termination на двух физических концах. Конкретные платы-концы, длины stub и номиналы common-mode/ESD protection определяются после 3D-компоновки.

### 5.3 Поведение при потере связи

1. локальная аппаратная защита каждого канала продолжает работать;
2. новые normal commands не принимаются;
3. платы переходят в заранее определённый communication-loss state;
4. hard safety lines остаются работоспособными;
5. board fault/communication loss отображается в GUI;
6. автоматический restart силовых функций без разрешения PCB-B запрещён.

## 6. PCB-C_POWER_12V ↔ PCB-B

### 6.1 Прямые аппаратные линии B→C

```text
P12_GROUP_SAFE_OFF
P12_GROUP_HARD_OFF
```

`P12_GROUP_HARD_OFF` имеет аппаратный приоритет над CAN-FD commands.

### 6.2 Прямая fault summary C→B

```text
P12_BOARD_FAULT_N
```

### 6.3 Логические объекты CAN-FD

```text
P12_CH_EN[1..11]
P12_CH_FAULT_N[1..14]
P12_CH_ISENSE[1..14]
P12_INPUT_VSENSE
P12_BOARD_TEMP
P12 board status/configuration
```

CH12…CH14 — Always-On monitored в RUN, но отключаются индивидуальной защитой, SAFE и HARD_OFF.

## 7. PCB-D_POWER_5V ↔ PCB-B

### 7.1 Прямые аппаратные линии B→D

```text
P5_GROUP_SAFE_OFF
P5_GROUP_HARD_OFF
```

### 7.2 Прямая fault summary D→B

```text
P5_BOARD_FAULT_N
```

### 7.3 Логические объекты CAN-FD

```text
5V_SYS_EN
P5_OUT_EN[1..7]
P5_OUT_FAULT_N[1..10]
P5_OUT_ISENSE[1..10]
5V_SYS_VSENSE
5V_SYS_TOTAL_ISENSE
P5_BOARD_TEMP
P5 board status/configuration
```

OUT8…OUT10 — Always-On monitored в RUN, но отключаются защитой, SAFE и HARD_OFF.

## 8. PCB-E_LIGHT_POWER ↔ PCB-B

### 8.1 Прямые аппаратные линии B→E

```text
LIGHT_GROUP_HARD_OFF
```

При необходимости отдельная `LIGHT_GROUP_SAFE_OFF` добавляется только новым интерфейсным решением; baseline safe state достигается снятием разрешения и HARD_OFF.

### 8.2 Прямая fault summary E→B

```text
LIGHT_BOARD_FAULT_N
```

### 8.3 Логические объекты CAN-FD

```text
LIGHT_BRANCH_EN
LED_PWM[1..6] command values
LED_FAULT_N[1..6]
LED_ISENSE[1..6]
LIGHT_INPUT_VSENSE
LIGHT_BOARD_TEMP
LIGHT board status/configuration
```

Физические PWM-последовательности формируются локально на PCB-E. CAN-FD передаёт заданные значения яркости, а не шесть высокочастотных PWM-линий через межплатный жгут.

## 9. PCB-B external interfaces

1. isolated RS-485 half-duplex;
2. hardware `EXT_KILL` input;
3. SWD и service UART;
4. EMG_4S2P connection;
5. сервисные I/O только после отдельного решения.

Предварительный внешний протокол RS-485:

```text
115200 bit/s
8N1
half-duplex
addressed binary frames
CRC-16
sequence number
timeout
heartbeat
```

## 10. Ground, shield and reference domains

| Сеть | Назначение |
|---|---|
| `POWER_GND` | силовой возврат |
| `SIGNAL_GND` | reference MCU и измерений |
| `ISO_GND` | isolated RS-485 side |
| `CHASSIS` | корпус и кабельные экраны |

Политика:

1. одна контролируемая точка `SIGNAL_GND–POWER_GND` на PCB-B;
2. подключение через net-tie/конфигурируемый элемент;
3. экраны соединяются с CHASSIS у ввода;
4. ISO_GND плавающий по DC;
5. опциональная ВЧ-связь ISO_GND–CHASSIS после EMC review;
6. безымянный `GND` в межплатных контрактах запрещён.

## 11. Классы соединений

1. `PWR-HI` — PACK_BUS и POWER_GND;
2. `PWR-CRIT` — critical power;
3. `CTRL-SAFE` — EXT_KILL, SAFE_OFF, HARD_OFF;
4. `FAULT-SUMMARY` — прямые board fault lines;
5. `COMM-INTERNAL` — CAN-FD;
6. `COMM-ISOLATED` — внешний RS-485;
7. `SERVICE` — SWD/UART/test.

## 12. Требования к физическому разъёму

Для каждого разъёма перед schematic freeze указываются:

1. обозначение и ответная часть;
2. pin number и net name;
3. направление и safe state;
4. длительный/пиковый ток;
5. рабочее напряжение;
6. reference domain;
7. тип сигнала и скорость;
8. требования к витой паре/экрану;
9. допустимое состояние при разъединении;
10. keying и защита от неверного подключения;
11. vibration rating и число циклов;
12. creepage/clearance.

Для сигнальных разъёмов предусматривается запас контактов 20–30 %.

## 13. Reference designators

| Плата | Диапазон |
|---|---:|
| PCB-A | 100–199 |
| PCB-B | 200–299 |
| PCB-C | 300–399 |
| PCB-D | 400–499 |
| PCB-E | 500–599 |

## 14. Следующий шаг

1. обновить логическую карту `02_INTERBOARD_POWER_AND_CONTROL` под CAN-FD + hard lines;
2. определить CAN-FD node order по 3D-компоновке;
3. подсчитать hard-line и power pin count;
4. выбрать физические разъёмы и pinout;
5. выполнить EMC/fault review communication-loss modes;
6. после этого заморозить межплатный жгут/backplane.
