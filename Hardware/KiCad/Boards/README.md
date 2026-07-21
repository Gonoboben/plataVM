# Preliminary PCB board outlines — PlataVM V1.9

Дата: 2026-07-21  
Статус: `PRELIMINARY MECHANICAL OUTLINES — NOT PRODUCTION PCB`

## 1. Назначение

Каталог содержит отдельные `.kicad_pcb` файлы для предварительной проверки envelope `PACKAGING-P1`.

```text
PCB-A_BFE_POWER.kicad_pcb
PCB-B_CTRL_RESERVE.kicad_pcb
PCB-C_POWER_12V.kicad_pcb
PCB-D_POWER_5V.kicad_pcb
PCB-E_LIGHT_POWER.kicad_pcb
```

## 2. Размеры

| Board | Edge.Cuts target | Assembly level | Component-height budget |
|---|---:|---:|---:|
| PCB-A | 110 × 94 мм | L0 | ≤23 мм |
| PCB-B | 180 × 94 мм | L2 | ≤16 мм |
| PCB-C | 130 × 94 мм | L0 | ≤23 мм |
| PCB-D | 125 × 94 мм | L1 | ≤23 мм |
| PCB-E | 110 × 94 мм | L1 | ≤23 мм |

Размеры соответствуют area budgets V1.9 и не являются окончательными производственными контурами.

## 3. Содержимое файлов

Каждый board file содержит только:

1. замкнутый прямоугольный `Edge.Cuts`;
2. название платы;
3. target size, level и height budget;
4. предупреждение `PRELIMINARY V1.9`;
5. графические круги `MHx_TBD` на `F.SilkS`.

Файлы не содержат:

- footprints;
- pads;
- actual drilled holes;
- nets;
- copper tracks/zones;
- vias;
- connector part numbers;
- production design rules;
- final stack-up.

## 4. Mounting zones

`MHx_TBD` — это графические зоны диаметром 10 мм, а не отверстия.

```text
NO FINAL DRILL
NO MOUNTING FOOTPRINT
NO MECHANICAL FREEZE
```

После выбора владельцем винтов и стоек необходимо:

1. определить drill и head/washer clearance;
2. определить plated/non-plated implementation;
3. подтвердить координаты;
4. проверить tool-access volumes между уровнями;
5. заменить графические zones на утверждённые mounting footprints.

## 5. PACKAGING-P1

```text
L0: PCB-A + PCB-C = 110 + 130 = 240 мм
L1: PCB-D + PCB-E = 125 + 110 = 235 мм
L2: PCB-B = 180 мм
```

Общий height budget:

```text
79 мм < 80 мм
```

Остаточный вертикальный резерв только 1 мм, поэтому component-height/3D review обязателен до сохранения этих размеров как baseline.

## 6. Правила следующего шага

Разрешено:

- открыть каждый board file в KiCad;
- проверить parser и Edge.Cuts;
- разместить только functional area blocks и mechanical keepouts;
- подготовить 3D placeholder stack;
- оценить connector and tool access.

Запрещено:

- считать контуры замороженными;
- выбирать final mounting drill;
- начинать production routing;
- добавлять случайные footprints для заполнения площади;
- менять schematic architecture через board-level workaround;
- скрывать thermal blocker PCB-E.

## 7. Источники

```text
Docs/PCB_PACKAGING_BOUNDARY_V1_9.md
Docs/PCB_MODULE_AREA_BUDGET_V1_9.md
Docs/PACKAGING_P1_REVIEW_CHECKLIST.md
Docs/PRE_KICAD_OUTLINE_GATE_V1_9.md
```
