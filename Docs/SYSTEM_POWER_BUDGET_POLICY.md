# Системная политика power budget и SINGLE_PACK_MODE — PlataVM

Дата актуализации: 2026-07-21  
Основание: ответы владельца V1.7 и V1.8, Q-SYS-001…Q-SYS-007  
Статус: `V1.8 ACCEPTED POLICY; SERVICE OVERRIDE DISABLED PENDING OWNER DECISION`

## 1. Назначение

Документ задаёт общий эксплуатационный предел по `PACK_BUS`, правила `DUAL_PACK_RUN` и `SINGLE_PACK_MODE`, предупреждения GUI, admission control новых нагрузок, short-event timing и обработку неизвестных load profiles.

Документ не заменяет:

- BMS;
- предохранители;
- eFuse/high-side protection;
- локальные аппаратные ограничения PCB-C/D/E;
- `SAFE_OFF`, `HARD_OFF` и `EXT_KILL`;
- тепловой расчёт плат, шин, проводов и соединителей.

## 2. Разделение hardware rating и system operating limit

| Узел | Локальный предварительный rating |
|---|---:|
| PCB-C POWER_12V | 30 А continuous по плате |
| Один CH PCB-C | 3 А continuous, 5 А peak до 1 с |
| PCB-D 5V_SYS_BUS | 15 А continuous, 20 А short на 5 В |
| PCB-E LIGHT_POWER | 6 независимых LED-каналов |

Локальные максимумы не разрешаются одновременно автоматически. Системный режим определяется измеренным током `PACK_BUS` и числом подключённых исправных основных АКБ.

## 3. Активные системные пределы

| Режим | Continuous limit | Short limit | Short duration | Warning threshold |
|---|---:|---:|---:|---:|
| `DUAL_PACK_RUN` | 40 А | 44 А | ≤1 с | 34 А |
| `SINGLE_PACK_MODE` | 20 А | 22 А | ≤1 с | 17 А |

Повторный short-event:

```text
minimum interval = 10 s
```

Дополнительно применяется `I²t / thermal accumulator`. Если thermal accumulator не восстановился, новый short-event запрещается даже после истечения 10 с.

После 1 с действует continuous limit соответствующего режима.

## 4. Источник измерения

Power-budget manager использует:

1. `BAT1_ISENSE`;
2. `BAT2_ISENSE`;
3. при наличии — независимый датчик суммарного тока `PACK_BUS`;
4. `BAT1_PRESENT`, `BAT2_PRESENT`;
5. состояние MAIN_SW1/MAIN_SW2;
6. диагностику PCB-C/D/E как вторичный контроль.

Канонический ток разряда:

```text
I_PACK_DISCHARGE = max(0; I_BAT1_DISCHARGE + I_BAT2_DISCHARGE)
```

Расхождение независимого суммарного датчика и суммы ветвей формирует measurement diagnostic fault. Точный допуск определяется после выбора датчиков.

## 5. DUAL_PACK_RUN

Условия:

```text
BAT1 available and connected
BAT2 available and connected
no battery isolation fault
not DECK_BALANCE
```

Правила:

- обе исправные АКБ работают параллельно;
- continuous budget = 40 А;
- short budget = 44 А не более 1 с;
- warning threshold = 34 А;
- отдельный automatic brightness limit отсутствует;
- локальные ratings плат и каналов действуют дополнительно.

Потеря одной батареи вызывает `SINGLE_PACK_TRANSITION`.

## 6. SINGLE_PACK_TRANSITION

```text
обнаружено отсутствие или отключение одной батареи
→ подтвердить исправность оставшейся ветви
→ установить continuous budget = 20 А
→ установить short budget = 22 А / 1 с
→ сформировать degraded-mode warning
→ запретить DECK_BALANCE
→ перейти в SINGLE_PACK_MODE
```

Сам переход не выключает свет, 12 В или 5 В нагрузки.

Если оставшаяся батарея недоступна либо активирован `EXT_KILL/HARD_OFF`, переход в SINGLE_PACK_MODE запрещён и выполняется безопасное отключение.

## 7. SINGLE_PACK_MODE

Режим деградированный, но функциональный.

Доступны:

- PCB-B critical domain;
- связь, диагностика и журналирование;
- разрешённые оператором CH1…CH14;
- разрешённые оператором 5V_OUT1…5V_OUT10;
- LED1…LED6;
- GUI и сервисные функции, не отменяющие аппаратную безопасность.

