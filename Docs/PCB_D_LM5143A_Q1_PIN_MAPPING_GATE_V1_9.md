# PCB-D POWER_5V — LM5143A-Q1 exact pin-mapping Gate V1.9

Дата: 2026-07-23  
Статус: `EXACT RHA-40 PIN MAP PASS — KICAD SYMBOL AND NATIVE ERC OPEN`

## 1. Назначение

Закрыть риск использования pinout прежнего LM5143-Q1/RWG вместо exact prototype controller:

```text
LM5143QRHARQ1
LM5143A-Q1 family
RHA VQFN-40 wettable-flank package
```

Pin mapping получен из TI datasheet `SNVSCC1`, May 2022. Product/orderable и package class остаются prototype inputs, а не production BOM freeze.

## 2. Критичное отличие

Запрещено переносить верхнюю группу выводов из старого LM5143-Q1 pinout без проверки.

Для LM5143A-Q1 RHA-40 exact mapping:

```text
31 EN1
32 RES
33 DEMB
34 MODE
35 AGND
36 VDDA
37 RT
38 DITH
39 SYNCOUT
40 EN2
```

Следовательно, любая symbol definition с `RT=31`, `EN1=32` или `EN2=33` является ошибочной для выбранного `LM5143QRHARQ1`.

## 3. Полный pin map

| Pin | Name | PCB-D contract |
|---:|---|---|
| 1 | SS2 | SS_COMMON |
| 2 | COMP2 | COMP_COMMON |
| 3 | FB2 | AGND; interleaved secondary EA disabled |
| 4 | CS2 | CS2_FILTERED |
| 5 | VOUT2 | 5V_SYS_BUS_SENSE |
| 6 | VCCX | 5V_SYS_BUS, startup constraints apply |
| 7 | PG2 | NC_PG2_TESTPAD; not system PGOOD |
| 8 | HOL2 | GH2_OFF |
| 9 | HO2 | GH2_ON |
| 10 | SW2 | PHASE2_SW |
| 11 | HB2 | HB2_BOOT |
| 12 | LOL2 | GL2_OFF |
| 13 | LO2 | GL2_ON |
| 14 | PGND2 | PGND2_LOCAL |
| 15 | VCC | VCC_BIAS |
| 16 | VCC | VCC_BIAS; connect to pin 15 |
| 17 | PGND1 | PGND1_LOCAL |
| 18 | LO1 | GL1_ON |
| 19 | LOL1 | GL1_OFF |
| 20 | HB1 | HB1_BOOT |
| 21 | SW1 | PHASE1_SW |
| 22 | HO1 | GH1_ON |
| 23 | HOL1 | GH1_OFF |
| 24 | PG1 | P5_PGOOD_OD; primary PGOOD |
| 25 | VIN | PACK_BUS_P5_IN_PROTECTED |
| 26 | VOUT1 | 5V_SYS_BUS_SENSE |
| 27 | CS1 | CS1_FILTERED |
| 28 | FB1 | AGND; fixed 5-V output |
| 29 | COMP1 | COMP_COMMON |
| 30 | SS1 | SS_COMMON |
| 31 | EN1 | EN_RUN |
| 32 | RES | RES_TIMER |
| 33 | DEMB | VDDA; FPWM |
| 34 | MODE | VDDA; single-output interleaved |
| 35 | AGND | AGND_LOCAL |
| 36 | VDDA | VDDA_BIAS |
| 37 | RT | RT_SET |
| 38 | DITH | VDDA; dithering disabled for prototype baseline |
| 39 | SYNCOUT | SYNCOUT_TESTPAD |
| 40 | EN2 | EN_RUN |
| EP | Exposed pad | controlled AGND/PGND layout boundary |

## 4. Single-output interleaved contract

Required connections:

```text
MODE -> VDDA
FB2 -> AGND
FB1 -> AGND for fixed 5 V
COMP1 <-> COMP2
SS1 <-> SS2
DEMB -> VDDA for FPWM
EN1 = EN2 = EN_RUN
```

`PG1` is the valid primary PGOOD indication. `PG2` is not wired into the board PGOOD/fault aggregate and remains an observable testpad only.

## 5. Validation

Machine-readable source:

```text
Hardware/KiCad/LM5143A_Q1_RHA40_PINMAP_V1_9.json
```

Validator:

```text
python Tools/erc/pcb_d_lm5143_pinmap_erc.py \
  Hardware/KiCad/LM5143A_Q1_RHA40_PINMAP_V1_9.json
```

Recorded result:

```text
LM5143A-Q1 RHA-40 pin-map ERC: PASS
physical pins: 40
exposed pad: 1
single-output interleaved ties: PASS
PG1/PG2 role separation: PASS
```

## 6. Freeze boundary

Closed:

```text
exact physical pin numbers and names
single-output interleaved logical ties
PG1/PG2 role separation
VCC 15/16 common-net requirement
```

Still open:

```text
KiCad symbol graphics and pin electrical types
symbol instantiation on 41_5V_DC_DC
owner KiCad 10.0 open/save
native KiCad ERC
footprint/land pattern
production BOM
```

The Gate does not authorize a footprint or production schematic freeze.

## 7. Architecture continuity

Unchanged:

- no `K_MAIN`;
- high current remains local to PCB-D and does not pass through PCB-B;
- `5V_SYS_BUS` remains separate from critical rails;
- EN1/EN2 are gated by direct hardware SAFE/HARD_OFF logic;
- CAN-FD/local MCU are not the only shutdown path;
- no hull thermal contact;
- no production footprint, copper or layout.

## 8. Next Gate

```text
create exact KiCad symbol from verified pin map
→ instantiate controller and discrete core symbols
→ owner KiCad 10.0 open/save
→ native ERC
→ exact UVLO/CS/gate/bootstrap/snubber calculation
```
