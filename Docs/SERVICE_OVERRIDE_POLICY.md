# Политика защищённого SERVICE_OVERRIDE — PlataVM V1.9

Дата фиксации: 2026-07-21  
Основание: решение владельца по Q-SYS-007 — вариант B  
Статус: `ACCEPTED GUARDED SERVICE FUNCTION`

## 1. Назначение

`SERVICE_OVERRIDE` — диагностический режим, позволяющий однократно выполнить команду включения внешней некритической нагрузки, которую обычный software power-budget admission control заблокировал бы из-за прогнозируемого превышения continuous budget.

Режим предназначен только для:

1. измерения фактического пускового и установившегося тока нагрузки;
2. уточнения `LOAD_PROFILE`;
3. проверки одного канала PCB-C, PCB-D или PCB-E;
4. калибровки измерительного тракта;
5. воспроизведения отказа на стенде;
6. проверки диагностик и журналирования.

`SERVICE_OVERRIDE` не является эксплуатационным режимом и не увеличивает допустимую мощность батарей, BMS, кабелей, шин, плат или разъёмов.

## 2. Граница обхода

Режим может обойти только программный запрет новой некритической команды по continuous budget.

Режим не может отключить, изменить или обойти:

```text
BMS
предохранители
eFuse / high-side protection
overcurrent protection
short-circuit protection
thermal protection
SAFE_OFF
HARD_OFF
EXT_KILL
K_BAT no-restart interlock
DECK_BALANCE interlocks
44 А / 22 А short limits
I²t / thermal accumulator
```

Любое аппаратное ограничение имеет приоритет.

## 3. Допустимые объекты управления

Разрешены только внешние некритические выходы:

```text
PCB-C: CH1…CH14
PCB-D: 5V_OUT1…5V_OUT10
PCB-E: LED1…LED6
```

Запрещено применять override к:

```text
K_BAT1 / K_BAT2
MAIN_SW1 / MAIN_SW2
BALANCE_SW1 / BALANCE_SW2
PACK_BUS_DISCHARGE
5V_CRIT / 3V3_CRIT
supervisor / watchdog / fault manager
REMOTE_OFF
SAFE_OFF / HARD_OFF / EXT_KILL
CAN-FD safety fallbacks
firmware update and boot control
```

## 4. Вход в SERVICE_MODE

`SERVICE_OVERRIDE` доступен только внутри подтверждённого `SERVICE_MODE`.

Минимальные требования к входу:

1. оператор должен перейти в отдельный сервисный экран;
2. требуется явная авторизация сервисного уровня;
3. GUI показывает предупреждение о возможной просадке PACK_BUS, BMS trip и потере функций;
4. оператор выполняет двойное подтверждение;
5. выбирается ровно один выход и одна команда;
6. перед выдачей разрешения проверяются текущие faults, режим АКБ и измеренный ток.

Конкретный механизм авторизации определяется firmware/UI implementation и не требует отдельного аппаратного bypass-переключателя.

## 5. Длительность

Разделяются два времени.

### 5.1 Окно разрешения

После двойного подтверждения создаётся одноразовое окно:

```text
T_SERVICE_AUTH = 60 с
```

В течение этого времени может быть выполнена только одна выбранная команда. Неиспользованное разрешение автоматически аннулируется по тайм-ауту.

### 5.2 Реальное превышение continuous budget

`SERVICE_OVERRIDE` не изменяет short policy:

```text
DUAL_PACK_RUN: 44 А не более 1 с
SINGLE_PACK_MODE: 22 А не более 1 с
repeat interval ≥10 с
I²t / thermal accumulator обязателен
```

Если после включения выбранного выхода измеренный ток остаётся выше active continuous limit дольше 1 с, система отключает именно overridden output.

Это специальное завершение диагностической команды и не является общим software load shedding остальных уже работающих нагрузок.

## 6. Проверка перед включением

Команда override допускается только при выполнении всех условий:

```text
SERVICE_MODE active
нет active hardware fault
нет SAFE_OFF / HARD_OFF / EXT_KILL
выбран только один разрешённый output
I_MEASURED < I_SHORT_LIMIT
I_MEASURED + I_INRUSH_EXPECTED ≤ I_SHORT_LIMIT
short cooldown завершён
I²t accumulator разрешает событие
```

Если `LOAD_PROFILE_UNKNOWN`, используется консервативный максимальный профиль канала.

Override не разрешает команду, которая по прогнозу превышает short limit.

