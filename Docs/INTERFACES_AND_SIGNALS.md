# Интерфейсы, шины и сигналы ПДУ БНПА / PlataVM

Статус:

```text
interfaces baseline for V1.5 battery architecture clarification
```

## 1. Основной интерфейс

```text
isolated RS-485 half-duplex
```

CAN/CAN-FD не входит в baseline V1.5 и допускается только как optional/future.

## 2. Энергетические шины

| Шина | Источник | Назначение |
|---|---|---|
| PACK_BUS | BFE_1/BFE_2 | главная силовая шина после двух АКБ |
| POWER_12V_BUS | PACK_BUS | CH1...CH14 |
| 5V_SYS_BUS | PACK_BUS через DC/DC | 5V_OUT1...5V_OUT10 |
| LIGHT_POWER_BRANCH | PACK_BUS | LED-драйверы |
| RESERVE_BRANCH | PACK_BUS + EMG | заряд EMG и keep-alive |
| 5V_CRIT | critical power path | MCU/связь/датчики |
| 3V3_CRIT | 5V_CRIT | цифровая логика |

`MAIN_INPUT_BUS` и центральный `K_MAIN` не используются.

## 3. Сигналы батарейных ветвей

Для АКБ_1:

1. `BAT1_CONTACTOR_ON` / `BAT1_CONTACTOR_OFF`.
2. `BAT1_CONTACTOR_FB`.
3. `BAT1_MAIN_SW_EN`.
4. `BAT1_BALANCE_SW_EN`.
5. `BAT1_PACK_PRESENT`.
6. `BAT1_V`.
7. `BAT1_I`.
8. `BAT1_T`.
9. `BAT1_BMS_STATUS`, если доступен.

Для АКБ_2 используются симметричные сигналы `BAT2_*`.

## 4. Сигналы HARD_OFF

1. `EXT_KILL` — независимый аппаратный запрос аварийного отключения.
2. `HARD_OFF_REQ` — программный запрос штатного завершения.
3. `BAT1_CONTACTOR_OFF`.
4. `BAT2_CONTACTOR_OFF`.
5. `BAT1_MAIN_SW_EN = 0`.
6. `BAT2_MAIN_SW_EN = 0`.
7. `PACK_BUS_DISCHARGE_EN`, если используется управляемый разряд.
8. `PACK_BUS_V` — контроль остаточного напряжения.

## 5. Сигналы POWER_12V_BUS

1. `CH1_EN` ... `CH11_EN`.
2. `CH1_FAULT` ... `CH14_FAULT`.
3. `CH1_ISENSE` ... `CH14_ISENSE`.
4. `CH12...CH14` являются Always-On monitored и отключаются защитой, SAFE и HARD_OFF.

## 6. Сигналы 5V_SYS_BUS

1. `5V_SYS_EN`.
2. `5V_OUT1_EN` ... `5V_OUT7_EN`.
3. `5V_OUT1_FAULT` ... `5V_OUT10_FAULT`.
4. `5V_OUT1_ISENSE` ... `5V_OUT10_ISENSE`.
5. `5V_OUT8...5V_OUT10` — Always-On monitored.

## 7. Сигналы LIGHT_POWER_BRANCH

1. `LED1_PWM` ... `LED6_PWM`.
2. `LED1_FAULT` ... `LED6_FAULT`.
3. `LED1_ISENSE` ... `LED6_ISENSE`.
4. общая команда `LIGHT_BRANCH_EN`.

## 8. Минимальная телеметрия

1. BAT1_V/I/T/SoC/PACK_PRESENT/contactor feedback.
2. BAT2_V/I/T/SoC/PACK_PRESENT/contactor feedback.
3. PACK_BUS_V и суммарный ток.
4. состояния CH1...CH14 и токи каналов.
5. состояния 5V_OUT1...5V_OUT10 и токи каналов.
6. состояния LED1...LED6 и токи каналов.
7. состояние EMG.
8. режим FSM.
9. fault-коды и журнал событий.
10. состояние RS-485.
