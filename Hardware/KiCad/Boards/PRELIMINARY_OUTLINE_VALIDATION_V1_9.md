# Проверка предварительных board outlines — PlataVM V1.9

Дата: 2026-07-21  
Статус: `STRUCTURAL PASS; LOCAL KICAD OPENING REQUIRED`

## 1. Проверенные файлы

```text
PCB-A_BFE_POWER.kicad_pcb
PCB-B_CTRL_RESERVE.kicad_pcb
PCB-C_POWER_12V.kicad_pcb
PCB-D_POWER_5V.kicad_pcb
PCB-E_LIGHT_POWER.kicad_pcb
```

## 2. Геометрическая проверка

| Board | Edge.Cuts | Target | Результат |
|---|---:|---:|---|
| PCB-A | 110 × 94 мм | 110 × 94 мм | PASS |
| PCB-B | 180 × 94 мм | 180 × 94 мм | PASS |
| PCB-C | 130 × 94 мм | 130 × 94 мм | PASS |
| PCB-D | 125 × 94 мм | 125 × 94 мм | PASS |
| PCB-E | 110 × 94 мм | 110 × 94 мм | PASS |

Каждый outline выполнен одним замкнутым `gr_rect` на `Edge.Cuts`.

## 3. Mounting-zone check

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

Это не drill и не footprint.

## 4. Структурная проверка

Для всех пяти файлов выполнено:

1. баланс круглых скобок S-expression;
2. проверка закрытия строк;
3. наличие заголовка `kicad_pcb`;
4. наличие версии `20240108`;
5. наличие `F.Cu`, `B.Cu`, `F.SilkS`, `B.SilkS`, `Edge.Cuts`;
6. наличие одного board outline;
7. отсутствие footprints;
8. отсутствие pads;
9. отсутствие nets;
10. отсутствие tracks/segments;
11. отсутствие vias;
12. отсутствие copper zones.

Результат:

```text
PASS
```

## 5. Проверка проектных ограничений

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

## 6. Ограничение проверки

В текущем окружении отсутствуют `kicad-cli` и `pcbnew`. Поэтому не выполнены:

- открытие файлов в установленной версии KiCad;
- graphical board editor review;
- DRC;
- 3D viewer;
- проверка автоматического обновления формата;
- board setup validation средствами KiCad.

До merge в production-ready baseline требуется открыть каждый файл в KiCad владельца. Для preliminary mechanical branch допускается merge после структурной проверки при явном статусе `PRELIMINARY`.

## 7. Следующая проверка владельца

Для каждого файла:

1. открыть напрямую в KiCad PCB Editor;
2. подтвердить отсутствие parser errors;
3. проверить размер Edge.Cuts;
4. проверить видимость labels и MH_TBD zones;
5. не сохранять как final layout;
6. сообщить версию KiCad;
7. при автоматической конвертации формата сохранить изменения отдельным commit.

## 8. Заключение

```text
S-expression structure: PASS
Outline dimensions: PASS
No component/routing content: PASS
Packaging arithmetic: PASS
KiCad application-level validation: OPEN OWNER CHECK
```
