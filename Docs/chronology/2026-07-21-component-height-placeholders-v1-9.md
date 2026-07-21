# Хронология: component-height placeholders и PACKAGING-P1 review

Дата: 2026-07-21  
Предыдущая контрольная точка: PR #40, KiCad 10.0 board verification  
Ветка: `hardware-component-height-placeholders-v1-9`

## 1. Выполнено

1. На PCB-A…PCB-E добавлены только графические functional-area blocks и height-class labels.
2. Сохранены Edge.Cuts и размеры пяти плат.
3. Сохранены MH_TBD, final drill не добавлен.
4. Footprints, pads, nets, tracks, vias и copper zones не добавлены.
5. Создан OpenSCAD placeholder model трёхуровневой сборки.
6. Выполнена номинальная проверка межуровневых зазоров.
7. Выбран предварительный A↔B интерфейс `16 CTRL + 16 DIAG`.
8. Выбран предварительный CAN-FD order `PCB-B → PCB-D → PCB-E → PCB-C`.
9. Концы termination предварительно назначены PCB-B и PCB-C.

## 2. Статус PACKAGING-P1

```text
2D area fit: PASS
nominal height classes: PASS
actual components: OPEN
connector mating volumes: OPEN
thermal qualification: OPEN
PACKAGING-P1: CONDITIONAL PASS
```

## 3. Номинальные зазоры

```text
L0 top → L1 plane: 4,4 мм
L1 top → L2 plane: 4,4 мм
L2 top → 80 мм envelope: 1,4 мм
```

Mechanical-freeze target:

```text
actual assembly height ≤75 мм
reserve ≥5 мм
```

## 4. Неизменённая архитектура

- K_MAIN отсутствует;
- high current не проходит через PCB-B;
- EXT_KILL независим;
- INTERCONNECT пассивный;
- CAN-FD не заменяет direct safety lines;
- thermal contact to hull не добавлен;
- PCB-E thermal blocker остаётся открытым.

## 5. Следующий этап

```text
real bounding dimensions
→ connector class comparison
→ mounting screw/standoff input
→ update OpenSCAD/KiCad placeholders
→ actual 3D clearance review
→ confirm or revise board sizes
→ begin subsystem candidate selection
```
