# PCB-D POWER_5V — кандидаты компонентов прототипа V1.9

Дата: 2026-07-21  
База: `main` commit `9ee73cf43f02a248cb81fffde2a2887105dc9a1e`  
Статус: `PROTOTYPE CANDIDATE SET SELECTED — NO PRODUCTION BOM FREEZE`

## 1. Назначение

Документ переводит принятые классы компонентов PCB-D в проверяемый набор заказных кандидатов для первого прототипа.

Этот набор разрешает:

- создание converter-core schematic;
- подготовку preliminary footprints;
- запуск официального design calculator;
- загрузку 3D-моделей;
- стендовый OCP/transient/thermal review.

Он не является:

- production BOM;
- подтверждением складского наличия на дату закупки;
- финальным footprint freeze;
- подтверждением thermal compliance;
- разрешением на серийное производство.

## 2. Замороженные требования

```text
VIN functional: 9,2…14,6 В
VIN calculation maximum: 16 В
VOUT: 5,0 В
IOUT continuous: 15 А
IOUT short: 20 А / 1 с
2 phases / 180°
fSW baseline: 400 кГц per phase
L: 3,3 мкГн per phase
controller voltage class: 65 В
MOSFET voltage class: 60 В minimum
input capacitor class: ≥35 В
sealed assembly; internal design point +60 °C
no thermal contact to hull
PCB-D: 125 × 94 мм
component height budget: ≤23 мм
```

## 3. Принятый prototype candidate set

| Ref group | Количество | Кандидат | Основные параметры | Статус |
|---|---:|---|---|---|
| U_DCDC | 1 | **LM5143QRHARQ1** | LM5143A-Q1; 3,5…65 В; VQFN-40 RHA 6 × 6 мм; automotive | PREFERRED PROTOTYPE |
| Q_HS1/Q_LS1/Q_HS2/Q_LS2 | 4 | **BUK9Y6R0-60E,115** | 60 В; logic-level; 6,0 мОм class; LFPAK56; AEC-Q101; 175 °C | PREFERRED PROTOTYPE |
| L1/L2 | 2 | **XAL1010-332MED** | 3,3 мкГн ±20 %; DCR 3,7 typ / 4,1 max мОм; Isat 27,4 А; Irms 18,2 А at 20 °C rise | PREFERRED PROTOTYPE |
| RSH1/RSH2 | 2 | **WSK25125L000FEA** | 5 мОм ±1 %; 1 Вт; 4-terminal; AEC-Q200; pulse/current-sense | PREFERRED PROTOTYPE |
| D_TVS | 1 | **Littelfuse SMCJ18A** | 18 В standoff; 20…22,1 В breakdown; 29,2 В clamp class; 1,5 кВт | PREFERRED PROTOTYPE |
| C_DAMP | 1 | **Panasonic EEH-ZK1V331P** | 330 мкФ; 35 В; 20 мОм max; 2,8 А RMS; 10 × 10,2 мм; −55…+125 °C | PREFERRED PROTOTYPE |
| R_DAMP | 1 | **Bourns PWR263S-35 family, 0,10 Ом /1 %** | D²PAK; AEC-Q200; pulse-capable; 35-Вт class with thermal-pad conditions | PROTOTYPE FAMILY; ORDER CODE VERIFY |
| C_IN_MLCC | 8 footprints | **TDK C3225X7R1H226M250AC class** | 22 мкФ; 50 В; X7R; 1210 | 6 POPULATED + 2 DNP START |
| C_OUT_POLY | 2 | **Panasonic 10SVPC330M** | 330 мкФ; 10 В; ESR 19 мОм; ripple 3,46 А; 8 × 6,9 мм | PREFERRED PROTOTYPE |
| C_OUT_MLCC | 6 footprints | **Murata GRM32ER71A476KE15L class** | 47 мкФ; 10 В; X7R; 1210 | 4 POPULATED + 2 DNP START |

## 4. Контроллер U_DCDC

Принят exact orderable:

```text
LM5143QRHARQ1
```

Причины:

1. активный orderable вариант LM5143A-Q1;
2. 65-В входной класс;
3. две interleaved synchronous buck-фазы;
4. single-output multiphase;
5. peak current-mode control;
6. independent ENABLE/PGOOD;
7. adjustable soft start;
8. VQFN-40 RHA с wettable flanks;
9. диапазон −40…+150 °C для устройства;
10. поддержка LM5143DESIGN-CALC.

До prototype schematic необходимо проверить:

- pin-1 orientation;
- exposed-pad land pattern;
- thermal-via array;
- MSL и правила пайки;
- exact pin mapping для multiphase connection;
- hard SAFE/HARD_OFF gating на EN/PWM path.

## 5. MOSFET Q1…Q4

Для первого прототипа используется один тип MOSFET во всех четырёх позициях:

```text
BUK9Y6R0-60E,115
```

Преимущества единого типа:

- один footprint;
- один закупаемый артикул;
- одинаковая thermal model;
- упрощённая замена при отладке;
- отсутствие ошибки HS/LS при сборке;
- логический gate class, совместимый с приблизительно 5-В gate drive.

Ограничения:

- 6-мОм class увеличивает conduction loss относительно 2…3-мОм альтернатив;
- gate/switching losses должны рассчитываться по фактическим Qg/Qgd/Coss и выбранным HOL/LOL resistors;
- LFPAK56 нельзя считать footprint-совместимым с каждым Power-SO8 без проверки manufacturer land pattern;
- переход на разные HS/LS MOSFET допускается только после измерения потерь прототипа.

Prototype footprint должен предусматривать:

- Kelvin source для gate return, если допускает корпус;
- минимальный gate loop;
- отдельные gate turn-on/turn-off resistors либо совместимые DNP options;
- SW copper keepout от CS/COMP/FB;
- thermal vias согласно расчёту, а не максимальное заполнение без проверки current path.

## 6. Дроссели L1/L2

Принят:

```text
XAL1010-332MED
```

Сравнение с требованиями:

| Параметр | Требование | Кандидат | Результат |
|---|---:|---:|---|
| Индуктивность | 3,3 мкГн ±20 % | 3,3 мкГн ±20 % | PASS |
| DCR max at 25 °C | ≤8 мОм | 4,1 мОм | PASS |
| Isat | ≥15 А hot target | 27,4 А at 25 °C, 30 % drop criterion | PRELIMINARY PASS |
| Irms | ≥10 А hot target | 18,2 А at 20 °C rise | PRELIMINARY PASS |
| Shielding | обязательно | molded shielded class | PASS |
| AEC-Q200 | preferred | AEC-Q flag | PASS |

Необходимо отдельно проверить manufacturer curves:

- inductance vs DC current at +60…+125 °C;
- DCR at operating temperature;
- core loss at 400 кГц and calculated ripple;
- component self-heating inside sealed volume;
- mutual heating of L1/L2.

## 7. Current shunts

Принят:

```text
WSK25125L000FEA
5 мОм ±1 %
1 Вт
4-terminal
```

Потери без учёта ripple:

```text
15 А total:
Iphase = 7,5 А
P per shunt = 7,5² × 0,005 = 0,281 Вт
P total = 0,563 Вт

20 А total:
Iphase = 10 А
P per shunt = 10² × 0,005 = 0,500 Вт
P total = 1,000 Вт for 1 с
```

Требования layout:

- force-current pads не используются как sense pickup;
- CS/CSG берутся только с Kelvin terminals;
- обе sense-pairs имеют симметричную длину и окружение;
- RC filters устанавливаются у controller pins;
- sense traces не пересекают SW copper и gate loops.

## 8. Input MLCC bank

Принят класс:

```text
22 мкФ / 50 В / X7R / 1210
TDK C3225X7R1H226M250AC class
8 footprints total
6 populated initially
2 DNP tuning positions
```

Причина отказа от условного `47 мкФ /35 В`:

- высокоёмкостный 35-В X7R в заданном габарите нельзя принимать без подтверждённого orderable;
- номинальная ёмкость MLCC не равна effective capacitance при DC bias;
- 50-В class даёт дополнительный запас над SMCJ18A clamp;
- восемь позиций дают возможность подобрать effective C без изменения PCB.

Acceptance:

```text
C_IN_EFFECTIVE_TOTAL at 16 В, tolerance, temperature and aging ≥100 мкФ
```

До schematic freeze требуется выгрузить DC-bias curves exact orderable и посчитать:

```text
Ceff_total = Σ Ceff_i(16 В, temperature, tolerance, aging)
```

Если шесть деталей не дают 100 мкФ effective, заполняются DNP positions либо выбирается более крупный/другой MLCC class.

## 9. RC damping branch

```text
C_DAMP = EEH-ZK1V331P
330 мкФ /35 В

R_DAMP = 0,10 Ом /1 %
PWR263S-35 family
```

Резистор выбирается как намеренно крупный prototype component для безопасной настройки hot-plug damping. Его 35-Вт обозначение не означает 35 Вт без теплоотвода; ключевой критерий этого применения — single-pulse energy и кратковременная SOA.

Перед заказом exact order code R_DAMP необходимо подтвердить:

- существование 0,10-Ом /1-% варианта;
- pulse-energy curve на 20…100 мкс;
- способность выдержать не менее 50 мДж, target 100 мДж;
- отсутствие обязательного внешнего радиатора для заданного импульса;
- footprint D²PAK и доступная площадь.

На плате также предусматриваются DNP/tuning positions для 0,068…0,15 Ом.

## 10. Output capacitor bank

Стартовая конфигурация:

```text
2 × Panasonic 10SVPC330M
4 × 47 мкФ /10 В X7R /1210
2 additional 47-мкФ footprints DNP
```

Номинальная bulk capacitance:

```text
Cpoly_nom = 660 мкФ
Cmlcc_nom populated = 188 мкФ
```

Но loop design использует:

- actual ESR/ESL;
- effective MLCC capacitance at 5 В;
- tolerance and aging;
- load-step target;
- compensation output official design tool.

`10SVPC330M` принят для прототипа из-за малой высоты и низкого ESR. Для production необходимо отдельное endurance/reliability решение, поскольку prototype part не является AEC-Q200 и имеет 2000 ч at 105 °C.

## 11. Mechanical fit

Предварительные высоты:

| Объект | Высота/габарит | Бюджет | Результат |
|---|---:|---:|---|
| LM5143QRHARQ1 | H1, около 1 мм package class | ≤23 мм | PASS |
| BUK9Y6R0-60E | low-profile LFPAK56 | ≤23 мм | PASS |
| XAL1010-332MED | около 10 мм class | ≤23 мм | PASS |
| WSK2512 | <1 мм class | ≤23 мм | PASS |
| SMCJ18A | DO-214AB low profile | ≤23 мм | PASS |
| EEH-ZK1V331P | 10,2 мм | ≤23 мм | PASS |
| 10SVPC330M | 6,9 мм | ≤23 мм | PASS |
| PWR263S-35 | D²PAK low-profile class | ≤23 мм | PASS |

Статус площади сохраняется `PRELIMINARY PASS`. Реальный 3D-fit требуется после получения официальных STEP-моделей и exact footprints.

## 12. Source hierarchy

При расхождении данных приоритет:

```text
exact manufacturer datasheet
→ exact manufacturer product page
→ reference-design documentation
→ present candidate table
```

Distributor data используется только для подтверждения orderable/packing и не заменяет manufacturer specifications.

## 13. Gate result

```text
controller exact orderable: SELECTED
MOSFET prototype type: SELECTED
inductor prototype type: SELECTED
shunt prototype type: SELECTED
TVS prototype type: SELECTED
damping capacitor: SELECTED
output polymer capacitor: SELECTED
input/output MLCC classes and footprint counts: SELECTED
R_DAMP exact order code: OPEN
DC-bias effective capacitance verification: OPEN
official calculator: OPEN
compensation: OPEN
prototype schematic: NEXT
production BOM: NOT FROZEN
```