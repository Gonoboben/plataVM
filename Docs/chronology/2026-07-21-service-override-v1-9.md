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

## 4. Переход к следующему этапу

Создан preliminary candidate:

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

## 5. Добавленные документы

```text
Docs/SERVICE_OVERRIDE_POLICY.md
Docs/PCB_PACKAGING_BOUNDARY_V1_9.md
Docs/PCB_MODULE_AREA_BUDGET_V1_9.md
Docs/adr/ADR-2026-07-21-service-override-v1-9.md
```

## 6. Следующий инженерный шаг

```text
physical interface count
→ connector classes
→ preliminary board outlines/mounting zones
→ thermal-loss budget PCB-D/PCB-E
→ component candidate search
```
