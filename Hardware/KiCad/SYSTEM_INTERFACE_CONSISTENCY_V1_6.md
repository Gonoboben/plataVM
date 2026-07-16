# PlataVM KiCad system interface consistency — V1.6

Дата: 2026-07-16  
Статус: `PASS WITH CONTROLLED PLACEHOLDERS`

## 1. Область проверки

Проверены и синхронизированы архитектурные листы:

```text
02_INTERBOARD_POWER_AND_CONTROL.kicad_sch
17_REMOTE_OFF_AND_EXT_KILL.kicad_sch
20_CTRL_RESERVE_TOP.kicad_sch
23_MCU_CORE.kicad_sch
27_CONTROL_IO.kicad_sch
29_CTRL_CONNECTORS_TESTPOINTS.kicad_sch
30_POWER_12V_TOP.kicad_sch
40_POWER_5V_TOP.kicad_sch
50_LIGHT_POWER_TOP.kicad_sch
```

## 2. Принятый межплатный контракт

### PCB-A ↔ PCB-B

Критические команды и измерения остаются прямыми. Внутренняя CAN-FD не является обязательным путём отключения основных АКБ.

### PCB-B ↔ PCB-C/D/E

Нормальные команды, setpoints и подробная телеметрия передаются через:

```text
CAN_INT_H
CAN_INT_L
```

Отдельными аппаратными линиями остаются:

```text
P12_GROUP_SAFE_OFF
P12_GROUP_HARD_OFF
P12_BOARD_FAULT_N

P5_GROUP_SAFE_OFF
P5_GROUP_HARD_OFF
P5_BOARD_FAULT_N

LIGHT_GROUP_HARD_OFF
LIGHT_BOARD_FAULT_N
```

Per-channel names сохраняются как внутренние функциональные/data-object contracts и не учитываются как обязательные отдельные контакты межплатного разъёма.

## 3. REMOTE_OFF / EXT_KILL

Устранена противоречивая физическая семантика `REMOTE_OFF_NC`.

Принято:

```text
energize-to-run REMOTE_OFF relay
physical NO run contact
```

Канонические placeholder names:

```text
BAT1_REMOTE_OFF_RUN_NO_TBD
BAT2_REMOTE_OFF_RUN_NO_TBD
```

EXT_KILL остаётся отдельным последовательным аппаратным путём и не зависит от MCU, CAN-FD или внешнего RS-485.

## 4. Ground/chassis policy

Добавлена единственная контролируемая точка:

```text
SIGNAL_GND_POWER_GND_NET_TIE
NET_TIE_GND_B
```

Сохраняются отдельные domains:

```text
POWER_GND
SIGNAL_GND
ISO_GND
CHASSIS
```

ISO_GND не соединяется с SIGNAL_GND по постоянному току. Экраны подключаются к CHASSIS у ввода. Компоненты net-tie и HF coupling пока не выбраны.

## 5. Проверка неизменяемых ограничений

| Ограничение | Результат |
|---|---|
| Центральный K_MAIN отсутствует | PASS |
| Высокие токи не проходят через PCB-B | PASS |
| EXT_KILL независим от firmware и цифровых шин | PASS |
| INTERCONNECT остаётся пассивным | PASS |
| Активная электроника в основные АКБ не добавлена | PASS |
| Внешний интерфейс остаётся isolated RS-485 | PASS |
| Внутренняя CAN-FD не заменяет hardware OFF | PASS |
| Автоматический restart после BMS recovery запрещён | PASS |
| Компоненты, footprints, BOM и layout не выбраны преждевременно | PASS |

## 6. Автоматическая структурная проверка

Для девяти изменённых `.kicad_sch` выполнены:

1. проверка баланса S-expression parentheses;
2. проверка закрытия строковых литералов;
3. проверка наличия `CAN_INT_H`/`CAN_INT_L`;
4. проверка наличия direct safety/fault lines;
5. проверка наличия ground net-tie boundaries;
6. проверка отсутствия `REMOTE_OFF_NC_TBD`;
7. проверка отсутствия `K_MAIN`.

Результат: `PASS`.

## 7. Контролируемые placeholders

Пока не выбраны:

1. CAN-FD transceivers и termination;
2. MCU package и локальные MCU/IO implementations PCB-C/D/E;
3. физические межплатные разъёмы и pinout;
4. energize-to-run relay part number;
5. EXT_KILL contact implementation;
6. ground net-tie/RC/ferrite/Y-cap components;
7. ESD/common-mode protection;
8. footprints, BOM и PCB layout.

## 8. Следующий gate

Перед physical pinout freeze необходимо:

1. получить ответы V1.7 по 3D-компоновке и условиям эксплуатации;
2. определить порядок CAN-FD nodes и места termination;
3. выполнить окончательный hard-line/power pin count;
4. выбрать физические разъёмы;
5. открыть изменённые листы в установленной версии KiCad и выполнить ERC/parsing review.
