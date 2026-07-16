# Открытые вопросы ПДУ БНПА / PlataVM V1.6

Дата пересмотра: 2026-07-16  
Источник: заполненная форма `Ответы_на_вопросы_ПДУ_БНПА_V1.6(1).docx`  
Статус: OWNER INPUT REVIEWED; Gate G-R остаётся открытым до закрытия разделов 2–7.

## 1. Закрытые и зафиксированные решения

| ID | Решение | Статус |
|---|---|---|
| Q-BFE-001 | Механическое соединение под нагрузкой не является штатной операцией | CLOSED |
| Q-BFE-002 | Обе исправные АКБ работают параллельно; межблочное выравнивание выполняется в DECK_BALANCE | CLOSED |
| Q-BFE-003A | Длина каждой батарейной кабельной сборки — 1 м | CLOSED |
| Q-BFE-004 | K_BAT1/K_BAT2 — однополюсные контакторы по плюсу | CLOSED |
| Q-BFE-005 | Центральный K_MAIN отсутствует; PACK_BUS — главная силовая шина | CLOSED |
| Q-BFE-006 | Штатный HARD_OFF: тяжёлые нагрузки → журнал → отключение электронных силовых трактов → разрыв hold loop K_BAT1/K_BAT2 → контроль токов и PACK_BUS | CLOSED |
| Q-BFE-007 | В корпусе АКБ не устанавливается дополнительная активная электроника | CLOSED |
| Q-BFE-008 | BMS работает автономно и не обязана передавать цифровую телеметрию | CLOSED |
| Q-BFE-009 | RS-485/CAN/UART через батарейный соединитель не используются | CLOSED |
| Q-BMS-001 | BMS рассматривается как закрытый двухполюсный защищённый источник BAT_PROT+ / BAT_PROT− | CLOSED |
| Q-BMS-002 | Raw-ветвь, внутренние точки и сигналы BMS не используются | CLOSED |
| Q-BMS-003 | Схема контактора не зависит от high-side/low-side топологии BMS | CLOSED |
| Q-KBAT-001 | K_BATx — моностабильный нормально разомкнутый SPST-NO контактор | CLOSED |
| Q-KBAT-002 | K_BATx имеет одну катушку непрерывного режима | CLOSED |
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
| Q-KBAT-016 | Главный контакт: минимум 30 А continuous, целевой класс 50 А и выше | CLOSED_PRELIMINARY |
| Q-KBAT-017 | DC breaking capacity: минимум 30 А при 16 В DC | CLOSED_PRELIMINARY |
| Q-KBAT-018 | Начальное сопротивление главного контакта ≤2 мОм, после ресурса ≤5 мОм | CLOSED_PRELIMINARY |
| Q-CON-001 | СН-176А-12 — единственный рабочий межкорпусный силовой вариант основных АКБ | CLOSED |
| Q-CON-002 | Контакты 1–5 — BAT+, контакты 6–10 — BAT− | CLOSED |
| Q-CON-005 | Контакт 11 — REMOTE_OFF / K_BAT_HOLD_RETURN | CLOSED |
| Q-CON-009 | Контакт 12 — резерв, пока не назначен | CLOSED |
| Q-CON-010 | Pin 11: ≤0,25 А continuous и ≤2 А / 150 мс | CLOSED_PRELIMINARY |
| Q-LS-001 | LOCAL_START выведен на отдельный двухконтактный разъём | CLOSED |
| Q-LS-002 | LOCAL_START — нормально разомкнутый пружинно-возвратный контакт без фиксации | CLOSED |
| Q-LS-003 | LOCAL_START включён параллельно K_BAT_AUX_NO | CLOSED |
| Q-LS-004 | K_BAT_AUX_NO: ≥0,5 А при 16 В DC и ≥2 А / 150 мс | CLOSED_PRELIMINARY |
| Q-LS-005 | LOCAL_START имеет рейтинг не ниже K_BAT_AUX_NO | CLOSED_PRELIMINARY |
| Q-ROFF-001 | REMOTE_OFF выполняется разрывом цепи удержания единственной катушки | CLOSED |
| Q-ROFF-002 | Восстановление REMOTE_OFF loop после отпускания не включает контактор повторно | CLOSED |
| Q-ROFF-003 | Pin 11 несёт ток катушки в пределах 0,25 А continuous и 2 А pulsed | CLOSED_PRELIMINARY |
| Q-ROFF-006 | t_OFF ≥ max(250 мс; 5 × t_release_max) | CLOSED_PRELIMINARY |
| Q-ROFF-007 | Программный loop восстанавливается только после выдержки времени и подтверждения OPEN | CLOSED |
| Q-KBAT-015 | Простой flyback-диод не принимается без проверки; анализируются TVS, bidirectional TVS и diode+resistor | CLOSED_DIRECTION |
| Q-P12-001 | Каналы сохраняют аппаратные имена CH1...CH14; назначения задаются программно | CLOSED |
| Q-P12-002 | Номинальный длительный ток каждого CH — 3 А | CLOSED |
| Q-P12-004 | CH12...CH14 Always-On monitored, но отключаются защитой, SAFE и HARD_OFF | CLOSED |
| Q-5V-001 | Внешних 5V_OUT — 10 | CLOSED |
| Q-5V-002 | Максимум одного 5V_OUT — 3 А | CLOSED |
| Q-5V-003 | Три 5 В выхода — Always-On monitored | CLOSED |
| Q-5V-004 | Токовая диагностика каждого 5V_OUT обязательна | CLOSED |
| Q-5V-005 | Общий лимит 5V_SYS_BUS: 15 А длительно, 20 А кратковременно | CLOSED_ASSUMPTION |
| Q-LGT-001 | Шесть световых каналов логически независимы | CLOSED |
| Q-LGT-002 | Расчётный максимум LED-тока — 1,05 А на матрицу | CLOSED_ASSUMPTION |
| Q-LGT-003 | Диагностика каждого LED-канала обязательна в первой версии | CLOSED |
| Q-IF-001 | Внешний CAN footprint — optional/DNP; baseline внешней связи остаётся RS-485 | CLOSED |
| Q-IF-003 | Внешний интерфейс ПДУ — изолированный RS-485 | CLOSED |
| Q-MECH-001 | Ширина каждого PCB-модуля не более 100 мм | CLOSED |
| Q-MECH-003 | Принята многоплатная архитектура из пяти функциональных PCB-модулей и пассивного INTERCONNECT | CLOSED |
| Q-SCH-001 | Принята иерархия листов из Docs/SCHEMATIC_ARCHITECTURE.md | CLOSED |
| Q-SCH-002 | Логические межплатные интерфейсы фиксируются до выбора физических разъёмов | CLOSED |
| Q-SCH-003 | Высокие токи распределяются от PCB-A и не проходят через PCB-B | CLOSED |
| Q-SCH-005 | Обычное управление и телеметрия PCB-B↔PCB-C/D/E передаются по внутренней CAN-FD; аппаратные SAFE/HARD_OFF и критические fault-линии остаются отдельными проводами | CLOSED_ARCHITECTURE |
| Q-SCH-007 | SIGNAL_GND соединяется с POWER_GND в одной контролируемой точке на PCB-B через net-tie/конфигурируемый элемент; другие прямые соединения запрещены | CLOSED_ARCHITECTURE |
| Q-SCH-008 | Экраны подключаются к CHASSIS у ввода; ISO_GND остаётся гальванически отделённым; допускается опциональная ВЧ-связь ISO_GND–CHASSIS после EMC-проверки | CLOSED_ARCHITECTURE |
| Q-SCH-009 | INTERCONNECT пассивный; PACK_BUS и мощные выходы идут отдельными шинами/жгутами, сигнальная backplane не несёт силовой ток | CLOSED |
| Q-SCH-010 | PCB-A размещается у батарейных вводов, PCB-B вдали от switching nodes, PCB-C/D/E у своих выходов; целевой логический жгут ≤300 мм | CLOSED_ARCHITECTURE |
| Q-SCH-011 | Reference designators: PCB-A 100–199, PCB-B 200–299, PCB-C 300–399, PCB-D 400–499, PCB-E 500–599 | CLOSED |
| Q-BMS-004 | Основные ячейки: Hunan Huaxing 32700-6000mAh LiFePO4, 3,2 В, 6 А·ч; сборка 4S24P = 12,8 В, 144 А·ч | CLOSED |
| Q-BMS-005 | Фактическая закупочная позиция BMS: LiFePO4 4S 12 V 30 A symmetric, 48volt.ru артикул 0102; производитель платы пока не идентифицирован | CLOSED_PRELIMINARY |
| Q-BMS-006 | По данным поставщика пороги защиты — 3,65 В/cell OV и 2,3 В/cell UV, ориентировочно 14,6/9,2 В для 4S; reconnect и задержки проверяются отдельно | CLOSED_PARTIAL |
| Q-BMS-009 | BMS main battery: 30 А continuous discharge, 40 А short-term, 60 А/1 с peak, 15 А continuous charge, 30 мА passive balance | CLOSED_PRELIMINARY |
| Q-LS-006 | F_CTRL размещается внутри каждого корпуса АКБ максимально близко к ответвлению BAT_PROT+ | CLOSED |
| Q-LS-007 | После восстановления питания запуск разрешается только после обнаружения отпущенного LOCAL_START; длительное замыкание считается fault | CLOSED_REQUIREMENT |
| Q-ROFF-004 | Программный REMOTE_OFF реализуется реле в energize-to-run: физический NO контакт замкнут только при healthy critical control; потеря питания открывает hold loop | CLOSED_ARCHITECTURE |
| Q-ROFF-005 | Для двух hold loop применяются два независимых последовательно включённых размыкающих контакта; аппаратный EXT_KILL действует независимо от MCU/RS-485 | CLOSED_ARCHITECTURE |
| Q-ROFF-009 | После OFF контролируются ток катушки, состояние контакта и PACK_BUS; при отсутствии OPEN за t_OFF фиксируется HARD_OFF_FAILED и запрещается restart | CLOSED_REQUIREMENT |
| Q-ROFF-010 | EXT_KILL включён последовательно после ветви LOCAL_START ∥ AUX_NO и имеет безусловный аппаратный приоритет | CLOSED_ARCHITECTURE |
| Q-ROFF-012 | Потеря 5V_CRIT/3V3_CRIT или healthy supervisor обесточивает REMOTE_OFF relay и разрывает hold loop | CLOSED_ARCHITECTURE |
| Q-KBAT-020 | Сваривание главного контакта диагностируется по напряжениям до/после K_BAT и току ветви; fault WELDED_CONTACT отображается в GUI и блокирует повторный запуск | CLOSED_REQUIREMENT |
| Q-KBAT-021 | Штатно: отключить нагрузки и электронные MAIN_SWx, дождаться снижения тока, затем разорвать hold loop; EXT_KILL может разорвать loop немедленно | CLOSED |
| Q-DB-001 | Паспортный максимум заряда BMS — 15 А; DECK_BALANCE остаётся отдельным ограниченным режимом 2 А nominal / 3 А hard limit | CLOSED_PRELIMINARY |
| Q-DB-002 | Номинальный ток DECK_BALANCE — 2 А | CLOSED_PRELIMINARY |
| Q-DB-003 | Максимальный ток DECK_BALANCE — 3 А с аппаратным/программным отключением по превышению | CLOSED_PRELIMINARY |
| Q-DB-005 | Стартовый критерий завершения: abs(ΔU) ≤50 мВ и abs(I) ≤0,2 А в течение 60 с; значения конфигурируемы после испытаний | CLOSED_PRELIMINARY |
| Q-DB-006 | Дополнительные датчики температуры в АКБ не добавляются; DECK_BALANCE разрешён только при подтверждённой температуре батарей 0…45 °C | CLOSED_OWNER_DECISION |
| Q-P12-003 | На канал PCB-C: 3 А continuous, 5 А peak до 1 с, индивидуальное ограничение и защита | CLOSED_PRELIMINARY |
| Q-P12-005 | POWER_12V_BUS и PCB-C проектируются на 30 А continuous как аппаратный рейтинг; фактическая одновременная нагрузка определяется общим power budget | CLOSED_PRELIMINARY |
| Q-P12-006 | PCB-C имеет локальный protected I/O/ADC и узел внутренней CAN-FD; аппаратные SAFE/HARD_OFF остаются прямыми | CLOSED_ARCHITECTURE |
| Q-5V-006 | OUT8…OUT10 — аппаратные Always-On monitored без жёсткого назначения; функции задаются в GUI | CLOSED |
| Q-5V-007 | Базовая топология 5V_SYS_BUS — двухфазный синхронный buck 15 А continuous / 20 А short с внешними MOSFET и тепловым отводом на корпус | CLOSED_TOPOLOGY_PRELIMINARY |
| Q-5V-008 | PCB-D имеет локальный I/O/ADC и внутреннюю CAN-FD; hard-off остаётся отдельной аппаратной линией | CLOSED_ARCHITECTURE |
| Q-LGT-004 | PCB-E делится на две симметричные силовые зоны 2×3 при сохранении шести независимых каналов | CLOSED |
| Q-LGT-005 | LED-driver: functional input 8…16 В, nominal protected range ориентировочно 9,2…14,6 В, отдельный transient margin | CLOSED_PRELIMINARY |
| Q-LGT-006 | Отдельный программный лимит яркости для SINGLE_PACK_MODE не вводится; полный свет разрешён, а защита выполняется аппаратными ограничителями/BMS с отображением перегрузок в GUI | CLOSED_OWNER_DECISION |
| Q-LGT-007 | PWM: 3,3 В active-high, default 1 кГц, конфигурируемый диапазон 100…1000 Гц; вход драйвера допускает level-shift option | CLOSED_PRELIMINARY |
| Q-IF-002 | Внешний RS-485: 115200 bit/s, half-duplex, 8N1, адресный бинарный протокол, CRC-16, sequence number, timeout и heartbeat | CLOSED_PRELIMINARY |
| Q-MCU-001 | Базовое семейство центрального и локальных контроллеров — STM32G4; конкретные корпуса выбираются после pin count | CLOSED_FAMILY |
| Q-MECH-002 | Электроника и межплатные разъёмы находятся в сухом закрытом корпусе; герметичность внутренних разъёмов не требуется, финальные part numbers выбираются при component selection | CLOSED_SCOPE |
| Q-MECH-005 | Гибрид: отдельные силовые шины/жгуты для PACK_BUS/load power и пассивный сигнальный INTERCONNECT/backplane | CLOSED_ARCHITECTURE |

