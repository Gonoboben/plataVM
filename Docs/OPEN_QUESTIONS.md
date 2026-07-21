# Открытые вопросы ПДУ БНПА / PlataVM V1.7

Дата пересмотра: 2026-07-21  
Источник: заполненная форма `Ответы_на_вопросы_ПДУ_БНПА_V1.7(1).docx`  
Статус: `OWNER INPUT V1.7 REVIEWED`; owner-level power-budget policy закрыта, полный Gate G-R остаётся открыт по расчётам, механике, компонентам и испытаниям.

## 1. Закрытые и зафиксированные решения

### 1.1 Battery Front-End и главная шина

| ID | Решение | Статус |
|---|---|---|
| Q-BFE-001 | Механическое соединение под нагрузкой не является штатной операцией | CLOSED |
| Q-BFE-002 | Обе исправные АКБ работают параллельно; межблочное выравнивание выполняется в DECK_BALANCE | CLOSED |
| Q-BFE-003A | Длина каждой батарейной кабельной сборки — 1 м | CLOSED |
| Q-BFE-004 | K_BAT1/K_BAT2 — однополюсные контакторы по плюсу | CLOSED |
| Q-BFE-005 | Центральный K_MAIN отсутствует; PACK_BUS — главная силовая шина | CLOSED |
| Q-BFE-006 | Штатный HARD_OFF: запрет новых команд → отключение тяжёлых нагрузок и электронных силовых трактов → журнал → разрыв hold loop K_BAT1/K_BAT2 → контроль токов и PACK_BUS | CLOSED |
| Q-BFE-007 | В корпусе АКБ не устанавливается дополнительная активная электроника | CLOSED |
| Q-BFE-008 | BMS работает автономно и не обязана передавать цифровую телеметрию | CLOSED |
| Q-BFE-009 | RS-485/CAN/UART через батарейный соединитель не используются | CLOSED |

### 1.2 BMS и основные ячейки

| ID | Решение | Статус |
|---|---|---|
| Q-BMS-001 | BMS рассматривается как закрытый двухполюсный защищённый источник BAT_PROT+ / BAT_PROT− | CLOSED |
| Q-BMS-002 | Raw-ветвь, внутренние точки и сигналы BMS не используются | CLOSED |
| Q-BMS-003 | Схема контактора не зависит от high-side/low-side топологии BMS | CLOSED |
| Q-BMS-004 | Ячейки: Hunan Huaxing 32700-6000mAh LiFePO4, 3,2 В, 6 А·ч; сборка 4S24P = 12,8 В, 144 А·ч | CLOSED |
| Q-BMS-005 | Закупочная позиция BMS: LiFePO4 4S 12 V 30 A symmetric, supplier item 0102; изготовитель платы не идентифицирован | CLOSED_PRELIMINARY |
| Q-BMS-006 | Предварительные пороги: 3,65 В/cell OV и 2,3 В/cell UV, ориентировочно 14,6/9,2 В для 4S; reconnect/delays проверяются отдельно | CLOSED_PARTIAL |
| Q-BMS-009 | 30 А continuous discharge, 40 А short, 60 А/1 с peak, 15 А continuous charge, 30 мА passive balance | CLOSED_PRELIMINARY |

### 1.3 K_BATx

