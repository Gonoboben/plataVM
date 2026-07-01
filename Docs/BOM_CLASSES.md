# Классы компонентов и BOM-логика ПДУ БНПА / PlataVM

## 1. Основные классы V1.5

1. Разъёмы АКБ_1/АКБ_2.
2. Battery Front-End fuse/TVS/MOSFET/ideal diode controller.
3. BATTERY_DISCONNECT: latching contactor/relay или эквивалентный силовой узел.
4. PRECHARGE: F_pre, SW_pre, R_pre.
5. Разъёмы POWER_12V_BUS CH1...CH14.
6. High-side switches/eFuse для CH1...CH14.
7. DC/DC 12→5 В для 5V_SYS_BUS.
8. Разъёмы 5V_OUT.
9. Защита 5V_OUT.
10. Onboard LED drivers для Epistar XY-J45.
11. Датчики тока.
12. MCU.
13. Isolated RS-485 transceiver.
14. Optional CAN transceiver footprint.
15. Watchdog/supervisor.
16. DC/DC 5V_CRIT.
17. 3V3_CRIT regulator.
18. Температурные датчики.
19. Test points.

## 2. Статусы BOM

```text
candidate / selected / tested / approved / replaced / obsolete
```

TRACO POWER относится к `legacy/current implementation`, а не к целевому BOM новой платы.