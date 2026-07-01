# RESERVE_BRANCH / KEEP_ALIVE / CRITICAL POWER

## 1. Назначение

RESERVE_BRANCH обеспечивает аварийную живучесть управления после потери основной шины.

## 2. Источник

```text
EMG_4S2P / АКБ_RES → critical power path → 5V_CRIT → 3V3_CRIT
```

## 3. Что питает резерв

1. MCU.
2. RS-485 critical side.
3. Критические датчики.
4. Fault manager.
5. Event log.
6. Watchdog/supervisor.
7. Логика SAFE/HARD OFF.

## 4. Что резерв не питает

1. POWER_12V_BUS.
2. 5V_SYS_BUS.
3. LIGHT_POWER_BRANCH.
4. Внешние силовые нагрузки.

## 5. Требование keep-alive

Минимальное целевое время — 30 минут. Требует расчёта по реальному потреблению 5V_CRIT/3V3_CRIT.

## 6. Логика потери основных АКБ

```text
оба PACK_PRESENT lost → SAFE → 7 секунд → HARD OFF
```