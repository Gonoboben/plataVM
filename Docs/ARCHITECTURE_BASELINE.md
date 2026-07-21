# Архитектурная база ПДУ БНПА / PlataVM

Дата актуализации: 2026-07-21  
Статус:

```text
V1.7 OWNER-INPUT-REVIEWED BASELINE
Architecture A/B preserved; power-budget and external mechanical envelope resolved
```

## 1. Назначение

Документ фиксирует действующую архитектуру питания, управления, резервирования, аварийного отключения, многоплатного разбиения, общего power budget и механического envelope PlataVM.

Связанные нормативные документы:

```text
Docs/PROJECT_MASTER.md
Docs/KBAT_ELECTRICAL_REQUIREMENTS.md
Docs/INTERBOARD_INTERFACES.md
Docs/SYSTEM_POWER_BUDGET_POLICY.md
Docs/MECHANICAL_ENVELOPE_V1_7.md
Docs/OPEN_QUESTIONS.md
Docs/OWNER_ANSWERS_REVIEW_V1_7.md
Docs/adr/ADR-2026-07-21-owner-input-v1-7.md
```

## 2. Основные исходные данные

| Параметр | Значение | Статус |
|---|---:|---|
| АКБ_1 | LiFePO4 4S24P, 12,8 В, 144 А·ч | ACCEPTED |
| АКБ_2 | LiFePO4 4S24P, 12,8 В, 144 А·ч | ACCEPTED |
| Ячейка | Hunan Huaxing 32700-6000mAh, 3,2 В, 6 А·ч | ACCEPTED |
| Основная BMS | LiFePO4 4S 12 V 30 A symmetric, supplier item 0102 | PRELIMINARY SUPPLIER DATA |
| Работа основных АКБ | параллельно в RUN | ACCEPTED |
| SINGLE_PACK_MODE | деградированный функциональный режим | ACCEPTED |
| Контакторы АКБ | K_BAT1/K_BAT2, однополюсные по плюсу, моностабильные SPST-NO | ACCEPTED |
| Межкорпусный соединитель | СН-176А-12 | OWNER-CONTROLLED INPUT |
| Длина каждой батарейной линии | 1 м | ACCEPTED |
| EMG / АКБ_RES | LiFePO4 4S2P | ACCEPTED |
| POWER_12V_BUS | 14 каналов; 3 А continuous/channel, 5 А peak/1 с | PRELIMINARY REQUIREMENT |
| PCB-C hardware rating | 30 А continuous | PRELIMINARY REQUIREMENT |
| 5V_SYS_BUS | 10 выходов, до 3 А/output; 15 А continuous, 20 А short total | PRELIMINARY REQUIREMENT |
| LIGHT_POWER_BRANCH | 6 независимых LED-каналов, две зоны 2×3 | ACCEPTED ARCHITECTURE |
| DUAL_PACK system limit | 40 А continuous / 44 А short по PACK_BUS | ACCEPTED PRELIMINARY |
| SINGLE_PACK system limit | 20 А continuous / 22 А short по PACK_BUS | ACCEPTED PRELIMINARY |
| Внешний интерфейс | isolated RS-485 half-duplex, 115200 bit/s preliminary | ACCEPTED / PRELIMINARY RATE |
| Внутренний интерфейс PCB-B↔PCB-C/D/E | CAN-FD + отдельные аппаратные safe/fault lines | ACCEPTED ARCHITECTURE |
| Корпус электроники | цилиндр Ø130 мм × 1000 мм; один торец заварен, второй — крышка с разъёмами | ACCEPTED EXTERNAL ENVELOPE |

## 3. Базовые силовые шины

| Шина | Источник | Назначение |
|---|---|---|
| `PACK_BUS` | АКБ_1/АКБ_2 через Battery Front-End | главная силовая шина |
| `PACK_BUS_CRIT_IN` | ответвление от PCB-A | заряд EMG и critical power path PCB-B |
| `PACK_BUS_P12_IN` | ответвление от PCB-A | PCB-C / 14 каналов 12 В |
| `PACK_BUS_P5_IN` | ответвление от PCB-A | PCB-D / DC/DC 12→5 В |
| `PACK_BUS_LIGHT_IN` | ответвление от PCB-A | PCB-E / LED-драйверы |
| `5V_CRIT` | critical power path PCB-B | MCU, supervisor, связь, аварийная логика |
| `3V3_CRIT` | 5V_CRIT | цифровая critical logic |
| `5V_SYS_BUS` | отдельный DC/DC PCB-D | внешние 5 В нагрузки |

