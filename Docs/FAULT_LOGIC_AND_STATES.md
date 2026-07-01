# Состояния, аварийная логика и реакции ПДУ БНПА / PlataVM

Статус:

```text
state-machine baseline for V1.5 integrated TO-BE architecture
```

## 1. Состояния

| Состояние | Назначение |
|---|---|
| OFF | питание силовых ветвей выключено |
| BOOT | запуск critical и MCU |
| SELF_TEST | самопроверка |
| DECK_BALANCE | палубное обслуживание, мягкие операции с АКБ и резервом |
| PRECHARGE | предзаряд MAIN_INPUT_BUS |
| RUN | штатная работа |
| SAFE | ограничение нагрузки перед отключением |
| KEEP_ALIVE | питание только критического домена |
| HARD_OFF | аппаратное отключение BATTERY_DISCONNECT |
| FAULT_LATCH | аварийная защёлка |

## 2. Ключевая логика

```text
оба PACK_PRESENT lost → SAFE → 7 секунд → HARD_OFF
```

## 3. Запрещено

1. Включать BATTERY_DISCONNECT без PRECHARGE.
2. Питать POWER_12V_BUS от EMG.
3. Питать 5V_SYS_BUS от EMG.
4. Питать LIGHT_POWER_BRANCH от EMG.
5. Сбрасывать latched fault без условий безопасности.
6. Игнорировать EXT_KILL.

## 4. Аварийные реакции

| Авария | Реакция |
|---|---|
| Precharge timeout | запрет включения BATTERY_DISCONNECT |
| EXT_KILL | немедленный HARD_OFF |
| Overcurrent CHx | отключить канал, записать fault |
| 5V_SYS fault | отключить 5V_SYS, сохранить critical |
| LED fault | отключить аварийный LED-канал |
| RS-485 timeout | перейти в безопасную политику |
| EMG undervoltage | ограничить keep-alive, отправить fault |