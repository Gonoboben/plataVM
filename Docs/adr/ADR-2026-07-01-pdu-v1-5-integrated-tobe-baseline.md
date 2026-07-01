# ADR-2026-07-01: Переход к V1.5 integrated TO-BE baseline

## 1. Контекст

Проект развивался через V1.3/V1.4 и TO-BE документы. Требовалось интегрировать полезные решения без возврата к устаревшим элементам.

## 2. Решение

Принять `V1.5 integrated TO-BE baseline`.

## 3. Принято

1. PACK_BUS / MAIN_INPUT_BUS / POWER_12V_BUS / 5V_SYS_BUS / LIGHT_POWER_BRANCH / RESERVE_BRANCH.
2. POWER_12V_BUS = 14 каналов.
3. CH1...CH11 MCU-controlled.
4. CH12...CH14 Always-On.
5. 5V_SYS_BUS отдельная от MAIN_INPUT_BUS.
6. LIGHT_POWER_BRANCH с onboard LED drivers.
7. RS-485 baseline.
8. CAN/CAN-FD optional future.
9. BATTERY_DISCONNECT + PRECHARGE обязательны.

## 4. Отклонено как baseline

1. TRACO POWER как целевая новая архитектура.
2. CAN/CAN-FD как обязательный интерфейс первой версии.
3. AUX1...AUX4 как модель выходов вместо CH1...CH14.
4. Питание 5V_SYS_BUS от EMG.

## 5. Последствия

Схема V1.5 должна проектироваться от MAIN_INPUT_BUS с четырьмя независимыми ветвями: POWER_12V_BUS, 5V_SYS_BUS, LIGHT_POWER_BRANCH, RESERVE_BRANCH.