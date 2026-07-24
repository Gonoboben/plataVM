# PCB-D POWER_5V — Gate LM5143DESIGN-CALC V1.9

Дата: 2026-07-21  
Исходный `main`: `c513dbb3c9da57b8b5a26e755accc94e893e3ef3`  
Статус: `CALCULATION PASS FOR PROTOTYPE SCHEMATIC — PRODUCTION FREEZE NOT GRANTED`

## 1. Назначение

Выполнить расчётный Gate для двухфазного преобразователя PCB-D до внесения детальной converter-core схемы:

```text
LM5143DESIGN-CALC
→ независимое сравнение
→ RT / UVLO / soft-start / OCP / slope compensation
→ compensation network
→ crossover / phase margin
→ prototype converter-core schematic
→ preliminary ERC
```

Этот Gate не утверждает production BOM, footprints, layout, copper, thermal qualification или серийную схему.

## 2. Проверенная архитектурная граница

Расчёт выполнен без изменения замороженной архитектуры:

```text
PACK_BUS_P5_IN → PCB-D two-phase buck → 5V_SYS_BUS
```

Сохранено:

- `K_MAIN` отсутствует;
- силовой ток PCB-D не проходит через PCB-B;
- `5V_SYS_BUS` отделён от `5V_CRIT/3V3_CRIT`;
- EMG не питает внешние 5-В нагрузки;
- `P5_GROUP_SAFE_OFF` и `P5_GROUP_HARD_OFF` остаются аппаратными;
- local MCU/CAN-FD не являются единственным путём отключения;
- thermal contact с корпусом не добавлен.

## 3. Входные данные official calculator

| Параметр | Значение |
|---|---:|
| Controller | LM5143A-Q1 / LM5143QRHARQ1 |
| Configuration | single-output, two-phase, 180° |
| Mode | FPWM |
| VIN functional | 9,2…14,6 В |
| VIN calculation maximum | 16 В |
| VIN nominal | 12,8 В |
| VOUT | 5,0 В |
| IOUT continuous | 15 А |
| IOUT short | 20 А /1 с |
| fSW | 400 кГц/phase |
| L1/L2 | 3,3 мкГн ±20 % |
| DCR | 4,1 мОм max at 25 °C |
| RSH1/RSH2 | 5 мОм ±1 % |
| COUT calculation baseline | 660 мкФ derated |
| COUT ESR baseline | 9 мОм |
| CIN effective | 100 мкФ |
| CIN ESR model | 1 мОм |
| TA design input | +60 °C |
| soft-start target | 15 мс |
| hiccup timing input | 30 мс |
| desired crossover input | 30 кГц |

Использован официальный TI quick-start workbook семейства LM5143/LM5143A, configuration `single-output – 2 phases`.

## 4. RT и switching frequency

Datasheet equation:

```text
RT[kΩ] = 22 / fSW[MHz]
```

Для 400 кГц:

```text
RT ideal = 55,0 кΩ
RT starting standard = 54,9 кΩ /1 %
fSW nominal from equation ≈400,73 кГц
```

Для ручного консервативного sweep до стендового измерения учтён диапазон:

```text
fSW ≈351,7…450,8 кГц
```

Этот диапазон включает controller oscillator tolerance, показанную для контрольной точки `RRT=100 кΩ`, и допуск выбранного резистора. Он является engineering sweep, а не гарантией точного распределения при 54,9 кОм.

## 5. Индуктивность и slope compensation

Datasheet reference inductance для вклада slope compensation, равного одной downslope:

```text
LIDEAL[µH] = VOUT[V] × RS[mΩ] / (24 × fSW[MHz])
```

Результат:

```text
LIDEAL = 2,604 мкГн
Lselected = 3,3 мкГн
Lselected / LIDEAL = 1,267
```

Official-workbook intermediate values при `VIN=12,8 В`:

```text
internal slope referred to IC ≈116,36 мВ/мкс
external slope referred to inductor ≈1,939 А/мкс
inductor on-slope ≈2,364 А/мкс
inductor off-slope ≈1,515 А/мкс
mc ≈1,821
Q ≈0,529
```

