# PCB-D POWER_5V — предварительные bounding boxes компонентов V1.9

Дата: 2026-07-21  
Статус: `MECHANICAL CANDIDATE ENVELOPE — NO FOOTPRINT FREEZE`

## 1. Назначение

Документ преобразует расчётную базу PCB-D в габаритные ограничения для проверки платы `125 × 94 мм`, уровня L1 и высоты компонентов `≤23 мм`.

Bounding boxes включают технологический запас вокруг корпуса, но не являются courtyard окончательного footprint.

## 2. Рабочая зона PCB-D

Существующие placeholder-зоны:

```text
INPUT PROT
TWO-PHASE POWER STAGE
BULK / OUTPUT CAPS
LOCAL MCU / CAN
OUT1…OUT5
OUT6…OUT10
THERMAL SPREADING
```

Высотные классы:

```text
H1: 0…5 мм
H2: >5…10 мм
H3: >10…16 мм
H4: >16…23 мм
```

## 3. Candidate bounding boxes

| Объект | Количество | Bounding box одного объекта | Класс | Комментарий |
|---|---:|---:|---:|---|
| Two-phase controller | 1 | 7 × 7 × 1,5 мм | H1 | включает 6 × 6 мм VQFN и assembly margin |
| High-side MOSFET | 2 | 7 × 6 × 1,5 мм | H1 | 5 × 6 мм class plus courtyard margin |
| Low-side MOSFET | 2 | 7 × 6 × 1,5 мм | H1 | 5 × 6 мм class plus courtyard margin |
| Kelvin current shunt | 2 | 7 × 4 × 1,5 мм | H1 | 4-terminal low-inductance class |
| Phase inductor | 2 | 13 × 11 × 11 мм | H3 | 3,3 мкГн / ≥15 А Isat class |
| Gate resistors/bootstrap/snubber block | 2 | 12 × 8 × 3 мм | H1 | один локальный блок на фазу |
| Input ceramic capacitor block | 2 | 14 × 10 × 3 мм | H1 | максимально близко к half-bridge |
| Input bulk capacitor bank | 1 | 22 × 18 × 12 мм | H3 | provisional polymer/electrolytic class |
| Output ceramic bank | 1 | 32 × 16 × 4 мм | H1 | несколько X7R параллельно |
| Output polymer bank | 1 | 34 × 24 × 16 мм | H3 | 2×220…330 мкФ class, ориентация TBD |
| Local MCU/CAN block | 1 | 18 × 16 × 5 мм | H1 | MCU/transceiver/support area, без точных деталей |
| Input protection/TVS/filter block | 1 | 18 × 22 × 12 мм | H3 | clamp и EMI topology открыты |
| Output protection group 1…5 | 1 | 42 × 24 × 12 мм | H3 | high-side switches/sense/connectors separate review |
| Output protection group 6…10 | 1 | 42 × 24 × 12 мм | H3 | high-side switches/sense/connectors separate review |

## 4. Power-stage cluster

Рекомендуемая относительная последовательность одной фазы:

```text
local CIN
→ high-side/low-side MOSFET pair
→ SW copper island
→ phase inductor
→ shared output capacitor bank
```

Контроллер и shunt-sense routing:

```text
controller near both phases
Kelvin sense separated from SW nodes
analog ground local and controlled
COMP/FB away from inductors and gate loops
```

Предварительный общий power-stage envelope, включая обе фазы:

```text
70 × 38 × 13 мм
```

Он включает:

- controller;
- четыре MOSFET;
- два шунта;
- два дросселя;
- bootstrap/gate/snubber blocks;
- local high-frequency input capacitors;
- routing and separation allowance.

## 5. Capacitor envelope

Предварительная объединённая зона:

```text
input bulk + output ceramic/polymer:
42 × 38 × 17 мм maximum placeholder
```

Высота `17 мм` относится к худшему bounding box до выбора low-profile polymer bank. Целевой выбор должен снизить фактическую высоту до `≤16 мм`, чтобы перейти из H4 в H3 и увеличить межуровневый запас.

## 6. Проверка площади

Плата:

```text
125 × 94 мм = 11 750 мм²
```

Рабочая оценка распределения:

| Функция | Area envelope |
|---|---:|
| Input protection | около 400 мм² |
| Two-phase control/power stage | около 2 660 мм² |
| Capacitor banks | около 1 600 мм² |
| 10 output channels | около 2 300 мм² |
| Local MCU/CAN | около 300 мм² |
| connectors, keepouts, creepage, tool access, routing | остаток около 4 490 мм² |

Суммарный номинальный fit возможен, но не подтверждает copper-current density, thermal spreading и connector mating volume.

## 7. Проверка высоты

Максимальные candidate objects:

```text
phase inductors: 11 мм
input bulk bank: 12 мм
output polymer bank: target ≤16 мм
input protection: 12 мм
```

Следствие:

```text
current expected PCB-D component height ≤16 мм
existing PCB-D budget ≤23 мм
nominal local height reserve ≥7 мм
```

Это позволяет потенциально уменьшить L1 allocation, но такая оптимизация запрещена до выбора реальных компонентов и 3D models.

## 8. Thermal keepout

Обязательные требования:

1. два phase inductors не устанавливать вплотную друг к другу;
2. не закрывать силовую зону верхней платой без воздушного зазора;
3. не размещать polymer capacitors в локальном горячем потоке MOSFET/inductor;
4. не использовать стенку корпуса как штатный радиатор;
5. предусмотреть измерительные точки температуры MOSFET, дросселей и capacitor bank;
6. конформное покрытие учитывать в thermal model;
7. полимерный термоклей не наносить на силовые компоненты как тепловую изоляцию.

## 9. Механические неопределённости

Открыты:

- точная высота выбранного inductor;
- ориентация polymer bank;
- connector mating direction;
- wire bend radius input и 10 outputs;
- screw/standoff diameter;
- access через L2;
- возможность демонтажа PCB-D без снятия PCB-B;
- расстояние PCB-D до PCB-E;
- положение платы относительно крышки.

## 10. Решение этапа

```text
PCB-D 125 × 94 мм area fit: PRELIMINARY PASS
PCB-D ≤23 мм height budget: PRELIMINARY PASS
expected real maximum height: ≤16 мм target
power-stage placeholder: 70 × 38 × 13 мм
capacitor placeholder: 42 × 38 × 17 мм maximum
final footprint/3D fit: OPEN
thermal qualification: OPEN
```