| ID | Решение | Статус |
|---|---|---|
| Q-KBAT-001 | K_BATx — моностабильный нормально разомкнутый SPST-NO контактор | CLOSED |
| Q-KBAT-002 | Одна катушка непрерывного режима | CLOSED |
| Q-KBAT-003 | При снятии питания катушки K_BATx пружиной возвращается в OPEN | CLOSED |
| Q-KBAT-004 | Самоподхват выполняется через механически связанный K_BAT_AUX_NO | CLOSED |
| Q-KBAT-005 | Исчезновение защищённого выхода BMS автоматически открывает K_BATx | CLOSED |
| Q-KBAT-006 | После восстановления BMS контактор остаётся OPEN до нового LOCAL_START | CLOSED |
| Q-KBAT-007 | Расчётный диапазон управляющей цепи 0…16 В; нормальный диапазон катушки 9…14,6 В | CLOSED_PRELIMINARY |
| Q-KBAT-008 | Гарантированное втягивание требуется при 9…16 В | CLOSED_PRELIMINARY |
| Q-KBAT-009 | Гарантированное удержание требуется при 7,5…16 В | CLOSED_PRELIMINARY |
| Q-KBAT-011 | Пусковой ток ограничен 2 А, длительность до 150 мс | CLOSED_PRELIMINARY |
| Q-KBAT-012 | Hold current target ≤0,15 А, limit ≤0,25 А; hold power target ≤2 Вт, limit ≤4 Вт | CLOSED_PRELIMINARY |
| Q-KBAT-013 | Встроенный economizer предпочтителен; циклический restart/chatter запрещён | CLOSED_ARCHITECTURE |
| Q-KBAT-015 | Простой flyback-диод не принимается без проверки; анализируются TVS, bidirectional TVS и diode+resistor | CLOSED_DIRECTION |
| Q-KBAT-016 | Главный контакт: минимум 30 А continuous, целевой класс 50 А и выше | CLOSED_PRELIMINARY |
| Q-KBAT-017 | DC breaking capacity: минимум 30 А при 16 В DC | CLOSED_PRELIMINARY |
| Q-KBAT-018 | Начальное сопротивление главного контакта ≤2 мОм, после ресурса ≤5 мОм | CLOSED_PRELIMINARY |
| Q-KBAT-019 | Work −20…+60 °C; storage −30…+70 °C; высокая влажность/возможная конденсация; conformal coating; mechanical life ≥100 000; electrical life ≥10 000 | CLOSED_REQUIREMENT_WITH_OPEN_VIBRATION_PROFILE |
| Q-KBAT-020 | Сваривание главного контакта диагностируется по напряжениям до/после K_BAT и току ветви; WELDED_CONTACT отображается и блокирует restart | CLOSED_REQUIREMENT |
| Q-KBAT-021 | Штатно: отключить нагрузки и электронные MAIN_SWx, дождаться снижения тока, затем разорвать hold loop; EXT_KILL может разорвать loop немедленно | CLOSED |

### 1.4 LOCAL_START и REMOTE_OFF

| ID | Решение | Статус |
|---|---|---|
| Q-LS-001 | LOCAL_START выведен на отдельный двухконтактный разъём | CLOSED |
| Q-LS-002 | LOCAL_START — normally open, пружинно-возвратный, без фиксации | CLOSED |
| Q-LS-003 | LOCAL_START включён параллельно K_BAT_AUX_NO | CLOSED |
| Q-LS-004 | K_BAT_AUX_NO: ≥0,5 А при 16 В DC и ≥2 А / 150 мс | CLOSED_PRELIMINARY |
| Q-LS-005 | LOCAL_START имеет рейтинг не ниже K_BAT_AUX_NO | CLOSED_PRELIMINARY |
| Q-LS-006 | F_CTRL размещается внутри корпуса АКБ у ответвления BAT_PROT+ | CLOSED |
| Q-LS-007 | После восстановления питания запуск разрешается только после обнаружения отпущенного LOCAL_START; длительное замыкание считается fault | CLOSED_REQUIREMENT |
| Q-ROFF-001 | REMOTE_OFF выполняется разрывом цепи удержания единственной катушки | CLOSED |
| Q-ROFF-002 | Восстановление REMOTE_OFF loop после отпускания не включает контактор повторно | CLOSED |
| Q-ROFF-003 | Pin 11 несёт ток катушки в пределах 0,25 А continuous и 2 А pulsed | CLOSED_PRELIMINARY |
| Q-ROFF-004 | REMOTE_OFF — energize-to-run relay с физическим NO run-contact | CLOSED_ARCHITECTURE |
| Q-ROFF-005 | Для двух hold loop применяются два независимых run-contact; EXT_KILL действует независимо от MCU/RS-485/CAN-FD | CLOSED_ARCHITECTURE |
| Q-ROFF-006 | t_OFF ≥ max(250 мс; 5 × t_release_max) | CLOSED_PRELIMINARY |
| Q-ROFF-007 | Программный loop восстанавливается только после выдержки времени и подтверждения OPEN | CLOSED |
| Q-ROFF-009 | После OFF контролируются ток катушки, состояние контакта и PACK_BUS; при отсутствии OPEN фиксируется HARD_OFF_FAILED и запрещается restart | CLOSED_REQUIREMENT |
| Q-ROFF-010 | EXT_KILL включён последовательно после ветви LOCAL_START ∥ AUX_NO и имеет безусловный аппаратный приоритет | CLOSED_ARCHITECTURE |
| Q-ROFF-012 | Потеря 5V_CRIT/3V3_CRIT или healthy supervisor обесточивает REMOTE_OFF relay и разрывает hold loop | CLOSED_ARCHITECTURE |

