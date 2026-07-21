# Хронология: SERVICE_OVERRIDE вариант B и packaging boundary V1.9

Дата: 2026-07-21  
Предыдущая контрольная точка: merge PR #37, ответы V1.8 применены

## 1. Решение владельца

Владелец выбрал:

```text
Q-SYS-007
Вариант B — защищённый SERVICE_OVERRIDE
```

## 2. Зафиксированная политика

1. Только SERVICE_MODE.
2. Авторизация сервисного уровня.
3. Двойное подтверждение.
4. Одна выбранная внешняя некритическая нагрузка.
5. Одноразовое окно разрешения 60 с.
6. Активная diagnostic command автоматически завершается не позднее 60 с.
7. Continuous-budget bypass не изменяет 44/22 А short limit ≤1 с.
8. Predicted short-limit exceed блокируется.
9. Аппаратные защиты, SAFE/HARD_OFF и EXT_KILL не обходятся.
10. Полное журналирование.
11. Reset, communication loss, mode change или fault отменяют override.

## 3. Архитектурное уточнение

60 с является максимальной service lease, а не разрешением держать PACK_BUS выше continuous limit 60 с.

```text
over-continuous interval ≤1 с
service output lease ≤60 с
```

Если после 1 с ток остаётся выше continuous limit, отключается только выбранный overridden output.

## 4. Предварительная компоновка

Создан candidate:

```text
PACKAGING-P1
L0: PCB-A + PCB-C
L1: PCB-D + PCB-E
L2: PCB-B
```

Предварительные размеры:

```text
PCB-A 94×110 мм
PCB-B 94×180 мм
PCB-C 94×130 мм
PCB-D 94×125 мм
PCB-E 94×110 мм
```

Проверено:

```text
L0 length 240 мм < 250 мм
L1 length 235 мм < 250 мм
L2 length 180 мм < 250 мм
height budget 79 мм < 80 мм
```

## 5. Physical interface count

Подготовлены предварительные logical classes:

```text
A↔B critical power: 2 poles
A↔B control/diagnostics: 32 positions target
B↔C signals: 8 positions
B↔D signals: 8 positions
B↔E signals: 8 positions
PCB-B service/debug: 10 positions
```

Power classes:

```text
A→C: 30 А class
A→D: 15 А class preliminary
A→E: 25 А class preliminary
```

Конкретные connector families не выбраны.

## 6. Предварительный расчёт PCB-D/PCB-E

При минимальном input 9,2 В и η=88 %:

```text
PCB-D 75 Вт output → 9,26 А input
PCB-D 100 Вт short → 12,35 А input
PCB-E 180 Вт output → 22,23 А input
```

Приняты предварительные классы:

```text
PACK_BUS_P5_IN: 15 А
PACK_BUS_LIGHT_IN: 25 А
```

Тепловые потери:

```text
PCB-D at 75 Вт: 6,52…10,23 Вт при η=92…88 %
PCB-E at 180 Вт: 15,65…24,55 Вт при η=92…88 %
```

PCB-E thermal compliance без контакта с корпусом не доказана и остаётся обязательным расчётно-испытательным пунктом.

## 7. Добавленные документы

```text
Docs/SERVICE_OVERRIDE_POLICY.md
Docs/PCB_PACKAGING_BOUNDARY_V1_9.md
Docs/PCB_MODULE_AREA_BUDGET_V1_9.md
Docs/PHYSICAL_INTERFACE_COUNT_V1_9.md
Docs/BRANCH_CURRENT_PRECALC_V1_9.md
Docs/adr/ADR-2026-07-21-service-override-v1-9.md
```

## 8. Следующий инженерный шаг

```text
preliminary KiCad board outlines
→ MOUNT_HOLE_TBD zones
→ component-height/3D audit
→ A↔B connector 32 vs 16+16 decision
→ CAN-FD node order/termination
→ PCB-B critical branch current
→ connector class comparison
→ detailed thermal-loss calculations
```
