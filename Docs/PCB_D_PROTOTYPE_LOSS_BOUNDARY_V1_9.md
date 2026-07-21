# PCB-D POWER_5V — boundary потерь prototype candidates V1.9

Дата: 2026-07-21  
Статус: `PRELIMINARY LOSS BOUNDARY — SWITCHING AND SEALED THERMAL TEST OPEN`

## 1. Назначение

Проверить, что выбранный prototype candidate set не ухудшает ранее принятую оценку `3,4…5,4 Вт` при 75-Вт output и помещается в существующий thermal Gate.

## 2. Рабочая точка

```text
VOUT = 5 В
IOUT = 15 А
POUT = 75 Вт
2 phases
Iphase average = 7,5 А
VIN sweep = 9,2…16 В
fSW = 400 кГц
L = 3,3 мкГн
```

Worst calculated nominal phase RMS около `7,54 А`.

## 3. Дроссели XAL1010-332MED

Используется maximum DCR at 25 °C:

```text
DCR25_MAX = 4,1 мОм
```

Оценка двух дросселей:

```text
P_L_25 ≈2 × 7,54² × 0,0041
       ≈0,47 Вт
```

Для горячего режима применяется preliminary multiplier `1,4` на copper resistance:

```text
P_L_HOT ≈0,65 Вт
```

В эту оценку не включены core losses. Они должны быть получены из manufacturer loss model при 400 кГц, actual flux swing и hot core temperature.

Boundary:

```text
P_L_TOTAL preliminary = 0,6…1,0 Вт
```

## 4. Current shunts

С учётом phase RMS:

```text
P_SHUNT_TOTAL ≈2 × 7,54² × 0,005
              ≈0,57 Вт
```

В режиме 20 А/1 с:

```text
P_SHUNT_TOTAL ≈1,0 Вт
```

## 5. MOSFET conduction

Prototype MOSFET:

```text
BUK9Y6R0-60E
RDS(on) class = 6 мОм
```

При одинаковом HS/LS типе суммарная conduction loss двух фаз приблизительно:

```text
P_FET_COND ≈2 × Iphase_rms² × RDS(on)
```

25-°C class:

```text
P_FET_COND_25 ≈2 × 7,54² × 0,006
              ≈0,68 Вт
```

Hot design boundary с удвоенным RDS(on):

```text
P_FET_COND_HOT ≈1,36 Вт
```

Фактический multiplier должен быть взят из exact datasheet curve при выбранном VGS.

## 6. Gate-drive loss

Для preliminary boundary используется datasheet gate-charge class около `40 нКл` при логическом gate drive.

```text
P_GATE ≈4 × QG × VDRV × fSW
```

При `QG = 40 нКл`, `VDRV = 5 В`, `fSW = 400 кГц`:

```text
P_GATE ≈0,32 Вт
```

Это power, поступающая из gate-drive supply; она распределяется между controller output resistance, gate resistors и MOSFET gates.

## 7. Switching/dead-time boundary

Точное значение невозможно зафиксировать без:

- Qgd/Coss curves;
- actual VGS drive;
- HOL/LOL resistor selection;
- measured rise/fall times;
- dead-time waveform;
- VIN/load sweep;
- layout parasitics.

Для feasibility сохраняется:

```text
P_SWITCH + P_DEADTIME = 0,5…1,6 Вт preliminary
```

Если измерение превышает 1,6 Вт, требуется:

- отдельный HS/LS candidate review;
- изменение gate resistors;
- снижение fSW;
- более низкий Qgd/Coss MOSFET;
- snubber optimization;
- layout correction.

## 8. Controller and support

```text
controller + VCC/VCCX + gate-drive quiescent: 0,2…0,6 Вт
```

Точное значение зависит от питания VCCX от 5V_SYS_BUS, gate charge и operating mode.

## 9. Capacitors, copper and damping

Normal continuous:

- TVS leakage negligible versus main loss;
- R_DAMP has no DC loss after C_DAMP charge;
- C_DAMP has ESR/ripple heating;
- input/output capacitor ESR and copper distribution contribute loss;
- shunt/copper current spreading adds local heating.

Boundary:

```text
P_CAP_COPPER_MISC = 0,3…0,8 Вт
```

## 10. Total preliminary boundary

| Source | Preliminary loss |
|---|---:|
| Inductors, copper + core allowance | 0,6…1,0 Вт |
| Shunts | около 0,57 Вт |
| MOSFET conduction | 0,7…1,4 Вт |
| Switching + dead time | 0,5…1,6 Вт |
| Gate drive/controller | 0,2…0,6 Вт |
| Capacitors/copper/snubber/misc. | 0,3…0,8 Вт |
| **Total** | **2,9…6,0 Вт** |

Equivalent estimated efficiency:

```text
η = 75 / (75 + Ploss)
```

```text
at 2,9 Вт: 96,3 %
at 6,0 Вт: 92,6 %
```

Следствие:

```text
η ≥92 % near 75 Вт remains feasible
```

но верхняя граница потерь всё ещё значительна для sealed +60 °C assembly.

## 11. 20-А /1-с pulse

При 20 А total:

- phase average = 10 А;
- phase peak nominal at 16 В ≈11,30 А;
- shunt total loss ≈1,0 Вт;
- inductor copper loss increases approximately with I²;
- MOSFET conduction increases approximately with I²;
- switching loss also increases with current.

20-А mode не используется для continuous thermal rating. Он допускается только system I²t manager и повторяется не ранее 10 с после thermal recovery.

## 12. Temperature instrumentation

Prototype PCB-D предусматривает точки контроля:

```text
TEMP_Q_HS1
TEMP_Q_LS1
TEMP_Q_HS2
TEMP_Q_LS2
TEMP_L1
TEMP_L2
TEMP_CIN
TEMP_COUT
TEMP_CONTROLLER
```

Допускаются:

- thermocouple attachment locations;
- IR-emissivity reference patches;
- local digital temperature sensor outside SW field.

Полимерный термоклей не наносится поверх MOSFET, дросселей, shunts или capacitor vents.

## 13. Sealed-volume acceptance

При внутренней температуре `+60 °C`:

```text
no thermal contact to hull
natural internal convection only
15 А continuous until thermal steady state
```

Pass criteria:

- no component exceeds derated temperature limit;
- no controller thermal shutdown;
- no current sharing drift >10 %;
- no polymer/electrolytic hot spot beyond lifetime boundary;
- no conformal-coating damage;
- output remains in regulation;
- fault telemetry remains valid.

## 14. Gate result

```text
candidate-set loss feasibility: PASS
calculated total boundary: 2,9…6,0 Вт
η feasibility: 92,6…96,3 %
exact switching loss: OPEN
exact core loss: OPEN
sealed +60 °C qualification: OPEN
production thermal rating: NOT GRANTED
```