### 1.5 DECK_BALANCE

| ID | Решение | Статус |
|---|---|---|
| Q-DB-001 | Паспортный максимум заряда BMS — 15 А; DECK_BALANCE — отдельный ограниченный режим | CLOSED_PRELIMINARY |
| Q-DB-002 | Номинальный ток — 2 А | CLOSED_PRELIMINARY |
| Q-DB-003 | Hard limit — 3 А | CLOSED_PRELIMINARY |
| Q-DB-005 | Завершение: abs(ΔU) ≤50 мВ и abs(I) ≤0,2 А в течение 60 с | CLOSED_PRELIMINARY |
| Q-DB-006 | Дополнительные датчики температуры в АКБ не добавляются; режим разрешён при подтверждённых 0…45 °C | CLOSED_OWNER_DECISION |

### 1.6 PCB-C POWER_12V

| ID | Решение | Статус |
|---|---|---|
| Q-P12-001 | Каналы сохраняют имена CH1…CH14; назначения задаются программно | CLOSED |
| Q-P12-002 | Номинальный длительный ток каждого CH — 3 А | CLOSED |
| Q-P12-003 | 3 А continuous, 5 А peak до 1 с, индивидуальное ограничение и защита | CLOSED_PRELIMINARY |
| Q-P12-004 | CH12…CH14 Always-On monitored, но отключаются защитой, SAFE и HARD_OFF | CLOSED |
| Q-P12-005 | PCB-C проектируется на 30 А continuous как hardware rating; фактическая нагрузка определяется global budget | CLOSED_PRELIMINARY |
| Q-P12-006 | Локальный protected I/O/ADC и узел CAN-FD; аппаратные SAFE/HARD_OFF остаются прямыми | CLOSED_ARCHITECTURE |

### 1.7 PCB-D POWER_5V

| ID | Решение | Статус |
|---|---|---|
| Q-5V-001 | Внешних 5V_OUT — 10 | CLOSED |
| Q-5V-002 | Максимум одного 5V_OUT — 3 А | CLOSED |
| Q-5V-003 | Три 5 В выхода — Always-On monitored | CLOSED |
| Q-5V-004 | Токовая диагностика каждого 5V_OUT обязательна | CLOSED |
| Q-5V-005 | 5V_SYS_BUS: 15 А continuous, 20 А short | CLOSED_ASSUMPTION |
| Q-5V-006 | OUT8…OUT10 — аппаратные Always-On monitored без жёсткого назначения; функции задаются в GUI | CLOSED |
| Q-5V-007 | Предварительная топология — two-phase synchronous buck с внешними MOSFET и тепловым отводом на корпус | CLOSED_TOPOLOGY_PRELIMINARY |
| Q-5V-008 | Локальный I/O/ADC и CAN-FD; hard-off остаётся прямой аппаратной линией | CLOSED_ARCHITECTURE |

### 1.8 PCB-E LIGHT_POWER

