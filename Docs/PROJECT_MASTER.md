# Главная концепция проекта ПДУ БНПА / PlataVM

Дата фиксации: 2026-07-01

Статус:

```text
главный управляющий документ проекта
```

Рабочая версия:

```text
V1.5 integrated TO-BE baseline
```

## 1. Назначение

Документ фиксирует полную рабочую концепцию проекта платы питания БНПА. Он является верхним уровнем проекта и должен использоваться как основная ссылка при разработке схемы, PCB, BOM, прошивки и испытаний.

## 2. Граница проекта

В проект входят:

1. АКБ_1 и АКБ_2 LiFePO4 4s24p.
2. Battery Front-End каждого основного аккумулятора.
3. PACK_BUS.
4. BATTERY_DISCONNECT / HARD OFF.
5. PRECHARGE.
6. MAIN_INPUT_BUS.
7. POWER_12V_BUS.
8. 5V_SYS_BUS.
9. LIGHT_POWER_BRANCH.
10. RESERVE_BRANCH / EMG_4S2P / KEEP_ALIVE.
11. 5V_CRIT / 3V3_CRIT.
12. MCU, RS-485, телеметрия, fault manager.
13. Схема, PCB, BOM, прошивка, испытания и выпускная документация.

## 3. Источник архитектуры

V1.5 собрана из:

1. ПДУ БНПА V1.3.
2. TO-BE Power v2.1.
3. TO-BE Control v2.1.
4. Узел BATTERY_DISCONNECT v1.1.
5. Аналитический отчёт проекта.
6. Решения владельца проекта в чате:
   - POWER_12V_BUS = 14 каналов;
   - 3 Always-On;
   - внешние 5 В разъёмы обязательны;
   - 5V_SYS_BUS отдельная;
   - TRACO не использовать как целевую архитектуру;
   - RS-485 baseline, CAN/CAN-FD optional.

## 4. Каноническая архитектура

```text
АКБ_1 LiFePO4 4s24p
        ↓
Battery Front-End #1
        ↓
PACK_BUS
        ↑
Battery Front-End #2
        ↑
АКБ_2 LiFePO4 4s24p

PACK_BUS
        ↓
BATTERY_DISCONNECT + PRECHARGE + EXT_KILL
        ↓
MAIN_INPUT_BUS
        ↓
 ┌────────────────────────┬────────────────────────┬────────────────────────┬────────────────────────┐
 ↓                        ↓                        ↓                        ↓
POWER_12V_BUS             5V_SYS_BUS                LIGHT_POWER_BRANCH        RESERVE_BRANCH
CH1...CH14                5V_OUT1...5V_OUTn         onboard LED drivers       EMG_4S2P
11 MCU-controlled         external 5 V outputs      Epistar XY-J45            KEEP_ALIVE
3 Always-On               protected outputs         PWM/current/fault         5V_CRIT/3V3_CRIT
```

## 5. Принятые решения

1. `POWER_12V_BUS` = 14 каналов.
2. `CH1...CH11` = MCU-controlled.
3. `CH12...CH14` = Always-On.
4. Назначения CH1...CH14 пока не задаются.
5. Все выходы с платы выводятся на разъёмы.
6. Внешние 5 В выходы обязательны.
7. `5V_SYS_BUS` питается от `MAIN_INPUT_BUS`, а не от `POWER_12V_BUS`.
8. `5V_SYS_BUS` не питается от `RESERVE_BRANCH`.
9. `5V_CRIT` и `3V3_CRIT` отделены от `5V_SYS_BUS`.
10. Световая ветвь строится на собственных преобразователях/LED-драйверах платы.
11. TRACO POWER — только legacy/current implementation.
12. Основной интерфейс — изолированный RS-485 half-duplex.
13. CAN/CAN-FD — future option.
14. `EXT_KILL` должен работать независимо от MCU.
15. `PRECHARGE` обязателен.

## 6. Следующий рубеж

```text
schematic freeze V1.5
```

До него нужно закрыть вопросы по 5V_OUT, токам каналов, LED-драйверу, Battery Front-End, precharge, BATTERY_DISCONNECT, EMG, MCU и механике.