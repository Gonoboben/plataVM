# PlataVM

Аппаратный проект платы питания / энергетического модуля БНПА.

## Текущая опорная версия

```text
ПДУ БНПА / PlataVM V1.6 — owner-input-reviewed multiboard architecture
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
11. `Docs/OWNER_ANSWERS_REVIEW_V1_6.md`
12. `Docs/CHRONOLOGY.md`
13. `Docs/adr/ADR-2026-07-16-owner-input-v1-6.md`
14. `Docs/adr/ADR-2026-07-10-multiboard-schematic-architecture.md`

## Главные решения

1. АКБ_1 и АКБ_2 — одинаковые LiFePO4 4S24P, 12,8 В, 144 А·ч каждая.
2. Обе основные АКБ в RUN работают параллельно через симметричные Battery Front-End.
3. `DECK_BALANCE` выполняет контролируемое межблочное выравнивание на палубе.
4. `K_BAT1/K_BAT2` — однополюсные моностабильные SPST-NO контакторы с электрическим самоподхватом.
5. При исчезновении защищённого выхода BMS контактор автоматически возвращается в OPEN; после восстановления требуется новый LOCAL_START.
6. BMS рассматривается как закрытый автономный двухполюсный источник без raw-ветви и цифрового управления.
7. СН-176А-12: 1–5 BAT+, 6–10 BAT−, 11 REMOTE_OFF / K_BAT_HOLD_RETURN, 12 RESERVE.
8. Центральный K_MAIN и MAIN_INPUT_BUS отсутствуют; PACK_BUS — главная силовая шина.
9. POWER_12V_BUS имеет 14 каналов по 3 А continuous и 5 А peak/1 с.
10. 5V_SYS_BUS имеет 10 выходов до 3 А и предварительный общий лимит 15/20 А.
11. LIGHT_POWER_BRANCH содержит шесть независимых LED-драйверов в двух зонах 2×3.
12. Основной внешний интерфейс — isolated RS-485 half-duplex.
13. Внутренний интерфейс PCB-B↔PCB-C/D/E — CAN-FD; SAFE/HARD_OFF и критические fault-линии остаются аппаратными.
14. `SIGNAL_GND–POWER_GND` соединяются в одной контролируемой точке PCB-B; `ISO_GND` и `CHASSIS` сохраняют отдельные функции.
15. Система состоит из пяти функциональных PCB-модулей и пассивного INTERCONNECT.

## Многоплатное разбиение

```text
PCB-A_BFE_POWER
PCB-B_CTRL_RESERVE
PCB-C_POWER_12V
PCB-D_POWER_5V
PCB-E_LIGHT_POWER
INTERCONNECT — пассивные шины/жгут/backplane
```

Высокие токи распределяются от PCB-A и не проходят через PCB-B.

## KiCad workspace

```text
Hardware/KiCad/
```

Архитектурная иерархия:

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

## Текущий следующий этап

Gate G-R открыт частично. Разрешены расчёты узлов с закрытыми входными данными.

Блокирующая последовательность:

1. получить ответы V1.7 по общему power budget, SINGLE_PACK_MODE, условиям эксплуатации и механике;
2. проверить KiCad workspace в установленной версии;
3. обновить физическую карту межплатных CAN-FD/hard-line interfaces;
4. выполнить pin count и выбрать разъёмы;
5. выбрать кандидаты K_BATx и REMOTE_OFF relay;
6. провести BMS/K_BATx fault, thermal и release tests;
7. после закрытия входных данных перейти к component selection и расчётным схемам PCB-C/D/E.

## Правило работы

Изменения выполняются через отдельные ветки и pull request. Перед изменением схемы питания, интерфейсов, земли, защит, аккумуляторной архитектуры или аварийного питания необходимо обновить архитектурную базу или добавить ADR.
