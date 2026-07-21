# PCB-D POWER_5V — входная защита и transient boundary V1.9

Дата: 2026-07-21  
Исходная точка: `main` commit `f5dcdf8cf141927a40566f6a371feb3304d4db2c`  
Статус: `PRELIMINARY PROTOTYPE PROTECTION BOUNDARY — MEASUREMENT REQUIRED`

## 1. Назначение

Документ задаёт входную защиту `PACK_BUS_P5_IN` для прототипа PCB-D и отделяет:

- штатный диапазон питания;
- допустимый кратковременный transient;
- локальную TVS-защиту;
- damping hot-plug ringing;
- sustained overvoltage, которое TVS не должна удерживать постоянно.

Документ не является финальным schematic/BOM freeze.

## 2. Входные данные

```text
normal functional input: 9,2…14,6 В
calculation DC upper point: 16 В
continuous input design class: 15 А
output: 5 В / 15 А continuous
short output: 5 В / 20 А / 1 с
internal ambient design point: +60 °C
```

`PACK_BUS_P5_IN` является внутренней ветвью после PCB-A. Это не автомобильная клемма аккумулятора и не должна подвергаться штатному load dump. Однако возможны:

1. hot-plug/branch-connect ringing;
2. cable/trace inductive overshoot;
3. отключение нагрузки при текущем токе;
4. коммутация PCB-A;
5. ошибочная последовательность подключения;
6. переходные процессы входного EMI-фильтра;
7. fault upstream power switch.

## 3. Принятая прототипная структура

```text
PACK_BUS_P5_IN connector
→ shortest possible power/return pair
→ local unidirectional TVS to POWER_GND
→ local high-frequency ceramic CIN
→ separate RC damping branch
→ two-phase buck power stage
```

На первом прототипе не вводится обязательный последовательный input inductor. Его footprint допускается только как DNP option после анализа EMI и устойчивости входного фильтра.

## 4. TVS class

Рабочий prototype class:

```text
SMCJ18A-class
unidirectional
VRWM = 18 В
VBR = 20…22,1 В
VC ≈29,2 В at rated pulse current
10/1000-µs peak pulse class = 1,5 кВт
```

Причины:

1. `VRWM = 18 В` выше расчётного DC maximum 16 В;
2. breakdown начинается выше штатного диапазона;
3. clamp около 29,2 В значительно ниже 65-В controller class;
4. SMC class имеет больший pulse-energy margin, чем SMB/SMF;
5. размер остаётся совместимым с H1/H2 input-protection zone.

Конкретный изготовитель и part number не замораживаются. Для BOM-кандидата должны быть проверены actual derating, temperature coefficient, pulse curves, package height и availability.

## 5. Voltage classes

После выбора 65-В контроллера сохраняется:

```text
controller voltage class: 65 В
power MOSFET class: 60 В minimum
input capacitor class: 25 В minimum for normal bank
TVS standoff: 18 В
```

25-В входные конденсаторы находятся за тем же TVS и должны проверяться по реальному измеренному peak. Если на capacitor terminals измеряется более 22 В с учётом допуска и ringing, необходимо перейти на 35-В capacitor class либо изменить clamp/layout.

40-В MOSFET class запрещён до отдельного measured transient review.

## 6. Прототипный критерий напряжения

Для первого прототипа принимаются следующие acceptance targets:

```text
normal steady input: ≤16 В
preferred transient peak at controller/MOSFET input: ≤32 В
absolute engineering acceptance target: ≤36 В
ringing above 32 В: as short as practicable; target <10 мкс
```

`36 В` не является новым nominal input. Это измерительный Gate, сохраняющий запас до 60-В MOSFET и 65-В controller class.

Если измерено:

```text
VPEAK >36 В
```

то prototype Gate не пройден и требуется:

1. уменьшение loop inductance;
2. изменение TVS class;
3. увеличение pulse power;
4. изменение damping network;
5. active surge stopper либо upstream disconnect;
6. пересмотр capacitor voltage class.

## 7. Placement requirements

TVS должна быть размещена:

- непосредственно у входа PCB-D;
- между `PACK_BUS_P5_IN` и `POWER_GND`;
- до длинных PCB traces и до optional EMI inductor;
- с минимальной общей длиной high-current loop;
- с широким отдельным возвратом в входную `POWER_GND` zone;
- не через sensitive ground, SIGNAL_GND или controlled net-tie.

Measurement points:

```text
TP_P5_IN_RAW
TP_P5_IN_CLAMPED
TP_P5_POWER_GND
```

Осциллографическое измерение выполняется low-inductance probe connection. Длинный ground lead запрещён, поскольку он искусственно увеличивает наблюдаемый ringing.

## 8. Sustained overvoltage

TVS не считается средством удержания длительного перенапряжения.

При sustained input выше допустимого диапазона:

```text
TVS alone → unacceptable continuous dissipation
```

Требуется upstream action:

- PCB-A branch switch OFF;
- branch fuse/protection coordination;
- HARD_OFF при системном fault;
- блокировка повторного включения до диагностики.

TVS должна переживать transient до отключения, но не постоянную ошибочную подачу повышенного напряжения.

## 9. Reverse polarity

PCB-D находится внутри управляемой многоплатной системы. Для prototype baseline принимается:

```text
reverse-polarity prevention:
connector keying + harness control + PCB-A branch architecture
```

Отдельный series ideal-diode MOSFET на PCB-D пока не добавляется из-за потерь, площади и усложнения hard-off coordination.

Если physical connector review покажет возможность обратного подключения, reverse-polarity stage становится обязательным до production schematic.

## 10. Fault behavior

| Fault | Требуемое поведение |
|---|---|
| Short transient | TVS clamp + local capacitors; converter survives |
| Repetitive ringing | damping network reduces Q; event logged during test |
| Sustained overvoltage | upstream branch OFF; TVS not used continuously |
| TVS short failure | upstream branch protection/fuse isolates PCB-D |
| TVS open failure | controller/MOSFET voltage margin remains last barrier; fault found by test/inspection |
| Input UV | controller disabled by UVLO; no chatter |
| HARD_OFF | gate drive disabled independently of local MCU |

## 11. Prototype test matrix

1. hot-plug at 9,2 В, 12,8 В, 14,6 В and 16 В;
2. source impedance minimum and maximum;
3. cable/harness inductance minimum and maximum;
4. no-load, 7,5-А, 15-А and 20-А/1-с output conditions;
5. turn-off of 15-А load;
6. repeated connect/disconnect;
7. TVS cold and hot;
8. damping branch populated and DNP comparison;
9. oscilloscope measurement at connector, TVS and controller input;
10. sustained overvoltage fault injection with upstream disconnect verification.

## 12. Sources

Primary sources:

```text
Texas Instruments — LM5143A-Q1 product page and datasheet
Texas Instruments — LM5143DESIGN-CALC supported products
Texas Instruments — input damping/hot-plug technical article SSZTDA5
Littelfuse — SMCJ18A official product data
```

## 13. Gate result

```text
65-V controller class: PRELIMINARY ACCEPTED
60-V MOSFET class: PRELIMINARY ACCEPTED
SMCJ18A-class TVS: PRELIMINARY ACCEPTED
40-V MOSFET class: REJECTED UNTIL MEASURED REVIEW
sustained overvoltage protection: UPSTREAM ACTION REQUIRED
transient measurement: OPEN
final TVS part number: OPEN
```
