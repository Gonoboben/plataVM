# PCB-D POWER_5V — amendment к расчётной базе после transient review V1.9

Дата: 2026-07-21  
Статус: `ACCEPTED AMENDMENT — SUPERSEDES CONTROLLER PREFERENCE ONLY`

## 1. Область действия

Документ изменяет только выбор предпочтительного controller voltage class в:

```text
Docs/PCB_D_TWO_PHASE_BUCK_DESIGN_BASIS_V1_9.md
```

Он не изменяет:

- 2-phase synchronous buck topology;
- 180° interleaving;
- 400-кГц стартовую частоту;
- 3,3-мкГн дроссели;
- 5-мОм prototype shunts;
- 15-А continuous и 20-А/1-с output modes;
- hard SAFE/HARD_OFF;
- PCB-D outline и height budget.

## 2. Superseded statements

Следующие прежние statements больше не являются текущим решением:

```text
preferred prototype controller = LM25143-Q1
65-V LM5143 family = contingency only
```

## 3. Current statement

Каноническое решение:

```text
preferred prototype controller family = LM5143A-Q1
compatible alternate = LM5143-Q1
42-V alternate after measured transient proof = LM25143-Q1
```

## 4. Причина

До measured transient review известны только:

```text
normal input = 9,2…14,6 В
DC calculation point = 16 В
```

Неизвестны:

- hot-plug peak;
- cable/trace inductance;
- TVS dynamic clamp in actual layout;
- turn-off overshoot;
- interaction with input capacitance and optional EMI filter;
- sustained upstream fault.

Поэтому первый прототип не должен зависеть от минимального voltage headroom 42-В class.

TI указывает LM5143A-Q1 как рекомендованную для новых разработок 65-В family. Та же официальная design-tool family поддерживает LM5143A-Q1, LM5143-Q1 и LM25143-Q1.

## 5. MOSFET consequence

Сохраняется:

```text
MOSFET VDS class = 60 В minimum
40-В MOSFET = prohibited until separate measured review
```

65-В controller не делает 60-В MOSFET неуязвимым. Поэтому local transient acceptance target остаётся `≤36 В`.

## 6. Capacitor consequence

Входной capacitor bank пока сохраняет `≥25 В`, но должен быть заменён на 35-В class, если measured peak на capacitor terminals превышает 22 В с учётом допуска и repetitive stress.

## 7. Traceability

Связанные документы:

```text
Docs/PCB_D_CONTROLLER_CANDIDATE_MATRIX_V1_9.md
Docs/PCB_D_INPUT_PROTECTION_TRANSIENT_BOUNDARY_V1_9.md
Docs/PCB_D_INPUT_DAMPING_CALC_V1_9.md
Docs/PCB_D_PROTOTYPE_PARAMETER_SET_V1_9.md
```

## 8. Gate

```text
controller preference conflict: RESOLVED
base topology: UNCHANGED
prototype voltage margin: INCREASED
final orderable part: OPEN
measurement Gate: OPEN
```
