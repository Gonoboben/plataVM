# PCB-D POWER_5V — расчёт OCP с допусками V1.9

Дата: 2026-07-21  
Статус: `MANUAL OCP WINDOW PASS — DESIGN TOOL AND BENCH CORRELATION OPEN`

## 1. Назначение

Проверить, что prototype current-sense set:

```text
LM5143A-Q1
RSHUNT = 5 мОм ±1 % per phase
L = 3,3 мкГн ±20 % per phase
fSW = 400 кГц nominal
```

не создаёт ложный cycle-by-cycle limit в разрешённом режиме `20 А /1 с`, но ограничивает фазовый ток до разрушительного уровня.

## 2. Исходные данные

```text
VIN maximum calculation = 16 В
VOUT = 5 В
IOUT continuous = 15 А
IOUT short mode = 20 А
VCS threshold min/typ/max = 66 / 73 / 82 мВ
RSHUNT nominal = 5,00 мОм
R tolerance = ±1 %
L tolerance = ±20 %
fSW tolerance allowance for manual sweep = ±10 %
```

Значение `±10 %` для частоты используется как консервативный ручной sweep до exact RT resistor/controller tolerance calculation.

## 3. Формулы

Фазовая пульсация:

```text
ΔIL = VOUT × (1 − VOUT/VIN) / (L × fSW)
```

Peak limit одной фазы:

```text
I_LIMIT_PEAK = VCS / RSHUNT
```

Эквивалентный средний current limit двух фаз:

```text
I_LIMIT_TOTAL_AVG = 2 × (I_LIMIT_PEAK − ΔIL/2)
```

## 4. Номинальный случай

При:

```text
VIN = 16 В
L = 3,3 мкГн
fSW = 400 кГц
VCS = 73 мВ
RSHUNT = 5 мОм
```

получено:

```text
ΔIL = 2,604 А p-p per phase
I_LIMIT_PEAK = 14,600 А per phase
I_LIMIT_TOTAL_AVG ≈26,596 А
```

## 5. Минимальный OCP window

Консервативная комбинация для наиболее раннего срабатывания:

```text
VCS = 66 мВ minimum
RSHUNT = 5,05 мОм maximum
L = 2,64 мкГн minimum
fSW = 360 кГц minimum
VIN = 16 В
```

Результат:

```text
ΔIL_MAX = 3,617 А p-p
I_LIMIT_PEAK_MIN = 13,069 А per phase
I_LIMIT_TOTAL_AVG_MIN ≈22,522 А
```

Пиковый ток разрешённого режима `20 А total` при той же maximum ripple:

```text
I_PHASE_PEAK_20A = 10 + 3,617/2
                   ≈11,808 А
```

Запас до minimum peak threshold:

```text
13,069 − 11,808 = 1,261 А
margin ≈10,7 %
```

Следствие:

```text
20 А /1 с не должен вызывать номинальный cycle-by-cycle limit
```

но запас нельзя считать большим. Он требует official calculator и bench correlation.

## 6. Максимальный OCP window

Консервативная комбинация для наиболее позднего срабатывания:

```text
VCS = 82 мВ maximum
RSHUNT = 4,95 мОм minimum
L = 3,96 мкГн maximum
fSW = 440 кГц maximum
VIN = 16 В
```

Получено:

```text
ΔIL_MIN = 1,973 А p-p
I_LIMIT_PEAK_MAX = 16,566 А per phase
I_LIMIT_TOTAL_AVG_MAX ≈31,158 А
```

Это означает, что аппаратный converter OCP не является точным ограничителем 20-А system mode. Он является более высоким защитным барьером от overload/short-circuit.

## 7. Итоговое tolerance window

| Параметр | Minimum | Typical | Maximum |
|---|---:|---:|---:|
| Phase peak threshold | 13,069 А | 14,600 А | 16,566 А |
| Equivalent total average threshold | 22,522 А | 26,596 А | 31,158 А |
| 20-A allowed phase peak, worst ripple | 11,808 А | 11,302 А nominal | — |

## 8. Архитектурное значение

Действуют три независимых уровня:

```text
system power-budget manager
→ разрешает/запрещает 15/20-А режимы по общему бюджету и I²t

PCB-D local current monitor
→ измеряет и сообщает фактический ток

LM5143A-Q1 cycle-by-cycle OCP
→ защищает power stage при overload/short
```

Запрещено использовать converter OCP как единственный механизм ограничения `20 А /1 с`.

## 9. Hiccup policy

До official calculator принимается:

- cycle-by-cycle protection active;
- hiccup behaviour enabled как prototype baseline;
- hard SAFE/HARD_OFF остаётся независимым;
- firmware не маскирует повторные hiccup events;
- `P5_BOARD_FAULT_N` устанавливается при устойчивом hiccup/fault;
- автоматический restart после hard system fault запрещён архитектурой.

Точное число циклов до hiccup и restart timing берутся из exact datasheet configuration.

## 10. Current-sense filter boundary

Prototype schematic предусматривает симметричные RC-filter footprints у CS pins.

Стартовые значения не замораживаются до design-tool/schematic review. Ограничения:

- нельзя чрезмерно фильтровать реальные short events;
- нельзя добавлять неодинаковую phase delay;
- Kelvin traces идут отдельно от силового пути;
- filter capacitors возвращаются в локальную quiet reference согласно datasheet;
- filter components размещаются у controller, не у shunt.

## 11. Bench acceptance

Проверки:

1. 15 А continuous при VIN 9,2/12,8/14,6/16 В;
2. 20 А ровно 1 с;
3. L1/L2 tolerance-equivalent samples либо worst-case simulation;
4. hot shunt resistance;
5. cold/hot controller threshold;
6. phase sharing;
7. current-limit onset;
8. hiccup entry/exit;
9. true short through controlled electronic load/short fixture;
10. SAFE_OFF/HARD_OFF during overload.

Acceptance:

```text
20-А /1-с pulse: no nuisance OCP
phase imbalance target: ≤10 % after settling
OCP onset: above legal 20-А mode with reproducible margin
no MOSFET/inductor/shunt damage
fault reporting deterministic
```

## 12. Gate result

```text
5-мОм shunt compatibility with 20-А mode: MANUAL PASS
minimum peak margin: 10,7 %
maximum equivalent OCP: about 31,2 А total average
exact RT/frequency tolerance: OPEN
slope compensation: OPEN
design-tool OCP result: OPEN
bench correlation: OPEN
production value freeze: NOT GRANTED
```