# PACKAGING-P1 — checklist следующего KiCad review

Дата: 2026-07-21  
Статус: `READY FOR PRELIMINARY MECHANICAL IMPLEMENTATION`

## Перед изменением `.kicad_pcb`

- [ ] Подтвердить наличие/отсутствие отдельных PCB project files A…E.
- [ ] Создать отдельную ветку для mechanical outlines.
- [ ] Не изменять `.kicad_sch` без необходимости.
- [ ] Не выбирать components/footprints ради заполнения площади.

## Board targets

| PCB | Target | Absolute preliminary maximum | Height |
|---|---:|---:|---:|
| A | 94×110 мм | 100×120 мм | ≤23 мм |
| B | 94×180 мм | 100×220 мм | ≤16 мм |
| C | 94×130 мм | 100×145 мм | ≤23 мм |
| D | 94×125 мм | 100×140 мм | ≤23 мм |
| E | 94×110 мм | 100×130 мм | ≤23 мм |

## Mechanical placeholders

- [ ] `MOUNT_HOLE_TBD` минимум 4 на плату.
- [ ] Keepout radius 5 мм вокруг центра mounting zone.
- [ ] Tool-access volumes не перекрываются соседним уровнем.
- [ ] Дополнительные опоры тяжёлых компонентов обозначены.
- [ ] Final drill и координаты не заморожены.

## Stack check

```text
L0: PCB-A + PCB-C
L1: PCB-D + PCB-E
L2: PCB-B
```

- [ ] L0 ≤240 мм target.
- [ ] L1 ≤235 мм target.
- [ ] L2 ≤180 мм target.
- [ ] Total stack ≤80 мм.
- [ ] Продольные воздушные проходы сохранены.
- [ ] Основные источники тепла не расположены строго друг над другом.
- [ ] PCB-B удалена от switching nodes PCB-D/E и BFE loops PCB-A.

## Interfaces

- [ ] A↔B signal class 32 positions либо documented split 16+16.
- [ ] B↔C/D/E 8-position classes.
- [ ] A→C 30 А class.
- [ ] A→D 15 А class preliminary.
- [ ] A→E 25 А class preliminary.
- [ ] CAN-FD route без длинных stubs.
- [ ] SAFE/HARD_OFF не зависят от CAN-FD.
- [ ] High current не проходит через PCB-B.

## Gate результата

Mechanical implementation принимается только если:

```text
all outlines inside envelope
mounting/tool access plausible
no frozen connector part numbers
no hidden architecture change
thermal blocker remains explicitly open
```
