# KiCad workspace PlataVM

Статус: `KICAD SCHEMATIC SKELETON CREATED`

## 1. Назначение

Каталог является источником истины для электрической принципиальной схемы и последующих PCB. Архитектурные ограничения задаются документами:

```text
Docs/SCHEMATIC_ARCHITECTURE.md
Docs/INTERBOARD_INTERFACES.md
Docs/NET_NAMING_RULES.md
```

Manifest созданного схемного скелета:

```text
Hardware/KiCad/SCHEMATIC_SKELETON_MANIFEST.md
```

## 2. Текущая созданная структура

```text
Hardware/KiCad/
├── PlataVM.kicad_pro
├── PlataVM.kicad_sch
├── 00_SYSTEM_TOP.kicad_sch
├── 01_EXTERNAL_BATTERIES_AND_HARNESS.kicad_sch
├── 02_INTERBOARD_POWER_AND_CONTROL.kicad_sch
├── 10_BFE_POWER_TOP.kicad_sch
├── 20_CTRL_RESERVE_TOP.kicad_sch
├── 30_POWER_12V_TOP.kicad_sch
├── 40_POWER_5V_TOP.kicad_sch
├── 50_LIGHT_POWER_TOP.kicad_sch
├── SCHEMATIC_SKELETON_MANIFEST.md
├── symbols/
├── footprints/
├── 3dmodels/
├── simulation/
├── exports/
│   ├── pdf/
│   ├── svg/
│   ├── bom/
│   └── netlists/
└── reviews/
```

Папки библиотек и экспортов будут наполняться после локальной проверки проекта и начала детализации узлов.

## 3. Правила проекта

1. Один корневой проект и единая логическая схема системы.
2. Физические PCB создаются как отдельные платы после фиксации границ и connector pinout.
3. Reference designators уникальны для всего проекта.
4. Пользовательские символы и footprints хранятся внутри репозитория.
5. Внешние библиотечные ссылки не должны быть единственным источником символа или footprint.
6. Каждый component freeze сопровождается datasheet, расчётом и статусом BOM.
7. ERC-исключения документируются, а не скрываются.
8. Экспорты PDF/SVG создаются для review, но не заменяют исходные `.kicad_sch`.
9. Силовые и сигнальные интерфейсы должны соответствовать `Docs/INTERBOARD_INTERFACES.md`.
10. Имена сетей должны соответствовать `Docs/NET_NAMING_RULES.md`.
11. Пока отсутствуют выбранные компоненты, на листах допускаются функциональные блоки и текстовые ограничения уровня A.

## 4. Проверка после открытия в KiCad

Локально открыть:

```text
Hardware/KiCad/PlataVM.kicad_pro
```

Проверить:

1. проект открывается;
2. корневой лист `PlataVM.kicad_sch` видит восемь верхних листов;
3. каждый лист открывается;
4. KiCad сохраняет файлы без потери структуры;
5. русские комментарии остаются в UTF-8;
6. изменения после первого локального сохранения вносятся отдельным commit.

## 5. Первый архитектурный комплект

```text
00_SYSTEM_TOP
01_EXTERNAL_BATTERIES_AND_HARNESS
02_INTERBOARD_POWER_AND_CONTROL
10_BFE_POWER_TOP
20_CTRL_RESERVE_TOP
30_POWER_12V_TOP
40_POWER_5V_TOP
50_LIGHT_POWER_TOP
```

## 6. Следующая детализация

Следующий рабочий лист:

```text
00_SYSTEM_TOP.kicad_sch
```

Задача следующего PR:

```text
заменить текстовую архитектуру на функциональные блоки
добавить hierarchical labels
проверить соответствие Docs/INTERBOARD_INTERFACES.md
не выбирать part numbers
```

## 7. Запреты

1. Не создавать PCB до проверки иерархии и интерфейсов.
2. Не назначать случайные footprints для TBD-компонентов.
3. Не объединять POWER_GND, SIGNAL_GND, ISO_GND и CHASSIS без отдельного решения.
4. Не прокладывать силовые токи через PCB-B_CTRL_RESERVE.
5. Не вводить новый функциональный интерфейс без обновления архитектурных документов.
6. Не считать созданные текстовые листы `schematic freeze`: это только архитектурный скелет.