### 1.1 Батарейная линия СН-176А-12 — owner-controlled scope

Владелец проекта исключил этот раздел из текущей зоны инженерной диагностики и рекомендаций. Ограничения всё равно учитываются как внешние входные данные системы.

| ID | Решение владельца / внешнее ограничение | Статус |
|---|---|---|
| Q-CON-003 | Владелец задаёт целевой предел батарейной линии 20 А continuous / 22 А short. Для работы на воздухе до отдельного подтверждения действует паспортный предел 17,5 А. | OWNER_CONTROLLED_PRELIMINARY |
| Q-CON-004 | Состав кабеля К25 принят соответствующим паспорту поставщика. | OWNER_CONFIRMED |
| Q-CON-006 | Нумерация контактов 1–12 подтверждена владельцем. | OWNER_CONFIRMED |
| Q-CON-007 | Равномерность распределения по пяти параллельным контактам принята владельцем; инженерная верификация исключена из текущего scope. | OWNER_ACCEPTED_ASSUMPTION |
| Q-CON-008 | Температурная квалификация контактов/кабеля исключена владельцем из текущей зоны диагностики и рекомендаций. | OWNER_SCOPE_EXTERNAL |
| Q-CON-011 | Пригодность pin 11 для 2 А/150 мс и 0,25 А continuous принята владельцем; F_CTRL и hold-current limits сохраняются. | OWNER_ACCEPTED_ASSUMPTION |

