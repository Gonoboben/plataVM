# Хронология: входная защита PCB-D и controller transient review

Дата: 2026-07-21  
Предыдущая точка: merge PR #42, PCB-D two-phase buck design basis  
База ветки: `main` commit `f5dcdf8cf141927a40566f6a371feb3304d4db2c`

## 1. Причина этапа

После расчёта фаз оставался блокер:

```text
Q-P5-009 — фактический transient envelope PACK_BUS_P5_IN
```

До измерений нельзя было окончательно решить:

- 42- или 65-В controller class;
- 40- или 60-В MOSFET class;
- TVS/clamp topology;
- damping hot-plug resonance;
- voltage class input capacitors.

## 2. Принятое prototype решение

```text
preferred controller family: LM5143A-Q1
compatible alternate: LM5143-Q1
42-V alternate after measurement: LM25143-Q1
MOSFET class: 60 В minimum
TVS class: SMCJ18A
RC damping: 330 мкФ + 0,10 Ом
Rd tuning: 0,068…0,15 Ом
series input inductor: DNP
```

## 3. Voltage targets

```text
normal input: 9,2…14,6 В
DC calculation point: 16 В
preferred measured transient peak: ≤32 В
engineering maximum acceptance: ≤36 В
```

40-В MOSFET не допускается на первом прототипе.

## 4. Damping calculation

Для:

```text
C1 effective = 100 мкФ
Ls = 0,3…2,0 мкГн
```

получено:

```text
f0 = 11,3…29,1 кГц
Z0 = 0,055…0,141 Ом
```

Стартовый `Rd = 0,10 Ом` находится в середине расчётного диапазона.

Энергия `Cd = 330 мкФ` при 16 В:

```text
42,2 мДж
```

Pulse-energy qualification resistor network обязательна.

## 5. Неизменяемые решения

Не изменены:

- two-phase synchronous buck;
- 180° interleaving;
- 400 кГц;
- 3,3 мкГн per phase;
- 5 мОм Kelvin shunt;
- 15 А continuous / 20 А for 1 с;
- hard SAFE/HARD_OFF;
- PCB-D outline 125 × 94 мм;
- no hull thermal contact;
- separation from critical 5V rails.

## 6. Созданные документы

```text
Docs/PCB_D_INPUT_PROTECTION_TRANSIENT_BOUNDARY_V1_9.md
Docs/PCB_D_INPUT_DAMPING_CALC_V1_9.md
Docs/PCB_D_CONTROLLER_TRANSIENT_AMENDMENT_V1_9.md
Docs/PCB_D_PROTOTYPE_PARAMETER_SET_V1_9.md
Docs/PCB_D_INPUT_PROTECTION_CONSISTENCY_V1_9.md
```

Обновлены:

```text
Docs/PCB_D_CONTROLLER_CANDIDATE_MATRIX_V1_9.md
Docs/V1_9_DOCUMENT_INDEX.md
```

## 7. Следующий Gate

```text
official LM5143DESIGN-CALC run
→ exact controller orderable
→ exact MOSFET/inductor/shunt/capacitor candidate table
→ OCP and compensation
→ transient simulation
→ prototype schematic core
→ KiCad review
```
