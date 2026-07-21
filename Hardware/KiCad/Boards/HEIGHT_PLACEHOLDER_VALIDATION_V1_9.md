# Проверка height-placeholder board files — PlataVM V1.9

Дата: 2026-07-21  
Статус: `STRUCTURAL PASS; KICAD 10.0 OWNER OPEN/SAVE CHECK REQUIRED`

## 1. Проверенные файлы

```text
PCB-A_BFE_POWER.kicad_pcb
PCB-B_CTRL_RESERVE.kicad_pcb
PCB-C_POWER_12V.kicad_pcb
PCB-D_POWER_5V.kicad_pcb
PCB-E_LIGHT_POWER.kicad_pcb
```

## 2. Формат

Во всех файлах:

```text
(version 20260206)
(generator "pcbnew")
(generator_version "10.0")
```

Каждый файл имеет закрытый верхний `kicad_pcb` S-expression и обязательные слои `F.Cu`, `B.Cu`, `F.SilkS`, `B.SilkS`, `Edge.Cuts`, `Margin`.

## 3. Контуры

| Board | Edge.Cuts | Результат |
|---|---:|---|
| PCB-A | 110 × 94 мм | PASS |
| PCB-B | 180 × 94 мм | PASS |
| PCB-C | 130 × 94 мм | PASS |
| PCB-D | 125 × 94 мм | PASS |
| PCB-E | 110 × 94 мм | PASS |

## 4. Добавленные объекты

Разрешённые объекты:

- `gr_rect` functional zones на `F.SilkS`;
- `gr_text` zone/height labels;
- `gr_rect` mating/thermal volumes на `Margin`;
- существующие `MHx_TBD` circles и labels.

## 5. Отсутствующие production objects

В файлы не добавлены:

```text
footprint
pad
net
segment
via
zone
final drill
production copper
```

Слово `zone` может встречаться только в пояснительном графическом тексте, но copper-zone objects отсутствуют.

## 6. Height-policy check

| Проверка | Результат |
|---|---|
| PCB-A/C/D/E допускают H4 ≤23 мм | PASS |
| PCB-B target ≤16 мм | PASS |
| PCB-B H4 prohibited label присутствует | PASS |
| PCB-B functional blocks только H2/H3 | PASS |
| PCB-D magnetics/capacitors отмечены H4 | PASS |
| PCB-E LED driver regions отмечены H4 | PASS |
| PCB-E thermal blocker сохранён | PASS |

## 7. Mounting zones

- PCB-A/B/C/D имеют по шесть `MHx_TBD`;
- PCB-E имеет четыре `MHx_TBD`;
- functional blocks не занимают центры этих зон;
- actual drill и mounting footprint отсутствуют.

## 8. Архитектурная проверка

| Ограничение | Результат |
|---|---|
| K_MAIN не добавлен | PASS |
| high-current routing через PCB-B отсутствует | PASS |
| footprints/components не выбраны | PASS |
| INTERCONNECT не стал активным | PASS |
| EXT_KILL architecture не изменена | PASS |
| ground domains не изменены | PASS |
| thermal contact to hull не добавлен | PASS |

## 9. Ограничение проверки

Файлы сформированы как текстовые KiCad 10.0 preliminary boards и структурно прочитаны через GitHub. В текущем окружении отсутствует `pcbnew/kicad-cli`, поэтому требуется владелецкая проверка:

1. открыть пять файлов в KiCad 10.0;
2. подтвердить отсутствие parser errors;
3. проверить отображение multiline labels;
4. проверить слои `F.SilkS` и `Margin`;
5. сохранить изменения отдельным commit, если KiCad нормализует формат;
6. не добавлять footprints или медь в этот commit.

## 10. Итог

```text
file structure: PASS
board dimensions: PASS
placeholder content: PASS
no production objects: PASS
architecture continuity: PASS
KiCad 10.0 application parse after placeholder update: OPEN OWNER CHECK
```
