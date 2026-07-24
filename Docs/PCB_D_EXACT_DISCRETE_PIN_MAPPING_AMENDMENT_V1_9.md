# PCB-D POWER_5V — exact discrete physical pin-map amendment V1.9

Дата: 2026-07-24  
Gate: `Q-P5-019C1`  
Статус: `CLOSED_EXACT_DISCRETE_PINMAP_NATIVE_INTERNAL_ERC_PASS`

## 1. Причина amendment

Owner visual review выявил, что controller symbol был exact, но силовые MOSFETs и Kelvin-шунты оставались generic symbols. Это было допустимо до footprint Gate, но недостаточно для физически проверяемой схемы.

## 2. Официальный physical contract

```text
BUK9Y6R0-60E, LFPAK56 / SOT669:
1 = Source
2 = Source
3 = Source
4 = Gate
mb = Drain

WSK2512 four-terminal:
I1, I2 = current connections
E1, E2 = voltage-sense connections
```

## 3. Реализация

Созданы exact symbols `BUK9Y6R0_60E_LFPAK56` и `WSK2512_4T_KELVIN`. Четыре MOSFET instances используют полный physical pin set. RSH1/RSH2 разделяют force path и Kelvin-sense path.

```text
RSH1: I1=PHASE1_L_OUT, I2=5V_SYS_BUS, E1=RSH1_SENSE_HI, E2=RSH1_SENSE_LO
RSH2: I1=PHASE2_L_OUT, I2=5V_SYS_BUS, E1=RSH2_SENSE_HI, E2=RSH2_SENSE_LO
```

Controller VOUT1/VOUT2, CS filters and phase-monitor placeholders now terminate on the corresponding per-phase Kelvin nodes.

## 4. Проверки

```text
exact MOSFET pin contract: PASS
exact MOSFET instances: 4
generic NMOS_POWER instances: 0
exact Kelvin shunt terminal contract: PASS
exact Kelvin shunt instances: 2
separate force/sense nets: PASS
controller exact pin map: PASS
generator byte parity: PASS
native KiCad internal topology: PASS
production footprints: 0
```

## 5. Freeze boundary

Закрыт physical symbol/pin contract. Не закрыты manufacturer land-pattern review, footprint assignment, copper geometry, Kelvin trace geometry, thermal-via design и production BOM.

## 6. Следующий Gate

`Q-P5-019D` — owner KiCad 10 open/save, hierarchy-context visual/ERC review на обновлённых exact symbols.
