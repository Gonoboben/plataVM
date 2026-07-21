# Проверка предварительных board outlines — PlataVM V1.9

Дата исходной проверки: 2026-07-21  
Дата проверки в KiCad 10.0: 2026-07-21  
Статус: `KICAD 10.0 APPLICATION OPEN/SAVE PASS; DRC AND 3D REVIEW OPEN`

## 1. Проверенные файлы

```text
PCB-A_BFE_POWER.kicad_pcb
PCB-B_CTRL_RESERVE.kicad_pcb
PCB-C_POWER_12V.kicad_pcb
PCB-D_POWER_5V.kicad_pcb
PCB-E_LIGHT_POWER.kicad_pcb
```

## 2. Зафиксированная версия

Владелец открыл и пересохранил платы в KiCad 10.0. Commit проверки:

```text
627571e82855c785df8b39ea929bb3d9d41c78dd
```

Во всех board-файлах после сохранения:

```text
(version 20260206)
(generator "pcbnew")
(generator_version "10.0")
```

Следовательно, application-level чтение и сохранение формата подтверждены.

## 3. Геометрическая проверка после миграции

| Board | Edge.Cuts | Target | Результат |
|---|---:|---:|---|
| PCB-A | 110 × 94 мм | 110 × 94 мм | PASS |
| PCB-B | 180 × 94 мм | 180 × 94 мм | PASS |
| PCB-C | 130 × 94 мм | 130 × 94 мм | PASS |
| PCB-D | 125 × 94 мм | 125 × 94 мм | PASS |
| PCB-E | 110 × 94 мм | 110 × 94 мм | PASS |

Каждый outline остаётся одним замкнутым `gr_rect` на `Edge.Cuts`.

## 4. Mounting-zone check

| Board | Графические MH_TBD zones |
|---|---:|
| PCB-A | 6 |
| PCB-B | 6 |
| PCB-C | 6 |
| PCB-D | 6 |
| PCB-E | 4 |

Каждая зона:

```text
radius = 5 мм
layer = F.SilkS
label = MHx_TBD
```

Это графические keepout/placeholder zones, а не drill и не mounting footprint.

## 5. Структурная проверка

Для всех пяти файлов подтверждено:

1. корректный S-expression после сохранения KiCad 10.0;
2. заголовок `kicad_pcb`;
3. версия board format `20260206`;
4. generator `pcbnew 10.0`;
5. наличие `F.Cu`, `B.Cu`, `F.SilkS`, `B.SilkS`, `Edge.Cuts`;
6. один board outline;
7. отсутствие footprints;
8. отсутствие pads;
9. отсутствие nets;
10. отсутствие tracks/segments;
11. отсутствие vias;
12. отсутствие copper zones;
13. сохранение preliminary labels и MH_TBD zones.

Результат:

```text
PASS
```

## 6. Проверка проектных ограничений

| Ограничение | Результат |
|---|---|
| Absolute board width ≤100 мм | PASS: 94 мм |
| L0 length A+C ≤250 мм | PASS: 240 мм |
| L1 length D+E ≤250 мм | PASS: 235 мм |
| L2 length B ≤250 мм | PASS: 180 мм |
| No final mounting drill | PASS |
| No component/footprint selection | PASS |
| No production routing | PASS |
| No schematic change | PASS |
| Thermal blocker PCB-E не скрыт | PASS |
| KiCad 10.0 format migration changed no geometry | PASS |

## 7. Project/session files

KiCad 10.0 создал `.kicad_pro` и `.kicad_prl` для каждой платы.

Принято:

```text
.kicad_pro = project configuration, хранить
.kicad_prl = local session state, не хранить
```

`.kicad_prl` удалены из рабочей ветки и добавлены в `.gitignore`.

## 8. Ограничение текущей проверки

Подтверждены application-level parse/save и сохранение геометрии. Пока не выполнены:

- DRC с реальными design rules;
- 3D Viewer inter-level clearance review;
- component-height audit;
- connector mating-volume review;
- mounting tool-access review;
- проверка final stack-up;
- production outputs.

DRC пустых preliminary boards не заменяет будущую release-проверку после появления footprints, nets, copper и окончательных правил.

## 9. Следующая проверка

```text
component-height placeholders
→ three-level 3D stack L0/L1/L2
→ connector/tool-access volumes
→ confirmation or revision of PACKAGING-P1
```

После выбора компонентов отдельно выполняются ERC/DRC и сохраняются как release record.

## 10. Заключение

```text
S-expression structure: PASS
KiCad 10.0 application open/save: PASS
Board format migration: PASS
Outline dimensions: PASS
No component/routing content: PASS
Packaging arithmetic: PASS
DRC: OPEN FOR LATER DESIGN STAGE
3D/component-height validation: OPEN
```
