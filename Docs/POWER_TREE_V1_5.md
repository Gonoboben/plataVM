# Дерево питания ПДУ БНПА V1.5

## 1. Схема верхнего уровня

```text
АКБ_1 → BFE_1 ┐
               ├→ PACK_BUS → BATTERY_DISCONNECT + PRECHARGE → MAIN_INPUT_BUS
АКБ_2 → BFE_2 ┘

MAIN_INPUT_BUS
    ├─ POWER_12V_BUS → CH1...CH14
    ├─ 5V_SYS_BUS → 5V_OUT1...5V_OUTn
    ├─ LIGHT_POWER_BRANCH → LED drivers → 6 × Epistar XY-J45
    └─ RESERVE_BRANCH → EMG / KEEP_ALIVE / 5V_CRIT / 3V3_CRIT
```

## 2. Правило разделения ветвей

`POWER_12V_BUS`, `5V_SYS_BUS`, `LIGHT_POWER_BRANCH` и `RESERVE_BRANCH` являются отдельными ветвями от `MAIN_INPUT_BUS`.

## 3. Что питается от резерва

Только critical/keep-alive домен:

1. MCU.
2. Связь.
3. Критические датчики.
4. Fault/event logic.
5. 5V_CRIT.
6. 3V3_CRIT.

## 4. Что не питается от резерва

1. CH1...CH14.
2. 5V_SYS_BUS.
3. LED-драйверы.
4. Силовые внешние нагрузки.