Запрещены:

- `DECK_BALANCE`;
- автоматическое повторное подключение восстановившейся батареи;
- автоматическое расширение бюджета до 40/44 А без подтверждённого подключения второй ветви.

Фиксированного списка автоматически выключаемых пользовательских нагрузок нет.

GUI постоянно показывает:

```text
SINGLE_PACK_MODE ACTIVE
активная батарея
причина отсутствия второй батареи
напряжение и ток активной батареи
измеренный ток PACK_BUS
continuous limit = 20 А
short limit = 22 А / 1 с
процент использования бюджета
остаточный токовый бюджет
thermal accumulator state
```

## 8. Фильтрация измерения

Для программного budget manager применяется:

```text
low-pass time constant / averaging window = 100 ms
```

Эта фильтрация не используется для аппаратной защиты КЗ, `SAFE_OFF`, `HARD_OFF` или `EXT_KILL`.

## 9. Warning logic

Warning включается, если:

```text
I_PACK > 85 % active continuous limit
непрерывно не менее 250 ms
```

Численные пороги:

```text
DUAL_PACK_RUN: 34 А
SINGLE_PACK_MODE: 17 А
```

Warning снимается, если:

```text
I_PACK < 80 % active continuous limit
непрерывно не менее 2 s
```

Система:

1. отображает warning;
2. журналирует вход и выход из warning zone;
3. не меняет яркость;
4. не отключает уже работающие нагрузки;
5. продолжает обрабатывать новые команды через admission control.

## 10. Admission control новой нагрузки

Команда новой некритической нагрузки разрешается только при выполнении:

```text
I_MEASURED + I_EXPECTED_NEW_LOAD < I_CONT_LIMIT
```

Для пускового события дополнительно:

```text
I_MEASURED + I_INRUSH_NEW_LOAD ≤ I_SHORT_LIMIT
short duration ≤1 s
thermal accumulator permits event
```

Команда отклоняется, если:

- прогноз после включения достигает или превышает 100 % continuous limit;
- фактический ток уже достиг continuous limit;
- прогноз пускового тока превышает short limit;
- short cooldown 10 с не завершён;
- thermal accumulator не восстановился;
- load profile неизвестен и консервативный профиль не помещается в бюджет.

Новые команды снова разрешаются после:

```text
I_PACK < 90 % active continuous limit
непрерывно не менее 2 s
```

При отклонении команды:

- выход не включается;
- GUI показывает причину;
- событие журналируется;
- уже работающие нагрузки не изменяются.

## 11. Уже включённые нагрузки

Power-budget manager не выполняет автоматический load shedding уже включённых пользовательских нагрузок только из-за превышения программного бюджета.

Отключение допускается только:

1. локальной аппаратной защитой;
2. защитой ветви или BMS;
3. `SAFE_OFF`;
4. `HARD_OFF`;
5. `EXT_KILL`;
6. будущей отдельно утверждённой таблицей приоритетов.

До отдельного решения программный load shedding отсутствует.

## 12. Критические и некритические нагрузки

### 12.1 Critical domain

Критическими считаются:

```text
5V_CRIT
3V3_CRIT
supervisor
fault manager
external communication
internal safety/control communication
journal/log retention
```

### 12.2 Некритические внешние нагрузки

Для admission control некритическими считаются:

```text
CH1…CH14
5V_OUT1…5V_OUT10
LED1…LED6
```

Исключения отсутствуют, пока владелец не примет отдельное решение.

Аппаратная защита действует независимо от классификации.

## 13. Load profile database

Для каждого назначенного внешнего устройства хранятся:

```text
I_NOM
I_PEAK
T_PEAK
I_INRUSH
```

Дополнительно рекомендуется хранить:

```text
supply branch
channel ID
load type
startup retry policy
measured/declared source
profile revision
```

Если профиль отсутствует:

1. применяется консервативный максимальный профиль канала;
2. GUI показывает `LOAD_PROFILE_UNKNOWN`;
3. оптимистичная оценка тока запрещена;
4. после измерения профиль может быть уточнён с записью revision/source.

## 14. Short-event control

Short-event определяется как разрешённое превышение continuous limit при токе не выше short limit.

