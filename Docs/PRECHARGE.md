# PRECHARGE

## 1. Назначение

PRECHARGE ограничивает бросок тока при заряде ёмкости MAIN_INPUT_BUS до включения BATTERY_DISCONNECT.

## 2. Базовая структура

```text
PACK_BUS → F_pre → SW_pre → R_pre → MAIN_INPUT_BUS
```

## 3. Последовательность включения

1. Проверить PACK_BUS.
2. Проверить отсутствие HARD FAULT.
3. Включить SW_pre.
4. Контролировать рост напряжения MAIN_INPUT_BUS.
5. Дождаться заданного процента предзаряда.
6. Включить BATTERY_DISCONNECT.
7. Отключить SW_pre.
8. Перейти в BOOT/RUN.

## 4. Открытые расчёты

1. Ёмкость MAIN_INPUT_BUS.
2. Допустимый ток precharge.
3. Номинал R_pre.
4. Энергия на R_pre.
5. Время precharge.
6. Порог завершения precharge.