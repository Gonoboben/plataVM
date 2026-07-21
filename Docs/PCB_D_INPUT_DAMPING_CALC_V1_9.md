# PCB-D POWER_5V — расчёт входного damping network V1.9

Дата: 2026-07-21  
Статус: `PRELIMINARY RC DAMPING SET — BENCH TUNING REQUIRED`

## 1. Цель

Снизить hot-plug ringing и входной LC resonance между:

```text
source/cable/PCB-A branch inductance
↔
local PCB-D input capacitance
```

Damping branch не должна находиться последовательно с рабочим током 15 А.

## 2. Расчётные допущения

```text
local effective ceramic capacitance C1 = 100 мкФ
source + harness + trace inductance sweep Ls = 0,3…2,0 мкГн
maximum DC calculation voltage = 16 В
selected damping capacitor Cd = 330 мкФ
```

`C1 = 100 мкФ` — effective capacitance после DC-bias derating, а не сумма номиналов на корпусах.

## 3. Недемпфированный resonance

Формулы:

```text
f0 = 1 / (2π√(Ls × C1))
Z0 = √(Ls / C1)
```

| Ls | f0 | Z0 |
|---:|---:|---:|
| 0,3 мкГн | 29,1 кГц | 0,055 Ом |
| 0,6 мкГн | 20,5 кГц | 0,077 Ом |
| 1,0 мкГн | 15,9 кГц | 0,100 Ом |
| 2,0 мкГн | 11,3 кГц | 0,141 Ом |

Без достаточного damping hot-plug peak может приближаться к удвоенному DC input. Для 16 В это около 32 В до учёта layout overshoot.

## 4. Принятая RC branch

Стартовый вариант:

```text
Cd = 330 мкФ
Rd = 0,10 Ом nominal
Rd tuning range = 0,068…0,15 Ом
```

Схема:

```text
PACK_BUS_P5_IN
→ Rd
→ Cd
→ POWER_GND
```

Ветка подключается параллельно основному ceramic bank и не проводит постоянный input current после зарядки.

## 5. Обоснование Cd

Для passive damping используется условие:

```text
Cd ≥3 × C1
```

При `C1 = 100 мкФ`:

```text
3 × C1 = 300 мкФ
```

Выбран ближайший стандартный стартовый класс:

```text
Cd = 330 мкФ
```

Точный тип конденсатора остаётся открытым. Предпочтителен low-profile polymer/electrolytic class с:

- voltage rating ≥25 В;
- подтверждённым ripple current при +60 °C;
- известным ESR;
- высотой ≤12 мм target;
- рабочей температурой не ниже −20…+105 °C;
- ресурсом, достаточным для sealed assembly.

## 6. Обоснование Rd

Для первого приближения:

```text
Rd ≈ Z0
```

Расчётный диапазон `Z0` равен `0,055…0,141 Ом`, поэтому принимается:

```text
prototype center value = 0,10 Ом
DNP/tuning options = 0,068 / 0,082 / 0,10 / 0,12 / 0,15 Ом
```

Реальный оптимум зависит от:

- ESR Cd;
- ESR/ESL ceramic bank;
- cable resistance;
- PCB-A switch resistance;
- connector resistance;
- TVS dynamic resistance;
- source impedance.

## 7. Pulse-energy check

Энергия, запасённая в `Cd`:

```text
E = 0,5 × Cd × VIN²
```

| VIN | E в 330 мкФ |
|---:|---:|
| 14,6 В | 35,2 мДж |
| 16,0 В | 42,2 мДж |

Теоретическая мгновенная мощность резистора при идеальном источнике:

```text
Ppk = VIN² / Rd
```

| Rd | Ppk при 16 В |
|---:|---:|
| 0,068 Ом | 3,76 кВт |
| 0,10 Ом | 2,56 кВт |
| 0,15 Ом | 1,71 кВт |

Это кратковременный импульс, но обычный маломощный chip resistor без pulse-energy qualification использовать запрещено.

## 8. Resistor implementation

Допустимые варианты:

1. pulse-rated low-ohm resistor;
2. несколько pulse-rated резисторов параллельно/последовательно;
3. использование контролируемого ESR capacitor bank после проверки;
4. NTC/inrush element только после thermal/repeatability review.

Требуется datasheet verification:

```text
single-pulse energy ≥50 мДж minimum
recommended engineering margin ≥100 мДж
peak power curve compatible with 20…100 мкс event
continuous dissipation at ripple verified
```

`50 мДж` является минимальной энергией, близкой к расчётной; целевой запас выше из-за допуска Cd, напряжения и повторных событий.

## 9. Time constant

Для `Rd = 0,10 Ом`, `Cd = 330 мкФ`:

```text
τ = Rd × Cd = 33 мкс
```

Это соответствует области resonance `11…29 кГц` и пригодно как стартовая точка для стендовой настройки.

## 10. Input ceramic bank

Сохраняется требование:

```text
effective ceramics at bias ≥100 мкФ total
ripple capability of full input bank ≥6 А RMS at +60 °C
local HF ceramics adjacent to each half-bridge
```

Damping capacitor не заменяет локальные ceramics, потому что его series resistor и ESL ограничивают высокочастотный ток.

## 11. EMI filter policy

На первом прототипе:

```text
series power inductor = DNP
common-mode element = DNP / interface-dependent
RC damping = populated
TVS = populated
```

Series LC filter разрешается устанавливать только после:

1. measurement of converter input impedance;
2. Middlebrook-style source/load impedance review;
3. damping calculation;
4. conducted-EMI pretest;
5. transient retest.

## 12. Bench tuning sequence

1. измерить Ls реального жгута либо оценить ringing frequency;
2. тест без Cd/Rd при ограниченной энергии;
3. установить `330 мкФ + 0,10 Ом`;
4. сравнить peak, ringing frequency и settling;
5. проверить 0,068…0,15 Ом;
6. выбрать значение по минимальному overshoot без чрезмерного resistor heating;
7. повторить при +60 °C и минимальной температуре;
8. повторить с TVS и без TVS для разделения функций clamp/damping;
9. проверить repeated hot-plug;
10. зафиксировать выбранные part numbers и pulse curves.

## 13. Acceptance targets

```text
VPEAK at controller input ≤36 В
preferred VPEAK ≤32 В
no sustained oscillation
settling target <100 мкс
no resistor damage or parameter drift
no TVS thermal runaway
no false UVLO/OVLO cycling
```

## 14. Sources

Primary source:

```text
Texas Instruments — SSZTDA5, input filter damping and hot-plug discussion
```

The article notes that inductive cabling and input capacitance can create hot-plug ringing approaching twice the DC voltage, recommends a damping capacitor of at least approximately three times the main input capacitance, and requires explicit pulse-energy verification of the damping resistor.

## 15. Gate result

```text
Cd prototype value: 330 мкФ
Rd prototype value: 0,10 Ом
Rd tuning range: 0,068…0,15 Ом
pulse energy qualification: REQUIRED
series input inductor: DNP
bench tuning: OPEN
```
