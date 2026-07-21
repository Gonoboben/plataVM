# PCB-D POWER_5V — расчётная база двухфазного синхронного buck V1.9

Дата: 2026-07-21  
Исходная точка: `main` commit `e98298061d6e699a325b9e83c188d9ac0c32bd0f`  
Статус: `PRELIMINARY ELECTRICAL DESIGN BASIS — NO FINAL PART OR FOOTPRINT FREEZE`

## 1. Назначение

Документ переводит PCB-D из абстрактной топологии в численно проверяемый двухфазный силовой узел.

В этом шаге:

- выбирается предпочтительный класс контроллера;
- задаются частота, индуктивность, токи фаз и токи конденсаторов;
- формируются классы MOSFET, дросселей, шунтов и capacitor banks;
- оценивается loss budget;
- задаются bounding boxes для следующей 3D-проверки.

Не выполняются:

- final part-number freeze;
- production schematic;
- footprints;
- copper routing;
- loop compensation freeze;
- thermal qualification;
- DRC/ERC release freeze.

## 2. Замороженные входные данные

```text
PACK_BUS_P5_IN functional range: 9,2…14,6 В preliminary
calculation upper point: 16 В
5V_SYS_BUS: 5 В
continuous output current: 15 А
short output current: 20 А
short duration: 1 с
repeat short event: не ранее 10 с и только при разрешении I²t model
sealed electronics volume
internal ambient design point: +60 °C
no thermal contact to pressure hull
PCB-D outline: 125 × 94 мм
PCB-D component height budget: ≤23 мм
```

Системные пределы PACK_BUS и локальные пределы PCB-D действуют одновременно.

## 3. Принятая топология

```text
single 5V_SYS_BUS output
2 interleaved phases
180° phase shift
external N-channel MOSFET half-bridges
one inductor per phase
current-mode controller
hard SAFE/HARD_OFF gating independent of local firmware
```

Преимущества двух фаз:

1. ток 15/20 А делится между двумя силовыми каналами;
2. уменьшается входной RMS ripple;
3. уменьшается суммарная выходная ripple-current;
4. тепловыделение распределяется по четырём MOSFET и двум дросселям;
5. сохраняется возможность независимой диагностики фаз;
6. topology соответствует уже принятой архитектуре PCB-D.

## 4. Предпочтительный контроллер

Рабочий кандидат:

```text
LM25143-Q1
```

Причины:

- два interleaved synchronous buck channels;
- поддержка single-output multiphase;
- входной диапазон контроллера 3,5…42 В;
- фиксированный 5 В либо adjustable output;
- shunt или inductor-DCR current sensing;
- hiccup current protection;
- independent EN/PGOOD;
- spread spectrum и slew-rate controlled drivers;
- automotive temperature qualification;
- корпус 6 × 6 мм VQFN-40;
- у изготовителя есть типовой двухфазный пример 5 В / 15 А.

Контроллер пока имеет статус:

```text
PREFERRED PROTOTYPE CONTROLLER
```

Финальное утверждение возможно после transient-clamp review, thermal estimate, compensation calculation и availability review.

## 5. Частота и индуктивность

Принята стартовая точка:

```text
fSW = 400 кГц на фазу
L1 = L2 = 3,3 мкГн ±20 %
```

Причина снижения частоты относительно высокочастотного vendor example — уменьшить switching losses в герметичном объёме без отвода тепла на корпус. Цена решения — более крупные дроссели.

Формула ripple одной фазы:

```text
ΔIL = VOUT × (1 − VOUT/VIN) / (L × fSW)
```

## 6. Расчёт фаз

| VIN | Duty | ΔIL phase p-p | Iphase RMS, 15 А total | Iphase peak, 15 А total | Iphase RMS, 20 А total | Iphase peak, 20 А total |
|---:|---:|---:|---:|---:|---:|---:|
| 9,2 В | 0,543 | 1,73 А | 7,52 А | 8,36 А | 10,01 А | 10,86 А |
| 12,8 В | 0,391 | 2,31 А | 7,53 А | 8,65 А | 10,02 А | 11,15 А |
| 14,6 В | 0,342 | 2,49 А | 7,53 А | 8,75 А | 10,03 А | 11,25 А |
| 16,0 В | 0,313 | 2,60 А | 7,54 А | 8,80 А | 10,03 А | 11,30 А |