## 2. Проверка KiCad и физическая компоновка

| ID | Открытый вопрос | Статус |
|---|---|---|
| Q-SCH-004 | Открывается ли текущий root project и все листы 00…56 в установленной версии KiCad без parsing/ERC errors? | OPEN_VERIFICATION |
| Q-SCH-006 | Какие физические межплатные разъёмы и окончательный pinout применяются после CAN-FD и hard-line pin count? | OPEN_COMPONENT_SELECTION |
| Q-MECH-004 | Каковы окончательные длины, расположение и 3D-компоновка PCB-A…PCB-E? | OPEN_3D_LAYOUT |

## 3. Фактическое поведение BMS

| ID | Открытый вопрос | Статус |
|---|---|---|
| Q-BMS-007 | Какова форма и скорость падения BAT_PROT при UV/OC/SCP? Важно для исключения chatter, затяжного отпускания и дуги K_BATx. | OPEN_TEST |
| Q-BMS-008 | Как BAT_PROT восстанавливается после защиты и требуется ли внешнее зарядное напряжение/сброс? | OPEN_TEST |

## 4. Выбор и испытание K_BATx

| ID | Открытый вопрос | Статус |
|---|---|---|
| Q-KBAT-010 | Гарантированный dropout диапазон выбранного контактора. | OPEN_CANDIDATE |
| Q-KBAT-014 | Поведение контактора при медленном падении/восстановлении напряжения. | OPEN_TEST |
| Q-KBAT-022 | Индуктивность катушки и энергия поля. | OPEN_MEASUREMENT |
| Q-KBAT-023 | Поведение economizer при повторном старте и brownout. | OPEN_TEST |
| Q-KBAT-024 | Температура катушки при 16 В и Tmax. | OPEN_THERMAL_TEST |
| Q-KBAT-025 | Конкретный suppression, обеспечивающий release ≤100 мс. | OPEN_CALC_TEST |
| Q-KBAT-019 | Требования к температуре, вибрации, влажности/конденсации и ресурсу. | OPEN_OWNER_INPUT |
| Q-KBAT-026 | DC breaking capacity кандидата 30 А/16 В для реальной L/R нагрузки. | OPEN_CANDIDATE_TEST |
| Q-KBAT-027 | Рост сопротивления и температуры контакта после ресурса. | OPEN_LIFE_TEST |

