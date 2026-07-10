# Архитектура управления V1.5

## 1. Верхний уровень

```text
HOST / Computer → isolated RS-485 → MCU → FSM / Fault Manager / Telemetry
```

## 2. Граница управления батарейными корпусами

BMS каждой основной АКБ работает автономно. MCU не взаимодействует с BMS через цифровые или дискретные сигналы и не использует её внутренние точки.

Для управления контактором доступны только:

1. локальный механический `LOCAL_START` на корпусе АКБ;
2. цепь `REMOTE_OFF / K_BAT_HOLD_RETURN` через контакт 11 СН-176А-12;
3. измерения напряжения и тока в корпусе электроники.

## 3. MCU управляет

1. Battery Front-End #1 и #2.
2. Электронными силовыми трактами `MAIN_SW1` и `MAIN_SW2`.
3. Ограниченными трактами `BALANCE_SW1 + R_BAL1` и `BALANCE_SW2 + R_BAL2`.
4. Программными запросами разрыва `BAT1_HOLD_LOOP` и `BAT2_HOLD_LOOP`.
5. `POWER_12V_BUS` CH1...CH14.
6. `5V_SYS_BUS` и 10 выходами 5 В.
7. `LIGHT_POWER_BRANCH` и шестью световыми каналами.
8. `RESERVE_BRANCH` и зарядом EMG.
9. Телеметрией, оценкой SoC и журналом событий.
10. Режимом `DECK_BALANCE`.

MCU не выполняет электрическое включение K_BAT1/K_BAT2. Включение выполняется только вручную через LOCAL_START. MCU может разрешать или запрещать удержание посредством REMOTE_OFF loop после появления питания корпуса электроники.

Центральные `K_MAIN` и `MAIN_INPUT_BUS` не используются.

## 4. Аппаратное управление вне MCU

`EXT_KILL` независимо от MCU:

1. размыкает BAT1_HOLD_LOOP;
2. размыкает BAT2_HOLD_LOOP;
3. отключает MAIN_SW1;
4. отключает MAIN_SW2;
5. блокирует повторный LOCAL_START до ручного сброса аварии.

## 5. Состояния MCU

```text
OFF
BOOT
SELF_TEST
DECK_BALANCE
RUN
SAFE
KEEP_ALIVE
HARD_OFF
FAULT_LATCH
```

Различия напряжений, токов и расчётного SoC батарейных ветвей являются диагностическими параметрами и не требуют отдельного состояния FSM.

## 6. Запуск батарейной ветви

Физическая последовательность:

```text
BMS protected output available
+ REMOTE_OFF/EXT_KILL loop closed
+ operator presses LOCAL_START
→ K_BAT coil energized
→ K_BAT main contact CLOSED
→ K_BAT_AUX_NO CLOSED
→ electrical self-hold
→ voltage appears at BFE input
```

Логическая последовательность после появления батарейной линии:

```text
BATx_PRESENT detected
→ keep MAIN_SWx disabled
→ measure BATx_RAW_V and BATx_I
→ perform branch self-test
→ compare with PACK_BUS limits
→ enable controlled connection path
→ enter RUN when all conditions are satisfied
```

## 7. RUN

Обе исправные основные АКБ работают параллельно. MCU измеряет ток, напряжение и расчётный SoC каждой ветви, но не отключает батарею только из-за различия уровня заряда.

В RUN:

1. K_BAT1/K_BAT2 удерживаются собственными катушками;
2. MAIN_SW1/MAIN_SW2 обеспечивают быстрое электронное управление и защиту;
3. состояние ветвей контролируется по BATx_RAW_V, BATx_I и PACK_BUS_V;
4. потеря выхода BMS автоматически отпускает соответствующий K_BATx.

## 8. Потеря и восстановление выхода BMS

```text
BMS protected output lost
→ coil de-energized
→ K_BATx OPEN
→ BATx_PRESENT lost
→ MAIN_SWx disabled
→ event logged
```

После восстановления BMS:

```text
K_BATx remains OPEN
→ branch does not return to RUN automatically
→ operator must perform LOCAL_START
→ branch SELF_TEST repeats
```

## 9. DECK_BALANCE

На палубе MCU:

1. отключает тяжёлые нагрузки;
2. измеряет состояние обеих АКБ;
3. включает ограниченный балансировочный тракт;
4. контролирует ток, внешнюю температуру и время;
5. завершает балансировку по заданным критериям;
6. при необходимости обслуживает заряд EMG.

## 10. HARD_OFF

### Штатный

```text
снять тяжёлые нагрузки
→ сохранить журнал и SoC
→ BAT1_HOLD_LOOP open
→ verify K_BAT1 OPEN
→ BAT2_HOLD_LOOP open
→ verify K_BAT2 OPEN
→ проверить токи ветвей и PACK_BUS
→ завершить работу от EMG
```

### Аварийный

```text
EXT_KILL / critical fault
→ hardware BAT1_HOLD_LOOP open
→ hardware BAT2_HOLD_LOOP open
→ MAIN_SW1 OFF
→ MAIN_SW2 OFF
→ FAULT_LATCH
→ сохранить причину события от EMG
```

## 11. Контроль результата

MCU оценивает физическое отключение по:

1. факту команды hold-loop open;
2. времени отпускания;
3. BATx_RAW_V;
4. BATx_I;
5. PACK_BUS_V.

Отсутствие ожидаемой реакции приводит к отключению MAIN_SWx и регистрации возможного сваривания контактора или отказа REMOTE_OFF.

## 12. Сервисные интерфейсы

1. UART — debug/service внутри корпуса электроники.
2. SWD — программирование и отладка.
3. CAN/CAN-FD — optional future footprint, не baseline.
4. Сервисные интерфейсы не проходят в корпуса основных АКБ.
