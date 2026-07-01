# ADR-2026-06-30: Фиксация мастер-концепции ПДУ БНПА V1.4

Статус:

```text
superseded by ADR-2026-07-01-pdu-v1-5-integrated-tobe-baseline.md
```

## Контекст

Этот ADR фиксировал промежуточную базу V1.4. После интеграции TO-BE решений проект переведён на `V1.5 integrated TO-BE baseline`.

## Что сохранено

1. Основные АКБ LiFePO4.
2. EMG как критический резерв.
3. Запрет питания силовых нагрузок от EMG.
4. RS-485 как основной интерфейс.
5. Требование отдельной архитектурной базы.

## Что изменено в V1.5

1. BAT_BUS_4S заменён архитектурной иерархией PACK_BUS / MAIN_INPUT_BUS.
2. AUX1...AUX4 заменены на POWER_12V_BUS CH1...CH14.
3. Добавлена отдельная 5V_SYS_BUS.
4. Световая ветвь переведена на onboard LED drivers.
5. BATTERY_DISCONNECT и PRECHARGE выделены как обязательные узлы.

Актуальная архитектура описана в `Docs/PROJECT_MASTER.md`, `Docs/ARCHITECTURE_BASELINE.md` и ADR V1.5.