# Хронология PlataVM

## 2026-07-01 — интеграция V1.5 integrated TO-BE baseline

Что изменено:

1. Принята архитектура `V1.5 integrated TO-BE baseline`.
2. Интегрирована структура PACK_BUS / MAIN_INPUT_BUS / POWER_12V_BUS / 5V_SYS_BUS / LIGHT_POWER_BRANCH / RESERVE_BRANCH.
3. POWER_12V_BUS расширена до 14 каналов.
4. Принято: CH1...CH11 MCU-controlled, CH12...CH14 Always-On.
5. Добавлена отдельная 5V_SYS_BUS для внешних 5 В разъёмов.
6. 5V_SYS_BUS питается от MAIN_INPUT_BUS через отдельный DC/DC.
7. 5V_SYS_BUS не питается от EMG.
8. LIGHT_POWER_BRANCH переведена на onboard LED drivers.
9. TRACO переведён в legacy/current implementation.
10. RS-485 принят как baseline.
11. CAN/CAN-FD переведён в optional future.
12. BATTERY_DISCONNECT, PRECHARGE, Battery Front-End вынесены в отдельные документы.

Что специально не изменялось:

1. Электрическая схема не создавалась.
2. PCB не создавалась.
3. BOM с артикулами не утверждался.
4. MCU не выбран.
5. Номиналы precharge не рассчитаны.
6. Назначения CH1...CH14 не заданы.

Следующий шаг:

```text
закрыть OPEN_QUESTIONS.md перед schematic freeze V1.5
```