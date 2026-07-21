# PCB-D POWER_5V — exact R_DAMP selection amendment V1.9

Дата: 2026-07-21  
Статус: `EXACT PROTOTYPE ORDERABLE SELECTED — PULSE TEST OPEN`

## 1. Superseded statement

The following earlier statement is no longer current:

```text
R_DAMP exact order code: OPEN
```

## 2. Exact prototype candidate

```text
R_DAMP = PWR263S-35-R100FE
manufacturer: Bourns
resistance: 0,10 Ом
absolute tolerance: ±1 %
package: D²PAK / TO-263 style
packaging: tape and reel
AEC-Q200 family
```

The code is derived directly from the manufacturer ordering scheme:

```text
PWR263S-35
-
R100 = 0,10 Ом
F = ±1 %
E = tape & reel
```

## 3. Datasheet boundary

Manufacturer data confirms:

```text
family range: 0,02 Ом…130 кОм
R100 is a listed popular value
1-% tolerance is available for R100
35-Вт rating is specified at 25 °C case temperature
about 3,5 Вт at 25 °C ambient on the stated FR4 reference board
operating temperature: −55…+155 °C
inductance: 0,1 мкГн maximum
```

The `35 Вт` marking must not be interpreted as free-air continuous capability on PCB-D.

## 4. Pulse-energy Gate

Exact orderable selection does not close the application-specific pulse Gate.

Required:

```text
calculated event energy: about 42,2 мДж at 16 В and 330 мкФ
minimum accepted single-pulse capability: ≥50 мДж
target engineering margin: ≥100 мДж
pulse duration region: 20…100 мкс
```

Before BOM freeze:

1. read the exact manufacturer pulse graph for R100;
2. account for initial temperature;
3. account for repeated connect events;
4. verify overload voltage limit;
5. test 0,068…0,15-Ом tuning alternatives;
6. verify no resistance drift;
7. verify PCB copper and package temperature.

## 5. Mechanical impact

```text
package class: D²PAK
body envelope class: about 15,4 ×10,1 ×4,5 мм
```

This is larger than a small chip resistor but remains below the 23-мм height budget. PCB area and thermal copper must be checked during converter-core placement.

## 6. Gate result

```text
R_DAMP exact prototype orderable: SELECTED
R_DAMP footprint family: SELECTED PRELIMINARY
manufacturer order-code verification: PASS
pulse-energy calculation: PASS PRELIMINARY
pulse graph/application verification: OPEN
hot-plug bench test: OPEN
production approval: NOT GRANTED
```