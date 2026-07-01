# Архитектура управления V1.5

## 1. Верхний уровень

```text
HOST / Computer → isolated RS-485 → MCU → FSM / Fault Manager / Telemetry
```

## 2. MCU управляет

1. Battery Front-End.
2. PRECHARGE.
3. BATTERY_DISCONNECT set/reset через разрешённые цепи.
4. POWER_12V_BUS CH1...CH14.
5. 5V_SYS_BUS.
6. LIGHT_POWER_BRANCH.
7. RESERVE_BRANCH.
8. Зарядом EMG.
9. Телеметрией и журналом событий.

## 3. Сервисные интерфейсы

1. UART — debug/service.
2. SWD — программирование и отладка.
3. CAN/CAN-FD — optional future footprint, не baseline.