# Gate component-height и 3D clearance — PlataVM V1.9

Дата: 2026-07-21  
Предыдущий Gate: preliminary board outlines открыты и пересохранены в KiCad 10.0  
Статус: `OPEN — NEXT PERMITTED MECHANICAL STEP`

## 1. Цель

Проверить, помещаются ли функциональные зоны и будущие высокие компоненты пяти плат в многоуровневую сборку `PACKAGING-P1` без изменения frozen electrical architecture.

## 2. Проверяемая структура

```text
L0: PCB-A + PCB-C
L1: PCB-D + PCB-E
L2: PCB-B
```

Размеры плат:

| Board | Outline | Level | Component-height target |
|---|---:|---:|---:|
| PCB-A | 110 × 94 мм | L0 | ≤23 мм |
| PCB-B | 180 × 94 мм | L2 | ≤16 мм |
| PCB-C | 130 × 94 мм | L0 | ≤23 мм |
| PCB-D | 125 × 94 мм | L1 | ≤23 мм |
| PCB-E | 110 × 94 мм | L1 | ≤23 мм |

## 3. Вертикальный бюджет

```text
base/mount allowance        3 мм
L0 PCB + components        26 мм
inter-level clearance       3 мм
L1 PCB + components        26 мм
inter-level clearance       3 мм
L2 PCB + components        18 мм
---------------------------------
total                      79 мм
assembly limit             80 мм
```

Остаточный формальный резерв:

```text
1 мм
```

Он не является допустимым manufacturing tolerance. Реальная сборка должна получить дополнительный запас за счёт фактической высоты компонентов, оптимизации стоек или изменения floorplan.

## 4. Разрешённые placeholders

На этом этапе разрешается добавлять только механические/графические объекты:

1. прямоугольные functional-area blocks;
2. height-class labels;
3. courtyard/keepout placeholders;
4. connector mating-volume placeholders;
5. wire-bend and strain-relief volumes;
6. tool-access cylinders над `MHx_TBD`;
7. local heatsink/inductor/transformer bounding boxes без part-number freeze.

Предварительные height classes:

```text
H1: 0…5 мм
H2: >5…10 мм
H3: >10…16 мм
H4: >16…23 мм
```

PCB-B допускает только H1…H3. H4 на PCB-B запрещён текущим budget `≤16 мм`.

## 5. Запрещённые действия

- выбирать final component part numbers только ради 3D-модели;
- добавлять production footprints без schematic/component decision;
- фиксировать final drill;
- начинать copper routing;
- менять PACK_BUS, ground domains или safety architecture;
- использовать корпус как heat sink;
- скрывать PCB-E thermal blocker;
- проводить high current через PCB-B;
- превращать INTERCONNECT в active board.

## 6. Обязательные зоны проверки

### PCB-A

```text
battery power entry
branch switching/protection
current sensing
PACK_BUS distribution
DECK_BALANCE elements
high-current connector/wire volume
```

### PCB-B

```text
critical power
MCU/supervisor
isolated RS-485
CAN-FD
service/debug access
controlled SIGNAL_GND–POWER_GND point
```

### PCB-C

```text
14 protected 12 V channels
power connector groups
output harness bend radius
local protection and diagnostics
```

### PCB-D

```text
two-phase DC/DC magnetic components
input/output capacitors
10 protected 5 V channels
thermal spreading area
```

### PCB-E

```text
six LED driver channels
input branch connector
channel output connectors
thermal spreading area
possible local heatsink volumes
```

## 7. Tool-access requirements

Для каждого `MHx_TBD` необходимо создать осевой service volume:

```text
no component
no connector
no cable crossing
no upper-level obstruction preventing controlled assembly
```

Конкретный диаметр инструмента остаётся `TBD` до выбора винта/стойки.

## 8. Connector clearance

Нужно проверить два кандидата A↔B:

```text
A: one 32-position signal connector
B: two 16-position connectors: CTRL + DIAG
```

Для каждого кандидата оцениваются:

1. корпус connector pair;
2. mating/unmating direction;
3. cable exit;
4. bend radius;
5. latch/tool access;
6. separation analog/control/power;
7. влияние на CAN-FD stubs;
8. демонтаж уровня PCB-B.

Part number на этом Gate не выбирается.

## 9. CAN-FD mechanical routing

Сравнить физический порядок:

```text
PCB-B — PCB-D — PCB-E — PCB-C
```

и

```text
PCB-B — PCB-C — PCB-D — PCB-E
```

Критерии:

- минимальная длина trunk;
- минимальные stubs;
- доступность termination;
- отсутствие соседства с high-current switching loops;
- удобство пассивного INTERCONNECT.

## 10. Критерии PASS

Gate считается пройденным только если:

1. все bounding boxes помещаются в level height budgets;
2. отсутствуют межуровневые пересечения;
3. имеется реальный, а не только арифметический, вертикальный запас;
4. все mounting zones имеют tool access;
5. connector mating volumes не пересекаются с соседними уровнями;
6. power wiring не проходит через PCB-B;
7. PCB-D/PCB-E thermal zones не блокируются соседними платами;
8. выбран предварительный A↔B connector topology;
9. выбран preliminary CAN-FD node order;
10. PACKAGING-P1 подтверждён либо выпущена его ревизия.

## 11. Результирующие артефакты

```text
3D/height placeholder model
per-board height-zone map
inter-level clearance table
tool-access review
connector topology decision
preliminary CAN-FD physical order
PACKAGING-P1 PASS or revision proposal
```

До выполнения этих артефактов размеры плат и высоты остаются `PRELIMINARY`.
