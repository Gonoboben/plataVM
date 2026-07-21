# PlataVM V1.9 — инженерные изменения

Дата: 2026-07-21  
Тип изменения: архитектурная документация и предварительные расчёты  
Аппаратная схема/PCB/BOM: не изменялись

## Принято

- guarded SERVICE_OVERRIDE, вариант B;
- packaging candidate `PACKAGING-P1`;
- preliminary board area budgets;
- logical physical interface count;
- preliminary power connector current classes PCB-D/PCB-E.

## Численные результаты

```text
PCB-D input:
9,26 А at 75 Вт / 9,2 В / 88 %
12,35 А at 100 Вт / 9,2 В / 88 %
connector class 15 А preliminary

PCB-E input:
22,23 А at 180 Вт / 9,2 В / 88 %
connector class 25 А preliminary
```

## Исправление проверки

A↔B signal count исправлен:

```text
25 used + 7 reserve = 32 positions
reserve = 21,9 %
```

## Контролируемые блокеры

- PCB-E thermal compliance;
- PCB-D final efficiency/ripple;
- PCB-B critical branch current;
- component-height/3D audit;
- connector selection;
- BMS/K_BAT/REMOTE_OFF tests;
- release ERC.
