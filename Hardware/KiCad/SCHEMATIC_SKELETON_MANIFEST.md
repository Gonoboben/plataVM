# KiCad schematic skeleton manifest

Дата фиксации: 2026-07-14  
Статус:

```text
ARCHITECTURE LEVEL A — KiCad workspace skeleton
```

## 1. Назначение

Этот пакет создаёт стартовый KiCad workspace для принятой многоплатной `SCHEMATIC ARCHITECTURE`. Он не выбирает компоненты, footprints или part numbers.

Источник истины:

```text
Docs/SCHEMATIC_ARCHITECTURE.md
Docs/INTERBOARD_INTERFACES.md
Docs/NET_NAMING_RULES.md
```

## 2. Созданные KiCad-файлы

```text
Hardware/KiCad/PlataVM.kicad_pro
Hardware/KiCad/PlataVM.kicad_sch
Hardware/KiCad/00_SYSTEM_TOP.kicad_sch
Hardware/KiCad/01_EXTERNAL_BATTERIES_AND_HARNESS.kicad_sch
Hardware/KiCad/02_INTERBOARD_POWER_AND_CONTROL.kicad_sch
Hardware/KiCad/10_BFE_POWER_TOP.kicad_sch
Hardware/KiCad/20_CTRL_RESERVE_TOP.kicad_sch
Hardware/KiCad/30_POWER_12V_TOP.kicad_sch
Hardware/KiCad/40_POWER_5V_TOP.kicad_sch
Hardware/KiCad/50_LIGHT_POWER_TOP.kicad_sch
```

## 3. Что уже зафиксировано в скелете

1. Корневой проект `PlataVM.kicad_pro`.
2. Корневой лист `PlataVM.kicad_sch`.
3. Верхние системные листы:
   - `00_SYSTEM_TOP`;
   - `01_EXTERNAL_BATTERIES_AND_HARNESS`;
   - `02_INTERBOARD_POWER_AND_CONTROL`.
4. Верхние листы пяти функциональных плат:
   - `10_BFE_POWER_TOP`;
   - `20_CTRL_RESERVE_TOP`;
   - `30_POWER_12V_TOP`;
   - `40_POWER_5V_TOP`;
   - `50_LIGHT_POWER_TOP`.
5. Архитектурные текстовые ограничения на каждом листе.
6. Безопасные границы: батареи, PACK_BUS, HARD_OFF, EXT_KILL, земли и межплатные интерфейсы.

## 4. Что пока не делается

1. Не выбирается контактор `K_BATx`.
2. Не выбираются `MAIN_SWx`.
3. Не выбираются датчики тока.
4. Не выбираются DC/DC, LED-драйверы, MCU и eFuse/high-side switches.
5. Не создаются footprints.
6. Не выполняется PCB layout.
7. Не объединяются автоматически `POWER_GND`, `SIGNAL_GND`, `ISO_GND` и `CHASSIS`.

## 5. Проверка перед дальнейшей детализацией

Перед следующими изменениями нужно локально открыть:

```text
Hardware/KiCad/PlataVM.kicad_pro
```

и проверить:

1. проект открывается в KiCad;
2. корневой лист показывает все восемь листов;
3. каждый лист открывается;
4. нет потери файлов при сохранении KiCad;
5. KiCad не заменил русские комментарии некорректной кодировкой;
6. изменения после первого локального сохранения должны быть внесены отдельным commit.

## 6. Следующий рабочий лист

Следующий детализируемый лист:

```text
00_SYSTEM_TOP.kicad_sch
```

На нём нужно заменить текстовую архитектуру на функциональные блоки с точными hierarchical labels:

```text
BAT1_TO_BFE
BAT2_TO_BFE
PACK_BUS_TO_P12
PACK_BUS_TO_P5
PACK_BUS_TO_LIGHT
PACK_BUS_TO_CRIT
CTRL_TO_BFE
CTRL_TO_P12
CTRL_TO_P5
CTRL_TO_LIGHT
EXT_KILL_HW
RS485_ISOLATED
```

После этого следует лист:

```text
02_INTERBOARD_POWER_AND_CONTROL.kicad_sch
```

где будет зафиксирована первая версия pin-count и logical connector grouping.
