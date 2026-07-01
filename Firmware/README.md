# Firmware

Раздел для прошивки ПДУ БНПА.

## Ожидаемая структура

```text
Firmware/
├─ Core/
├─ Drivers/
├─ State_Machine/
├─ Telemetry/
├─ Fault_Manager/
└─ Protocol/
```

## Минимальные функции прошивки

1. конечный автомат состояний;
2. управление BAT1/BAT2;
3. управление precharge;
4. управление EMG;
5. управление ИЗС;
6. управление AUX;
7. измерения ADC;
8. fault manager;
9. telemetry over RS-485;
10. watchdog.

Прошивка должна соответствовать `Docs/FAULT_LOGIC_AND_STATES.md`.