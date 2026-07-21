# PCB-D POWER_5V — prototype component Gate summary V1.9

Дата: 2026-07-21  
Статус: `READY FOR OFFICIAL CALCULATOR AND CONVERTER-CORE SCHEMATIC`

## Selected

```text
LM5143QRHARQ1
4 × BUK9Y6R0-60E,115
2 × XAL1010-332MED
2 × WSK25125L000FEA
Littelfuse SMCJ18A
Panasonic EEH-ZK1V331P
Bourns PWR263S-35-R100FE
TDK 22-мкФ/50-В X7R input-MLCC class
2 × Panasonic 10SVPC330M
Murata 47-мкФ/10-В X7R output-MLCC class
```

## Manual checks

```text
phase ripple at 16 В: 2,604 А p-p
legal 20-А worst phase peak: 11,808 А
minimum OCP phase threshold: 13,069 А
minimum OCP margin: 10,7 %
maximum equivalent OCP: 30,350 А total average
candidate losses at 75 Вт: 2,9…6,0 Вт
```

## Open before production freeze

```text
LM5143DESIGN-CALC
slope compensation and exact OCP
loop compensation
input MLCC Ceff
R_DAMP pulse application
footprints and 3D
hot-plug/load-step/Bode tests
sealed +60 °C thermal test
```

## Permission

```text
prototype converter-core schematic: PERMITTED WITH CALC_TBD MARKERS
production schematic/BOM freeze: NOT PERMITTED
```