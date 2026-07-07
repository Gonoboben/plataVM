# Архитектура управления V1.5

## 1. Верхний уровень

```text
HOST / Computer → isolated RS-485 → MCU → FSM / Fault Manager / Telemetry
```

## 2. MCU управляет

1. Battery Front-End #1 и #2.
2. Электронными силовыми трактами `MAIN_SW1` и `MAIN_SW2`.
3. Ограниченными трактами `BALANCE_SW1 + R_BAL1` и `BALANCE_SW2 + R_BAL2`.
4. Командами включения и отключения `K_BAT1` и `K_BAT2`.
5. `POWER_12V_BUS` CH1...CH14.
6. `5V_SYS_BUS` и 10 выходами 5 В.
7. `LIGHT_POWER_BRANCH` и шестью световыми каналами.
8. `RESERVE_BRANCH` и зарядом EMG.
9. Телеметрией, оценкой SoC и журналом событий.
10. Режимом `DECK_BALANCE`.

Центральные `K_MAIN` и `MAIN_INPUT_BUS` не используются.

## 3. Состояния MCU

```text
OFF
BOOT
SELF_TEST
DECK_BALANCE
RUN
SAFE
KEEP_ALIVE
HARD_OFF
FAULT_LATCH
```

Отдельного состояния `BATTERY_MISMATCH` нет.

## 4. RUN

Обе исправные основные АКБ работают параллельно. MCU измеряет ток, напряжение, температуру и SoC каждой ветви, но не отключает батарею только из-за различия уровня заряда.

## 5. DECK_BALANCE

На палубе MCU:

1. отключает тяжёлые нагрузки;
2. измеряет состояние обеих АКБ;
3. включает ограниченный балансировочный тракт;
4. контролирует ток, температуру и время;
5. завершает балансировку по заданным критериям;
6. при необходимости обслуживает заряд EMG.

## 6. HARD_OFF

### Штатный

```text
снять тяжёлые нагрузки
→ сохранить журнал и SoC
→ K_BAT1 OFF
→ K_BAT2 OFF
→ проверить токи ветвей и PACK_BUS
→ завершить работу от EMG
```

### Аварийный

```text
EXT_KILL / critical fault
→ MAIN_SW1 OFF
→ MAIN_SW2 OFF
→ K_BAT1 OFF
→ K_BAT2 OFF
→ сохранить причину события от EMG
```

## 7. Сервисные интерфейсы

1. UART — debug/service.
2. SWD — программирование и отладка.
3. CAN/CAN-FD — optional future footprint, не baseline.
