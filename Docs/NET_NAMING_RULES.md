# Правила именования сетей PlataVM

Дата фиксации: 2026-07-10  
Статус: `SCHEMATIC NAMING BASELINE`

## 1. Общие правила

1. Имена сетей пишутся латиницей, верхним регистром, слова разделяются `_`.
2. Активный низкий уровень обозначается суффиксом `_N`.
3. Команда разрешения — `_EN`, запрос — `_REQ`, подтверждение — `_ACK`, авария — `_FAULT_N`.
4. Измерение напряжения — `_VSENSE`, тока — `_ISENSE`, температуры — `_TEMP`.
5. Номер батареи, платы, канала или выхода является частью имени.
6. Не использовать неоднозначные имена `VCC`, `VIN`, `OUT`, `GND`, `ENABLE`, `FAULT` без префикса узла.
7. Глобальные power symbols допускаются только для утверждённых системных шин.

## 2. Системные силовые сети

```text
BAT1_P
BAT1_N
BAT2_P
BAT2_N
PACK_BUS
POWER_GND
PACK_BUS_P12_IN
PACK_BUS_P5_IN
PACK_BUS_LIGHT_IN
PACK_BUS_CRIT_IN
5V_SYS
5V_CRIT
3V3_CRIT
SIGNAL_GND
ISO_GND
CHASSIS
```

`POWER_GND`, `SIGNAL_GND`, `ISO_GND` и `CHASSIS` не объединяются автоматически.

## 3. Батарейные ветви

```text
BAT1_PRESENT
BAT2_PRESENT
BAT1_VSENSE
BAT2_VSENSE
BAT1_ISENSE
BAT2_ISENSE
BAT1_MAIN_SW_EN
BAT2_MAIN_SW_EN
BAT1_BALANCE_SW_EN
BAT2_BALANCE_SW_EN
BAT1_HOLD_LOOP_OPEN_CMD
BAT2_HOLD_LOOP_OPEN_CMD
BFE1_FAULT_N
BFE2_FAULT_N
```

Внутренние точки ячеек и BMS не именуются и не вводятся в проект.

## 4. PACK_BUS и аварийное отключение

```text
PACK_BUS_VSENSE
PACK_BUS_ISENSE
PACK_BUS_DISCHARGE_EN
PACK_BUS_DISCHARGE_FAULT_N
EXT_KILL
EXT_KILL_HW
BAT1_HOLD_LOOP_OPEN_HW
BAT2_HOLD_LOOP_OPEN_HW
BAT1_MAIN_SW_OFF_HW
BAT2_MAIN_SW_OFF_HW
```

## 5. POWER_12V_BUS

```text
P12_CH_EN[1..11]
P12_CH_FAULT_N[1..14]
P12_CH_ISENSE[1..14]
P12_GROUP_SAFE_OFF
P12_GROUP_HARD_OFF
P12_INPUT_VSENSE
P12_BOARD_TEMP
P12_BOARD_FAULT_N
CH1_OUT ... CH14_OUT
```

## 6. 5V_SYS_BUS

```text
5V_SYS_EN
P5_OUT_EN[1..7]
P5_OUT_FAULT_N[1..10]
P5_OUT_ISENSE[1..10]
P5_GROUP_SAFE_OFF
P5_GROUP_HARD_OFF
5V_SYS_VSENSE
5V_SYS_TOTAL_ISENSE
P5_BOARD_TEMP
P5_BOARD_FAULT_N
5V_OUT1 ... 5V_OUT10
```

## 7. LIGHT_POWER_BRANCH

```text
LIGHT_BRANCH_EN
LIGHT_GROUP_HARD_OFF
LED_PWM[1..6]
LED_FAULT_N[1..6]
LED_ISENSE[1..6]
LIGHT_INPUT_VSENSE
LIGHT_BOARD_TEMP
LIGHT_BOARD_FAULT_N
LED1_P/LED1_N ... LED6_P/LED6_N
```

## 8. Связь и сервис

```text
RS485_A
RS485_B
RS485_ISO_GND
RS485_TX_EN
RS485_RX
RS485_TX
SWDIO
SWCLK
UART_TX
UART_RX
NRST
```

## 9. Имена иерархических портов

1. Порт листа должен иметь то же имя, что и логическая сеть верхнего уровня.
2. Для шин использовать KiCad bus syntax без ручного перечисления на верхнем листе.
3. Не создавать локальные алиасы, отличающиеся только регистром или сокращением.
4. Для повторяемых каналов использовать одинаковые шаблоны имён и reference designators.

## 10. Reference designators по функциональным группам

```text
K*  — контакторы и реле
Q*  — транзисторы и силовые ключи
U*  — IC и функциональные модули
F*  — предохранители
D*  — диоды/TVS/LED
R*  — резисторы
C*  — конденсаторы
L*  — индуктивности
J*  — разъёмы
TP* — контрольные точки
H*  — крепёжные элементы
```

Уникальность reference designator поддерживается в пределах всего проекта, а не отдельного листа.

## 11. Запреты

1. Не использовать сеть `GND` как универсальную.
2. Не использовать `BAT_RAW`, если речь не идёт о точке после межкорпусного соединителя; предпочтительно конкретное имя `BATx_INPUT_VSENSE`.
3. Не применять одно имя для команды и физического силового пути.
4. Не использовать `_FAULT` без указания активного уровня.
5. Не назначать контакт 12 СН-176А-12 в netlist до отдельного ADR.