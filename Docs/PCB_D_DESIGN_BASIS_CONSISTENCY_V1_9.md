# Проверка связности расчётной базы PCB-D POWER_5V V1.9

Дата: 2026-07-21  
Статус: `STRUCTURAL AND NUMERICAL REVIEW PASS; COMPONENT/THERMAL GATES OPEN`

## 1. Проверенные документы

```text
Docs/ARCHITECTURE_BASELINE.md
Docs/PROJECT_MASTER.md
Docs/BRANCH_CURRENT_PRECALC_V1_9.md
Docs/PCB_D_TWO_PHASE_BUCK_DESIGN_BASIS_V1_9.md
Docs/PCB_D_CONTROLLER_CANDIDATE_MATRIX_V1_9.md
Docs/PCB_D_COMPONENT_BOUNDING_BOXES_V1_9.md
Hardware/Mechanical/PCB_D_POWER_STAGE_PLACEHOLDER.scad
```

## 2. Численная проверка

Исходная формула:

```text
D = VOUT / VIN
ΔIL = VOUT × (1 − D) / (L × fSW)
Iphase_avg = IOUT / 2
Iphase_rms = sqrt(Iphase_avg² + ΔIL²/12)
Iphase_peak = Iphase_avg + ΔIL/2
```

Параметры:

```text
VOUT = 5 В
L = 3,3 мкГн
fSW = 400 кГц
IOUT_CONT = 15 А
IOUT_SHORT = 20 А
```

Проверенные предельные результаты:

```text
maximum ΔIL at 16 В = 2,60 А p-p
maximum phase peak at 15 А total = 8,80 А
maximum phase peak at 20 А total = 11,30 А
minimum phase peak design class = 13 А
```

Результат:

```text
phase arithmetic: PASS
short-mode margin direction: PASS
inductor current class ≥15 А: CONSISTENT
```

## 3. Согласование с входным током ветви

Ранее рассчитано:

```text
75 Вт at 9,2 В and η=88 % → 9,26 А input
100 Вт at 9,2 В and η=88 % → 12,35 А input
```

Принятый класс входного соединения:

```text
15 А continuous/short design class
```

Результат:

```text
branch current class versus converter basis: PASS
```

## 4. Согласование с системным power budget

Локальные пределы PCB-D:

```text
15 А continuous at 5 В
20 А / 1 с at 5 В
```

Они не означают автоматическое разрешение режима. Команда нагрузки дополнительно проходит общий PACK_BUS budget:

```text
DUAL_PACK_RUN: 40 А continuous / 44 А short
SINGLE_PACK_MODE: 20 А continuous / 22 А short
```

Результат:

```text
local versus system rating separation: PASS
SERVICE_OVERRIDE does not bypass hardware protection: PASS
```

## 5. Согласование аппаратного отключения

Сохранены:

```text
normal commands via local MCU/CAN-FD
P5_GROUP_SAFE_OFF direct line
P5_GROUP_HARD_OFF direct line
P5_BOARD_FAULT_N direct summary
```

Контроллер/driver enable должен иметь аппаратный путь запрета, не зависящий от MCU и CAN-FD.

Результат:

```text
hard safety architecture: PASS
```

## 6. Согласование с механикой

PCB-D:

```text
outline = 125 × 94 мм
component-height budget = 23 мм
```

Candidate envelopes:

```text
power stage = 70 × 38 × 13 мм maximum placeholder
capacitor bank = 42 × 38 × 17 мм maximum placeholder
expected selected component height target ≤16 мм
```

OpenSCAD model после исправления использует продольный power-stage block `70 × 38 мм`.

Результат:

```text
2D board fit: PRELIMINARY PASS
height fit: PRELIMINARY PASS
actual connector/footprint fit: OPEN
```

## 7. Тепловая проверка

Предварительная оценка потерь:

```text
3,4…5,4 Вт at 75 Вт output
η estimate ≈93,3…95,7 %
```

Это согласуется с целевым условием:

```text
η ≥92 % near 75 Вт
```

Но не доказывает допустимость при:

```text
sealed volume
internal ambient +60 °C
no thermal contact to hull
conformal coating
adjacent PCB-E heat generation
```

Результат:

```text
efficiency feasibility: PRELIMINARY PASS
thermal qualification: OPEN/BLOCKING FOR RATING FREEZE
```

## 8. Transient margin

Контроллер 42-В класса и MOSFET 40/60-В класса не могут быть окончательно утверждены без измеренного или рассчитанного входного transient envelope.

Правило:

```text
60-В MOSFET preferred until clamp verification
40-В MOSFET permitted only if clamped worst-case including tolerance/overshoot ≤30 В
LM5143-Q1 contingency if controller voltage headroom is insufficient
```

Результат:

```text
normal VIN compatibility: PASS
transient compatibility: OPEN
```

## 9. Неизменённые архитектурные ограничения

| Ограничение | Результат |
|---|---|
| K_MAIN отсутствует | PASS |
| High current не проходит через PCB-B | PASS |
| 5V_SYS_BUS отделён от 5V_CRIT | PASS |
| EMG не питает PCB-D user load bus | PASS |
| EXT_KILL независим от CAN/firmware | PASS |
| INTERCONNECT пассивный | PASS |
| Ground domains не объединены произвольно | PASS |
| Корпус не используется как радиатор | PASS |
| Final component/footprint не зафиксирован | PASS |

## 10. Gate result

```text
two-phase architecture: PASS
numerical phase sizing: PASS
current-class consistency: PASS
preliminary board-area fit: PASS
preliminary height fit: PASS
hard-off continuity: PASS
controller family selection: PRELIMINARY PASS
exact component selection: OPEN
loop stability: OPEN
transient clamp: OPEN
sealed-volume thermal test: OPEN
```