Расчётный minimum peak-current capability одной фазы:

```text
I_PHASE_PEAK_DESIGN ≥13 А
```

Для выбора дросселя и MOSFET применяется дополнительный температурный и tolerance margin.

## 7. Дроссели

Предварительное требование на каждый дроссель:

```text
L = 3,3 мкГн ±20 %
Isat at operating temperature ≥15 А
Irms at operating temperature ≥10 А
DCR target at 25 °C ≤8 мОм
shielded construction
AEC-Q200 preferred
bounding box target ≤13 × 11 × 11 мм
```

Пример соответствующего класса — molded/high-current 3,3 мкГн с rated current около 15,5 А, saturation current около 19 А и DCR около 7,7 мОм. Это только доказательство доступности класса, а не part-number freeze.

Оценка copper loss для двух дросселей при 15 А total и DCR 7,7 мОм при 25 °C:

```text
P_L_25C ≈ 2 × 7,54² × 7,7 мОм ≈ 0,88 Вт
```

При нагреве DCR возрастёт; в thermal budget принимается 0,9…1,4 Вт total.

## 8. MOSFET class

На каждую фазу:

```text
1 × high-side N-MOSFET
1 × low-side N-MOSFET
```

Всего — четыре MOSFET.

Предварительный класс:

```text
VDS = 60 В preferred until clamp is verified
40 В allowed only if PCB-D input clamp including tolerance/overshoot ≤30 В
RDS(on) at 10 V and 25 °C target ≤3 мОм
hot design RDS(on) target ≤6 мОм
Qg target ≤40 нКл
package target 5 × 6 мм, height ≤1,5 мм
TJ max ≥150 °C; 175 °C preferred
AEC-Q101 preferred
```

40-V devices around 2…2,5 мОм in 5 × 6 мм packages exist, but the 40-V class is not accepted until the transient envelope is measured or formally clamped.

## 9. Current sensing и current limit

### 9.1 Prototype baseline

Для первого прототипа принимается точный low-inductance Kelvin shunt на каждую фазу:

```text
RSHUNT = 5 мОм ±1 %
power rating ≥1 Вт continuous
4-terminal/Kelvin connection preferred
low TCR
```

Потери:

```text
15 А total: около 0,57 Вт total по двум шунтам
20 А total: около 1,01 Вт total по двум шунтам в течение 1 с
```

Типовой current-limit threshold выбранного семейства около 73 мВ. Для 5 мОм номинальный threshold-current без учёта slope compensation и tolerances составляет около 14,6 А на фазу.

Точное cycle-by-cycle current limit должно быть рассчитано инструментом изготовителя и проверено по min/max threshold, slope compensation, ripple и температуре.

### 9.2 Production optimization

Inductor-DCR sensing допускается только после:

1. температурной корреляции DCR;
2. проверки current sharing;
3. проверки OCP во всём диапазоне;
4. сравнения потерь и точности с shunt вариантом.

До этого shunt sensing является более проверяемым вариантом.

## 10. Input capacitor RMS

Для двух фаз 180° и `L = 3,3 мкГн`, `fSW = 400 кГц`:

| VIN | CIN RMS при 15 А output | CIN RMS при 20 А output |
|---:|---:|---:|
| 9,2 В | 2,15 А | 2,85 А |
| 12,8 В | 3,16 А | 4,18 А |
| 14,6 В | 3,53 А | 4,68 А |
| 16,0 В | 3,68 А | 4,88 А |

Предварительное требование:

```text
input capacitor bank total ripple rating ≥6 А RMS at +60 °C
voltage rating ≥25 В
effective ceramic capacitance at bias ≥100 мкФ total
local high-frequency ceramics at each half-bridge
additional low-ESR bulk capacitor bank
```

Окончательное значение определяется cable inductance, PCB-A branch impedance, EMI filter и measured transient.

