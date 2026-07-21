# ADR-2026-07-21: применение ответов владельца V1.8

Дата: 2026-07-21  
Статус: `ACCEPTED WITH Q-SYS-007 OPEN`

## Контекст

После V1.7 оставались вопросы по внутренней механике электронной сборки и реализации программного power-budget manager:

```text
Q-MECH-006…Q-MECH-010
Q-SYS-004…Q-SYS-007
```

Владелец заполнил форму V1.8. Восемь ответов принимаются как решения. По Q-SYS-007 запрошено подробное объяснение service override, поэтому этот пункт остаётся открытым.

## Решение

### 1. Внутренний и рабочий envelope

Владелец задаёт:

```text
доступный внутренний цилиндр: Ø130 мм × 1000 мм
рабочий envelope электронной сборки: 100 × 250 × 80 мм
компоновка: многоуровневая
```

Длина 250 мм — предварительная проектная граница.

### 2. Извлечение и крепление

Вся электроника извлекается вместе со съёмной крышкой.

Платы:

- крепятся винтами к стойкам;
- имеют монтажные отверстия и keepout;
- не требуют обязательного отдельного carrier/tray;
- не должны использовать пайку разъёмов как механическую опору.

Винты, стойки и механическая рама находятся в owner-controlled scope.

### 3. Корпус и давление

Pressure-hull design исключается из текущего scope электроники. Корпус принимается как owner-provided qualified enclosure.

Фиксируется инженерное замечание: герметичность не устраняет внешнее дифференциальное давление, поэтому прочность корпуса остаётся ответственностью владельца/изготовителя корпуса.

### 4. Вибрационная фиксация

Основные способы удержания — пайка и винтовое крепление.

Полиэтиленовый hot-melt adhesive разрешён только как вспомогательная anti-vibration/strain-relief фиксация. Он не должен быть единственной опорой тяжёлых компонентов, применяться у горячих деталей или нарушать creepage/clearance и ремонтопригодность.

### 5. Тепловая архитектура

Штатный тепловой контакт электронной сборки с корпусом запрещён.

Принято:

```text
cooling = low-loss design + PCB copper + internal natural convection
```

Thermal pads, heat spreader или carrier-to-hull heat path не применяются без нового решения владельца.

PCB-D и PCB-E должны проходить тепловую проверку в закрытом объёме при +60 °C без контакта с корпусом. Если температурный режим не выполняется, корректируются потери, компоненты, topology, площадь/число плат либо разрешённая continuous нагрузка.

Это решение отменяет прежнее предварительное утверждение о тепловом отводе PCB-D на корпус.

### 6. Short-limit timing

Принято:

```text
DUAL_PACK_RUN: 44 А ≤1 с
SINGLE_PACK_MODE: 22 А ≤1 с
minimum repeat interval: 10 с
I²t / thermal accumulator required
```

После 1 с действует continuous limit.

### 7. Filtering и hysteresis

Принято:

```text
budget low-pass: 100 мс
warning ON: >85 % for 250 мс
warning OFF: <80 % for 2 с
block new noncritical command: predicted ≥100 % or actual limit reached
re-enable: <90 % for 2 с
```

Hardware protection и EXT_KILL не задерживаются этой логикой.

### 8. Load classification

Critical domain:

```text
5V_CRIT / 3V3_CRIT
supervisor
fault manager
communication
journal retention
```

Все внешние CH, 5V_OUT и LED считаются некритическими для admission control, пока владелец не примет исключение.

Для каждого внешнего устройства хранятся:

```text
I_NOM
I_PEAK
T_PEAK
I_INRUSH
```

При неизвестном профиле используется консервативный максимум канала и статус `LOAD_PROFILE_UNKNOWN`.

### 9. Service override

Решение владельца ещё не принято.

До закрытия Q-SYS-007:

```text
SERVICE_OVERRIDE = DISABLED BY DEFAULT
```

Production firmware не должна обходить admission control.

## Последствия

Положительные:

1. можно начинать PCB packaging в envelope 100 × 250 × 80 мм;
2. можно проектировать многоуровневую сборку на стойках;
3. снят блокер по обязательной карте крышки;
4. снят блокер по pressure-hull данным для PCB architecture;
5. определён thermal-path constraint;
6. закрыты timing/filtering/classification параметры power-budget manager;
7. разрешена разработка load-profile database и I²t accumulator.

Ограничения:

1. thermal verification обязателен до подтверждения continuous ratings;
2. physical interboard connectors и pinout остаются открыты;
3. координаты mounting holes зависят от первого packaging layout;
4. service override не реализуется до решения владельца;
5. BMS/K_BATx/REMOTE_OFF tests остаются обязательными.

## Неизменяемые решения

Настоящий ADR не изменяет:

- отсутствие `K_MAIN`;
- PACK_BUS как единственную главную силовую шину;
- параллельный DUAL_PACK_RUN;
- запрет automatic restart после BMS recovery;
- независимость EXT_KILL;
- отсутствие дополнительной активной электроники в основных АКБ;
- разделение 5V_SYS_BUS и 5V_CRIT/3V3_CRIT;
- внутренний CAN-FD с direct safety/fault lines;
- пассивный INTERCONNECT;
- отдельные POWER_GND, SIGNAL_GND, ISO_GND и CHASSIS.

## Связанные документы

```text
Docs/OWNER_ANSWERS_REVIEW_V1_8.md
Docs/MECHANICAL_ENVELOPE_V1_8.md
Docs/SYSTEM_POWER_BUDGET_POLICY.md
Docs/ARCHITECTURE_BASELINE.md
Docs/PROJECT_MASTER.md
Docs/OPEN_QUESTIONS.md
```