Результат:

```text
slope-compensation compatibility: PASS FOR CALCULATION
subharmonic/beat stability: BENCH BODE AND LOAD-STEP OPEN
```

Отдельный внешний slope-compensation component не вводится.

## 6. OCP — результат calculator

При requested output current-limit point `22,5 А` official workbook рекомендует:

```text
RS recommended ≈5,879 мΩ
```

Для выбранных `5,0 мΩ` nominal calculator output:

| VIN | Equivalent total-average OCP |
|---:|---:|
| 9,2 В | 27,454 А |
| 12,8 В | 26,867 А |
| 16,0 В | 26,566 А |

Calculator использует nominal threshold; эти числа не заменяют tolerance sweep.

## 7. OCP — независимое сравнение

Предыдущий ручной расчёт:

```text
minimum equivalent total-average threshold ≈22,522 А
typical equivalent total-average threshold ≈26,596 А
maximum equivalent total-average threshold ≈30,350 А
```

После подстановки консервативной lower-frequency точки RT:

```text
maximum phase ripple at VIN=16 В, Lmin=2,64 мкГн, fSWmin≈351,7 кГц:
ΔIL ≈3,703 А p-p

legal 20-А-mode phase peak:
Iphase_peak ≈11,851 А

minimum phase threshold:
Ilimit_peak_min ≈13,069 А

minimum preliminary margin:
≈10,28 %
```

Итог:

```text
20 А /1 с no-nuisance OCP: PRELIMINARY PASS
converter OCP as exact 20-А limiter: PROHIBITED
bench onset/hiccup/short correlation: OPEN
```

## 8. Current-sense filter

Для каждого CS path сохраняются симметричные footprints:

```text
RCS_FILT = CALC_TBD
CCS_FILT = CALC_TBD
```

Ограничения:

- Kelvin pair от shunt;
- одинаковая задержка двух фаз;
- components у controller;
- возврат capacitor в quiet reference согласно datasheet;
- фильтр не должен скрывать реальный short;
- production value freeze только после waveform review.

## 9. Soft-start

Datasheet equation:

```text
CSS[nF] = 35 × tSS[ms]
```

Для 15 мс:

```text
CSS calculated = 525 нФ
CSS starting standard = 510 нФ
tSS nominal ≈14,57 мс
```

`510 нФ` находится внутри принятой цели `10…20 мс`. Значение остаётся prototype starting value до startup/load test.

## 10. UVLO Gate

Требование проекта:

```text
rising: 8,8…9,0 В
falling: 8,2…8,5 В
```

LM5143A-Q1 EN input:

```text
enable above 2 В
shutdown below 0,4 В
```

Один passive divider на EN не создаёт требуемую узкую гистерезисную пару. Внутренний VCC/VDDA UVLO защищает controller bias, но не является system operating UVLO для PACK_BUS.

Принято для prototype schematic:

```text
U_UVLO = external supervisor/comparator, CALC_TBD
UVLO_RISE = 8,9 В nominal target
UVLO_FALL = 8,35 В nominal target
UVLO_HYST ≈0,55 В
UVLO_OK gates both EN1 and EN2
```

Требования к future exact implementation:

- fail-safe low output;
- работает при снижении PACK_BUS ниже falling target;
- hardware path independent of local MCU/CAN-FD;
- совместим с `5V_SYS_EN`, SAFE_OFF и HARD_OFF;
- exact device/resistors/tolerance analysis before production freeze.

## 11. Output-capacitor model

Starting population remains:

```text
2 × 330 мкФ /10 В polymer
4 ×47 мкФ /10 В X7R populated
2 ×47 мкФ DNP tuning
```

Calculator baseline:

```text
COUT = 660 мкФ derated
ESR = 9 мΩ
calculated switching ripple ≈21,0 мВ p-p
```

Steady ripple does not close load-step performance. Actual `Ceff/ESR/ESL`, tolerance, temperature and layout remain measured inputs.

## 12. Compensation — calculator proposal

