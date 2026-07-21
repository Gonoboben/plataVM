# Хронология: применение ответов владельца V1.8

Дата: 2026-07-21  
Предыдущая опорная точка: merge PR #36  
Источник: `Ответы_на_вопросы_ПДУ_БНПА_V1.8(1).docx`

## 1. Проверенные вопросы

```text
Q-MECH-006
Q-MECH-007
Q-MECH-008
Q-MECH-009
Q-MECH-010
Q-SYS-004
Q-SYS-005
Q-SYS-006
Q-SYS-007
```

## 2. Принятые механические решения

1. Внутренний owner-defined цилиндрический envelope: Ø130 мм × 1000 мм.
2. Рабочий envelope электронной сборки: 100 × 250 × 80 мм.
3. Компоновка многоуровневая.
4. Вся электроника извлекается вместе с крышкой.
5. Платы крепятся винтами к стойкам.
6. Винты и стойки выбирает владелец; PCB должны иметь монтажные отверстия.
7. Обязательный отдельный carrier/tray отменён.
8. Карта разъёмов крышки не является блокером текущего PCB architecture step.
9. Pressure-hull design находится вне scope электроники.
10. Пайка и винтовое крепление — основные способы удержания компонентов.
11. Полиэтиленовый hot-melt adhesive допускается как вспомогательная фиксация.
12. Тепловой контакт с корпусом запрещён.
13. Охлаждение — малое тепловыделение, PCB copper и внутренняя естественная конвекция.
14. Thermal verification выполняется в закрытом объёме при +60 °C без hull heat sink.

## 3. Принятые параметры power-budget manager

1. Short-limit 44 А/22 А разрешён не более 1 с.
2. Повторный short-event — не ранее чем через 10 с.
3. Повторяющиеся события контролируются I²t/thermal accumulator.
4. Budget low-pass — 100 мс.
5. Warning ON — выше 85 % непрерывно 250 мс.
6. Warning OFF — ниже 80 % непрерывно 2 с.
7. Новая некритическая команда блокируется при прогнозе ≥100 % либо фактическом достижении continuous limit.
8. Повторное разрешение — ниже 90 % в течение 2 с.
9. Critical domain ограничен PCB-B critical power, supervisor, fault manager, communication и journal retention.
10. Все внешние CH, 5V_OUT и LED — некритические для admission control.
11. Для нагрузок хранятся I_NOM, I_PEAK, T_PEAK и I_INRUSH.
12. Неизвестный профиль использует консервативный максимум и `LOAD_PROFILE_UNKNOWN`.

## 4. Открытый вопрос

```text
Q-SYS-007 — service override
```

Владелец запросил подробное объяснение назначения режима.

До решения:

```text
SERVICE_OVERRIDE = DISABLED BY DEFAULT
```

## 5. Исправленные прежние допущения

Отменены:

- обязательный продольный carrier/tray;
- обязательный thermal path к корпусу;
- предварительный thermal contact PCB-D с корпусом;
- требование получить pressure-hull данные до продолжения PCB architecture;
- требование получить карту крышки до текущей компоновки.

## 6. Сохранённая архитектура

Не изменены:

- две основные АКБ 4S24P;
- PACK_BUS;
- отсутствие K_MAIN;
- независимые BFE_1/BFE_2;
- K_BAT1/K_BAT2;
- EXT_KILL;
- no-restart after BMS recovery;
- PCB-A…PCB-E;
- внутренний CAN-FD и hard safety lines;
- пассивный INTERCONNECT;
- отдельные ground domains.

## 7. Следующая последовательность

```text
PCB envelope 100 × 250 × 80 мм
→ preliminary board outlines
→ mounting-hole and multilevel stack concept
→ large-component placement
→ internal power/signal harness concept
→ thermal loss budget without hull contact
→ physical pin count and connector selection
→ subsystem calculations and component selection
```

Q-SYS-007 закрывается отдельным решением владельца после объяснения service override.
