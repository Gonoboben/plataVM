# PlataVM

Аппаратный проект платы питания / энергетического модуля БНПА.

## Текущая опорная версия

```text
ПДУ БНПА / PlataVM V1.9 — guarded service policy, packaging boundary and preliminary KiCad board outlines
```

## Главная точка входа

1. `Docs/PROJECT_MASTER.md`
2. `Docs/ARCHITECTURE_BASELINE.md`
3. `Docs/SYSTEM_POWER_BUDGET_POLICY.md`
4. `Docs/SERVICE_OVERRIDE_POLICY.md`
5. `Docs/MECHANICAL_ENVELOPE_V1_8.md`
6. `Docs/PCB_PACKAGING_BOUNDARY_V1_9.md`
7. `Docs/PCB_MODULE_AREA_BUDGET_V1_9.md`
8. `Docs/PHYSICAL_INTERFACE_COUNT_V1_9.md`
9. `Docs/BRANCH_CURRENT_PRECALC_V1_9.md`
10. `Docs/BASELINE_CONSISTENCY_V1_9.md`
11. `Docs/SCHEMATIC_ARCHITECTURE.md`
12. `Docs/INTERBOARD_INTERFACES.md`
13. `Docs/NET_NAMING_RULES.md`
14. `Docs/POWER_TREE_V1_5.md`
15. `Docs/SN176A12_BATTERY_LINE_PINOUT.md`
16. `Docs/BATTERY_DISCONNECT.md`
17. `Docs/KBAT_ELECTRICAL_REQUIREMENTS.md`
18. `Docs/OPEN_QUESTIONS.md`
19. `Docs/OWNER_ANSWERS_REVIEW_V1_8.md`
20. `Docs/CHRONOLOGY.md`
21. `Docs/chronology/2026-07-21-service-override-v1-9.md`
22. `Docs/adr/ADR-2026-07-21-service-override-v1-9.md`
23. `Hardware/KiCad/SYSTEM_INTERFACE_CONSISTENCY_V1_6.md`
24. `Hardware/KiCad/Boards/README.md`
25. `Hardware/KiCad/Boards/PRELIMINARY_OUTLINE_VALIDATION_V1_9.md`

## Главные решения

1. АКБ_1 и АКБ_2 — LiFePO4 4S24P, 12,8 В, 144 А·ч каждая.
2. Обе исправные АКБ работают параллельно в `DUAL_PACK_RUN`.
3. `SINGLE_PACK_MODE` — деградированный, но функциональный режим одной АКБ.
4. PACK_BUS budget: 40 А continuous / 44 А short для двух АКБ; 20 А / 22 А для одной.
5. Short-limit действует не более 1 с; repeat interval не менее 10 с; используется I²t/thermal accumulator.
6. Budget manager: low-pass 100 мс; warning ON >85 %/250 мс; OFF <80 %/2 с; re-enable new loads <90 %/2 с.
7. При 100 % budget отклоняется новая некритическая команда; уже включённые нагрузки software manager не сбрасывает.
8. Critical domain — 5V_CRIT/3V3_CRIT, supervisor, fault manager, communication и journal retention.
9. CH1…CH14, 5V_OUT1…10 и LED1…6 — некритические для admission control.
10. Unknown load profile использует консервативный maximum и `LOAD_PROFILE_UNKNOWN`.
11. `SERVICE_OVERRIDE` принят как guarded service function: только SERVICE_MODE, двойное подтверждение, один output, lease 60 с, short limits не изменяются.
12. `DECK_BALANCE` выполняется на палубе и запрещён в SINGLE_PACK_MODE.
13. K_BAT1/K_BAT2 — однополюсные моностабильные SPST-NO с self-hold.
14. После BMS recovery требуется новый LOCAL_START.
15. BMS — автономный protected source без raw/digital control.
16. СН-176А-12: 1–5 BAT+, 6–10 BAT−, 11 REMOTE_OFF, 12 RESERVE.
17. K_MAIN и MAIN_INPUT_BUS отсутствуют; PACK_BUS — главная силовая шина.
18. Внешняя связь — isolated RS-485; внутренняя PCB-B↔C/D/E — CAN-FD с direct safety/fault lines.
19. SIGNAL_GND–POWER_GND соединяются в одной controlled point PCB-B; ISO_GND и CHASSIS отдельны.
20. Пять PCB-модулей и пассивный INTERCONNECT.
21. Доступный внутренний корпус — цилиндр Ø130 × 1000 мм.
22. Электронная сборка — многоуровневая, ≤100 × 250 × 80 мм.
23. Вся сборка извлекается вместе с крышкой; платы винтами крепятся к стойкам.
24. Отдельный mandatory carrier/tray не требуется.
25. Thermal contact с корпусом запрещён; охлаждение — low-loss design, PCB copper и internal natural convection.
26. Thermal verification выполняется при +60 °C без hull heat sink.
27. Hot-melt polyethylene adhesive — только auxiliary anti-vibration/strain relief.
28. Preliminary packaging candidate: L0 PCB-A+PCB-C, L1 PCB-D+PCB-E, L2 PCB-B.
29. Preliminary board targets: A 94×110, B 94×180, C 94×130, D 94×125, E 94×110 мм.
30. Preliminary signal classes: A↔B 32 positions; B↔C/D/E standardized 8 positions each.
31. Preliminary power classes: A→C 30 А, A→D 15 А, A→E 25 А.
32. PCB-D preliminary input current: 9,26 А continuous worst checked point and 12,35 А short.
33. PCB-E preliminary input current at 180 Вт: 22,23 А worst checked point.
34. PCB-E thermal compliance at 180 Вт is not proven and remains a mandatory calculation/test item.
35. Созданы пять preliminary `.kicad_pcb` files только с Edge.Cuts, labels и графическими `MHx_TBD` zones.
36. Board files не содержат footprints, pads, nets, copper, vias, actual drills или production routing.