For nominal `COUT=660 мкФ`, `ESR=9 мΩ`, desired `fc=30 кГц`, workbook calculated approximately:

```text
RCOMP calculated ≈25,918 кΩ
CCOMP calculated ≈2,047 нФ
CHF calculated ≈222,8 пФ
```

Nearest initial set:

```text
26,1 кΩ /2,0 нФ /220 пФ
```

Independent reproduction of workbook equations gives:

```text
crossover ≈29,90 кГц
phase margin ≈70,02°
```

Однако tolerance sweep показал minimum phase margin около `51,1°` в наиболее неблагоприятной принятой модели.

## 13. Compensation — selected prototype starting network

Для увеличения modelled corner margin выбран стартовый набор:

```text
RCOMP = 24,9 кΩ /1 %
CCOMP = 3,3 нФ
CHF = 220 пФ
```

Nominal independent result:

```text
crossover ≈29,18 кГц
phase margin ≈73,55°
```

Corner sweep:

```text
VIN: 9,2 /12,8 /16 В
IOUT: 3 /7,5 /15 /20 А
fSW: 351,7 /400 /450,8 кГц
L: 2,64 /3,30 /3,96 мкГн
COUT/ESR:
  528 мкФ /12 мΩ
  660 мкФ /9 мΩ
  900 мкФ /3 мΩ
```

Результат проверенного extreme-corner subset:

```text
crossover ≈18,31…39,14 кГц
minimum phase margin ≈56,21°
```

Итог:

```text
calculated phase-margin target ≥50°: PASS
preferred nominal ≥60°: PASS
bench Bode correlation: OPEN
load-step correlation: OPEN
production compensation freeze: NOT GRANTED
```

## 14. Converter configuration record

Prototype single-output interleaved configuration:

```text
MODE → VDDA
FB1 → AGND for fixed 5 В
FB2 → AGND
COMP1 ↔ COMP2
SS1 ↔ SS2
DEMB → VDDA for FPWM
DITH → VDDA for spread-spectrum disabled baseline
VOUT1 and VOUT2 sense the common 5V_SYS_BUS
VCCX → 5V_SYS_BUS after startup, subject to datasheet constraints
```

Both EN inputs receive the same hardware-qualified enable:

```text
EN_RUN =
5V_SYS_EN
AND UVLO_OK
AND NOT P5_GROUP_SAFE_OFF
AND NOT P5_GROUP_HARD_OFF
```

This is an electrical logic requirement; the exact gates/transistors/supervisor remain `CALC_TBD`.

## 15. Preliminary loss result

Official workbook loss tabs are not accepted as final because the exact selected MOSFET curves, hot inductor core-loss curves and all thermal impedances are not fully represented.

Current project loss boundary remains:

```text
75-Вт output:
2,9…6,0 Вт candidate-set estimate
```

The sealed-volume `+60 °C` thermal Gate remains open.

## 16. Gate result

```text
official calculator configuration: EXECUTED
input/output calculator record: CREATED
RT starting value: 54,9 кΩ
UVLO passive-divider solution: REJECTED
external UVLO supervisor: CALC_TBD
soft-start starting value: 510 нФ
OCP calculator/manual comparison: PASS
slope-compensation calculation: PASS
prototype compensation: 24,9 кΩ /3,3 нФ /220 пФ
nominal crossover/PM: ≈29,18 кГц /73,55°
modeled minimum PM: ≈56,21°
prototype converter-core permission: GRANTED WITH CALC_TBD
production schematic/BOM/footprints: NOT FROZEN
bench Bode/load-step/OCP/thermal correlation: OPEN
```

## 17. Required next verification

1. Open converter-core sheet in owner KiCad 10.0.
2. Run native KiCad ERC after symbols and exact pin mapping are instantiated.
3. Measure RT frequency.
4. Measure startup and UVLO thresholds.
5. Measure both phase currents and current sharing.
6. Bode measurement at VIN/load/cap corners.
7. Tier A/B/C/D load-step tests.
8. Controlled OCP/hiccup/short test.
9. Sealed-volume thermal test at +60 °C.
10. Only then consider footprint and prototype BOM Gate.
