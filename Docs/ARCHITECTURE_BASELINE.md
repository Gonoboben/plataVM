# Архитектурная база ПДУ БНПА / PlataVM

Дата актуализации: 2026-07-21  
Статус:

```text
V1.8 OWNER-INPUT-REVIEWED BASELINE
Architecture A/B preserved; PCB envelope and power-budget implementation parameters resolved
```

## 1. Назначение

Документ фиксирует действующую архитектуру питания, управления, резервирования, аварийного отключения, многоплатного разбиения, общего power budget и механического envelope электронной сборки.

Связанные нормативные документы:

```text
Docs/PROJECT_MASTER.md
Docs/KBAT_ELECTRICAL_REQUIREMENTS.md
Docs/INTERBOARD_INTERFACES.md
Docs/SYSTEM_POWER_BUDGET_POLICY.md
Docs/MECHANICAL_ENVELOPE_V1_8.md
Docs/OPEN_QUESTIONS.md
Docs/OWNER_ANSWERS_REVIEW_V1_8.md
Docs/adr/ADR-2026-07-21-owner-input-v1-8.md
```

## 2. Основные исходные данные

| Параметр | Значение | Статус |
|---|---:|---|
| АКБ_1 | LiFePO4 4S24P, 12,8 В, 144 А·ч | ACCEPTED |
| АКБ_2 | LiFePO4 4S24P, 12,8 В, 144 А·ч | ACCEPTED |
| Ячейка | Hunan Huaxing 32700-6000mAh, 3,2 В, 6 А·ч | ACCEPTED |
| Основная BMS | LiFePO4 4S 12 V 30 A symmetric, supplier item 0102 | PRELIMINARY SUPPLIER DATA |
| Работа основных АКБ | параллельно в DUAL_PACK_RUN | ACCEPTED |
| SINGLE_PACK_MODE | деградированный функциональный режим | ACCEPTED |
| Контакторы АКБ | K_BAT1/K_BAT2, однополюсные по плюсу, моностабильные SPST-NO | ACCEPTED |
| Межкорпусный соединитель | СН-176А-12 | OWNER-CONTROLLED INPUT |
| Длина каждой батарейной линии | 1 м | ACCEPTED |
| EMG / АКБ_RES | LiFePO4 4S2P | ACCEPTED |
| POWER_12V_BUS | 14 каналов; 3 А continuous/channel, 5 А peak/1 с | PRELIMINARY REQUIREMENT |
| PCB-C hardware rating | 30 А continuous | PRELIMINARY REQUIREMENT |
| 5V_SYS_BUS | 10 выходов, до 3 А/output; 15 А continuous, 20 А short total | PRELIMINARY REQUIREMENT |
| LIGHT_POWER_BRANCH | 6 независимых LED-каналов, две зоны 2×3 | ACCEPTED ARCHITECTURE |
| DUAL_PACK system limit | 40 А continuous / 44 А short ≤1 с | ACCEPTED PRELIMINARY |
| SINGLE_PACK system limit | 20 А continuous / 22 А short ≤1 с | ACCEPTED PRELIMINARY |
| Short repeat interval | ≥10 с + I²t/thermal accumulator | ACCEPTED PRELIMINARY |
| Внешний интерфейс | isolated RS-485 half-duplex, 115200 bit/s preliminary | ACCEPTED / PRELIMINARY RATE |
| Внутренний интерфейс PCB-B↔PCB-C/D/E | CAN-FD + отдельные аппаратные safe/fault lines | ACCEPTED ARCHITECTURE |
| Доступный внутренний корпус | цилиндр Ø130 мм × 1000 мм | OWNER-DEFINED |
| Электронная сборка | ≤100 × 250 × 80 мм, многоуровневая | ACCEPTED / LENGTH PRELIMINARY |
| Извлечение | вся сборка вместе с крышкой | ACCEPTED |
| Тепловой контакт с корпусом | запрещён | ACCEPTED |
| Охлаждение | внутренняя естественная конвекция, low-loss design | ACCEPTED |

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

Центральный `K_MAIN` и отдельная `MAIN_INPUT_BUS` отсутствуют. Высокие токи не проходят через PCB-B.

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

1. PCB-A — Battery Front-End, измерения, DECK_BALANCE и распределение PACK_BUS;
2. PCB-B — critical power, MCU, supervisor, внешний RS-485, внутренняя CAN-FD и аппаратная аварийная логика;
3. PCB-C — 14 защищённых каналов 12 В;
4. PCB-D — DC/DC 5 В и 10 защищённых выходов;
5. PCB-E — шесть независимых LED-драйверов;
6. INTERCONNECT — пассивная транспортная среда без активных компонентов.

Все платы и уровни должны укладываться в assembly envelope `100 × 250 × 80 мм`.

## 5. Батарейная архитектура

```text
АКБ_1 → autonomous BMS → fuse → K_BAT1 → СН-176А-12 → BFE_1 ┐
                                                                  ├→ PACK_BUS
АКБ_2 → autonomous BMS → fuse → K_BAT2 → СН-176А-12 → BFE_2 ┘
```

