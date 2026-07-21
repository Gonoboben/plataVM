# PCB-D POWER_5V — component-selection consistency amendment V1.9

Дата: 2026-07-21  
Статус: `CONSISTENCY AMENDMENT — R_DAMP ORDERABLE CLOSED, PULSE GATE OPEN`

## 1. Superseded section

This amendment supersedes only section `Damping resistor status` of:

```text
Docs/PCB_D_COMPONENT_SELECTION_CONSISTENCY_V1_9.md
```

The earlier statement:

```text
R_DAMP exact orderable: OPEN
```

is no longer current.

## 2. Current result

```text
R_DAMP exact prototype orderable: PWR263S-35-R100FE
resistance: 0,10 Ом
absolute tolerance: ±1 %
package: D²PAK
manufacturer order-code verification: PASS
pulse-graph/application verification: OPEN
hot-plug bench correlation: OPEN
```

## 3. Consistency effect

No architectural or electrical boundary changes:

- `Cd = 330 мкФ /35 В` remains;
- nominal `Rd = 0,10 Ом` remains;
- tuning range `0,068…0,15 Ом` remains;
- calculated event energy remains about `42,2 мДж`;
- minimum pulse capability remains `50 мДж`;
- engineering target remains `100 мДж`;
- the resistor remains outside the continuous 15-А main path.

## 4. Mechanical effect

D²PAK body class remains below the 23-мм height budget but requires explicit PCB area and copper review.

## 5. Gate result

```text
component-selection consistency: PASS
R_DAMP exact orderable inconsistency: RESOLVED
pulse application Gate: OPEN
production BOM: NOT FROZEN
```