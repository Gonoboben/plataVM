# Physical interface count — PlataVM V1.9

Дата: 2026-07-21  
Основание: V1.6 interface architecture, V1.8 envelope, V1.9 packaging boundary  
Статус: `PRELIMINARY LOGICAL CONTACT COUNT — CONNECTOR FAMILY NOT SELECTED`

## 1. Назначение

Документ определяет количество электрических функций и требуемых позиций для межплатных соединений до выбора connector family.

Разделяются:

```text
logical net count — число электрических функций
connector position count — logical nets + returns + reserve
power pole count — определяется током и технологией соединения
```

Высокотоковые ветви не проходят через PCB-B и не объединяются с signal connectors.

## 2. Принцип разделения

Используются отдельные группы:

1. A↔B critical power;
2. A↔B direct control/diagnostics;
3. A↔C/D/E high-current branch power;
4. B↔C/D/E CAN-FD + hardware safety/fault;
5. external isolated RS-485;
6. EXT_KILL;
7. service/debug;
8. external load outputs.

Signal reserve target:

```text
20…30 %
```

Power contacts не считаются резервом сигнального разъёма.

## 3. PCB-A ↔ PCB-B critical power

### 3.1 Логические poles

| Функция | Количество |
|---|---:|
| PACK_BUS_CRIT_IN | 1 |
| POWER_GND return | 1 |

```text
logical power poles = 2
```

Физическое количество параллельных контактов определяется после расчёта тока PCB-B critical domain и рейтинга выбранного connector family.

### 3.2 Требование

- отдельный power connector или отдельные силовые контакты;
- не объединять с analog sensing;
- polarity/keying обязательны;
- ветвь остаётся current-limited на PCB-A.

## 4. PCB-A ↔ PCB-B direct control and diagnostics

### 4.1 Команды PCB-B → PCB-A

| Сигнал | Количество |
|---|---:|
| BAT1_MAIN_SW_EN | 1 |
| BAT2_MAIN_SW_EN | 1 |
| BAT1_BALANCE_SW_EN | 1 |
| BAT2_BALANCE_SW_EN | 1 |
| BAT1_HOLD_LOOP_OPEN_CMD | 1 |
| BAT2_HOLD_LOOP_OPEN_CMD | 1 |
| PACK_BUS_DISCHARGE_EN | 1 |

```text
normal control outputs = 7
```

### 4.2 Независимые hardware safety actions PCB-B → PCB-A

| Сигнал | Количество |
|---|---:|
| BAT1_HOLD_LOOP_OPEN_HW | 1 |
| BAT2_HOLD_LOOP_OPEN_HW | 1 |
| EXT_KILL_HW_CHAIN / ASSERT | 1 |

```text
hardware safety outputs = 3
```

### 4.3 Диагностика PCB-A → PCB-B

| Сигнал | Тип | Количество |
|---|---|---:|
| BAT1_PRESENT | digital | 1 |
| BAT2_PRESENT | digital | 1 |
| BAT1_VSENSE | analog | 1 |
| BAT2_VSENSE | analog | 1 |
| BAT1_ISENSE | analog | 1 |
| BAT2_ISENSE | analog | 1 |
| PACK_BUS_VSENSE | analog | 1 |
| BFE_FAULT_SUMMARY_N | digital | 1 |
| BAT1_HOLD_LOOP_STATUS | digital | 1 |
| BAT2_HOLD_LOOP_STATUS | digital | 1 |

```text
diagnostic inputs = 10
```

### 4.4 References and reserve

| Позиция | Количество |
|---|---:|
| SIGNAL_GND / digital return | 2 |
| ANALOG_REF_GND / Kelvin reference | 2 |
| CHASSIS/shield drain, optional | 1 |
| Reserved signals | 7 |

### 4.5 Итог

```text
7 normal control
+3 hardware safety
+10 diagnostics
+4 references
+1 optional shield
+7 reserve
=32 positions
```

Рекомендуемый connector class для сравнения:

```text
32-position signal connector
```

Это не выбор конкретного разъёма и не финальный pinout.

Допускается разделение на два connector classes:

```text
AB-CTRL: 16 positions
AB-DIAG: 16 positions
```

Разделение предпочтительно, если analog integrity и монтаж улучшаются.

## 5. PCB-B ↔ PCB-C/D/E standard signal interface

Для унификации вводится предварительный 8-position logical class.

### 5.1 Общая карта функций

| Position class | PCB-C | PCB-D | PCB-E |
|---|---|---|---|
| 1 | CAN_INT_H | CAN_INT_H | CAN_INT_H |
| 2 | CAN_INT_L | CAN_INT_L | CAN_INT_L |
| 3 | CAN_REF_GND | CAN_REF_GND | CAN_REF_GND |
| 4 | P12_GROUP_SAFE_OFF | P5_GROUP_SAFE_OFF | RESERVED / future LIGHT_SAFE_OFF |
| 5 | P12_GROUP_HARD_OFF | P5_GROUP_HARD_OFF | LIGHT_GROUP_HARD_OFF |
| 6 | P12_BOARD_FAULT_N | P5_BOARD_FAULT_N | LIGHT_BOARD_FAULT_N |
| 7 | RESERVE_1 | RESERVE_1 | RESERVE_1 |
| 8 | RESERVE_2 | RESERVE_2 | RESERVE_2 |

### 5.2 Итог

```text
J_BC_SIG = 8 positions
J_BD_SIG = 8 positions
J_BE_SIG = 8 positions
```

Преимущества:

- единый signal connector class для PCB-C/D/E;
- одинаковое keying/pin numbering;
- 25…37 % reserve в зависимости от платы;
- отдельный hardware OFF сохраняется;
- CAN-FD не становится единственным safety path.

Окончательное назначение position 4 PCB-E остаётся reserve, если LIGHT_SAFE_OFF не потребуется.

## 6. PCB-A → PCB-C power branch

| Функция | Logical poles |
|---|---:|
| PACK_BUS_P12_IN | 1 |
| POWER_GND | 1 |

```text
J_AC_PWR = 2 high-current poles
branch hardware rating = 30 А continuous
```

Физический connector/cable должен быть рассчитан на ток ветви, температуру и падение напряжения. Количество параллельных контактов определяется выбранной технологией.

## 7. PCB-A → PCB-D power branch

| Функция | Logical poles |
|---|---:|
| PACK_BUS_P5_IN | 1 |
| POWER_GND | 1 |

```text
J_AD_PWR = 2 power poles
```

Предварительный input-current design class:

```text
15 А continuous connector class
```

Основание:

```text
75 Вт output, 9,2 В input, η=88 % → 9,26 А
100 Вт short, 9,2 В input, η=88 % → 12,35 А
```

Окончательное значение требует efficiency/ripple/temperature-rise расчёта.

## 8. PCB-A → PCB-E power branch

| Функция | Logical poles |
|---|---:|
| PACK_BUS_LIGHT_IN | 1 |
| POWER_GND | 1 |

```text
J_AE_PWR = 2 high-current poles
```

Предварительный design class:

```text
25 А continuous connector class
```

Основание:

```text
180 Вт output, 9,2 В input, η=88 % → 22,23 А
```

Thermal compliance и actual LED load остаются открытыми.

## 9. External isolated RS-485

| Функция | Positions |
|---|---:|
| RS485_A_ISO | 1 |
| RS485_B_ISO | 1 |
| ISO_GND reference | 1 |
| CHASSIS / shield | 1 |
| RESERVE | 1 |

```text
external RS-485 class = 5 positions
```

Shield position электрически относится к CHASSIS и не объединяется с ISO_GND внутри cable connector без EMC decision.

## 10. EXT_KILL external interface

Базовый интерфейс — isolated/passive dry-contact loop.

| Функция | Positions |
|---|---:|
| EXT_KILL_LOOP_OUT | 1 |
| EXT_KILL_LOOP_RETURN | 1 |
| SHIELD/CHASSIS optional | 1 |

```text
EXT_KILL class = 2 required + 1 optional shield
```

EXT_KILL не разделяет connector с обычным RS-485 command channel, если это создаёт common failure or handling risk.