Правила:

```text
maximum event duration = 1 s
minimum cooldown = 10 s
I²t / thermal accumulator mandatory
```

Событие завершается при первом из условий:

- истекла 1 с;
- ток снизился ниже continuous limit;
- достигнут аппаратный порог защиты;
- активирован SAFE/HARD_OFF/EXT_KILL;
- thermal accumulator достиг предела.

Повторный short-event запрещён до завершения cooldown и восстановления accumulator.

## 15. Service override — назначение и текущий статус

Service override — это диагностическая возможность один раз разрешить команду, которую обычный software admission control отклонил бы из-за расчётного power budget.

Он предназначен только для:

- измерения фактического пускового тока новой нагрузки;
- проверки корректности load profile;
- стендовой диагностики одного канала;
- воспроизведения отказа под контролем инженера;
- проверки датчиков и журналирования.

Service override не увеличивает физическую способность батареи, BMS, разъёмов, дорожек или ключей. Он не отменяет:

- BMS;
- eFuse/fuse;
- overcurrent/thermal protection;
- `SAFE_OFF`;
- `HARD_OFF`;
- `EXT_KILL`;
- short limit;
- no-restart interlocks.

Риск режима: инженер может сознательно создать нагрузку выше normal software budget, что способно вызвать BMS trip, просадку PACK_BUS или потерю части функций. Поэтому режим требует отдельного решения владельца.

Текущий статус:

```text
SERVICE_OVERRIDE = DISABLED BY DEFAULT
Q-SYS-007 = OPEN_OWNER_DECISION_AFTER_EXPLANATION
```

До закрытия Q-SYS-007 production firmware не должна позволять обход admission control.

## 16. Предлагаемая защищённая реализация service override

Рекомендуемый вариант, если функция будет принята:

1. доступ только в `SERVICE_MODE`;
2. отдельное явное подтверждение в GUI;
3. действие только для одной выбранной команды;
4. максимальная длительность 60 с;
5. постоянный warning и обратный таймер;
6. полное журналирование режима, тока, оператора/сеанса, команды и результата;
7. автоматическая отмена при timeout;
8. автоматическая отмена при выходе из SERVICE_MODE;
9. автоматическая отмена при смене DUAL/SINGLE режима;
10. автоматическая отмена при communication loss;
11. автоматическая отмена при любом hardware fault;
12. автоматическая отмена при достижении short limit;
13. безусловная отмена при SAFE/HARD_OFF/EXT_KILL.

Этот раздел является предложением, а не принятым решением.

## 17. Возврат к DUAL_PACK_RUN

Восстановление BMS отсутствующей батареи не подключает K_BATx автоматически.

Возврат возможен только после:

1. подтверждения исправности второй батареи;
2. нового разрешённого `LOCAL_START`;
3. проверки разности напряжений;
4. запрета опасного прямого параллельного соединения;
5. при необходимости — `DECK_BALANCE` на палубе;
6. подтверждения обеих ветвей;
7. перевода бюджета с 20/22 А на 40/44 А.

## 18. Приоритеты команд

От высшего к низшему:

```text
EXT_KILL
HARD_OFF / hardware critical fault
local hardware protection
SAFE_OFF
battery isolation / no-restart interlock
short-limit / thermal-accumulator control
power-budget admission control
normal operator commands
service override, если впоследствии разрешён
```

Service override никогда не имеет приоритета над защитами.

## 19. Минимальная программа испытаний

1. warning ON/OFF в DUAL_PACK_RUN;
2. warning ON/OFF в SINGLE_PACK_MODE;
3. проверка low-pass 100 мс;
4. warning delay 250 мс;
5. warning clear 80 % / 2 с;
6. block новой нагрузки при прогнозе 100 %;
7. повторное разрешение ниже 90 % / 2 с;
8. short event 1 с;
9. cooldown 10 с;
10. повторяющиеся импульсы и I²t accumulator;
11. `LOAD_PROFILE_UNKNOWN` с консервативной оценкой;
12. потеря одной батареи при различных нагрузках;
13. отсутствие automatic brightness reduction;
14. отсутствие software load shedding уже включённых нагрузок;
15. восстановление BMS без automatic restart;
16. приоритет SAFE/HARD_OFF/EXT_KILL;
17. service override — только после отдельного принятия Q-SYS-007.
