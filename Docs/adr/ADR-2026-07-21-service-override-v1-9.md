# ADR-2026-07-21: защищённый SERVICE_OVERRIDE и переход к packaging V1.9

Дата: 2026-07-21  
Статус: `ACCEPTED`

## Контекст

В форме V1.8 владелец запросил подробное объяснение `SERVICE_OVERRIDE`. После объяснения выбрана политика B: защищённый сервисный режим.

Одновременно owner-defined mechanical envelope уже позволяет начать предварительный floorplanning PCB-A…PCB-E:

```text
assembly ≤100 × 250 × 80 мм
multi-level
вся сборка извлекается вместе с крышкой
thermal contact с корпусом отсутствует
```

## Решение по SERVICE_OVERRIDE

Принять guarded service function:

1. доступ только из `SERVICE_MODE`;
2. авторизация сервисного уровня;
3. двойное подтверждение;
4. одна выбранная внешняя некритическая нагрузка;
5. одноразовое окно разрешения 60 с;
6. активный overridden output автоматически отключается не позднее 60 с;
7. превышение continuous budget разрешается только в рамках существующего short limit ≤1 с;
8. predicted current выше short limit блокируется;
9. режим не отменяет BMS, fuse, eFuse, thermal protection, SAFE/HARD_OFF или EXT_KILL;
10. все действия и результаты журналируются;
11. после reset/communication loss/mode change override возвращается в disabled.

Q-SYS-007 закрывается:

```text
CLOSED_OWNER_DECISION
```

## Решение по packaging

Принять предварительный кандидат `PACKAGING-P1`:

```text
L0: PCB-A + PCB-C
L1: PCB-D + PCB-E
L2: PCB-B
```

Ввести целевую внутреннюю ширину плат 94 мм при абсолютном ограничении 100 мм.

Ввести предварительные area budgets:

```text
PCB-A 94×110 мм
PCB-B 94×180 мм
PCB-C 94×130 мм
PCB-D 94×125 мм
PCB-E 94×110 мм
```

Размеры не замораживаются до component-height и thermal audit.

Mounting holes остаются `MOUNT_HOLE_TBD` до выбора владельцем винтов и стоек.

## Последствия

Положительные:

- завершён owner-level блок Q-SYS-007;
- service diagnostics не требует hardware bypass path;
- software budget нельзя обходить из обычного режима;
- short policy остаётся неизменной;
- появилась проверяемая геометрическая гипотеза для пяти плат;
- можно переходить к physical pin count и connector classes.

Ограничения:

- конкретная авторизация service level не выбрана;
- firmware ещё не реализована;
- размеры плат предварительные;
- высоты магнитных компонентов не подтверждены;
- thermal compliance при +60 °C не доказана;
- mounting-hole drill и coordinates не определены;
- connector families не выбраны.

## Неизменяемые решения

ADR не изменяет:

- отсутствие K_MAIN;
- PACK_BUS;
- BFE_1/BFE_2;
- K_BATx и no-restart после BMS recovery;
- независимый EXT_KILL;
- direct hardware safety lines;
- внешний isolated RS-485;
- внутренний CAN-FD;
- passive INTERCONNECT;
- ground-domain policy;
- запрет thermal contact с корпусом.

## Связанные документы

```text
Docs/SERVICE_OVERRIDE_POLICY.md
Docs/PCB_PACKAGING_BOUNDARY_V1_9.md
Docs/PCB_MODULE_AREA_BUDGET_V1_9.md
Docs/SYSTEM_POWER_BUDGET_POLICY.md
Docs/OPEN_QUESTIONS.md
```
