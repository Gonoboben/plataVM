# PCB-D POWER_5V — consistency review входной защиты V1.9

Дата: 2026-07-21  
Статус: `CONSISTENCY PASS WITH MEASUREMENT GATES OPEN`

## 1. Проверенные документы

```text
PCB_D_TWO_PHASE_BUCK_DESIGN_BASIS_V1_9.md
PCB_D_CONTROLLER_TRANSIENT_AMENDMENT_V1_9.md
PCB_D_CONTROLLER_CANDIDATE_MATRIX_V1_9.md
PCB_D_INPUT_PROTECTION_TRANSIENT_BOUNDARY_V1_9.md
PCB_D_INPUT_DAMPING_CALC_V1_9.md
PCB_D_PROTOTYPE_PARAMETER_SET_V1_9.md
BRANCH_CURRENT_PRECALC_V1_9.md
ARCHITECTURE_BASELINE.md
SYSTEM_POWER_BUDGET_POLICY.md
```

## 2. Controller conflict resolution

Историческая расчётная база содержала:

```text
preferred controller = LM25143-Q1
```

После transient review каноническим является:

```text
preferred prototype family = LM5143A-Q1
compatible alternate = LM5143-Q1
LM25143-Q1 = alternate after measured proof
```

Конфликт устранён отдельным amendment и обновлённой candidate matrix. Топология и расчёт фаз не изменились.

## 3. Voltage hierarchy

| Domain | Current requirement | Status |
|---|---:|---|
| Normal PACK_BUS_P5_IN | 9,2…14,6 В | CONSISTENT |
| DC calculation point | 16 В | CONSISTENT |
| TVS standoff | 18 В | ABOVE NORMAL RANGE |
| TVS breakdown | 20…22,1 В | ABOVE STANDOFF |
| TVS clamp class | около 29,2 В | BELOW TARGET CONTROLLER/MOSFET LIMIT |
| Preferred transient peak | ≤32 В | CONSISTENT |
| Engineering maximum acceptance | ≤36 В | CONSISTENT |
| MOSFET class | 60 В | MARGIN PRESERVED |
| Controller class | 65 В | MARGIN PRESERVED |

Ни одно значение не превращает transient limit в nominal operating voltage.

## 4. Capacitor voltage review

Текущий input capacitor class:

```text
25 В minimum
```

Это допустимо только при фактическом measured peak на capacitor terminals, совместимом с derating и repetitive stress.

Правило escalation:

```text
measured peak >22 В
→ 35-В capacitor class or clamp redesign
```

Статус:

```text
25-В class = PROTOTYPE CONDITIONAL
```

## 5. Damping calculation review

Проверено:

```text
C1 effective = 100 мкФ
Ls sweep = 0,3…2,0 мкГн
f0 = 11,3…29,1 кГц
Z0 = 0,055…0,141 Ом
Cd = 330 мкФ ≥3×C1
Rd = 0,10 Ом center
Rd range = 0,068…0,15 Ом
τ at 0,10 Ом = 33 мкс
```

Энергия `Cd` при 16 В:

```text
42,2 мДж
```

Поэтому pulse-energy qualification резистора обязательна. Ошибочное использование обычного маломощного resistor запрещено.

## 6. Power path review

RC damping branch подключается параллельно и не проводит continuous 15-А current.

Это согласуется с:

```text
PACK_BUS_P5_IN connector class = 15 А
PCB-D continuous output = 15 А at 5 В
PCB-D short output = 20 А /1 с
```

Series power inductor остаётся DNP, поэтому новый непрерывный loss element в main path не добавлен.

## 7. Safety architecture review

Не изменены:

- `P5_GROUP_SAFE_OFF`;
- `P5_GROUP_HARD_OFF`;
- `P5_BOARD_FAULT_N`;
- независимость аппаратного отключения от MCU/CAN-FD;
- запрет SERVICE_OVERRIDE bypass;
- отсутствие high-current path через PCB-B;
- отсутствие питания PCB-D от EMG;
- разделение `5V_SYS_BUS` и critical rails.

## 8. Mechanical review

Новые candidate envelopes:

```text
SMCJ TVS class: compatible with input H1/H2 zone
Cd damping capacitor: target height ≤12 мм
Rd pulse network: within input-protection block
controller placeholder: unchanged 7 × 7 × 1,5 мм
```

PCB-D outline и `70 × 38 × 13 мм` power-stage placeholder не изменяются.

Damping capacitor может увеличить input bulk area; окончательный fit проверяется после exact candidate selection.

## 9. Thermal review

Добавленные losses:

- TVS: только leakage/short transient в normal operation;
- Rd: no DC loss after Cd charge, but pulse heating;
- Cd: ripple/ESR heating;
- 65-В controller: similar class, exact gate-drive loss open.

Основной continuous thermal budget PCB-D `3,4…5,4 Вт` остаётся preliminary и требует sealed-volume test.

## 10. Failure-mode review

| Failure | Result |
|---|---|
| TVS short | upstream branch protection must isolate PCB-D |
| TVS open | 65-В controller + 60-В MOSFET are last voltage barrier; measurement/inspection required |
| Rd open | damping lost, TVS still clamps; ringing fault found in test |
| Rd short | Cd becomes direct bulk capacitor; inrush increases; upstream current path must tolerate event |
| Cd open | damping lost; detected by transient test |
| Cd short | Rd limits initial current but sustained fault requires upstream protection |
| sustained overvoltage | upstream branch OFF; TVS not allowed to dissipate continuously |

## 11. Remaining Gates

```text
exact TVS candidate and pulse curves
exact Cd/Rd candidates
measured harness/branch inductance
hot-plug and turn-off waveforms
exact LM5143A-Q1 orderable
LM5143DESIGN-CALC run
OCP min/max
loop compensation
input capacitor 25-V versus 35-V decision
sealed thermal test
```

## 12. Result

```text
architecture continuity: PASS
controller preference conflict: RESOLVED
voltage hierarchy: PASS
manual damping calculation: PASS
prototype input protection concept: PASS
measurement qualification: OPEN
production schematic permission: NOT YET GRANTED
```
