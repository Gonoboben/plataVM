# PCB-D POWER_5V — матрица кандидатов контроллера V1.9

Дата: 2026-07-21  
Статус: `PREFERRED CONTROLLER CLASS SELECTED; FINAL ORDERABLE PART OPEN`

## 1. Критерии выбора

Обязательные:

```text
VIN normal: 9,2…14,6 В
calculation point: 16 В
VOUT: 5 В
IOUT: 15 А continuous
IOUT: 20 А / 1 с
2 interleaved phases
single-output operation
external power stages or equivalent current scalability
current protection independent of firmware
operation in sealed assembly at +60 °C internal ambient
```

Желательные:

- shunt и/или DCR current sensing;
- adjustable current limit;
- independent enable and power-good;
- programmable soft start;
- spread spectrum или управляемый slew rate;
- automotive/high-temperature qualification;
- доступный design calculator;
- компактный корпус не выше H2.

## 2. Кандидаты

| Candidate | Input class | Two-phase single output | Package / height class | Основное преимущество | Главный риск | Решение |
|---|---:|---|---|---|---|---|
| **LM25143-Q1 / LM25143** | 3,5…42 В controller class | Да | 6 × 6 мм VQFN-40, H1/H2 | точное соответствие topology; shunt/DCR sensing; protection; design tools; официальный 15-А two-phase example | требуется расчёт compensation/current limit; окончательный Q1 orderable и доступность ещё не зафиксированы | **PREFERRED** |
| **LM5143-Q1** | 3,5…65 В controller class | Да | 6 × 6 мм VQFN-40, H1/H2 | большой transient headroom; automotive; та же архитектурная семья и design tool | избыточный voltage class; вероятно выше cost/complexity без необходимости | CONTINGENCY |
| **ADP1850** | 2,75…20 В controller class | Да | 5 × 5 мм LFCSP, H1 | компактный; accurate two-phase sharing; достаточен по normal VIN | малый запас над 16 В; более строгая transient clamp; менее предпочтителен для морской силовой ветви | ALTERNATE ONLY |
| **TPSM41615** | 4…16 В power module | один модуль 15 А; stacking/interleaving поддерживается | 11 × 16 × 4,2 мм, H1 | быстрая prototype implementation; интегрированные magnetics; высокая плотность | верхний предел совпадает с calculation point; 20-А режим требует stacking/derating; ограниченная свобода защиты и thermal layout | BENCHMARK / NOT BASELINE |

## 3. Предпочтительное решение

```text
Primary controller family:
LM25143-Q1 / LM25143

Transient contingency:
LM5143-Q1
```

До окончательной фиксации необходимо выбрать точный orderable вариант по:

1. температурной квалификации;
2. availability/second-source strategy;
3. MSL и package data;
4. design-calculator compatibility;
5. functional-safety documentation, если она потребуется для проекта;
6. price только после технического PASS.

## 4. Условие перехода на LM5143-Q1

LM5143-Q1 становится предпочтительным, если хотя бы одно условие подтверждено:

```text
PACK_BUS_P5_IN transient после защиты >36 В
требуемый abs-max margin для 42-В класса недостаточен
load-dump/inductive overshoot невозможно надёжно ограничить существующей защитой
EMI filter и TVS не обеспечивают повторяемый clamp с допустимым запасом
```

Порог `36 В` здесь является engineering review trigger, а не abs-max контроллера. Он сохраняет запас до 42-В operating class и должен уточняться по допускам конкретного clamp.

## 5. Почему module option не принят базовым

TPSM41615 показывает, что 15-А класс физически можно уместить в малом объёме, но не закрывает проект без дополнительных решений:

- 16 В — недостаточный подтверждённый transient запас;
- 20 А /1 с выше nominal одного модуля;
- параллель двух модулей увеличивает площадь и требует thermal/current-sharing review;
- проекту нужны прямые hard-off линии, отдельная диагностика и согласование с локальными выходами;
- thermal compliance в герметичном объёме всё равно требует испытаний.

Поэтому module вариант сохраняется только как benchmark для размера и prototype risk comparison.

## 6. Источники для design review

Нормативные первичные источники:

```text
Texas Instruments — LM25143 product page and datasheet SNVSC10
Texas Instruments — LM25143-Q1 product documentation
Texas Instruments — LM5143-Q1 product page and datasheet
Texas Instruments — LM5143DESIGN-CALC / supported LM25143 family
Analog Devices — ADP1850 product page and datasheet
Texas Instruments — TPSM41615 product page and datasheet
```

При расхождении настоящего документа с актуальным datasheet приоритет имеет datasheet конкретного orderable part.

## 7. Gate

```text
topology/controller family: PRELIMINARY PASS
preferred controller: LM25143 family
65-V contingency: LM5143-Q1
final orderable part: OPEN
transient clamp verification: OPEN
design-tool calculation: OPEN
prototype thermal validation: OPEN
```