В каждом корпусе основной АКБ находятся только:

1. аккумуляторная сборка;
2. автономная BMS;
3. силовой предохранитель;
4. F_CTRL;
5. K_BATx;
6. одна катушка continuous duty;
7. K_BAT_AUX_NO;
8. LOCAL_START wiring;
9. минимальная passive suppression.

Запрещены дополнительный MCU, управляющая плата, RS-485, CAN, UART, цифровая телеметрия BMS и raw-доступ к ячейкам/BMS.

## 6. K_BATx и LOCAL_START

```text
BAT_PROT+ → F_CTRL → (LOCAL_START_NO ∥ K_BAT_AUX_NO)
→ K_BAT_COIL → pin 11 K_BAT_HOLD_RETURN
→ REMOTE_OFF_RUN_CONTACT → EXT_KILL path → BAT_PROT−
```

K_BATx:

- SPST-NO по положительному проводнику;
- моностабильный;
- одна катушка continuous duty;
- economizer preferred;
- automatic OPEN при исчезновении BAT_PROT;
- no automatic restart после восстановления BMS.

| Параметр | Требование |
|---|---:|
| Диапазон управляющей цепи | 0…16 В DC |
| Guaranteed pull-in | 9…16 В |
| Guaranteed hold | 7,5…16 В |
| Inrush | ≤2 А / 150 мс |
| Hold current | target ≤0,15 А; limit ≤0,25 А |
| Hold power | target ≤2 Вт; limit ≤4 Вт |
| Главный контакт | ≥30 А continuous; target class ≥50 А |
| DC breaking capacity | ≥30 А при 16 В DC |
| Рабочая температура | −20…+60 °C |
| Механический ресурс | ≥100 000 циклов |
| Электрический ресурс | ≥10 000 операций |

Конкретная модель не выбрана до измерений и испытаний.

## 7. REMOTE_OFF и EXT_KILL

REMOTE_OFF:

```text
healthy critical power + healthy supervisor
→ energize-to-run relay energized
→ physical NO run contact CLOSED

loss of critical power / supervisor fault / OFF command
→ relay de-energized
→ NO run contact OPEN
→ hold loop OPEN
```

EXT_KILL:

- разрывает оба hold loop;
- запрещает MAIN_SW1/MAIN_SW2;
- независим от MCU, RS-485 и CAN-FD;
- имеет приоритет над LOCAL_START;
- не допускает automatic restart.

```text
t_OFF ≥ max(250 мс; 5 × t_release_max)
t_release_system target ≤100 мс
```

`HARD_OFF_FAILED` и `WELDED_CONTACT` блокируют restart.

## 8. Межплатное управление и диагностика

PCB-A↔PCB-B critical controls и key measurements остаются прямыми.

PCB-B↔PCB-C/D/E:

1. normal commands, setpoints, configuration и detailed telemetry — CAN-FD;
2. SAFE_OFF, HARD_OFF и board fault summary — direct hardware lines;
3. CAN-FD loss не препятствует аппаратному shutdown;
4. внешний isolated RS-485 не используется как внутренняя шина.

Физическая topology и termination определяются после multilevel packaging и pin count.

## 9. Ground, chassis и shield policy

| Сеть | Назначение |
|---|---|
| `POWER_GND` | силовой возврат |
| `SIGNAL_GND` | MCU и измерения |
| `ISO_GND` | изолированная сторона RS-485 |
| `CHASSIS` | корпус и экраны |

Принято:

1. одна controlled point `SIGNAL_GND–POWER_GND` на PCB-B;
2. другие прямые соединения запрещены;
3. экраны к CHASSIS у ввода;
4. ISO_GND не соединяется с SIGNAL_GND по DC;
5. optional HF coupling ISO_GND–CHASSIS только после EMC review.

## 10. DECK_BALANCE

| Параметр | Значение |
|---|---:|
| Номинальный ток | 2 А |
| Hard limit | 3 А |
| Завершение | abs(ΔU) ≤50 мВ и abs(I) ≤0,2 А в течение 60 с |
| Температура | подтверждённые 0…45 °C |

Режим выполняется только на палубе, при двух доступных батареях и отключённых тяжёлых нагрузках. В SINGLE_PACK_MODE запрещён.

## 11. Выходные платы

### PCB-C

- CH1…CH11 controlled;
- CH12…CH14 Always-On monitored;
- 3 А continuous / 5 А peak до 1 с;
- board rating 30 А continuous;
- local protection/current diagnostics;
- local MCU/I/O/ADC и CAN-FD.

### PCB-D

- 10 выходов до 3 А;
- OUT8…OUT10 Always-On monitored;
- 15 А continuous / 20 А short на 5V_SYS_BUS;
- preliminary two-phase synchronous buck;
- local MCU/I/O/ADC и CAN-FD;
- тепловой контакт с корпусом запрещён;
- thermal design выполняется через low-loss components, PCB copper и внутреннюю конвекцию.

`5V_SYS_BUS` не питает critical domain PCB-B.

### PCB-E

