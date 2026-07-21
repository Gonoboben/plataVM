# Запись версии KiCad и проверка board-файлов — PlataVM V1.9

Дата: 2026-07-21  
Источник: сообщение владельца и commit `627571e82855c785df8b39ea929bb3d9d41c78dd`  
Статус: `KICAD 10.0 APPLICATION OPEN/SAVE CONFIRMED; DRC AND 3D REVIEW OPEN`

## 1. Зафиксированный toolchain

```text
KiCad: 10.0
PCB Editor generator: pcbnew
board file version: 20260206
```

Все пять preliminary board-файлов содержат:

```text
(generator "pcbnew")
(generator_version "10.0")
```

Это подтверждает, что файлы были прочитаны и пересохранены PCB Editor KiCad 10.0.

## 2. Проверенные платы

```text
Hardware/KiCad/Boards/PCB-A_BFE_POWER.kicad_pcb
Hardware/KiCad/Boards/PCB-B_CTRL_RESERVE.kicad_pcb
Hardware/KiCad/Boards/PCB-C_POWER_12V.kicad_pcb
Hardware/KiCad/Boards/PCB-D_POWER_5V.kicad_pcb
Hardware/KiCad/Boards/PCB-E_LIGHT_POWER.kicad_pcb
```

## 3. Результат миграции формата

| Board | Edge.Cuts после сохранения | Требование | Результат |
|---|---:|---:|---|
| PCB-A | 110 × 94 мм | 110 × 94 мм | PASS |
| PCB-B | 180 × 94 мм | 180 × 94 мм | PASS |
| PCB-C | 130 × 94 мм | 130 × 94 мм | PASS |
| PCB-D | 125 × 94 мм | 125 × 94 мм | PASS |
| PCB-E | 110 × 94 мм | 110 × 94 мм | PASS |

Сохранены:

1. замкнутые прямоугольные `Edge.Cuts`;
2. labels `PRELIMINARY V1.9`;
3. target dimensions и level designation;
4. графические `MHx_TBD` zones;
5. отсутствие final drill, footprints, pads, nets, tracks, vias и copper zones.

Миграция формата не изменила PACKAGING-P1 и не внесла электрических изменений.

## 4. Project и session files

KiCad 10.0 создал для каждой платы `.kicad_pro`. Эти файлы допускается хранить в репозитории как project/configuration files.

`.kicad_prl` содержит локальное состояние пользовательской сессии PCB Editor и не является проектной исходной документацией. Поэтому:

```text
*.kicad_prl = NOT VERSIONED
```

Файлы удаляются из репозитория, а шаблон добавляется в `.gitignore`.

## 5. Что подтверждено

```text
KiCad version record: PASS
application-level parse/save: PASS
board format migration: PASS
outline dimensions after migration: PASS
PACKAGING-P1 continuity: PASS
no electrical architecture change: PASS
```

`application-level parse/save: PASS` основан на факте пересохранения всех пяти файлов PCB Editor KiCad 10.0. Визуальное содержимое дополнительно сверено по сохранённым координатам и объектам файлов.

## 6. Что ещё не подтверждено

```text
DRC: NOT RUN / NOT APPLICABLE TO EMPTY PRELIMINARY BOARDS
3D Viewer clearance review: OPEN
component-height audit: OPEN
connector mating clearance: OPEN
mounting screw/tool-access review: OPEN
final board outlines: OPEN
final mounting drills: OPEN
production stack-up and rules: OPEN
```

Полный DRC имеет инженерный смысл после появления footprints, nets, design rules и copper. До schematic/PCB freeze результаты ERC/DRC должны быть сохранены отдельным release record.

## 7. Следующий Gate

```text
KiCad 10.0 board opening complete
→ component-height placeholder audit
→ 3D level stack L0/L1/L2
→ tool-access and connector clearance review
→ A↔B connector topology decision
→ CAN-FD physical node order
→ thermal/current calculations
```

До прохождения этого Gate board dimensions остаются `PRELIMINARY`.
