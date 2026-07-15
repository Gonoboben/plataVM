# KiCad schematic skeleton manifest

Дата фиксации: 2026-07-14  
Дата обновления `00_SYSTEM_TOP`: 2026-07-15  
Статус:

```text
ARCHITECTURE LEVEL A — KiCad workspace skeleton + 00_SYSTEM_TOP functional sheet
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
5. Архитектурные текстовые ограничения на листах-заглушках.
6. Безопасные границы: батареи, PACK_BUS, HARD_OFF, EXT_KILL, земли и межплатные интерфейсы.
7. `00_SYSTEM_TOP.kicad_sch` переведён из текстовой заглушки в функциональный архитектурный лист уровня A.

## 4. Что зафиксировано на `00_SYSTEM_TOP`

Лист `00_SYSTEM_TOP.kicad_sch` содержит функциональные блоки и следующие top-level hierarchical labels:

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

Эти labels являются архитектурными именами интерфейсных групп. Детальный pin-count и физические connector groupings ещё не назначены.

## 5. Что пока не делается

1. Не выбирается контактор `K_BATx`.
2. Не выбираются `MAIN_SWx`.
3. Не выбираются датчики тока.
4. Не выбираются DC/DC, LED-драйверы, MCU и eFuse/high-side switches.
5. Не создаются footprints.
6. Не выполняется PCB layout.
7. Не объединяются автоматически `POWER_GND`, `SIGNAL_GND`, `ISO_GND` и `CHASSIS`.
8. Не назначаются физические межплатные разъёмы.

## 6. Проверка перед merge листа `00_SYSTEM_TOP`

Перед слиянием нужно локально открыть:

```text
Hardware/KiCad/PlataVM.kicad_pro
```

и проверить:

1. проект открывается в KiCad;
2. `00_SYSTEM_TOP.kicad_sch` открывается без ошибки парсинга;
3. видны функциональные текстовые блоки;
4. видны hierarchical labels из раздела 4;
5. KiCad не удаляет labels при сохранении;
6. `.kicad_prl` не появляется в Git changes из-за `.gitignore`.

## 7. Следующий рабочий лист

После проверки `00_SYSTEM_TOP` следует лист:

```text
02_INTERBOARD_POWER_AND_CONTROL.kicad_sch
```

На нём будет зафиксирована первая версия:

```text
logical connector grouping
pin-count estimate
power/control/diagnostic bundle separation
EXT_KILL routing group
POWER_GND/SIGNAL_GND/ISO_GND reference policy placeholders
```
