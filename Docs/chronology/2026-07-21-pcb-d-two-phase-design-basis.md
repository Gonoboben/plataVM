# Хронология: расчётная база PCB-D двухфазного buck

Дата: 2026-07-21  
Предыдущая контрольная точка: PR #41 и owner KiCad normalization commit `e98298061d6e699a325b9e83c188d9ac0c32bd0f`  
Ветка: `design-pcb-d-two-phase-buck-v1-9`

## 1. Проверенный вход

```text
PACK_BUS_P5_IN = 9,2…14,6 В preliminary
calculation point = 16 В
5V_SYS_BUS = 5 В
15 А continuous
20 А / 1 с short
PCB-D = 125 × 94 мм
height budget ≤23 мм
sealed volume at +60 °C
no thermal contact to hull
```

## 2. Принятая рабочая архитектура

```text
2-phase interleaved synchronous buck
180° phase shift
single 5V_SYS_BUS output
external N-MOSFET half bridges
one 3,3 мкГн inductor per phase
prototype current sensing by 5 мОм Kelvin shunts
hard SAFE/HARD_OFF independent of MCU/CAN-FD
```

## 3. Предпочтительный контроллер

```text
LM25143 family — preferred prototype controller
LM5143-Q1 — contingency if transient headroom requires 65-V class
```

Final orderable part остаётся открыт.

## 4. Основные расчётные результаты

```text
fSW = 400 кГц per phase
L = 3,3 мкГн per phase
maximum ripple = 2,60 А p-p
phase peak at 15 А total = 8,80 А
phase peak at 20 А total = 11,30 А
phase design class ≥13 А
inductor class: Isat ≥15 А, Irms ≥10 А
```

Input capacitor RMS design requirement:

```text
≥6 А RMS at +60 °C
```

## 5. Предварительные потери

```text
3,4…5,4 Вт at 75 Вт output
η estimate ≈93,3…95,7 %
```

Это расчётная гипотеза. Thermal rating не закрыт.

## 6. Механический результат

```text
power-stage placeholder = 70 × 38 × 13 мм
capacitor placeholder = 42 × 38 × 17 мм maximum
expected selected component height target ≤16 мм
PCB-D area fit = PRELIMINARY PASS
PCB-D height fit = PRELIMINARY PASS
```

Первая механическая расстановка была исправлена: вместо фактического блока около `52 × 74 мм` OpenSCAD-модель приведена к принятому продольному envelope `70 × 38 мм`.

## 7. Сохранённые блокеры

```text
PACK_BUS_P5_IN transient/clamp
allowed 5V droop/overshoot
real load-step profiles
final switching frequency
exact MOSFET/inductor/shunt/capacitor candidates
loop compensation/stability
sealed-volume thermal test at +60 °C
```

## 8. Архитектурная непрерывность

- K_MAIN не добавлен;
- high current не проходит через PCB-B;
- 5V_SYS_BUS не объединён с critical rails;
- EMG не питает пользовательскую 5-В шину;
- SAFE/HARD_OFF остаются аппаратными;
- SERVICE_OVERRIDE не отменяет аппаратные защиты;
- корпус не используется как радиатор;
- board, schematic, footprints и copper на этом этапе не изменены.

## 9. Следующий этап

```text
transient/clamp design input
→ official design-calculator run
→ exact prototype candidates
→ compensation and OCP min/max
→ prototype schematic for PCB-D converter core
→ ERC
→ footprint/3D candidate review
→ thermal prototype test
```
