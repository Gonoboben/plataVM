# PlataVM

Аппаратный проект платы питания / энергетического модуля БНПА.

## Текущая опорная версия

```text
ПДУ БНПА / PlataVM V1.5 — multiboard schematic architecture
```

## Главная точка входа

1. `Docs/PROJECT_MASTER.md`
2. `Docs/ARCHITECTURE_BASELINE.md`
3. `Docs/SCHEMATIC_ARCHITECTURE.md`
4. `Docs/INTERBOARD_INTERFACES.md`
5. `Docs/NET_NAMING_RULES.md`
6. `Docs/POWER_TREE_V1_5.md`
7. `Docs/SN176A12_BATTERY_LINE_PINOUT.md`
8. `Docs/BATTERY_DISCONNECT.md`
9. `Docs/KBAT_ELECTRICAL_REQUIREMENTS.md`
10. `Docs/OPEN_QUESTIONS.md`
11. `Docs/CHRONOLOGY.md`
12. `Docs/adr/ADR-2026-07-10-multiboard-schematic-architecture.md`

## Главные решения V1.5

1. АКБ_1 и АКБ_2 — одинаковые LiFePO4 4S24P, 12,8 В, 144 А·ч каждая.
2. Обе основные АКБ в RUN работают параллельно через симметричные Battery Front-End.
3. `DECK_BALANCE` выполняет контролируемое межблочное выравнивание на палубе.
4. `K_BAT1/K_BAT2` — однополюсные моностабильные SPST-NO контакторы с электрическим самоподхватом.
5. При исчезновении защищённого выхода BMS контактор автоматически возвращается в OPEN; после восстановления требуется новый LOCAL_START.
6. BMS рассматривается как закрытый автономный двухполюсный источник без raw-ветви и цифрового управления.
7. СН-176А-12: 1–5 BAT+, 6–10 BAT−, 11 REMOTE_OFF / K_BAT_HOLD_RETURN, 12 RESERVE.
8. Центральный K_MAIN и MAIN_INPUT_BUS отсутствуют; PACK_BUS — главная силовая шина.
9. POWER_12V_BUS имеет 14 каналов по 3 А nominal/channel.
10. 5V_SYS_BUS имеет 10 выходов до 3 А и предварительный общий лимит 15/20 А.
11. LIGHT_POWER_BRANCH содержит шесть независимых LED-драйверов.
12. Основной внешний интерфейс — isolated RS-485 half-duplex.
13. Система принята как многоплатная архитектура из пяти функциональных PCB-модулей.

## Многоплатное разбиение

```text
PCB-A_BFE_POWER
PCB-B_CTRL_RESERVE
PCB-C_POWER_12V
PCB-D_POWER_5V
PCB-E_LIGHT_POWER
INTERCONNECT — пассивные шины/жгут/backplane
```

Высокие токи распределяются от PCB-A звездой или рассчитанной силовой шиной и не проходят через PCB-B.

## KiCad workspace

```text
Hardware/KiCad/
```

Первый архитектурный комплект:

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

## Текущий следующий этап

Подбор конкретных компонентов временно не является главным направлением. Следующая работа:

1. создать архитектурный каркас KiCad;
2. зафиксировать верхний лист системы;
3. построить логические листы пяти плат;
4. подсчитать межплатные сигналы;
5. определить ground/chassis/shield policy;
6. после этого детализировать узлы по одному через отдельные PR.

Конкретные part number на первом проходе могут оставаться TBD, но назначение узла, направление энергии, интерфейс и безопасное состояние должны быть определены.

## Правило работы

Изменения выполняются через отдельные ветки и pull request. Перед изменением схемы питания, интерфейсов, земли, защит, аккумуляторной архитектуры или аварийного питания необходимо обновить архитектурную базу или добавить ADR.