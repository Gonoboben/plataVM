# Классы компонентов и BOM-логика ПДУ БНПА / PlataVM

## 1. Основные классы V1.5

1. Глубоководные соединители СН-176А-12 для АКБ_1/АКБ_2.
2. Кабельные сборки длиной 1 м для каждой основной АКБ.
3. Однополюсные контакторы K_BAT1/K_BAT2.
4. Предохранители батарейных блоков.
5. Battery Front-End #1/#2: TVS, измерения V/I/T, PACK_PRESENT.
6. Двунаправленные электронные силовые ключи MAIN_SW1/MAIN_SW2.
7. Ключи балансировочного тракта BALANCE_SW1/BALANCE_SW2.
8. Балансировочные резисторы R_BAL1/R_BAL2.
9. Элементы разряда PACK_BUS.
10. Разъёмы POWER_12V_BUS CH1...CH14.
11. High-side switches/eFuse для CH1...CH14.
12. DC/DC 12→5 В для 5V_SYS_BUS.
13. Разъёмы 5V_OUT1...5V_OUT10.
14. Защита и токовая диагностика каждого 5V_OUT.
15. Onboard LED drivers для 6 × Epistar XY-J45.
16. Датчики тока батарейных ветвей, выходов 12 В, 5 В и LED.
17. MCU.
18. Isolated RS-485 transceiver.
19. Optional CAN transceiver footprint.
20. Watchdog/supervisor.
21. DC/DC critical power path / 5V_CRIT.
22. 3V3_CRIT regulator.
23. Температурные датчики.
24. Test points.
25. Силовые межплатные соединения для многоплатной архитектуры.

Центральные `K_MAIN` и глобальный `PRECHARGE` после PACK_BUS в BOM не включаются.

## 2. Статусы BOM

```text
candidate / selected / tested / approved / replaced / obsolete
```

## 3. Правила выбора

1. K_BAT1 и K_BAT2 должны быть одинаковыми.
2. MAIN_SW1/MAIN_SW2 и BALANCE_SW1/BALANCE_SW2 должны быть симметричными по двум ветвям.
3. Силовые элементы выбираются после подтверждения допустимого тока СН-176А-12.
4. Балансировочные элементы выбираются после подтверждения допустимого зарядного тока BMS.
5. Компоненты HARD_OFF должны иметь гарантированный независимый путь отключения.
6. TRACO POWER относится только к `legacy/current implementation`, а не к целевому BOM новой платы.
