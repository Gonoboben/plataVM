# Карта функциональных зон и классов высоты — PlataVM V1.9

Дата: 2026-07-21  
Статус: `PRELIMINARY HEIGHT-ZONE MAP`

## 1. Назначение

Документ фиксирует графические placeholder-зоны, добавленные в пять preliminary board-файлов. Зоны используются только для проверки компоновки `PACKAGING-P1`.

Не выбраны:

- part numbers;
- footprints;
- final mounting holes;
- production copper;
- connector families;
- heatsinks;
- magnetics.

## 2. Классы высоты

```text
H1: 0…5 мм
H2: >5…10 мм
H3: >10…16 мм
H4: >16…23 мм
```

Ограничения:

- PCB-A/C/D/E допускают H1…H4;
- PCB-B допускает только H1…H3;
- высота считается над верхней поверхностью PCB;
- mating-volume и wire-bend volume учитываются отдельно от корпуса компонента.

## 3. PCB-A_BFE_POWER

| Зона | Класс | Назначение |
|---|---:|---|
| BAT ENTRY | H4 | вводы двух батарейных ветвей и силовой жгут |
| BFE SW/PROT | H4 | силовые ключи, защита, ограничение переходных процессов |
| CURRENT SENSE | H2 | измерение токов батарейных ветвей |
| PACK BUS DIST | H3 | распределение PACK_BUS и POWER_GND |
| DECK_BALANCE | H3 | ограниченный выравнивающий тракт |
| CTRL/DIAG | H2 | прямые линии управления и диагностики PCB-B |
| POWER/WIRE MATING VOL | mechanical | объём силовых вводов и изгиба кабеля |

## 4. PCB-B_CTRL_RESERVE

| Зона | Класс | Назначение |
|---|---:|---|
| CRITICAL PWR | H3 | 5V_CRIT/3V3_CRIT и critical power path |
| MCU/SUPERVISOR | H2 | STM32G4, watchdog, supervisor, fault manager |
| ISO RS485 | H2 | изолированный внешний интерфейс |
| CAN/SAFE | H2 | внутренняя CAN-FD и direct safety lines |
| SERVICE | H2 | service/debug access |
| A-B CTRL 16 + DIAG 16 | mating volume | preliminary split topology |
| C/D/E 8-position groups | mating volume | CAN-FD и прямые safe/fault lines |
| EMG/LOG/GND TIE | H3 | аварийная ветвь, журналирование и controlled net-tie |

H4 на PCB-B запрещён.

## 5. PCB-C_POWER_12V

| Зона | Класс | Назначение |
|---|---:|---|
| INPUT PROT | H3 | входная защита PACK_BUS_P12_IN |
| CH1…CH7 | H3 | protected switching/current diagnostics |
| CH8…CH14 | H3 | protected switching/current diagnostics |
| LOCAL MCU/CAN | H2 | локальное управление и CAN-FD |
| OUTPUT GROUPS | H3 | 14 выходов и harness bend volume |

## 6. PCB-D_POWER_5V

| Зона | Класс | Назначение |
|---|---:|---|
| INPUT PROT | H3 | входная защита PACK_BUS_P5_IN |
| TWO-PHASE POWER STAGE | H4 | силовые MOSFET и два магнитных канала |
| BULK/OUTPUT CAPS | H4 | входные и выходные накопительные конденсаторы |
| LOCAL MCU/CAN | H2 | локальное управление и диагностика |
| OUT1…OUT5 | H3 | protected 5 V outputs |
| OUT6…OUT10 | H3 | protected 5 V outputs |
| THERMAL SPREADING | mechanical | внутренняя зона распределения тепла без контакта с корпусом |

## 7. PCB-E_LIGHT_POWER

| Зона | Класс | Назначение |
|---|---:|---|
| INPUT PROT | H3 | входная защита PACK_BUS_LIGHT_IN |
| LED CH1…CH3 | H4 | первая зона LED-драйверов |
| LED CH4…CH6 | H4 | вторая зона LED-драйверов |
| LOCAL MCU/CAN | H2 | локальное управление и PWM |
| LED OUTPUTS | H3 | выходные группы и mating volume |
| THERMAL SPREADING | mechanical | внутренняя зона распределения тепла |

Тепловой блокер PCB-E остаётся открыт: оценочные потери 15…25 Вт при максимальном световом режиме не подтверждены для герметичного объёма при +60 °C.

## 8. Mounting/tool-access

На платах сохранены графические `MHx_TBD` диаметром 10 мм. Functional zones не занимают эти области в 2D.

Не подтверждены:

- диаметр головки винта;
- диаметр инструмента;
- стойки;
- доступ через верхние уровни;
- демонтаж платы без снятия соседнего уровня.

## 9. Статус

```text
2D functional-zone placement: PASS
nominal height-class allocation: PASS
actual component height: OPEN
connector mating clearance: OPEN
wire bend clearance: OPEN
inter-level tool access: OPEN
thermal qualification: OPEN
```