Отдельные `MAIN_INPUT_BUS` и центральный `K_MAIN` отсутствуют. Высокие токи не проходят через PCB-B.

## 4. Многоплатное разбиение

```text
PCB-A_BFE_POWER
PCB-B_CTRL_RESERVE
PCB-C_POWER_12V
PCB-D_POWER_5V
PCB-E_LIGHT_POWER
INTERCONNECT — только пассивные шины, жгуты и/или backplane
```

Назначение:

1. PCB-A — объединение батарейных ветвей, электронные силовые тракты, измерения, DECK_BALANCE и распределение PACK_BUS;
2. PCB-B — critical power, MCU, supervisor, внешний RS-485, внутренняя CAN-FD и аппаратная аварийная логика;
3. PCB-C — 14 защищённых каналов 12 В;
4. PCB-D — DC/DC 5 В и 10 защищённых выходов;
5. PCB-E — шесть независимых LED-драйверов;
6. INTERCONNECT — пассивная транспортная среда без активных компонентов.

Ширина каждого PCB-модуля не более 100 мм. Окончательная высота и длина плат определяются после получения внутреннего диаметра и 3D-компоновки цилиндрического корпуса.

## 5. Батарейная архитектура

```text
АКБ_1 → autonomous BMS → fuse → K_BAT1 → СН-176А-12 → BFE_1 ┐
                                                                  ├→ PACK_BUS
АКБ_2 → autonomous BMS → fuse → K_BAT2 → СН-176А-12 → BFE_2 ┘
```

В каждом корпусе основной АКБ находятся только:

1. аккумуляторная сборка;
2. существующая автономная BMS;
3. силовой предохранитель;
4. `F_CTRL` у ответвления `BAT_PROT+`;
5. K_BATx;
6. одна катушка continuous duty;
7. механически связанный `K_BAT_AUX_NO`;
8. LOCAL_START wiring;
9. минимальные пассивные элементы suppression.

Запрещены дополнительный MCU, локальная управляющая плата, RS-485, CAN, UART, цифровая телеметрия BMS и raw-доступ к ячейкам/BMS.

## 6. K_BATx и LOCAL_START

Функциональная цепь:

```text
BAT_PROT+ → F_CTRL → (LOCAL_START_NO ∥ K_BAT_AUX_NO)
→ K_BAT_COIL → pin 11 K_BAT_HOLD_RETURN
→ REMOTE_OFF_RUN_CONTACT → EXT_KILL path → BAT_PROT−
```

K_BATx:

- SPST-NO по положительному силовому проводнику;
- моностабильный;
- пружинный возврат в OPEN;
- одна катушка continuous duty;
- economizer preferred;
- автоматический возврат в OPEN при исчезновении BAT_PROT;
- после восстановления BMS остаётся OPEN до нового LOCAL_START.

Предварительная численная база:

| Параметр | Требование |
|---|---:|
| Диапазон управляющей цепи | 0…16 В DC |
| Гарантированное втягивание | 9…16 В |
| Гарантированное удержание | 7,5…16 В |
| Inrush | ≤2 А / 150 мс |
| Hold current | target ≤0,15 А; limit ≤0,25 А |
| Hold power | target ≤2 Вт; limit ≤4 Вт |
| Главный контакт | ≥30 А continuous; target class ≥50 А |
| DC breaking capacity | ≥30 А при 16 В DC |
| Рабочая температура | −20…+60 °C |
| Механический ресурс | ≥100 000 циклов |
| Электрический ресурс | ≥10 000 операций |

Конкретная модель K_BATx не выбрана до измерений dropout, L, inrush, release, температуры, vibration и ресурса.

## 7. REMOTE_OFF и EXT_KILL

Программный REMOTE_OFF реализуется по принципу `energize-to-run`:

```text
healthy 5V_CRIT/3V3_CRIT + healthy supervisor
→ relay coil energized
→ physical NO run contact CLOSED

loss of critical power / supervisor fault / OFF command
→ relay coil de-energized
→ physical NO run contact OPEN
→ hold loop OPEN
```

Требования:

1. по одному независимому run-contact на hold loop каждой АКБ;
2. потеря critical power приводит к OPEN;
3. восстановление питания не включает K_BATx автоматически;
4. аппаратный EXT_KILL разрывает оба hold loop и запрещает оба MAIN_SW независимо от MCU, RS-485 и CAN-FD;
5. приоритет EXT_KILL над LOCAL_START обеспечивается физической последовательной цепью;
6. после OFF контролируются ток катушки, состояние ветви и PACK_BUS;
7. `HARD_OFF_FAILED` и `WELDED_CONTACT` блокируют restart и отображаются в GUI.

Штатное время разрыва:

```text
t_OFF ≥ max(250 мс; 5 × t_release_max)
t_release_system target ≤100 мс
```

## 8. Межплатное управление и диагностика

### 8.1 PCB-A ↔ PCB-B

Критическое управление Battery Front-End и ключевые измерения остаются прямыми аппаратными линиями. Внутренняя CAN-FD не является обязательным условием отключения основных АКБ.

### 8.2 PCB-B ↔ PCB-C/D/E

Принято:

1. нормальные команды, конфигурация, per-channel telemetry и журналирование — внутренняя CAN-FD;
2. PCB-C/D/E имеют локальные MCU либо защищённые I/O/ADC узлы семейства STM32G4;
3. `SAFE_OFF`, `HARD_OFF` и board fault summary передаются отдельными аппаратными линиями;
4. отсутствие CAN-FD не должно препятствовать аппаратному безопасному отключению;
5. внешний isolated RS-485 не используется как внутренняя шина.

Физическая топология CAN-FD, termination и pinout фиксируются после 3D-компоновки и pin count.

## 9. Ground, chassis и shield policy

Сети остаются раздельными:

| Сеть | Назначение |
|---|---|
| `POWER_GND` | силовой возврат PACK_BUS и нагрузок |
| `SIGNAL_GND` | MCU и низкоуровневые измерения |
| `ISO_GND` | изолированная сторона внешнего RS-485 |
| `CHASSIS` | корпус, экраны и EMC-отводы |

Принято:

1. единственная контролируемая точка `SIGNAL_GND–POWER_GND` на PCB-B через net-tie/конфигурируемый элемент;
2. другие прямые соединения запрещены;
3. экраны подключаются к CHASSIS у ввода коротким низкоиндуктивным путём;
4. ISO_GND не соединяется с SIGNAL_GND по постоянному току;
5. опциональная ВЧ-связь ISO_GND–CHASSIS допускается после EMC review.

## 10. DECK_BALANCE

DECK_BALANCE выполняется только на палубе при отключённых тяжёлых нагрузках и двух доступных батареях.

| Параметр | Значение |
|---|---:|
| Номинальный ток | 2 А |
| Hard limit | 3 А |
| Завершение | abs(ΔU) ≤50 мВ и abs(I) ≤0,2 А в течение 60 с |
| Температурное условие | батареи подтверждённо в диапазоне 0…45 °C |

Дополнительная активная электроника и датчики внутри корпусов АКБ не добавляются. Тайм-аут и критерий отсутствия прогресса определяются расчётом и испытанием.

В `SINGLE_PACK_MODE` DECK_BALANCE запрещён.

## 11. Выходные платы

### PCB-C POWER_12V

- CH1…CH11 controlled;
- CH12…CH14 Always-On monitored в RUN;
- все каналы отключаются защитой, SAFE и HARD_OFF;
- 3 А continuous / 5 А peak до 1 с на канал;
- hardware board rating 30 А continuous;
- локальные I/O/ADC и внутренняя CAN-FD.

### PCB-D POWER_5V

- 10 выходов до 3 А;
- OUT8…OUT10 Always-On monitored;
- общий preliminary limit 15 А continuous / 20 А short;
- preliminary topology: two-phase synchronous buck с внешними MOSFET и тепловым отводом на корпус;
- локальные I/O/ADC и внутренняя CAN-FD.

`5V_SYS_BUS` не питает critical domain PCB-B.

### PCB-E LIGHT_POWER

- шесть независимых каналов;
- две локальные силовые зоны 2×3;
- functional input 8…16 В;
- PWM 3,3 В active-high;
- default 1 кГц, configurable 100…1000 Гц;
- default safe state — все LED OFF;
- общий HARD_OFF действует на обе зоны;
- отдельный brightness limit в SINGLE_PACK_MODE отсутствует.

## 12. Общий power budget

Локальные аппаратные рейтинги плат не означают, что все максимумы разрешены одновременно.

Системные пределы:

| Режим | Continuous | Short | Warning 85 % |
|---|---:|---:|---:|
| DUAL_PACK_RUN | 40 А | 44 А | 34 А |
| SINGLE_PACK_MODE | 20 А | 22 А | 17 А |

