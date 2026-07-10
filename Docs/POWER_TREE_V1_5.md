# Дерево питания ПДУ БНПА V1.5

## 1. Схема верхнего уровня

```text
АКБ_1 → autonomous BMS → protected output → fuse → K_BAT1 → СН-176А-12 → BFE_1 ┐
                                                                                      ├→ PACK_BUS
АКБ_2 → autonomous BMS → protected output → fuse → K_BAT2 → СН-176А-12 → BFE_2 ┘

PACK_BUS
    ├─ POWER_12V_BUS → CH1...CH14
    ├─ 5V_SYS_BUS → 5V_OUT1...5V_OUT10
    ├─ LIGHT_POWER_BRANCH → LED drivers → 6 × Epistar XY-J45
    └─ RESERVE_BRANCH → EMG charge path / KEEP_ALIVE / 5V_CRIT / 3V3_CRIT
```

## 2. Главная силовая шина

`PACK_BUS` является единственной главной силовой шиной после двух управляемых Battery Front-End.

Отдельные `K_MAIN` и `MAIN_INPUT_BUS` отсутствуют.

## 3. Батарейные ветви

Обе батарейные ветви симметричны и в режиме `RUN` работают параллельно.

Каждая ветвь включает:

1. аккумуляторную сборку LiFePO4 4s24p, 12,8 В, 144 А·ч;
2. существующую автономную BMS в корпусе АКБ;
3. защищённый внешний выход `BAT_PROT+ / BAT_PROT−`;
4. предохранитель;
5. однополюсный моностабильный нормально разомкнутый контактор `K_BATx` по плюсу;
6. одну катушку непрерывного режима;
7. вспомогательный NO-контакт самоподхвата;
8. межкорпусную линию `СН-176А-12`, длина 1 м;
9. Battery Front-End в корпусе электроники с измерением напряжения и тока;
10. основной электронный силовой тракт;
11. ограниченный тракт `DECK_BALANCE`.

Температура ячеек и цифровой статус BMS через батарейную линию не передаются. Raw-ветвь и внутренние точки BMS не используются.

## 4. Управление контактором

```text
BAT_PROT+ ─ F_CTRL ─┬─ LOCAL_START_NO ─┐
                    └─ K_BAT_AUX_NO ───┤─ K_BAT_COIL ─ pin 11 REMOTE_OFF
                                                        │
BAT_PROT− ───────────── REMOTE_OFF/EXT_KILL interrupt ──┘
```

### Включение

```text
LOCAL_START short
→ K_BATx CLOSED
→ K_BAT_AUX_NO CLOSED
→ coil self-hold
```

### Выключение

```text
REMOTE_OFF loop open
или BMS protected output lost
→ coil de-energized
→ K_BATx OPEN
→ K_BAT_AUX_NO OPEN
```

После восстановления BMS или цепи REMOTE_OFF контактор остаётся OPEN до нового LOCAL_START.

Контакт 12 `СН-176А-12` — резерв.

## 5. Правило разделения ветвей нагрузки

`POWER_12V_BUS`, `5V_SYS_BUS`, `LIGHT_POWER_BRANCH` и `RESERVE_BRANCH` являются отдельными ветвями от `PACK_BUS`.

## 6. Что питается от резерва

Только critical/keep-alive домен:

1. MCU;
2. связь;
3. критические датчики;
4. fault/event logic;
5. 5V_CRIT;
6. 3V3_CRIT.

Катушка K_BATx не питается от EMG. Она питается только от защищённого выхода соответствующей основной АКБ.

## 7. Что не питается от резерва

1. CH1...CH14;
2. 5V_SYS_BUS;
3. LED-драйверы;
4. силовые внешние нагрузки;
5. катушки K_BAT1/K_BAT2.

## 8. HARD_OFF

```text
штатно:
снять тяжёлые нагрузки
→ сохранить журнал и SoC
→ разомкнуть REMOTE_OFF loop K_BAT1
→ разомкнуть REMOTE_OFF loop K_BAT2
→ проверить токи ветвей
→ проверить разряд PACK_BUS
→ завершить работу MCU от EMG

аварийно:
EXT_KILL
→ аппаратно разомкнуть hold loops K_BAT1/K_BAT2
→ аппаратно отключить электронные силовые тракты
→ записать причину от EMG
→ проверить токи и разряд PACK_BUS
```

## 9. Реакция на BMS

```text
BMS output disabled
→ K_BATx OPEN

BMS output restored
→ K_BATx remains OPEN
→ manual LOCAL_START required
```

Эта логика не зависит от внутренней топологии BMS.

## 10. Следующий этап

До выбора модели контактора должны быть определены диапазон защищённого напряжения, параметры катушки и economizer, рейтинг вспомогательного контакта, реализация REMOTE_OFF/EXT_KILL loop, защита катушки, время отпускания, силовой ток, DC breaking capacity и отказобезопасность.