| ID | Решение | Статус |
|---|---|---|
| Q-LGT-001 | Шесть световых каналов логически независимы | CLOSED |
| Q-LGT-002 | Расчётный максимум LED-тока — 1,05 А на матрицу | CLOSED_ASSUMPTION |
| Q-LGT-003 | Диагностика каждого LED-канала обязательна | CLOSED |
| Q-LGT-004 | PCB-E делится на две симметричные силовые зоны 2×3 | CLOSED |
| Q-LGT-005 | Functional input 8…16 В, nominal protected range ориентировочно 9,2…14,6 В, отдельный transient margin | CLOSED_PRELIMINARY |
| Q-LGT-006 | Отдельный brightness limit для SINGLE_PACK_MODE отсутствует; общий 20/22 А system budget и admission control сохраняются | CLOSED_OWNER_DECISION |
| Q-LGT-007 | PWM 3,3 В active-high, default 1 кГц, configurable 100…1000 Гц; допускается level-shift option | CLOSED_PRELIMINARY |

### 1.9 Интерфейсы, MCU и земли

| ID | Решение | Статус |
|---|---|---|
| Q-IF-001 | Внешний CAN footprint optional/DNP; внешний baseline — RS-485 | CLOSED |
| Q-IF-002 | RS-485: 115200 bit/s, half-duplex, 8N1, адресный бинарный протокол, CRC-16, sequence number, timeout/heartbeat | CLOSED_PRELIMINARY |
| Q-IF-003 | Внешний интерфейс — isolated RS-485 | CLOSED |
| Q-MCU-001 | Базовое семейство центрального и локальных контроллеров — STM32G4; корпуса после pin count | CLOSED_FAMILY |
| Q-SCH-001 | Принята иерархия листов Docs/SCHEMATIC_ARCHITECTURE.md | CLOSED |
| Q-SCH-002 | Логические интерфейсы фиксируются до физических разъёмов | CLOSED |
| Q-SCH-003 | Высокие токи распределяются от PCB-A и не проходят через PCB-B | CLOSED |
| Q-SCH-004 | Владелец подтвердил нормальное открытие root project и листов 00…56 | CLOSED_OWNER_VERIFICATION |
| Q-SCH-005 | Normal PCB-B↔PCB-C/D/E — CAN-FD; SAFE/HARD_OFF и critical fault lines — отдельные провода | CLOSED_ARCHITECTURE |
| Q-SCH-007 | SIGNAL_GND соединяется с POWER_GND в одной контролируемой точке PCB-B | CLOSED_ARCHITECTURE |
| Q-SCH-008 | Экраны к CHASSIS у ввода; ISO_GND гальванически отделён; optional HF coupling после EMC | CLOSED_ARCHITECTURE |
| Q-SCH-009 | INTERCONNECT пассивный; силовые шины/жгуты отделены от signal backplane | CLOSED |
| Q-SCH-010 | PCB-A у батарейных вводов, PCB-B в наименее шумной зоне, PCB-C/D/E у выходов; целевой logical harness ≤300 мм | CLOSED_ARCHITECTURE |
| Q-SCH-011 | Refdes: PCB-A 100–199, PCB-B 200–299, PCB-C 300–399, PCB-D 400–499, PCB-E 500–599 | CLOSED |

### 1.10 Механика и окружающая среда

| ID | Решение | Статус |
|---|---|---|
| Q-MECH-001 | Ширина каждого PCB-модуля ≤100 мм | CLOSED |
| Q-MECH-002 | Электроника и межплатные разъёмы находятся в сухом закрытом корпусе; внутренняя самостоятельная герметизация разъёмов не требуется | CLOSED_SCOPE |
| Q-MECH-003 | Пять PCB-модулей и пассивный INTERCONNECT | CLOSED |
| Q-MECH-004 | Внешний корпус: цилиндр Ø130 мм × 1000 мм; один торец заварен, второй — съёмная крышка с разъёмами; сервис со стороны крышки | CLOSED_PARTIAL |
| Q-MECH-005 | Гибрид: отдельные силовые шины/жгуты и пассивный signal INTERCONNECT/backplane | CLOSED_ARCHITECTURE |

### 1.11 Общий power budget и SINGLE_PACK_MODE