## Многоплатное разбиение

```text
PCB-A_BFE_POWER
PCB-B_CTRL_RESERVE
PCB-C_POWER_12V
PCB-D_POWER_5V
PCB-E_LIGHT_POWER
INTERCONNECT — passive power/signal wiring or backplane
```

High current распределяется от PCB-A и не проходит через PCB-B.

## Preliminary packaging

```text
L0: PCB-A + PCB-C
L1: PCB-D + PCB-E
L2: PCB-B
```

Формальная геометрическая проверка:

```text
L0 length = 240 мм < 250 мм
L1 length = 235 мм < 250 мм
L2 length = 180 мм < 250 мм
height budget = 79 мм < 80 мм
```

Размеры являются area budget, а не final board outlines.

## Preliminary branch-current result

```text
PACK_BUS_P5_IN:
15 А connector class preliminary

PACK_BUS_LIGHT_IN:
25 А connector class preliminary
```

При 9,2 В и η=88 %:

```text
PCB-D 75 Вт output → 9,26 А input
PCB-D 100 Вт short → 12,35 А input
PCB-E 180 Вт output → 22,23 А input
```

Значения задают нижнюю границу для connector candidate search. Финальные efficiency, ripple, temperature rise и sealed-volume thermal compliance остаются открытыми.

## Проверка связности V1.9

```text
Architecture continuity: PASS
Service policy consistency: PASS
Packaging arithmetic: PASS PRELIMINARY
Interface arithmetic: PASS AFTER CORRECTION
Power branch precalc: PASS PRELIMINARY
Thermal compliance: OPEN CONTROLLED BLOCKER
```

Подробности — `Docs/BASELINE_CONSISTENCY_V1_9.md`.

## KiCad workspace

Схемы:

```text
Hardware/KiCad/
00_SYSTEM_TOP
01_EXTERNAL_BATTERIES_AND_HARNESS
02_INTERBOARD_POWER_AND_CONTROL
10…19 PCB-A
20…29 PCB-B
30…36 PCB-C
40…46 PCB-D
50…56 PCB-E
```

Preliminary board outlines:

```text
Hardware/KiCad/Boards/PCB-A_BFE_POWER.kicad_pcb
Hardware/KiCad/Boards/PCB-B_CTRL_RESERVE.kicad_pcb
Hardware/KiCad/Boards/PCB-C_POWER_12V.kicad_pcb
Hardware/KiCad/Boards/PCB-D_POWER_5V.kicad_pcb
Hardware/KiCad/Boards/PCB-E_LIGHT_POWER.kicad_pcb
```

Владелец подтвердил открытие root schematic project и листов 00…56. Board files прошли структурную проверку, но должны быть открыты владельцем в KiCad PCB Editor; `kicad-cli/pcbnew` в текущем окружении отсутствуют.

## Текущий следующий этап

1. открыть пять preliminary board files в установленной версии KiCad и подтвердить отсутствие parser errors;
2. выполнить component-height/3D audit для трёх уровней;
3. проверить tool-access к `MHx_TBD` zones;
4. решить A↔B connector topology: 32 positions либо 16+16;
5. определить physical CAN-FD node order и termination;
6. рассчитать PCB-B critical branch current;
7. уточнить PCB-D efficiency/input ripple;
8. уточнить actual LED load и PCB-E efficiency;
9. сравнить connector classes по току, высоте, mating cycles и coating compatibility;
10. выполнить thermal-loss budget PCB-D/PCB-E без контакта с корпусом;
11. выбрать кандидаты K_BATx и REMOTE_OFF relay;
12. провести BMS/K_BATx/thermal tests.

## Правило работы

Изменения выполняются через отдельные ветки и pull request. Перед изменением power architecture, interfaces, grounds, protections, battery architecture, emergency power, thermal path, system power policy или packaging boundary необходимо обновить архитектурную базу или добавить ADR.
