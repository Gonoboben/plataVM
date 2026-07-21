# PCB-D POWER_5V — prototype load-transient targets V1.9

Дата: 2026-07-21  
Статус: `PRELIMINARY ENGINEERING TARGETS — OWNER LOAD PROFILES AND LOOP CALC OPEN`

## 1. Назначение

Задать численные входы для output capacitor bank, compensation и стендовых испытаний до получения фактических профилей всех внешних 5-В нагрузок.

Цели не являются характеристиками готового изделия. Они являются design/test targets.

## 2. Исходные ограничения

```text
5V_SYS_BUS nominal = 5,0 В
continuous total = 15 А
short system mode = 20 А /1 с
10 independently protected outputs
preliminary one-channel class = 3 А continuous /5 А peak for 1 с
```

## 3. Классы load step

### Tier A — один канал

```text
step: 0 ↔ 3 А
allowed undershoot/overshoot: ±5 % of 5 В = ±0,25 В
settling to ±2 % target: <500 мкс
```

### Tier B — два канала либо scheduled group

```text
step: 0 ↔ 6 А
allowed undershoot/overshoot: ±8 % = ±0,40 В
settling to ±2 % target: <1 мс
```

### Tier C — worst-case validation

```text
step: 0 ↔ 15 А
not a normal simultaneous command
absolute validation window: 4,25…5,75 В
return to ±5 % target: <2 мс
no latch-off, no phase loss, no false OCP
```

### Tier D — 20-А short mode

```text
transition: 15 →20 А
hold: 1 с maximum
allowed steady droop: ≤5 % target
no nuisance converter OCP
thermal/I²t permission required
```

## 4. Enable staggering

До получения реальных load profiles применяется:

```text
minimum interval between commanded high-inrush output enables: 5 мс
```

Исключения допускаются только если:

- у обоих устройств известны `I_INRUSH` и `T_INRUSH`;
- predicted combined step проходит budget;
- PCB-D load-step Gate проверен;
- firmware event logged.

Staggering не используется для задержки safety/HARD_OFF.

## 5. Output capacitor starting set

```text
2 × 330 мкФ /10 В OS-CON
4 × 47 мкФ /10 В X7R populated
2 × 47 мкФ /10 В X7R DNP options
```

Номинальная сумма не используется напрямую для loop calculation. Требуется actual:

```text
Ceff
ESR
ESL
bias derating
temperature tolerance
aging tolerance
layout inductance
```

## 6. Reference benchmark

TI reference design PMP23452 демонстрирует 5-В/20-А output с приблизительно 5-% undershoot/overshoot при 15-А step/dump. Это подтверждает реализуемость порядка величины, но не переносит compensation или capacitor values на PCB-D, потому что отличаются VIN, topology use, layout и load conditions.

## 7. Control-mode baseline

Для prototype calculation:

```text
FPWM
2 phases /180°
400 кГц per phase
single-output multiphase
```

Light-load/diode-emulation mode не разрешается до проверки:

- phase sharing;
- output ripple;
- transition to FPWM;
- diagnostic observability;
- no conflict with hard-off.

## 8. Measurement points

```text
TP_5V_SYS_BUS near output capacitor bank
TP_5V_SYS_BUS_REMOTE at output connector group
TP_PHASE1_SW
TP_PHASE2_SW
TP_PHASE1_ISENSE
TP_PHASE2_ISENSE
TP_PGOOD
```

Измерения выполняются одновременно:

- differential voltage probe at bus;
- current probe/load telemetry;
- both SW nodes;
- PGOOD/fault.

## 9. Acceptance matrix

| Test | VIN | Ambient | Pass target |
|---|---:|---:|---|
| Tier A step/dump | 9,2/12,8/14,6/16 В | room | ±5 %, settle <500 мкс |
| Tier B step/dump | same | room | ±8 %, settle <1 мс |
| Tier C validation | min/nom/max | room | 4,25…5,75 В, recover <2 мс |
| Tier D 20-А/1-с | min/nom/max | room | no nuisance OCP; droop target ≤5 % |
| Tier A/B | min/nom/max | +60 °C internal | same voltage targets; no thermal fault |
| Repeated sequence | nominal | +60 °C | no drift or oscillation |

## 10. Stability targets

Preliminary targets for official calculator and bench Bode review:

```text
phase margin ≥50° target
preferred ≥60° at nominal
crossover initial target: 20…40 кГц
no subharmonic or beat instability
no sustained ringing after Tier A/B
```

Final crossover is not frozen. It must remain sufficiently below 400-кГц switching frequency and account for output capacitor ESR/ESL and current-mode slope compensation.

## 11. Open owner/device data

For each external 5-В device:

```text
I_NOM
I_PEAK
T_PEAK
I_INRUSH
T_INRUSH
minimum operating voltage
maximum allowed overshoot
restart behaviour
input capacitance
```

Without these data, Tier A/B remain conservative design targets.

## 12. Gate result

```text
single-channel 3-А target: DEFINED
two-channel 6-А target: DEFINED
15-А validation target: DEFINED
20-А /1-с transition target: DEFINED
enable staggering start: 5 мс
exact compensation: OPEN
actual load profiles: OPEN
bench Bode/load-step correlation: OPEN
```