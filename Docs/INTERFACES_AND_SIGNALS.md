# Интерфейсы, шины и сигналы ПДУ БНПА / PlataVM

Статус:

```text
interfaces baseline for V1.5 integrated TO-BE architecture
```

## 1. Основной интерфейс

```text
isolated RS-485 half-duplex
```

CAN/CAN-FD не входит в baseline V1.5 и допускается только как optional/future.

## 2. Энергетические шины

| Шина | Источник | Назначение |
|---|---|---|
| PACK_BUS | BFE_1/BFE_2 | объединение АКБ |
| MAIN_INPUT_BUS | BATTERY_DISCONNECT/PRECHARGE | главная шина |
| POWER_12V_BUS | MAIN_INPUT_BUS | CH1...CH14 |
| 5V_SYS_BUS | MAIN_INPUT_BUS через DC/DC | 5V_OUT |
| LIGHT_POWER_BRANCH | MAIN_INPUT_BUS | LED-драйверы |
| RESERVE_BRANCH | EMG/MAIN_INPUT_BUS | keep-alive |
| 5V_CRIT | critical power path | MCU/связь/датчики |
| 3V3_CRIT | 5V_CRIT | цифровая логика |

## 3. Канальные сигналы

1. `CH1_EN` ... `CH11_EN`.
2. `CH1_FAULT` ... `CH14_FAULT`.
3. `CH1_ISENSE` ... `CH14_ISENSE`, если измерение реализовано.
4. `5V_SYS_EN`.
5. `5V_OUTx_EN`, если 5 В выходы будут канальными.
6. `LED1_PWM` ... `LED6_PWM`.
7. `LED1_FAULT` ... `LED6_FAULT`.
8. `PRECHARGE_EN`.
9. `BATTERY_DISCONNECT_SET`.
10. `BATTERY_DISCONNECT_RESET`.
11. `EXT_KILL`.
12. `PACK_PRESENT_1/2`.

## 4. Минимальная телеметрия

Напряжения, токи, температуры, состояния каналов, fault-коды, режим FSM, состояние BATTERY_DISCONNECT, состояние PRECHARGE, статус связи.