# PlataVM

Аппаратный проект платы питания / энергетического модуля БНПА.

## Текущая опорная версия

```text
ПДУ БНПА / PlataVM V1.8 — owner-input-reviewed multiboard architecture
```

## Главная точка входа

1. `Docs/PROJECT_MASTER.md`
2. `Docs/ARCHITECTURE_BASELINE.md`
3. `Docs/SYSTEM_POWER_BUDGET_POLICY.md`
4. `Docs/MECHANICAL_ENVELOPE_V1_8.md`
5. `Docs/SCHEMATIC_ARCHITECTURE.md`
6. `Docs/INTERBOARD_INTERFACES.md`
7. `Docs/NET_NAMING_RULES.md`
8. `Docs/POWER_TREE_V1_5.md`
9. `Docs/SN176A12_BATTERY_LINE_PINOUT.md`
10. `Docs/BATTERY_DISCONNECT.md`
11. `Docs/KBAT_ELECTRICAL_REQUIREMENTS.md`
12. `Docs/OPEN_QUESTIONS.md`
13. `Docs/OWNER_ANSWERS_REVIEW_V1_8.md`
14. `Docs/CHRONOLOGY.md`
15. `Docs/chronology/2026-07-21-owner-input-v1-8.md`
16. `Docs/adr/ADR-2026-07-21-owner-input-v1-8.md`
17. `Hardware/KiCad/SYSTEM_INTERFACE_CONSISTENCY_V1_6.md`

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
11. `SERVICE_OVERRIDE` disabled by default до отдельного решения владельца.
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

## KiCad workspace

```text
Hardware/KiCad/
```

```text
00_SYSTEM_TOP
01_EXTERNAL_BATTERIES_AND_HARNESS
02_INTERBOARD_POWER_AND_CONTROL
10…19 PCB-A
20…29 PCB-B
30…36 PCB-C
40…46 PCB-D
50…56 PCB-E
```

Владелец подтвердил открытие root project и листов 00…56. Перед schematic freeze требуется ERC release commit с записью версии KiCad.

## Текущий следующий этап

1. объяснить владельцу Q-SYS-007 и зафиксировать `SERVICE_OVERRIDE = disabled` либо guarded service mode;
2. выполнить preliminary PCB outlines внутри 100 × 250 × 80 мм;
3. определить уровни, mounting holes и размещение крупных компонентов;
4. сформировать internal power/signal harness concept;
5. выполнить physical CAN-FD/hard-line/power pin count;
6. выбрать interboard connectors;
7. рассчитать PCB-D/PCB-E losses без thermal contact с корпусом;
8. выбрать кандидаты K_BATx и REMOTE_OFF relay;
9. провести BMS/K_BATx/thermal tests;
10. продолжить component selection по закрытым подсистемам.

## Правило работы

Изменения выполняются через отдельные ветки и pull request. Перед изменением power architecture, interfaces, grounds, protections, battery architecture, emergency power, thermal path или system power policy необходимо обновить архитектурную базу или добавить ADR.
