# Предварительный area budget PCB-A…PCB-E — PlataVM V1.9

Дата: 2026-07-21  
Основание: `Docs/PCB_PACKAGING_BOUNDARY_V1_9.md`  
Статус: `PRELIMINARY FUNCTIONAL FLOORPLAN — DIMENSIONS NOT FROZEN`

## 1. Назначение

Документ распределяет доступную площадь и высоту между пятью PCB-модулями до выбора конкретных компонентов. Значения используются для оценки реализуемости, pin count, connector classes и component candidate search.

Размеры не являются производственными контурами плат.

## 2. Сводный бюджет

| Плата | Целевой outline | Допустимый предварительный максимум | Высота компонентов над PCB | Уровень |
|---|---:|---:|---:|---|
| PCB-A_BFE_POWER | 94 × 110 мм | 100 × 120 мм | ≤23 мм | L0 |
| PCB-B_CTRL_RESERVE | 94 × 180 мм | 100 × 220 мм | ≤16 мм | L2 |
| PCB-C_POWER_12V | 94 × 130 мм | 100 × 145 мм | ≤23 мм | L0 |
| PCB-D_POWER_5V | 94 × 125 мм | 100 × 140 мм | ≤23 мм | L1 |
| PCB-E_LIGHT_POWER | 94 × 110 мм | 100 × 130 мм | ≤23 мм | L1 |

Проверка длины уровней:

```text
L0: PCB-A 110 + PCB-C 130 = 240 мм
L1: PCB-D 125 + PCB-E 110 = 235 мм
L2: PCB-B 180 мм
```

Остающийся резерв используется под межплатный зазор, изгиб жгута и технологический доступ.

## 3. PCB-A_BFE_POWER

### 3.1 Функциональные блоки

```text
BAT1 input / BFE_1
BAT2 input / BFE_2
MAIN_SW1 / MAIN_SW2
BALANCE_SW1 / BALANCE_SW2
current sensing
voltage sensing
PACK_BUS node
PACK_BUS discharge
four branch outputs to PCB-B/C/D/E
hardware EXT_KILL final action
control/diagnostic interface to PCB-B
```

### 3.2 Зональность

| Зона | Предварительная площадь | Требования |
|---|---:|---|
| A1 BAT1 BFE | 38 × 42 мм | симметрия с A2; короткий high-current path |
| A2 BAT2 BFE | 38 × 42 мм | симметрия с A1 |
| A3 PACK_BUS distribution | 18 × 90 мм | центральная шина/узел распределения |
| A4 DECK_BALANCE | 28 × 45 мм | отдельная ограниченная ветвь 2/3 А |
| A5 sensing/control | 28 × 55 мм | удаление от switching/gate loops |
| A6 branch connectors | edge allocation | PCB-B/C/D/E отдельными ответвлениями |

### 3.3 Правила

1. BFE_1 и BFE_2 должны оставаться зеркально симметричными.
2. Токи батарей не проходят через control zone.
3. PACK_BUS распределяется звездой/короткими ответвлениями, а не последовательно через платы.
4. Shunt/Kelvin routing отделяется от gate drive и discharge path.
5. PCB-A не содержит главный MCU.
6. Mounting-hole zones не пересекают BAT/PACK copper.

## 4. PCB-B_CTRL_RESERVE

### 4.1 Функциональные блоки

```text
PACK_BUS_CRIT_IN protection
EMG_4S2P charge / ORing / KEEP_ALIVE
5V_CRIT / 3V3_CRIT
STM32G4 central MCU
supervisor / watchdog
fault manager
isolated RS-485
internal CAN-FD
REMOTE_OFF relay control
EXT_KILL sensing/fanout
service/debug
controlled SIGNAL_GND–POWER_GND point
```

### 4.2 Зональность

| Зона | Предварительная площадь | Требования |
|---|---:|---|
| B1 critical input/ORing | 35 × 45 мм | у входа PACK_BUS_CRIT_IN/EMG |
| B2 DC/DC critical rails | 35 × 45 мм | минимальные loops, отдельная от analog |
| B3 MCU/digital core | 45 × 55 мм | центральная low-noise zone |
| B4 supervisor/fault manager | 30 × 45 мм | независимые hardware paths |
| B5 isolated RS-485 | 30 × 50 мм | isolation gap и ISO_GND |
| B6 CAN-FD/direct hard lines | 30 × 55 мм | ближе к interboard interface |
| B7 service/debug | 25 × 35 мм | доступ после извлечения сборки |

### 4.3 Правила

1. Высота ограничена 16 мм для верхнего уровня.
2. Высокие токи пользовательских нагрузок отсутствуют.
3. RS-485 isolation barrier не пересекается copper/adhesive/coating bridge.
4. Единственная controlled point SIGNAL_GND–POWER_GND находится на PCB-B.
5. SERVICE_OVERRIDE реализуется только firmware/UI и не требует hardware bypass path.

## 5. PCB-C_POWER_12V

### 5.1 Функциональные блоки

```text
PACK_BUS_P12_IN protection
14 protected high-side channels
14 current diagnostics
CH1…CH11 controlled
CH12…CH14 Always-On monitored
local STM32G4/I/O/ADC
CAN-FD
P12_GROUP_SAFE_OFF
P12_GROUP_HARD_OFF
P12_BOARD_FAULT_N
```