## 5. LOCAL_START, REMOTE_OFF и fault injection

| ID | Открытый вопрос | Статус |
|---|---|---|
| Q-LS-008 | Схема диагностики сваривания K_BAT_AUX_NO. | OPEN_DESIGN |
| Q-LS-009 | Bounce-test LOCAL_START 5…20 мс. | OPEN_TEST |
| Q-LS-010 | Minimum wetting current AUX выбранного контактора. | OPEN_CANDIDATE |
| Q-LS-011 | Окончательный F_CTRL по time-current curve и I²t. | OPEN_CALC |
| Q-ROFF-008 | FMEA короткого замыкания pin 11 на BAT_PROT− и защита от обхода EXT_KILL. | OPEN_FMEA_TEST |
| Q-ROFF-011 | Конкретное energize-to-run relay и его DC rating с учётом transient катушки. | OPEN_CANDIDATE |

## 6. DECK_BALANCE

| ID | Открытый вопрос | Статус |
|---|---|---|
| Q-DB-004 | Максимальный тайм-аут DECK_BALANCE и критерий отсутствия прогресса. | OPEN_CALC_TEST |

## 7. Общий системный power budget

| ID | Открытый вопрос | Статус |
|---|---|---|
| Q-SYS-001 | Какие максимальные нагрузки POWER_12V_BUS, 5V_SYS_BUS и LIGHT_POWER_BRANCH разрешены одновременно? | OPEN_OWNER_INPUT |
| Q-SYS-002 | Является ли SINGLE_PACK_MODE полноценным режимом с полным светом и 12/5 В нагрузками либо только деградированным/аварийным режимом? | OPEN_OWNER_INPUT |
| Q-SYS-003 | При прогнозе перегрузки система только предупреждает пользователя либо запрещает несовместимую комбинацию команд? | OPEN_OWNER_INPUT |

## 8. Gate G-R

Переход к component selection разрешается по узлам, для которых закрыты входные данные. Полный Gate G-R остаётся заблокирован до:

1. KiCad verification текущего workspace;
2. выбора и испытания K_BATx/REMOTE_OFF relay;
3. закрытия global simultaneous-load matrix;
4. определения 3D-компоновки и межплатных разъёмов;
5. выполнения BMS BAT_PROT fault/recovery tests.

Численные решения V1.6 и замечания приведены в `Docs/OWNER_ANSWERS_REVIEW_V1_6.md` и ADR `Docs/adr/ADR-2026-07-16-owner-input-v1-6.md`.
