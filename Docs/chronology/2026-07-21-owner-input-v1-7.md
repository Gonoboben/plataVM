# Хронология: применение ответов владельца V1.7

Дата: 2026-07-21  
Предыдущая опорная точка: merge PR #35, KiCad interfaces aligned with V1.6  
Источник: `Ответы_на_вопросы_ПДУ_БНПА_V1.7(1).docx`

## 1. Полученные ответы

Владелец ответил на:

```text
Q-SCH-004
Q-KBAT-019
Q-MECH-004
Q-SYS-001
Q-SYS-002
Q-SYS-003
```

## 2. Принятые решения

1. Текущий root KiCad project и листы 00…56 открываются нормально по проверке владельца.
2. Рабочая температура: −20…+60 °C.
3. Хранение: −30…+70 °C.
4. Высокая влажность и возможная конденсация учитываются.
5. Conformal coating PCB обязателен.
6. Требуемый механический ресурс K_BATx ≥100 000 циклов.
7. Требуемый электрический ресурс K_BATx ≥10 000 операций.
8. Корпус электроники — цилиндр Ø130 мм × 1000 мм.
9. Один торец корпуса заварен.
10. Второй торец — съёмная крышка с разъёмами.
11. Сервисный доступ и извлечение электроники выполняются со стороны крышки.
12. DUAL_PACK_RUN: 40 А continuous / 44 А short по PACK_BUS.
13. SINGLE_PACK_MODE: 20 А continuous / 22 А short по PACK_BUS.
14. SINGLE_PACK_MODE — деградированный, но функциональный.
15. Вход в SINGLE_PACK_MODE не выключает нагрузки автоматически.
16. Отдельный automatic brightness limit не вводится.
17. При 85 % active continuous budget отображается warning.
18. При 100 % active continuous budget отклоняется новая некритическая команда.
19. Уже включённые пользовательские нагрузки software budget manager не сбрасывает.
20. Service override разрешён только в диагностическом режиме с журналированием.

## 3. Инженерное согласование

Ответ «ничего автоматически запрещать не нужно» согласован с запретом новой некритической нагрузки при 100 % следующим образом:

```text
вход в SINGLE_PACK_MODE
→ не отключает и не блокирует функции по категории
→ active budget становится 20/22 А
→ warning at 17 А
→ новая некритическая команда отклоняется после исчерпания continuous budget
→ уже включённые нагрузки продолжают работу до аппаратной защиты/SAFE/HARD_OFF/EXT_KILL
```

## 4. Архитектура не изменена

Сохранены:

- отсутствие K_MAIN;
- PACK_BUS как единственная главная силовая шина;
- высокие токи вне PCB-B;
- независимый EXT_KILL;
- отсутствие дополнительной активной электроники в основных АКБ;
- внешний isolated RS-485;
- внутренний CAN-FD с direct safety/fault lines;
- раздельные POWER_GND, SIGNAL_GND, ISO_GND, CHASSIS;
- пассивный INTERCONNECT;
- запрет автоматического restart после BMS recovery.

## 5. Новые нормативные документы

```text
Docs/OWNER_ANSWERS_REVIEW_V1_7.md
Docs/SYSTEM_POWER_BUDGET_POLICY.md
Docs/MECHANICAL_ENVELOPE_V1_7.md
Docs/adr/ADR-2026-07-21-owner-input-v1-7.md
```

Обновлены:

```text
Docs/PROJECT_MASTER.md
Docs/ARCHITECTURE_BASELINE.md
Docs/OPEN_QUESTIONS.md
README.md
```

## 6. Закрытые блокеры

- owner verification текущего KiCad workspace;
- owner-level global power budget;
- SINGLE_PACK_MODE policy;
- warning/block command policy;
- environmental baseline;
- external cylindrical envelope.

## 7. Следующая последовательность

```text
internal cylinder dimensions and pressure/vibration data
→ connector-lid map
→ removable carrier/tray concept
→ physical CAN-FD/hard-line/power pin count
→ connector selection
→ short-limit/filter/load-profile closure
→ K_BATx/REMOTE_OFF candidate calculations and tests
→ subsystem component selection
```