## 7. Поведение после включения

Последовательность:

```text
SERVICE_OVERRIDE_ARMED
→ включение выбранного выхода
→ измерение I_INRUSH и I_SETTLED
→ запись waveform summary
→ проверка short-duration и I²t
→ работа до завершения диагностического окна
→ автоматическое отключение выбранного выхода
→ сохранение результата
→ SERVICE_OVERRIDE_COMPLETE
```

Максимальная длительность включённого overridden output:

```text
T_OVERRIDE_OUTPUT_MAX = 60 с
```

При истечении времени выбранный выход автоматически отключается.

Если нагрузка после пуска укладывается в обычный continuous budget, оператор может затем включить её обычной командой после завершения override и повторной штатной admission check.

## 8. Автоматическая отмена

Разрешение и активная команда немедленно отменяются при:

1. истечении 60 с;
2. выходе из `SERVICE_MODE`;
3. потере связи с управляющим интерфейсом;
4. перезапуске MCU;
5. смене `DUAL_PACK_RUN` / `SINGLE_PACK_MODE`;
6. потере или подключении батарейной ветви;
7. любом новом hardware fault;
8. достижении short limit;
9. превышении continuous limit более 1 с;
10. запрете I²t accumulator;
11. `SAFE_OFF`;
12. `HARD_OFF`;
13. `EXT_KILL`.

При отмене отключается только выбранный overridden output, если аппаратная защита не требует более широкого отключения.

## 9. GUI

Во время режима GUI постоянно отображает:

```text
SERVICE MODE
SERVICE OVERRIDE ACTIVE
выбранный output
активный DUAL/SINGLE режим
I_PACK
continuous limit
short limit
время разрешения
время активности output
предупреждение о диагностическом риске
```

Цветовая и звуковая индикация должна отличаться от штатного режима.

Команда не должна быть доступна из обычного эксплуатационного экрана.

## 10. Журналирование

Обязательные поля события:

```text
timestamp
operator/session ID
firmware version
project/configuration ID
DUAL_PACK_RUN or SINGLE_PACK_MODE
active battery state
selected output
commanded state/setpoint
I_PACK before command
BAT1_ISENSE / BAT2_ISENSE
I_EXPECTED
I_INRUSH_EXPECTED
measured I_PEAK
measured T_PEAK
measured I_SETTLED
minimum PACK_BUS voltage
termination reason
faults during event
final output state
```

События журнала:

```text
SERVICE_OVERRIDE_REQUESTED
SERVICE_OVERRIDE_ARMED
SERVICE_OVERRIDE_STARTED
SERVICE_OVERRIDE_CANCELLED
SERVICE_OVERRIDE_TIMEOUT
SERVICE_OVERRIDE_SHORT_LIMIT
SERVICE_OVERRIDE_COMPLETE
```

## 11. Состояния firmware

```text
DISABLED
→ SERVICE_MODE_READY
→ OVERRIDE_REQUESTED
→ OVERRIDE_ARMED
→ OVERRIDE_ACTIVE
→ OVERRIDE_COMPLETE
```

Переход в `OVERRIDE_ACTIVE` возможен только после всех interlocks.

Любой safety event переводит состояние в `DISABLED` или `FAULT_LOCKED` согласно общей state machine.

## 12. Значение по умолчанию

В обычной эксплуатации:

```text
SERVICE_OVERRIDE = DISABLED
```

После включения питания, reset, firmware update, потери связи или выхода из SERVICE_MODE override всегда возвращается в disabled.

Состояние override не сохраняется как автоматически восстанавливаемое.

## 13. Испытания

Минимальная программа:

1. попытка override без SERVICE_MODE;
2. отмена на первом и втором подтверждении;
3. тайм-аут неиспользованного разрешения;
4. запуск одного разрешённого выхода;
5. запрет второго выхода;
6. predicted current выше short limit;
7. ток выше continuous менее 1 с;
8. ток выше continuous более 1 с;
9. истечение 60 с;
10. потеря связи;
11. смена DUAL/SINGLE режима;
12. BMS/fault event;
13. SAFE_OFF;
14. HARD_OFF;
15. EXT_KILL;
16. reset MCU;
17. проверка полноты журнала;
18. доказательство невозможности override критических и батарейных команд.

## 14. Закрытие вопроса

```text
Q-SYS-007 = CLOSED_OWNER_DECISION
SERVICE_OVERRIDE = GUARDED SERVICE FUNCTION
```
