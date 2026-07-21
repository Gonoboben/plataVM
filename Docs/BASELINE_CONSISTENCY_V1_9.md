# Проверка связности архитектурной базы PlataVM V1.9

Дата: 2026-07-21  
Статус: `PASS WITH CONTROLLED OPEN CALCULATIONS`

## 1. Проверенные нормативные документы

```text
README.md
Docs/PROJECT_MASTER.md
Docs/ARCHITECTURE_BASELINE.md
Docs/SYSTEM_POWER_BUDGET_POLICY.md
Docs/SERVICE_OVERRIDE_POLICY.md
Docs/MECHANICAL_ENVELOPE_V1_8.md
Docs/PCB_PACKAGING_BOUNDARY_V1_9.md
Docs/PCB_MODULE_AREA_BUDGET_V1_9.md
Docs/PHYSICAL_INTERFACE_COUNT_V1_9.md
Docs/BRANCH_CURRENT_PRECALC_V1_9.md
Docs/OPEN_QUESTIONS.md
Docs/adr/ADR-2026-07-21-service-override-v1-9.md
Docs/chronology/2026-07-21-service-override-v1-9.md
```

Документы `OWNER_ANSWERS_REVIEW_V1_8.md` и ADR V1.8 сохраняются как исторические источники. Их прежняя отметка `SERVICE_OVERRIDE disabled pending decision` не является действующей политикой после ADR V1.9.

## 2. SERVICE_OVERRIDE

Проверены одинаковые значения:

```text
SERVICE_MODE required
service authorization required
double confirmation required
one noncritical output only
authorization lease = 60 с
output lease ≤60 с
over-continuous interval ≤1 с
short limits unchanged: 44 А / 22 А
full logging
reset/communication loss/mode change/fault cancels override
```

Проверено:

- override не применяется к K_BAT, MAIN_SW, BALANCE_SW, PACK_BUS_DISCHARGE, critical rails, REMOTE_OFF, SAFE/HARD_OFF, EXT_KILL или DECK_BALANCE;
- predicted current выше short limit блокируется;
- аппаратные защиты имеют приоритет;
- после reset/power cycle override disabled;
- отключение overridden output не превращено в общий load shedding остальных нагрузок.

Результат: `PASS`.

## 3. Power-budget policy

| Режим | Continuous | Short | Duration | Warning |
|---|---:|---:|---:|---:|
| DUAL_PACK_RUN | 40 А | 44 А | ≤1 с | 34 А |
| SINGLE_PACK_MODE | 20 А | 22 А | ≤1 с | 17 А |

Проверены:

```text
short cooldown ≥10 с
I²t / thermal accumulator
low-pass 100 мс
warning ON >85 % /250 мс
warning OFF <80 % /2 с
block new noncritical at predicted ≥100 %
re-enable below 90 % /2 с
```

Результат: `PASS`.

## 4. Packaging boundary

Проверенная конфигурация:

```text
PACKAGING-P1
L0: PCB-A 110 мм + PCB-C 130 мм = 240 мм
L1: PCB-D 125 мм + PCB-E 110 мм = 235 мм
L2: PCB-B 180 мм
```

Проверка envelope:

```text
width target 94 мм ≤ absolute 100 мм
L0 240 мм <250 мм
L1 235 мм <250 мм
L2 180 мм <250 мм
height budget 79 мм <80 мм
```

Остаточный вертикальный резерв составляет только 1 мм. Поэтому конфигурация считается геометрически допустимой, но не замороженной до component-height и 3D clearance audit.

Результат: `PASS PRELIMINARY`.

## 5. Mounting policy

Проверено:

```text
MOUNT_HOLE_TBD
NO FINAL DRILL
MECHANICAL KEEPOUT ONLY
```

- не менее четырёх mounting zones на плату;
- tool access обязателен;
- тяжёлые компоненты имеют дополнительные опоры;
- винты/стойки owner-selected;
- hot-melt adhesive только auxiliary.

Результат: `PASS`.

## 6. Physical interface count

### A↔B direct signal class

```text
7 normal control
+3 hardware safety
+10 diagnostics
+4 references
+1 optional shield
+7 reserve
=32 positions
```

Исправлена прежняя арифметическая ошибка `+6 reserve =31`.

Проверка резерва:

```text
used =25
reserve =7
7/32 =21,875 % ≈21,9 %
```

Target 20…30 % выполнен.

### B↔C/D/E

```text
8 positions each
```

- B↔C used 6, reserve 2 =25 %;
- B↔D used 6, reserve 2 =25 %;
- B↔E used 5, reserve 3 =37,5 %; увеличение принято ради унификации.

Результат: `PASS`.

## 7. Power branch classes

| Ветвь | Предварительный класс | Основание |
|---|---:|---|
| A→C | 30 А | PCB-C hardware rating |
| A→D | 15 А | 12,35 А worst checked short input + margin |
| A→E | 25 А | 22,23 А worst checked continuous input + margin |

Значения A→D/A→E являются connector-current boundaries, а не подтверждением thermal compliance или разрешённого системного режима.

Результат: `PASS PRELIMINARY`.

## 8. Thermal consistency

Принято во всех действующих документах:

```text
thermal contact с корпусом запрещён
internal ambient test = +60 °C
cooling by low-loss design, PCB copper/local internal heatsink and natural convection
```

Предварительные потери:

```text
PCB-D at 75 Вт output: 6,52…10,23 Вт
PCB-E at 180 Вт output: 15,65…24,55 Вт
```

PCB-E thermal compliance не доказана. Это явно сохранено как Q-THERM-001/Q-THERM-002 и не скрыто утверждением connector class.

Результат: `OPEN CONTROLLED BLOCKER`.

## 9. Frozen architecture check

| Ограничение | Результат |
|---|---|
| K_MAIN отсутствует | PASS |
| PACK_BUS остаётся главной шиной | PASS |
| High current не проходит через PCB-B | PASS |
| EXT_KILL независим от firmware/RS-485/CAN-FD | PASS |
| No automatic restart after BMS recovery | PASS |
| Main battery housings без дополнительной active electronics | PASS |
| INTERCONNECT пассивный | PASS |
| 5V_SYS_BUS отделён от 5V_CRIT/3V3_CRIT | PASS |
| EMG не питает user power loads | PASS |
| CAN-FD не заменяет direct safety lines | PASS |
| Ground domains не объединены произвольно | PASS |
| Thermal contact с корпусом не добавлен | PASS |
| SERVICE_OVERRIDE не создаёт hardware bypass | PASS |

## 10. Не выполнено намеренно

На этапе V1.9 не выполнялись:

1. выбор конкретных connector families;
2. final pinout;
3. final PCB outlines;
4. final mounting-hole drill/coordinates;
5. part-number selection;
6. footprints;
7. PCB layout;
8. CAN-FD termination placement;
9. detailed thermal simulation;
10. KiCad ERC release check.

## 11. Заключение

```text
Architecture continuity: PASS
Service policy consistency: PASS
Packaging arithmetic: PASS PRELIMINARY
Interface arithmetic: PASS AFTER CORRECTION
Power branch precalc: PASS PRELIMINARY
Thermal compliance: OPEN CONTROLLED BLOCKER
```

Ветка пригодна для демонстрации как инженерная фиксация V1.9 и для перехода к preliminary KiCad mechanical outlines, connector class comparison и detailed thermal/current calculations.
