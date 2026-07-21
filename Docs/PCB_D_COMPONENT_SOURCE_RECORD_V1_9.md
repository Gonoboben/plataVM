# PCB-D POWER_5V — source record prototype components V1.9

Дата: 2026-07-21  
Статус: `SOURCE TRACEABILITY RECORDED — AVAILABILITY AT PURCHASE OPEN`

## 1. Purpose

Record the primary manufacturer sources used for prototype candidate selection. This file contains source names and verification scope; exact datasheets remain authoritative.

## 2. Sources

| Component | Primary manufacturer source | Verified scope |
|---|---|---|
| LM5143QRHARQ1 | Texas Instruments LM5143A-Q1 product/orderable page and datasheet | active orderable, RHA-40, 3,5…65 В, temperature/package family, design-tool support |
| BUK9Y6R0-60E | Nexperia product page and interactive datasheet | 60 В, 6,0-мОм logic-level class, LFPAK56, AEC-Q101, 175 °C |
| XAL1010-332MED | Coilcraft exact product page/datasheet | 3,3 мкГн, ±20 %, DCR, Isat, Irms, package/model resources |
| WSK2512 5-мОм | Vishay WSK2512 family datasheet and orderable record | 4-terminal family, low resistance, 1-% capability; exact code verification required at purchase |
| SMCJ18A | Littelfuse exact product page/datasheet | standoff, breakdown, clamp, pulse power and package |
| EEH-ZK1V331P | Panasonic exact product page/datasheet | 330 мкФ/35 В, ESR, ripple, temperature and dimensions |
| PWR263S-35 | Bourns family product page/datasheet | D²PAK, 0,02…130 кОм family, 1/5 %, power/pulse family |
| C3225X7R1H226M250AC | TDK exact product page and characteristic data | 22 мкФ/50 В/X7R/1210 class; DC-bias data required |
| 10SVPC330M | Panasonic exact product page/datasheet | 330 мкФ/10 В, ESR, ripple, temperature/endurance and dimensions |
| GRM32ER71A476KE15L | Murata exact product page/SimSurfing | 47 мкФ/10 В/X7R/1210 class; Ceff data required |

## 3. Rules

1. Manufacturer datasheet overrides this project document.
2. Distributor pages may verify packaging/orderability but do not override ratings.
3. Inventory and lifecycle status are checked again immediately before purchase.
4. Exact land patterns and STEP models are downloaded only from manufacturer sources or verified ECAD portals.
5. A part is not production-approved merely because it is available for purchase.
6. MLCC nominal capacitance is not accepted as effective capacitance without DC-bias/temperature/tolerance review.
7. Pulse resistor selection requires the exact pulse-energy curve, not only continuous power rating.

## 4. Availability Gate

Before prototype purchase:

```text
active/lifecycle status
minimum order quantity
packaging format
lead time
authorized distributor
lot traceability
MSL/reflow data
change-notification availability
```

must be recorded for each exact orderable.

## 5. Result

```text
manufacturer source hierarchy: PASS
exact candidate traceability: PASS
inventory/lead-time freeze: OPEN
production lifecycle strategy: OPEN
```