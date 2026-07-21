# PlataVM

Аппаратный проект платы питания / энергетического модуля БНПА.

## Текущая опорная версия

```text
ПДУ БНПА / PlataVM V1.7 — owner-input-reviewed multiboard architecture
```

## Главная точка входа

1. `Docs/PROJECT_MASTER.md`
2. `Docs/ARCHITECTURE_BASELINE.md`
3. `Docs/SYSTEM_POWER_BUDGET_POLICY.md`
4. `Docs/MECHANICAL_ENVELOPE_V1_7.md`
5. `Docs/SCHEMATIC_ARCHITECTURE.md`
6. `Docs/INTERBOARD_INTERFACES.md`
7. `Docs/NET_NAMING_RULES.md`
8. `Docs/POWER_TREE_V1_5.md`
9. `Docs/SN176A12_BATTERY_LINE_PINOUT.md`
10. `Docs/BATTERY_DISCONNECT.md`
11. `Docs/KBAT_ELECTRICAL_REQUIREMENTS.md`
12. `Docs/OPEN_QUESTIONS.md`
13. `Docs/OWNER_ANSWERS_REVIEW_V1_7.md`
14. `Docs/CHRONOLOGY.md`
15. `Docs/adr/ADR-2026-07-21-owner-input-v1-7.md`
16. `Hardware/KiCad/SYSTEM_INTERFACE_CONSISTENCY_V1_6.md`

## Главные решения

1. АКБ_1 и АКБ_2 — одинаковые LiFePO4 4S24P, 12,8 В, 144 А·ч каждая.
2. Обе исправные основные АКБ в DUAL_PACK_RUN работают параллельно через симметричные Battery Front-End.
3. `SINGLE_PACK_MODE` — деградированный, но функциональный режим одной основной АКБ.
4. Системный предел PACK_BUS: 40/44 А для двух АКБ и 20/22 А для одной АКБ.
5. При 85 % active continuous budget формируется warning; при 100 % отклоняется новая некритическая команда.
6. Сам вход в SINGLE_PACK_MODE не выключает нагрузки и не снижает яркость автоматически.
7. `DECK_BALANCE` выполняет контролируемое межблочное выравнивание на палубе и запрещён в SINGLE_PACK_MODE.
8. `K_BAT1/K_BAT2` — однополюсные моностабильные SPST-NO контакторы с электрическим самоподхватом.
9. При исчезновении защищённого выхода BMS контактор автоматически возвращается в OPEN; после восстановления требуется новый LOCAL_START.
10. BMS рассматривается как закрытый автономный двухполюсный источник без raw-ветви и цифрового управления.
11. СН-176А-12: 1–5 BAT+, 6–10 BAT−, 11 REMOTE_OFF / K_BAT_HOLD_RETURN, 12 RESERVE.
12. Центральный K_MAIN и MAIN_INPUT_BUS отсутствуют; PACK_BUS — главная силовая шина.
13. POWER_12V_BUS имеет 14 каналов по 3 А continuous и 5 А peak/1 с.
14. 5V_SYS_BUS имеет 10 выходов до 3 А и предварительный общий лимит 15/20 А.
15. LIGHT_POWER_BRANCH содержит шесть независимых LED-драйверов в двух зонах 2×3.
16. Основной внешний интерфейс — isolated RS-485 half-duplex.
17. Внутренний интерфейс PCB-B↔PCB-C/D/E — CAN-FD; SAFE/HARD_OFF и критические fault-линии остаются аппаратными.
18. `SIGNAL_GND–POWER_GND` соединяются в одной контролируемой точке PCB-B; `ISO_GND` и `CHASSIS` сохраняют отдельные функции.
19. Система состоит из пяти функциональных PCB-модулей и пассивного INTERCONNECT.
20. Корпус электроники — цилиндр Ø130 мм × 1000 мм, один торец заварен, второй закрыт съёмной крышкой с разъёмами.
21. Внутренняя механика предварительно строится на продольном извлекаемом carrier/tray со стороны крышки.
22. Рабочая температура −20…+60 °C, хранение −30…+70 °C, conformal coating обязателен.

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

Владелец подтвердил, что текущий root project и листы 00…56 открываются нормально. Перед schematic freeze требуется ERC конкретного release commit с фиксацией версии KiCad.

## Текущий следующий этап

Owner-level решения V1.7 закрыты. Следующая последовательность:

1. получить внутренние размеры цилиндра, материал, pressure/vibration data и карту разъёмов крышки;
2. построить первый 3D packaging/carrier concept;
3. определить физический порядок CAN-FD nodes и termination;
4. выполнить power/hard-line/signal pin count;
5. выбрать physical interboard connectors;
6. определить short-limit duration, filters/hysteresis и реальные load profiles;
7. выбрать кандидаты K_BATx и REMOTE_OFF relay;
8. провести BMS/K_BATx fault, thermal, release, vibration и life tests;
9. продолжить component selection по подсистемам с закрытыми входными данными.

## Правило работы

Изменения выполняются через отдельные ветки и pull request. Перед изменением схемы питания, интерфейсов, земли, защит, аккумуляторной архитектуры, аварийного питания или общего power-budget policy необходимо обновить архитектурную базу или добавить ADR.
