# Предварительный расчёт токов ветвей PCB-D и PCB-E — PlataVM V1.9

Дата: 2026-07-21  
Статус: `PRELIMINARY CALCULATION — COMPONENT EFFICIENCY NOT SELECTED`

## 1. Назначение

Документ проверяет предварительные классы силовых соединений:

```text
PACK_BUS_P5_IN → PCB-D
PACK_BUS_LIGHT_IN → PCB-E
```

Расчёт не выбирает разъёмы, провод, MOSFET, дроссели или драйверы. Он задаёт минимальный диапазон, который должен выдерживать дальнейший candidate selection.

## 2. Исходные данные

### 2.1 PACK_BUS

```text
V_IN_MIN = 9,2 В preliminary
V_IN_NOM = 12,8 В
V_IN_MAX = 14,6 В preliminary
```

### 2.2 PCB-D

```text
5V_SYS_BUS continuous = 5 В × 15 А = 75 Вт
5V_SYS_BUS short = 5 В × 20 А = 100 Вт
```

### 2.3 PCB-E

Существующая оценка максимальной суммарной световой мощности:

```text
P_LIGHT_OUT ≈ 180 Вт
```

### 2.4 Эффективность

До выбора topology/components проверяется диапазон:

```text
η = 88 %, 90 %, 92 %
```

Формула:

```text
I_IN = P_OUT / (V_IN × η)
```

## 3. PCB-D continuous input current

Для `P_OUT = 75 Вт`:

| V_IN | η=88 % | η=90 % | η=92 % |
|---:|---:|---:|---:|
| 9,2 В | 9,26 А | 9,06 А | 8,86 А |
| 12,8 В | 6,66 А | 6,51 А | 6,37 А |
| 14,6 В | 5,84 А | 5,71 А | 5,58 А |

Худшая проверенная точка:

```text
I_P5_CONT_PRECALC = 9,26 А
```

С учётом:

- допуска датчика;
- пульсаций input current;
- деградации эффективности при +60 °C;
- старения;
- токового запаса разъёма;
- переходного режима;

принимается предварительный continuous design current:

```text
I_P5_CONNECTOR_CONT_DESIGN = 12 А minimum
recommended connector/wire class = 15 А continuous
```

## 4. PCB-D short input current

Для `P_OUT = 100 Вт`:

| V_IN | η=88 % | η=90 % | η=92 % |
|---:|---:|---:|---:|
| 9,2 В | 12,35 А | 12,08 А | 11,81 А |
| 12,8 В | 8,88 А | 8,68 А | 8,49 А |
| 14,6 В | 7,78 А | 7,61 А | 7,45 А |

Худшая проверенная точка:

```text
I_P5_SHORT_PRECALC = 12,35 А
```

Предварительное требование:

```text
I_P5_CONNECTOR_SHORT_DESIGN ≥15 А
T_SHORT = 1 с preliminary
```

Это согласуется с предварительным классом `≥15 А`, но окончательное решение требует:

1. efficiency map выбранного DC/DC;
2. input-current ripple;
3. capacitor RMS current;
4. wire/contact temperature rise;
5. sealed-volume test at +60 °C.

## 5. PCB-E input current при 180 Вт

| V_IN | η=88 % | η=90 % | η=92 % |
|---:|---:|---:|---:|
| 9,2 В | 22,23 А | 21,74 А | 21,27 А |
| 12,8 В | 15,98 А | 15,63 А | 15,29 А |
| 14,6 В | 14,01 А | 13,70 А | 13,40 А |

Худшая проверенная точка:

```text
I_LIGHT_PRECALC = 22,23 А
```

С учётом токового запаса принимается предварительный design class:

```text
I_LIGHT_CONNECTOR_CONT_DESIGN = 25 А
```

Это не означает, что 180 Вт всегда разрешены в `SINGLE_PACK_MODE`.

При одной АКБ:

```text
system continuous limit = 20 А
```