- 6 independent LED channels;
- две зоны 2×3;
- functional input 8…16 В;
- PWM 3,3 В active-high, default 1 кГц, 100…1000 Гц configurable;
- local current regulation и diagnostics;
- HARD_OFF direct;
- отдельный brightness limit в SINGLE_PACK_MODE отсутствует;
- thermal contact с корпусом запрещён.

## 12. Системный power budget

| Режим | Continuous | Short | Duration | Warning |
|---|---:|---:|---:|---:|
| DUAL_PACK_RUN | 40 А | 44 А | ≤1 с | 34 А |
| SINGLE_PACK_MODE | 20 А | 22 А | ≤1 с | 17 А |

Повторный short-event:

```text
не ранее 10 с
I²t / thermal accumulator required
```

## 13. Filtering и admission control

Принято:

```text
budget low-pass = 100 мс
warning ON >85 % for 250 мс
warning OFF <80 % for 2 с
block new noncritical command at predicted ≥100 %
re-enable below 90 % for 2 с
```

Уже включённые нагрузки software budget manager не сбрасывает. Hardware protection, SAFE/HARD_OFF и EXT_KILL имеют приоритет.

## 14. Critical/noncritical classification

Critical domain:

```text
5V_CRIT / 3V3_CRIT
supervisor
fault manager
communication
journal retention
```

Некритические внешние нагрузки:

```text
CH1…CH14
5V_OUT1…5V_OUT10
LED1…LED6
```

Для каждого внешнего устройства хранятся `I_NOM`, `I_PEAK`, `T_PEAK`, `I_INRUSH`.

Неизвестный профиль:

```text
conservative channel maximum
LOAD_PROFILE_UNKNOWN
```

## 15. Service override

Назначение режима разъясняется владельцу. До отдельного решения:

```text
SERVICE_OVERRIDE = DISABLED BY DEFAULT
```

Production firmware не должна обходить admission control. Hardware protections не могут быть отменены ни при каком варианте.

## 16. Механический envelope электронной сборки

Принято:

```text
доступный внутренний цилиндр: Ø130 × 1000 мм
рабочая электронная сборка: ≤100 × 250 × 80 мм
многоуровневая конструкция
извлечение вместе с крышкой
крепление PCB винтами к стойкам
```

Винты, стойки и крышечная механика — owner-controlled scope. PCB должны иметь монтажные отверстия и keepout.

Отдельный обязательный carrier/tray не применяется.

## 17. Вибрационная фиксация

- пайка и винтовое крепление — основные;
- тяжёлые компоненты не удерживаются только пайкой;
- hot-melt polyethylene adhesive — только auxiliary anti-vibration/strain relief;
- клей не применяется как единственная опора, у горячих деталей, с нарушением creepage/clearance или ремонтопригодности;
- совместимость с −20…+60 °C и conformal coating проверяется.

## 18. Тепловая архитектура

Штатный thermal contact с корпусом запрещён.

```text
component
→ PCB copper / local internal heatsink
→ internal air
→ natural convection inside sealed volume
```

Обязательна thermal verification при +60 °C, maximum allowed system load и без hull heat sink.

Если режим не проходит, допускается:

```text
уменьшить потери
→ заменить topology/components
→ увеличить площадь/число PCB
→ изменить внутреннюю компоновку
→ снизить continuous rating
```

Добавление thermal contact к корпусу требует нового решения владельца.

## 19. Корпус и mechanical scope

Pressure-hull design, материал, толщина стенки и квалификация крышки находятся вне scope электроники. Корпус принимается как owner-provided qualified enclosure.

Герметичность не отменяет внешнее дифференциальное давление; ответственность за механическую пригодность корпуса остаётся у владельца/изготовителя.

## 20. KiCad workspace

Владелец подтвердил открытие root project и листов 00…56. Перед schematic freeze обязательны запись версии KiCad, ERC release commit и отсутствие `.kicad_prl` в репозитории.

## 21. Неизменяемые ограничения

1. `K_MAIN` отсутствует;
2. PACK_BUS — главная силовая шина;
3. high current не проходит через PCB-B;
4. EXT_KILL независим от firmware и цифровых шин;
5. INTERCONNECT пассивный;
6. EMG не питает пользовательские силовые ветви;
7. внешняя связь — isolated RS-485;
8. внутренняя CAN-FD не заменяет hardware safety;
9. батарейный разъём не используется для digital communication;
10. automatic restart после BMS recovery запрещён;
11. part numbers выбираются только после закрытия входов, расчёта и проверки.

## 22. Текущий Gate G-R

Закрыты:

- owner-level system budget;
- short timing;
- filtering/hysteresis;
- critical/noncritical classification;
- PCB assembly envelope;
- mounting/service concept;
- thermal-path constraint.

Остаются:

1. Q-SYS-007 service override decision;
2. BMS BAT_PROT tests;
3. K_BATx/REMOTE_OFF candidate selection and tests;
4. physical CAN-FD/hard-line pin count и connector selection;
5. first PCB packaging/layout review;
6. thermal calculations/tests without hull contact.

Разрешено продолжать расчёты и component selection по узлам с закрытыми входными данными.
