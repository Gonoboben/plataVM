# KiCad workspace PlataVM

Статус: `SCHEMATIC ARCHITECTURE INITIALIZED`

## 1. Назначение

Каталог является источником истины для электрической принципиальной схемы и последующих PCB. До создания валидных KiCad-файлов архитектура определяется документами:

```text
Docs/SCHEMATIC_ARCHITECTURE.md
Docs/INTERBOARD_INTERFACES.md
Docs/NET_NAMING_RULES.md
```

## 2. Планируемая структура

```text
Hardware/KiCad/
├── PlataVM.kicad_pro
├── PlataVM.kicad_sch
├── sheets/
│   ├── system/
│   ├── pcb_a_bfe_power/
│   ├── pcb_b_ctrl_reserve/
│   ├── pcb_c_power_12v/
│   ├── pcb_d_power_5v/
│   └── pcb_e_light_power/
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

## 4. Порядок создания файлов

1. Создать `PlataVM.kicad_pro` в локальной актуальной версии KiCad.
2. Создать корневой `PlataVM.kicad_sch`.
3. Добавить верхние иерархические листы без конкретных компонентов.
4. Проверить имена всех портов и шин.
5. Экспортировать PDF/SVG первого архитектурного review.
6. После review детализировать по одному функциональному узлу через отдельные ветки/PR.

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

## 6. Запреты

1. Не создавать PCB до проверки иерархии и интерфейсов.
2. Не назначать случайные footprints для TBD-компонентов.
3. Не объединять POWER_GND, SIGNAL_GND, ISO_GND и CHASSIS без отдельного решения.
4. Не прокладывать силовые токи через PCB-B_CTRL_RESERVE.
5. Не вводить новый функциональный интерфейс без обновления архитектурных документов.