Поэтому при низком PACK_BUS полная световая мощность 180 Вт может исчерпать либо превысить весь однобатарейный continuous budget ещё до учёта PCB-B и других нагрузок.

Software admission control должен использовать фактический ток и load profile; hardware connector PCB-E при этом рассчитывается на локальный потенциальный максимум ветви.

## 6. Проверка потерь

### 6.1 PCB-D

При 75 Вт output:

| η | Потери |
|---:|---:|
| 88 % | 10,23 Вт |
| 90 % | 8,33 Вт |
| 92 % | 6,52 Вт |

При 100 Вт output:

| η | Потери |
|---:|---:|
| 88 % | 13,64 Вт |
| 90 % | 11,11 Вт |
| 92 % | 8,70 Вт |

Для герметичного объёма без thermal contact с корпусом даже 6,5…10,2 Вт continuous на PCB-D являются существенной тепловой нагрузкой.

Целевое требование для candidate search:

```text
η_PCB_D_TARGET ≥92 % near 75 Вт
```

Но значение не считается подтверждённым до расчёта и испытания.

### 6.2 PCB-E

При 180 Вт output:

| η | Потери |
|---:|---:|
| 88 % | 24,55 Вт |
| 90 % | 20,00 Вт |
| 92 % | 15,65 Вт |

Такие потери могут быть несовместимы с внутренней естественной конвекцией при +60 °C.

Следовательно, для PCB-E необходимо:

1. уточнить, является ли 180 Вт электрической input power существующей нагрузки или optical/LED output estimate;
2. определить driver topology;
3. получить actual LED voltage/current per channel;
4. рассчитать потери каждого канала;
5. проверить simultaneous operation;
6. при необходимости снизить continuous lighting power или увеличить эффективность/площадь.

До этого `25 А branch class` сохраняется как electrical connector boundary, но thermal compliance не подтверждена.

## 7. Влияние на system budget

### DUAL_PACK_RUN

```text
continuous limit = 40 А
```

При 9,2 В и η=88 %:

```text
PCB-D continuous ≈9,26 А
PCB-E 180 Вт ≈22,23 А
sum ≈31,49 А
```

Остаётся около:

```text
40 − 31,49 = 8,51 А
```

для PCB-B, PCB-C и потерь других ветвей.

### SINGLE_PACK_MODE

```text
continuous limit = 20 А
```

Одна только PCB-E при 180 Вт в худшей точке требует около 22,23 А. Поэтому полная световая мощность при низком напряжении не проходит однобатарейный continuous budget.

Это не вводит отдельный brightness limit автоматически, но normal admission control не должен разрешать новую команду, которая превышает измеренный общий бюджет.

## 8. Принятые предварительные классы

| Ветвь | Continuous design class | Short design class | Статус |
|---|---:|---:|---|
| PACK_BUS_P5_IN | 12 А calculated; 15 А connector class | ≥15 А /1 с | PRELIMINARY ACCEPTED |
| PACK_BUS_LIGHT_IN | 25 А connector class | определяется driver/inrush profile | PRELIMINARY ACCEPTED |

## 9. Открытые данные

| ID | Данные |
|---|---|
| Q-PWR-002A | efficiency map PCB-D vs VIN/load/T |
| Q-PWR-002B | input ripple and capacitor RMS PCB-D |
| Q-PWR-003A | actual LED voltage/current and meaning of 180 Вт |
| Q-PWR-003B | efficiency/loss map each PCB-E channel |
| Q-THERM-001 | sealed-volume loss budget at +60 °C |
| Q-THERM-002 | confirm ratings or derating by test |

## 10. Результат

```text
Q-PWR-002 = CLOSED_PRELIMINARY_CONNECTOR_CURRENT_CLASS
Q-PWR-003 = CLOSED_PRELIMINARY_CONNECTOR_CURRENT_CLASS
```

Финальный connector part number и continuous system permission остаются открытыми.
