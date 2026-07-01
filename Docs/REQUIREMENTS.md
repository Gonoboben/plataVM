# Требования к ПДУ БНПА / PlataVM

Статус:

```text
requirements baseline for V1.5 integrated TO-BE architecture
```

## 1. Верхнеуровневое требование

Плата должна безопасно распределять энергию от двух основных АКБ и резервного источника на 12 В выходы, 5 В выходы, световую ветвь и критическую управляющую подсистему.

## 2. Ключевые требования

| ID | Требование | Статус |
|---|---|---|
| REQ-PWR-001 | Поддержать АКБ_1/АКБ_2 LiFePO4 4s24p | принято |
| REQ-PWR-002 | Сформировать PACK_BUS | принято |
| REQ-PWR-003 | Реализовать BATTERY_DISCONNECT / HARD OFF | принято |
| REQ-PWR-004 | Реализовать PRECHARGE MAIN_INPUT_BUS | принято |
| REQ-PWR-005 | Сформировать POWER_12V_BUS CH1...CH14 | принято |
| REQ-PWR-006 | CH1...CH11 сделать MCU-controlled | принято |
| REQ-PWR-007 | CH12...CH14 сделать Always-On monitored | принято |
| REQ-5V-001 | Сформировать отдельную 5V_SYS_BUS | принято |
| REQ-5V-002 | Вывести 5V_SYS_BUS на внешние разъёмы | принято |
| REQ-5V-003 | Не питать 5V_SYS_BUS от EMG | принято |
| REQ-LGT-001 | Не использовать TRACO как целевую архитектуру | принято |
| REQ-LGT-002 | Реализовать onboard LED drivers для Epistar XY-J45 | принято |
| REQ-IF-001 | Использовать isolated RS-485 как baseline | принято |
| REQ-IF-002 | CAN/CAN-FD оставить optional future | принято |
| REQ-SAFE-001 | EXT_KILL должен работать независимо от MCU | принято |
| REQ-SAFE-002 | Потеря обеих АКБ → SAFE → 7 секунд → HARD_OFF | принято |

## 3. Открыто перед schematic freeze

1. Количество 5V_OUT.
2. Ток 5V_OUT.
3. Токи CH1...CH14.
4. Топология LED-драйверов.
5. Тип BATTERY_DISCONNECT.
6. Расчёт PRECHARGE.
7. MCU.
8. Механика платы.