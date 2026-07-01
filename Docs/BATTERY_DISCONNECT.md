# BATTERY_DISCONNECT / HARD OFF

## 1. Назначение

BATTERY_DISCONNECT — аппаратный узел полного отключения питания после PACK_BUS и перед MAIN_INPUT_BUS.

## 2. Базовая топология

```text
PACK_BUS → BATTERY_DISCONNECT → MAIN_INPUT_BUS
PACK_BUS → F_pre → SW_pre → R_pre → MAIN_INPUT_BUS
EXT_KILL → RESET BATTERY_DISCONNECT
MCU_HARD_OFF → RESET BATTERY_DISCONNECT
EXT_START → SET BATTERY_DISCONNECT после precharge
```

## 3. Требования

1. Узел должен обеспечивать HARD OFF независимо от MCU.
2. EXT_KILL имеет приоритет над программной логикой.
3. Перед включением BATTERY_DISCONNECT должен выполняться PRECHARGE.
4. Состояние контактора/реле должно диагностироваться.
5. При потере обеих основных АКБ: SAFE → 7 секунд → HARD OFF.

## 4. Отказовые сценарии

1. Не замкнулся после команды SET.
2. Не разомкнулся после команды RESET.
3. Precharge timeout.
4. EXT_KILL active.
5. Противоречие команд MCU и аппаратной логики.