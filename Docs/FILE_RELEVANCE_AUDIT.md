# Аудит актуальности файлов проекта

## 1. Интегрировано в V1.5

1. TO-BE Power: MAIN_INPUT_BUS, POWER_12V_BUS, LIGHT_POWER_BRANCH, RESERVE_BRANCH.
2. TO-BE Control: FSM, SAFE → 7 секунд → HARD OFF, DECK_BALANCE, KEEP_ALIVE.
3. BATTERY_DISCONNECT: HARD OFF, EXT_KILL, PRECHARGE.
4. Аналитический отчёт: Battery Front-End, измерения 2%, логирование 10 Гц, SoC через токовый учёт.

## 2. Пересмотрено

1. 10 каналов POWER_12V_BUS заменены на 14 каналов.
2. 2 Always-On заменены на 3 Always-On.
3. TRACO исключён из целевой архитектуры новой платы.
4. CAN/CAN-FD переведён из baseline в optional future.
5. RS-485 принят как baseline.

## 3. Legacy

TRACO POWER TEP 100-1216 ×3 описывает существующую систему, но не целевую V1.5.