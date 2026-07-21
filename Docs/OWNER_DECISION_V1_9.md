# Решение владельца PlataVM V1.9

Дата: 2026-07-21  
Вопрос: `Q-SYS-007`  
Статус: `ACCEPTED`

## Решение

Владелец выбрал:

```text
Вариант B — защищённый SERVICE_OVERRIDE
```

## Каноническое значение

```text
SERVICE_OVERRIDE = GUARDED SERVICE FUNCTION
```

Основные ограничения:

1. только SERVICE_MODE;
2. сервисная авторизация;
3. двойное подтверждение;
4. один выбранный внешний некритический output;
5. одноразовое окно 60 с;
6. output автоматически отключается не позднее 60 с;
7. превышение continuous budget не более 1 с;
8. short limits 44/22 А не изменяются;
9. hardware protection, SAFE/HARD_OFF и EXT_KILL не обходятся;
10. полное журналирование;
11. reset, communication loss, mode/battery-state change или fault отменяют override.

Подробности:

```text
Docs/SERVICE_OVERRIDE_POLICY.md
Docs/SYSTEM_POWER_BUDGET_POLICY.md
Docs/adr/ADR-2026-07-21-service-override-v1-9.md
```
