# Правила проектирования PCB ПДУ БНПА / PlataVM

## 1. Зонирование

PCB должна иметь зоны:

1. Battery Front-End.
2. BATTERY_DISCONNECT / PRECHARGE.
3. MAIN_INPUT_BUS.
4. POWER_12V_BUS CH1...CH14.
5. 5V_SYS_BUS.
6. LIGHT_POWER_BRANCH.
7. RESERVE_BRANCH / critical.
8. MCU/ADC.
9. RS-485.
10. Service/debug.

## 2. Главные ограничения

1. Не разводить PCB до schematic freeze V1.5.
2. Силовые токи не должны возвращаться через MCU-зону.
3. 5V_SYS_BUS и 5V_CRIT должны быть разведены как разные домены.
4. LIGHT_POWER_BRANCH не смешивать с POWER_12V_BUS.
5. EXT_KILL и BATTERY_DISCONNECT должны иметь понятную аппаратную трассу.
6. Все выходы должны иметь разъёмы и маркировку.

## 3. Обязательные test points

PACK_BUS, MAIN_INPUT_BUS, POWER_12V_BUS, 5V_SYS_BUS, 5V_CRIT, 3V3_CRIT, LIGHT_POWER_BRANCH, RS-485 A/B, SWD, UART, GND_PWR, GND_SIG.