Политика:

1. учитывается фактический суммарный ток PACK_BUS;
2. вход в SINGLE_PACK_MODE не выключает нагрузки по категории;
3. при 85 % active continuous budget отображается предупреждение;
4. при 100 % запрещается включение новой некритической нагрузки;
5. уже включённые нагрузки не отключаются обычным программным budget manager;
6. яркость автоматически не изменяется;
7. service override допускается только в диагностическом режиме с журналированием;
8. аппаратные защиты, SAFE/HARD_OFF и EXT_KILL имеют приоритет.

Подробная логика приведена в `Docs/SYSTEM_POWER_BUDGET_POLICY.md`.

## 13. SINGLE_PACK_MODE

Условия:

```text
одна основная батарея доступна и подключена
вторая отсутствует, отключена или изолирована
```

Режим:

- деградированный, но функциональный;
- active budget = 20 А continuous / 22 А short;
- не вводит автоматическое выключение света, 12 В или 5 В нагрузок;
- запрещает DECK_BALANCE;
- отображается постоянно в GUI;
- не допускает автоматический restart второй батареи после BMS recovery;
- возврат к DUAL_PACK_RUN требует нового LOCAL_START и проверки безопасного параллельного подключения.

## 14. Условия эксплуатации

Принято:

| Параметр | Требование |
|---|---:|
| Рабочая температура | −20…+60 °C |
| Хранение | −30…+70 °C |
| Влажность | высокая |
| Конденсация | возможна |
| PCB coating | conformal coating обязательно |
| Среда | морская, внутренний объём штатно сухой |

Вибрационный и ударный профиль остаётся открытым до данных о креплении аппарата.

## 15. Механический envelope

Подтверждено:

```text
цилиндрический корпус
наружный диаметр 130 мм
длина 1000 мм
один торец заварен
второй торец — съёмная крышка с разъёмами
сервисный доступ со стороны крышки
```

Предварительная внутренняя концепция:

- единый продольный извлекаемый carrier/tray;
- PCB-A у батарейных вводов;
- PCB-C/D/E с короткими путями к выходным разъёмам;
- PCB-B в наименее шумной зоне;
- PACK_BUS/POWER_GND и сигнальный harness трассируются раздельно;
- глухой заваренный торец не требует обслуживания.

Окончательная 3D-компоновка запрещена до получения внутреннего диаметра, материала, полезной длины, карты разъёмов, pressure/vibration data и thermal interface policy.

## 16. Проверка KiCad

Владелец подтвердил, что текущий root project и листы 00…56 открываются нормально.

Статус:

```text
OWNER VERIFIED FOR CONTINUED ARCHITECTURE WORK
```

Перед schematic freeze требуется ERC/parsing review конкретного release commit с записью версии KiCad.

## 17. Неизменяемые ограничения

1. `K_MAIN` отсутствует;
2. PACK_BUS — единственная главная силовая шина;
3. высокие токи не проходят через PCB-B;
4. EXT_KILL независим от firmware и цифровых шин;
5. INTERCONNECT пассивный;
6. EMG не питает POWER_12V_BUS, 5V_SYS_BUS или LIGHT_POWER_BRANCH;
7. внешняя связь — isolated RS-485;
8. внутренняя CAN-FD применяется только между PCB-B и PCB-C/D/E и не заменяет hard safety lines;
9. батарейный соединитель не используется для цифровой связи;
10. автоматический рестарт после BMS recovery запрещён;
11. конкретные part numbers не выбираются без расчёта и подтверждения входных данных.

## 18. Текущий Gate G-R

Закрыты owner-level блокеры:

- KiCad workspace verification;
- стартовый global power budget;
- SINGLE_PACK_MODE policy;
- реакция на прогнозируемую перегрузку;
- базовые environmental requirements;
- внешний корпусной envelope.

Полный Gate G-R остаётся открыт до:

1. выбора и испытания K_BATx и REMOTE_OFF relay;
2. BMS BAT_PROT fault/recovery tests;
3. определения внутренних размеров, pressure/vibration условий и 3D-компоновки;
4. physical CAN-FD/hard-line pin count и выбора разъёмов;
5. закрытия short-limit duration, filters/hysteresis и load profiles.

При этом разрешены расчёты и component selection по отдельным узлам, для которых входные данные уже закрыты и которые не зависят от оставшихся блокеров.
