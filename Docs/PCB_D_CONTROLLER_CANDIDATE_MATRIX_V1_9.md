# PCB-D POWER_5V — матрица кандидатов контроллера V1.9

Дата исходной фиксации: 2026-07-21  
Дата актуализации transient review: 2026-07-21  
Статус: `65-V CONTROLLER CLASS PREFERRED; FINAL ORDERABLE PART OPEN`

## 1. Критерии выбора

Обязательные:

```text
VIN normal: 9,2…14,6 В
calculation DC point: 16 В
uncharacterized hot-plug/inductive transient
VOUT: 5 В
IOUT: 15 А continuous
IOUT: 20 А / 1 с
2 interleaved phases
single-output operation
external power stages
current protection independent of firmware
operation in sealed assembly at +60 °C internal ambient
```

Желательные:

- shunt и/или DCR current sensing;
- adjustable current limit;
- independent enable and power-good;
- programmable soft start;
- spread spectrum и управляемый slew rate;
- automotive/high-temperature qualification;
- официальный design calculator;
- PSpice/reference-design support;
- компактный корпус не выше H2;
- достаточный voltage headroom до измерения transient envelope.

## 2. Актуализированные кандидаты

| Candidate | Input class | Two-phase single output | Package / height class | Основное преимущество | Главный риск | Решение |
|---|---:|---|---|---|---|---|
| **LM5143A-Q1** | 3,5…65 В controller class | Да | 6 × 6 мм VQFN-40, H1/H2 | TI рекомендует для новых разработок; большой transient headroom; automotive; single-output multiphase; supported design tool | final orderable, compensation/OCP и availability ещё не зафиксированы | **PREFERRED PROTOTYPE FAMILY** |
| **LM5143-Q1** | 3,5…65 В controller class | Да | 6 × 6 мм VQFNP-40, H1/H2 | проверенная 65-В family; те же основные функции и design tool | TI указывает newer LM5143A-Q1 as recommended for new designs | COMPATIBLE ALTERNATE |
| **LM25143-Q1 / LM25143** | 3,5…42 В controller class | Да | 6 × 6 мм VQFN-40, H1/H2 | точное соответствие topology; низкий voltage-class cost/availability potential | зависит от гарантированного clamp и имеет меньший transient margin | ALTERNATE ONLY AFTER MEASUREMENT |
| **ADP1850** | 2,75…20 В controller class | Да | 5 × 5 мм LFCSP, H1 | компактный; two-phase sharing | практически отсутствует transient margin над 16 В | REJECTED FOR BASELINE |
| **TPSM41615** | 4…16 В power module | один модуль 15 А; stacking possible | 11 × 16 × 4,2 мм, H1 | быстрый bench prototype; integrated magnetics | upper input equals calculation point; 20-А mode и transient margin неудовлетворительны | BENCHMARK ONLY |

## 3. Предпочтительное решение

```text
Primary prototype controller family:
LM5143A-Q1

Compatible alternate:
LM5143-Q1

Lower-voltage alternate after measured clamp proof:
LM25143-Q1 / LM25143
```

Решение по 65-В class принято не потому, что штатный PACK_BUS равен 65 В, а потому что реальный hot-plug/inductive transient ещё не измерен и проекту нельзя зависеть от идеального TVS clamp на первом прототипе.

## 4. Условие возврата к 42-В class

LM25143-Q1 может стать production candidate только после одновременного выполнения:

```text
normal DC input ≤16 В
measured preferred transient peak ≤30 В
all tolerances/layout/temperature included
repetitive events verified
TVS failure/open scenario reviewed
minimum controller abs-max margin accepted
40-V MOSFET question reviewed separately
```

Даже при возврате к 42-В controller 40-В MOSFET не принимается автоматически.

## 5. Совместимость расчётного инструмента

Официальный `LM5143DESIGN-CALC` поддерживает:

```text
LM25143
LM25143-Q1
LM5143
LM5143-Q1
LM5143A-Q1
```

Инструмент позволяет:

- выбирать dual/two-phase/multiphase configuration;
- рассчитывать inductance и capacitor values;
- задавать OCP, soft start, hiccup и switching frequency;
- рассчитывать compensation и crossover;
- оценивать efficiency, losses, size и EMI filter;
- формировать preliminary schematic/BOM.

Design-tool output остаётся отдельным обязательным Gate и не заменяется ручным расчётом.

## 6. Package and mechanical impact

Переход с LM25143-Q1 на LM5143A-Q1 не требует изменения принятого controller bounding box:

```text
controller placeholder: 7 × 7 × 1,5 мм
height class: H1
power-stage envelope: 70 × 38 × 13 мм
```

Конкретный footprint создаётся только после выбора exact orderable part и проверки land pattern производителя.

## 7. Electrical consequences

Сохраняются без изменения:

```text
2 phases / 180°
fSW baseline 400 кГц
L = 3,3 мкГн per phase
5 мОм Kelvin shunt per phase
60-В MOSFET class
15 А continuous / 20 А for 1 с
hard SAFE/HARD_OFF gating
```

Изменяется только controller voltage headroom.

## 8. Sources for design review

Primary sources:

```text
Texas Instruments — LM5143A-Q1 product page and datasheet
Texas Instruments — LM5143-Q1 product page; LM5143A-Q1 recommended for new designs
Texas Instruments — LM25143-Q1 product page and datasheet
Texas Instruments — LM5143DESIGN-CALC supported products and functions
Texas Instruments — PMP23262/PMP23452 reference-design material
```

При расхождении настоящего документа с актуальным datasheet приоритет имеет datasheet exact orderable part.

## 9. Gate

```text
topology/controller family: PRELIMINARY PASS
preferred controller: LM5143A-Q1
compatible alternate: LM5143-Q1
42-V alternate: LM25143-Q1 after measured proof
final orderable part: OPEN
transient clamp verification: OPEN
design-tool calculation: OPEN
prototype thermal validation: OPEN
```
