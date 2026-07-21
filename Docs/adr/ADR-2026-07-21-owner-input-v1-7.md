# ADR-2026-07-21: применение ответов владельца V1.7

Дата: 2026-07-21  
Статус: `ACCEPTED WITH OPEN IMPLEMENTATION AND MECHANICAL ITEMS`

## Контекст

После review V1.6 оставались owner-level вопросы по:

- проверке KiCad workspace;
- условиям эксплуатации;
- механическому envelope;
- общему power budget;
- `SINGLE_PACK_MODE`;
- поведению при прогнозируемой перегрузке.

Владелец заполнил форму V1.7 и подтвердил либо уточнил все шесть пунктов.

## Решение

### 1. KiCad workspace

Владелец подтвердил, что текущий проект и листы открываются нормально. Q-SCH-004 закрывается как owner verification. Перед schematic freeze остаётся обязательным ERC на конкретном release commit.

### 2. Условия эксплуатации

Приняты:

```text
work: −20…+60 °C
storage: −30…+70 °C
high humidity
possible condensation
conformal coating required
K_BAT mechanical life ≥100 000 cycles
K_BAT electrical life ≥10 000 operations
```

Вибрационный профиль остаётся отдельным открытым входом.

### 3. Корпус

Принят внешний envelope:

```text
cylinder Ø130 mm × 1000 mm
one welded end
one removable connector lid
service access from lid side
```

Предварительная архитектура внутренней механики — продольный извлекаемый carrier/tray. Внутренний диаметр, материал, давление, карта разъёмов, крепления и thermal interfaces остаются открытыми.

### 4. Системный power budget

Приняты стартовые ограничения по PACK_BUS:

```text
DUAL_PACK_RUN: 40 A continuous / 44 A short
SINGLE_PACK_MODE: 20 A continuous / 22 A short
```

Это эксплуатационные системные пределы. Локальные hardware ratings плат остаются отдельными.

### 5. SINGLE_PACK_MODE

Режим:

- деградированный, но функциональный;
- не выключает нагрузки автоматически при входе;
- не вводит отдельный brightness limit;
- запрещает DECK_BALANCE;
- не допускает автоматическое повторное подключение восстановившейся батареи;
- использует общий бюджет 20/22 А.

### 6. Admission control нагрузки

Принято:

```text
85 % continuous budget → warning
100 % continuous budget → reject new noncritical load command
```

Уже включённые нагрузки обычным программным power manager не сбрасываются. Аппаратные защиты, SAFE/HARD_OFF и EXT_KILL действуют независимо.

Service override допускается только в диагностическом режиме с журналированием и не отменяет аппаратную безопасность.

## Согласование решений

Указание «ничего автоматически запрещать не нужно» относится к самому входу в `SINGLE_PACK_MODE`: функции не выключаются и не блокируются по категории.

Указание о запрете новой некритической нагрузки при 100 % относится к command admission после исчерпания активного измеренного бюджета. Поэтому решения совместимы.

## Последствия

Положительные:

1. закрыт owner-level global power budget;
2. определено поведение SINGLE_PACK_MODE;
3. определены GUI warning и command block thresholds;
4. KiCad verification больше не является текущим owner blocker;
5. появился подтверждённый внешний механический envelope;
6. можно переходить к physical packaging inputs, pin count и subsystem calculations.

Ограничения:

1. short-limit duration и фильтрация не определены;
2. отсутствует окончательная классификация внешних critical loads;
3. нет внутренних размеров и pressure/vibration данных корпуса;
4. BMS и K_BATx требуют испытаний;
5. physical connector selection пока запрещён.

## Неизменяемые решения

Настоящий ADR не изменяет:

- отсутствие `K_MAIN`;
- главную шину `PACK_BUS`;
- параллельную работу двух исправных АКБ;
- запрет автоматического restart после BMS recovery;
- независимость EXT_KILL от firmware/RS-485/CAN-FD;
- отсутствие активной дополнительной электроники в основных АКБ;
- разделение `5V_SYS_BUS` и `5V_CRIT/3V3_CRIT`;
- пассивный INTERCONNECT;
- отдельные `POWER_GND`, `SIGNAL_GND`, `ISO_GND`, `CHASSIS`.

## Связанные документы

```text
Docs/OWNER_ANSWERS_REVIEW_V1_7.md
Docs/SYSTEM_POWER_BUDGET_POLICY.md
Docs/MECHANICAL_ENVELOPE_V1_7.md
Docs/OPEN_QUESTIONS.md
Docs/ARCHITECTURE_BASELINE.md
```