### 5.2 Канальная структура

Предварительно используются две одинаковые банки:

```text
BANK-C1: CH1…CH7
BANK-C2: CH8…CH14
```

Area cell одного канала до выбора компонента:

```text
12 × 22 мм target
```

В cell входят:

- switch/protection placeholder;
- current-sense placeholder;
- local decoupling;
- output connector allocation;
- thermal copper allowance.

### 5.3 Зональность

| Зона | Предварительная площадь |
|---|---:|
| C1 input/protection | 30 × 35 мм |
| C2 channel bank 1 | 88 × 45 мм |
| C3 channel bank 2 | 88 × 45 мм |
| C4 local control/CAN | 35 × 45 мм |
| C5 output connector edges | по двум длинным краям |

### 5.4 Правила

1. 30 А — hardware board rating, но общий режим ограничен system budget.
2. Channel cells должны быть повторяемыми.
3. SAFE/HARD_OFF действует независимо от CAN-FD.
4. Service override допускается только для одного выбранного CH и не отменяет local protection.

## 6. PCB-D_POWER_5V

### 6.1 Функциональные блоки

```text
PACK_BUS_P5_IN protection
preliminary two-phase synchronous buck
5V_SYS_BUS 15 А continuous / 20 А short
10 protected outputs
10 current diagnostics
local STM32G4/I/O/ADC
CAN-FD
P5_GROUP_SAFE_OFF
P5_GROUP_HARD_OFF
P5_BOARD_FAULT_N
```

### 6.2 Зональность

| Зона | Предварительная площадь | Требования |
|---|---:|---|
| D1 input EMI/protection | 30 × 35 мм | короткая петля к power stage |
| D2 phase 1 | 38 × 45 мм | симметрия с D3 |
| D3 phase 2 | 38 × 45 мм | симметрия с D2 |
| D4 output capacitors/bus | 80 × 28 мм | распределение 5V_SYS_BUS |
| D5 output protection 1…5 | 88 × 30 мм | повторяемые cells |
| D6 output protection 6…10 | 88 × 30 мм | повторяемые cells |
| D7 local control/CAN | 32 × 42 мм | удаление от switch nodes |

### 6.3 Тепловое ограничение

PCB-D не использует корпус как heatsink. Поэтому candidate selection должен обеспечить:

- низкие switching/conduction losses;
- допустимую температуру при +60 °C internal ambient;
- распределение тепла по PCB copper;
- высоту магнитных компонентов ≤23 мм;
- отсутствие обязательного принудительного обдува.

Если расчёт не проходит, continuous rating уменьшается либо topology/area пересматриваются.

## 7. PCB-E_LIGHT_POWER

### 7.1 Функциональные блоки

```text
PACK_BUS_LIGHT_IN protection
six independent LED current drivers
two zones 2×3
local PWM generation
six current diagnostics
open/short/thermal diagnostics
local STM32G4/I/O/ADC
CAN-FD
LIGHT_GROUP_HARD_OFF
LIGHT_BOARD_FAULT_N
```

### 7.2 Зональность

| Зона | Предварительная площадь |
|---|---:|
| E1 input/protection | 30 × 35 мм |
| E2 zone A, LED1…3 | 88 × 35 мм |
| E3 zone B, LED4…6 | 88 × 35 мм |
| E4 local control/CAN | 35 × 42 мм |
| E5 output connectors | edge allocation |

Area cell одного LED driver:

```text
26 × 32 мм target
```

### 7.3 Правила

1. Шесть PWM не проходят через межплатный жгут; PWM генерируется локально.
2. HARD_OFF общий, local channel faults остаются индивидуальными.
3. Нет автоматического brightness reduction в SINGLE_PACK_MODE.
4. SERVICE_OVERRIDE может выбрать один LED output/setpoint, но не отменяет current/thermal protection.

## 8. Mounting-hole placeholders

Для каждого модуля на следующем механическом шаге создаются:

```text
MH1_TBD
MH2_TBD
MH3_TBD
MH4_TBD
```

Для длинных PCB-B/C/D допускаются дополнительные `MH5_TBD/MH6_TBD`.

До выбора винтов и стоек:

- drill отсутствует либо отмечен mechanical placeholder;
- вокруг центра сохраняется keepout radius 5 мм;
- tool-access cylinder проверяется между уровнями;
- координаты не замораживаются.

## 9. Проверка сборочного envelope

Текущая компоновочная гипотеза проходит формальную проверку:

```text
width target ≤94 мм < 100 мм
L0 length = 240 мм < 250 мм
L1 length = 235 мм < 250 мм
L2 length = 180 мм < 250 мм
height budget = 79 мм < 80 мм
```

Проверка является геометрической. Электрическая, тепловая и компонентная реализуемость ещё не доказана.

## 10. Следующий результат

Следующий документ должен содержать physical interface count:

```text
PCB-A↔PCB-B direct control/diagnostic count
PCB-B↔PCB-C power + CAN + SAFE/HARD/fault count
PCB-B↔PCB-D power + CAN + SAFE/HARD/fault count
PCB-B↔PCB-E power + CAN + HARD/fault count
service/debug count
ground/shield contacts
reserve percentage 20…30 %
```

После pin count разрешается переход к connector-class comparison без выбора окончательной модели.