## 11. Output ripple и capacitor bank

Суммарная interleaved inductor ripple:

| VIN | 5V_SYS_BUS ripple current p-p | ripple current RMS |
|---:|---:|---:|
| 9,2 В | 0,28 А | 0,08 А |
| 12,8 В | 0,83 А | 0,24 А |
| 14,6 В | 1,19 А | 0,34 А |
| 16,0 В | 1,42 А | 0,41 А |

Следовательно, steady-state switching ripple не является главным ограничением output capacitance. Главный ограничитель — включение внешних нагрузок до 3 А на канал и возможное одновременное включение нескольких каналов.

Стартовый bounding set для прототипа, без value freeze:

```text
4 × 47 мкФ X7R ceramics minimum
2 × 220…330 мкФ low-ESR polymer class
additional 1…10 мкФ и 100 нФ local decoupling
```

До финального выбора необходимо утвердить:

```text
allowed 5V droop/overshoot
single-channel load step
maximum simultaneous load step
enable staggering policy
control-loop crossover target
```

## 12. Preliminary loss budget при 75 Вт

| Источник потерь | Предварительный диапазон |
|---|---:|
| MOSFET conduction + switching | 1,2…2,0 Вт |
| Два дросселя | 0,9…1,4 Вт |
| Два current shunt | около 0,57 Вт |
| Controller + gate drive | 0,4…0,8 Вт |
| Capacitors, copper, snubbers, misc. | 0,3…0,6 Вт |
| **Итого** | **3,4…5,4 Вт** |

Соответствующий оценочный efficiency range:

```text
η ≈ 93,3…95,7 % при 75 Вт
```

Это расчётная гипотеза, а не подтверждённая характеристика. Цель `η ≥92 % near 75 Вт` выглядит достижимой, но thermal compliance при +60 °C остаётся испытательным Gate.

## 13. Аппаратное отключение

PCB-D должна иметь два независимых уровня управления:

```text
normal enable/setpoint from local MCU
AND
hard P5_GROUP_SAFE_OFF / P5_GROUP_HARD_OFF gating
```

Hard lines должны физически запрещать gate drive/enable независимо от:

- MCU;
- CAN-FD;
- firmware state;
- SERVICE_OVERRIDE.

`P5_BOARD_FAULT_N` формируется аппаратной и локальной диагностикой и передаётся на PCB-B.

## 14. 20-А short mode

`20 А / 1 с` — разрешённый кратковременный output mode, а не overcurrent trip.

Требования:

1. current limit не должен срабатывать при корректном 20-А импульсе;
2. фаза должна выдерживать не менее 11,3 А peak plus margin;
3. short mode разрешается только системным I²t manager;
4. повтор не ранее 10 с;
5. аппаратная защита от настоящего КЗ остаётся быстрее и независимее;
6. temperature/PGOOD/fault telemetry контролируется в течение импульса.

## 15. Открытые вопросы PCB-D

| ID | Открытый параметр |
|---|---|
| Q-P5-009 | фактический transient envelope на PACK_BUS_P5_IN и clamp threshold |
| Q-P5-010 | допустимый droop/overshoot 5V_SYS_BUS |
| Q-P5-011 | single и simultaneous load-step profiles внешних выходов |
| Q-P5-012 | final fSW после efficiency/EMI comparison 300/400/500/600 кГц |
| Q-P5-013 | shunt 5 мОм versus DCR sensing после prototype correlation |
| Q-P5-014 | final inductor, MOSFET и capacitor candidates |
| Q-P5-015 | sealed-volume thermal result at +60 °C |
| Q-P5-016 | loop compensation и stability across VIN/load/cap tolerance |

## 16. Решение этапа

```text
2-phase synchronous buck: CONFIRMED AS WORKING ARCHITECTURE
preferred controller class: LM25143-Q1
fSW baseline: 400 кГц
L baseline: 3,3 мкГн per phase
prototype current sensing: 5 мОм Kelvin shunt per phase
PCB-D estimated losses: 3,4…5,4 Вт at 75 Вт
final component selection: OPEN
thermal qualification: OPEN
```