| ID | Решение | Статус |
|---|---|---|
| Q-SYS-001 | DUAL_PACK: 40 А continuous / 44 А short; SINGLE_PACK: 20 А continuous / 22 А short; отдельный brightness limit отсутствует | CLOSED_SYSTEM_LIMIT_PRELIMINARY |
| Q-SYS-002 | SINGLE_PACK_MODE — деградированный функциональный режим; вход не выключает и не запрещает функции по категории; DECK_BALANCE запрещён | CLOSED_OWNER_DECISION |
| Q-SYS-003 | 85 % budget — warning; 100 % — reject новой некритической нагрузки; уже включённые нагрузки software budget manager не сбрасывает; service override только с журналом | CLOSED_OWNER_DECISION |

### 1.12 Батарейная линия СН-176А-12 — owner-controlled scope

Владелец исключил этот раздел из текущей зоны инженерной диагностики и рекомендаций. Ограничения учитываются как внешние входные данные.

| ID | Решение владельца / внешнее ограничение | Статус |
|---|---|---|
| Q-CON-001 | СН-176А-12 — единственный рабочий межкорпусный силовой вариант | CLOSED |
| Q-CON-002 | Контакты 1–5 BAT+, 6–10 BAT− | CLOSED |
| Q-CON-003 | Целевой предел линии 20 А continuous / 22 А short; для работы на воздухе до подтверждения действует паспортный предел 17,5 А | OWNER_CONTROLLED_PRELIMINARY |
| Q-CON-004 | Состав кабеля К25 принят по паспорту поставщика | OWNER_CONFIRMED |
| Q-CON-005 | Контакт 11 — REMOTE_OFF / K_BAT_HOLD_RETURN | CLOSED |
| Q-CON-006 | Нумерация контактов 1–12 подтверждена | OWNER_CONFIRMED |
| Q-CON-007 | Равномерность распределения по пяти параллельным контактам принята владельцем | OWNER_ACCEPTED_ASSUMPTION |
| Q-CON-008 | Температурная квалификация контактов/кабеля исключена из текущей инженерной зоны | OWNER_SCOPE_EXTERNAL |
| Q-CON-009 | Контакт 12 — RESERVE | CLOSED |
| Q-CON-010 | Pin 11: ≤0,25 А continuous и ≤2 А / 150 мс | CLOSED_PRELIMINARY |
| Q-CON-011 | Пригодность pin 11 принята владельцем; F_CTRL/hold limits сохраняются | OWNER_ACCEPTED_ASSUMPTION |

## 2. Проверка KiCad и physical interfaces

| ID | Открытый вопрос | Статус |
|---|---|---|
| Q-SCH-006 | Какие physical interboard connectors и окончательный pinout применяются после CAN-FD/hard-line/power pin count? | OPEN_COMPONENT_SELECTION |
| Q-SCH-012 | Зафиксировать версию KiCad и ERC-report конкретного release commit перед schematic freeze | OPEN_RELEASE_VERIFICATION |

## 3. Фактическое поведение BMS

| ID | Открытый вопрос | Статус |
|---|---|---|
| Q-BMS-007 | Форма и скорость падения BAT_PROT при UV/OC/SCP | OPEN_TEST |
| Q-BMS-008 | Восстановление BAT_PROT после защиты и необходимость внешнего charge/reset | OPEN_TEST |

## 4. Выбор и испытание K_BATx

| ID | Открытый вопрос | Статус |
|---|---|---|
| Q-KBAT-010 | Guaranteed dropout range выбранного контактора | OPEN_CANDIDATE |
| Q-KBAT-014 | Поведение при медленном падении/восстановлении напряжения | OPEN_TEST |
| Q-KBAT-022 | Индуктивность катушки и энергия поля | OPEN_MEASUREMENT |
| Q-KBAT-023 | Поведение economizer при repeated start и brownout | OPEN_TEST |
| Q-KBAT-024 | Температура катушки при 16 В и Tmax | OPEN_THERMAL_TEST |
| Q-KBAT-025 | Конкретный suppression, обеспечивающий release ≤100 мс | OPEN_CALC_TEST |
| Q-KBAT-026 | DC breaking capacity кандидата 30 А/16 В для реальной L/R нагрузки | OPEN_CANDIDATE_TEST |
| Q-KBAT-027 | Рост сопротивления и температуры контакта после ресурса | OPEN_LIFE_TEST |
| Q-KBAT-028 | Vibration/shock profile по месту крепления корпуса и аппарата | OPEN_OWNER_INPUT_TEST_PROFILE |

