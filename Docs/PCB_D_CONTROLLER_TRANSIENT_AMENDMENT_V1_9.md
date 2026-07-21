# PCB-D POWER_5V — amendment к расчётной базе после transient review V1.9

Дата: 2026-07-21  
Статус: `ACCEPTED AMENDMENT — SUPERSEDES CONTROLLER PREFERENCE AND INPUT CAPACITOR CLASS`

## 1. Область действия

Документ изменяет выбор предпочтительного controller voltage class и prototype input capacitor voltage class в:

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
input capacitor voltage class = 25 В minimum
```

## 3. Current statement

Каноническое решение:

```text
preferred prototype controller family = LM5143A-Q1
compatible alternate = LM5143-Q1
42-V alternate after measured transient proof = LM25143-Q1
input ceramic/bulk capacitor class = 35 В minimum
RC damping capacitor class = 35 В minimum
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

Принято:

```text
input ceramic/bulk capacitors = 35 В minimum
RC damping capacitor = 35 В minimum
25-В input capacitors = rejected for prototype
```

Причина: паспортный clamp SMCJ18A около 29,2 В превышает rating 25-В capacitor. Prototype design не должен использовать кратковременное перенапряжение конденсатора как штатный запас.

Если measured peak приближается к 35 В либо derating/repetitive stress недостаточны, требуется 50-В capacitor class или redesign clamp.

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
input capacitor class conflict: RESOLVED
base topology: UNCHANGED
prototype voltage margin: INCREASED
final orderable part: OPEN
measurement Gate: OPEN
```
