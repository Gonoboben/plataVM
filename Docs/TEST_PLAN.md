# План испытаний ПДУ БНПА / PlataVM

## 1. Последовательность

1. Документарная проверка.
2. Проверка без питания.
3. Первое питание critical.
4. Battery Front-End.
5. PRECHARGE.
6. BATTERY_DISCONNECT.
7. MAIN_INPUT_BUS.
8. POWER_12V_BUS CH1...CH14.
9. 5V_SYS_BUS.
10. LIGHT_POWER_BRANCH.
11. RESERVE_BRANCH / KEEP_ALIVE.
12. RS-485.
13. FSM.
14. Fault injection.
15. Тепловые испытания.
16. Soak-test.

## 2. Обязательные проверки V1.5

1. EXT_KILL отключает независимо от MCU.
2. PRECHARGE блокирует включение при timeout.
3. CH1...CH14 включаются/отключаются по логике.
4. CH12...CH14 контролируются как Always-On.
5. 5V_SYS_BUS работает от MAIN_INPUT_BUS.
6. 5V_SYS_BUS не работает от EMG.
7. EMG питает только 5V_CRIT/3V3_CRIT и keep-alive.
8. Световая ветвь не питается от POWER_12V_BUS.
9. LED-каналы управляются PWM и имеют fault-реакцию.
10. RS-485 устойчив при работе силовых ветвей.