## 5. LOCAL_START, REMOTE_OFF и fault injection

| ID | Открытый вопрос | Статус |
|---|---|---|
| Q-LS-008 | Схема диагностики сваривания K_BAT_AUX_NO | OPEN_DESIGN |
| Q-LS-009 | Bounce-test LOCAL_START 5…20 мс | OPEN_TEST |
| Q-LS-010 | Minimum wetting current AUX выбранного контактора | OPEN_CANDIDATE |
| Q-LS-011 | Окончательный F_CTRL по time-current curve и I²t | OPEN_CALC |
| Q-ROFF-008 | FMEA short pin 11 to BAT_PROT− и защита от bypass EXT_KILL | OPEN_FMEA_TEST |
| Q-ROFF-011 | Конкретное energize-to-run relay и DC rating с transient катушки | OPEN_CANDIDATE |

## 6. DECK_BALANCE

| ID | Открытый вопрос | Статус |
|---|---|---|
| Q-DB-004 | Maximum timeout и no-progress criterion DECK_BALANCE | OPEN_CALC_TEST |

## 7. Реализация системного power budget

| ID | Открытый вопрос | Статус |
|---|---|---|
| Q-SYS-004 | Допустимая длительность 44 А/22 А, measurement window и short-event criterion | OPEN_CALC_TEST |
| Q-SYS-005 | Фильтрация, debounce и hysteresis warning/block thresholds | OPEN_FIRMWARE_REQUIREMENT |
| Q-SYS-006 | Окончательная классификация external critical/noncritical loads и I_EXPECTED/I_INRUSH profiles | OPEN_OWNER_INPUT_DATA |
| Q-SYS-007 | Service override duration, authorization и automatic termination | OPEN_REQUIREMENT |

## 8. Механический envelope, pressure и thermal packaging

| ID | Открытый вопрос | Статус |
|---|---|---|
| Q-MECH-006 | Внутренний диаметр, стенка, материал, полезная длина и глубина захода крышки | OPEN_OWNER_INPUT |
| Q-MECH-007 | Чертёж/карта разъёмов крышки, типы вводов и внутренние cable tails | OPEN_OWNER_INPUT |
| Q-MECH-008 | Carrier/tray, точки крепления, число уровней, извлечение и service clearances | OPEN_MECHANICAL_DESIGN |
| Q-MECH-009 | Расчётная глубина, pressure test, vibration/shock и место крепления корпуса | OPEN_OWNER_INPUT_TEST_PROFILE |
| Q-MECH-010 | Тепловой контакт carrier/плат с корпусом и допустимая температура стенки | OPEN_THERMAL_INPUT |

## 9. Текущий Gate G-R

Закрыты owner-level вопросы V1.7:

1. current KiCad owner verification;
2. стартовый global power budget;
3. SINGLE_PACK_MODE;
4. warning/block policy;
5. environmental baseline;
6. external cylindrical envelope.

Полный Gate G-R остаётся заблокирован до:

1. BMS BAT_PROT fault/recovery tests;
2. candidate selection/tests K_BATx и REMOTE_OFF relay;
3. internal mechanical dimensions, pressure/vibration и 3D packaging;
4. physical CAN-FD/hard-line/power pin count и connector selection;
5. short-limit duration, filters/hysteresis и load profiles.

Разрешено начинать расчёты и component selection по узлам с закрытыми входными данными, если это не меняет замороженную архитектуру.

Подробности V1.7:

```text
Docs/OWNER_ANSWERS_REVIEW_V1_7.md
Docs/SYSTEM_POWER_BUDGET_POLICY.md
Docs/MECHANICAL_ENVELOPE_V1_7.md
Docs/adr/ADR-2026-07-21-owner-input-v1-7.md
```