## 11. Service/debug interface PCB-B

Минимальный внутренний service class:

| Функция | Positions |
|---|---:|
| SWDIO | 1 |
| SWCLK | 1 |
| NRST | 1 |
| 3V3_CRIT reference | 1 |
| SIGNAL_GND | 2 |
| SWO / debug UART TX | 1 |
| debug UART RX | 1 |
| SERVICE_MODE detect / key | 1 |
| RESERVE | 1 |

```text
SERVICE_DEBUG class = 10 positions
```

`SERVICE_MODE detect/key` является логической возможностью. Конкретная реализация может быть firmware-authenticated без отдельного аппаратного контакта; тогда position остаётся reserve.

## 12. External 12 V load outputs

PCB-C имеет 14 независимых двухпроводных outputs.

```text
14 × (12V_OUT + POWER_GND_RETURN)
=28 logical load contacts
```

Разрешается группировать по connector modules, но каждый канал сохраняет индивидуальную защиту и диагностику.

Общий ground conductor не должен создавать недопустимое падение напряжения или потерю независимости диагностики.

## 13. External 5 V load outputs

PCB-D имеет 10 независимых двухпроводных outputs.

```text
10 × (5V_OUT + POWER_GND_RETURN)
=20 logical load contacts
```

Общий многоконтактный return допускается только после current-sharing и voltage-drop calculation.

## 14. External LED outputs

PCB-E имеет шесть независимых двухпроводных current-regulated outputs.

```text
6 × (LED+ + LED−)
=12 logical load contacts
```

LED− не объединяется произвольно с POWER_GND, если выбранная driver topology требует floating/current-regulated return.

## 15. EMG_4S2P external branch

Предварительный power interface:

| Функция | Logical poles |
|---|---:|
| EMG_BAT+ | 1 |
| EMG_BAT− | 1 |

Optional diagnostics:

| Функция | Positions |
|---|---:|
| EMG_PRESENT | 1 |
| EMG_TEMP / reserve | 1 |
| signal return | 1 |

До подтверждения внешней EMG assembly применяется:

```text
2 power poles + 3 optional signal positions
```

## 16. Сводная таблица внутренних интерфейсов

| Interface | Power poles | Signal positions | Статус |
|---|---:|---:|---|
| A↔B critical power | 2 | 0 | current rating TBD |
| A↔B control/diagnostics | 0 | 32 target | split 16+16 optional |
| A→C power | 2 high-current | 0 | 30 А class |
| B↔C signals | 0 | 8 | standardized |
| A→D power | 2 | 0 | 15 А preliminary |
| B↔D signals | 0 | 8 | standardized |
| A→E power | 2 high-current | 0 | 25 А preliminary |
| B↔E signals | 0 | 8 | standardized |
| PCB-B service/debug | 0 | 10 | internal/service |

## 17. Проверка резерва

| Signal group | Used | Total | Reserve |
|---|---:|---:|---:|
| A↔B control/diagnostics | 25 including refs/shield | 32 | 7 = 21,9 % |
| B↔C | 6 | 8 | 2 = 25 % |
| B↔D | 6 | 8 | 2 = 25 % |
| B↔E | 5 | 8 | 3 = 37,5 % |
| Service/debug | 8…9 | 10 | 10…20 % |

A↔B reserve удовлетворяет target 20…30 %. B↔E имеет увеличенный резерв, но сохраняется ради унификации.

## 18. Следующий Gate

Перед connector family selection требуется:

1. подтвердить максимальный ток PCB-B critical branch;
2. уточнить PCB-D efficiency/input ripple/temperature rise;
3. уточнить PCB-E actual load/efficiency/temperature rise;
4. решить, разделяется ли A↔B 32-position class на два 16-position connectors;
5. определить допустимую высоту mating pairs в 80 мм assembly;
6. определить требуемое число mating cycles;
7. проверить coating/marine compatibility;
8. определить wire gauge и strain relief;
9. построить physical node order CAN-FD;
10. выполнить preliminary 3D connector clearance review.

После этого разрешается comparison connector classes, но не финальный part-number freeze.
