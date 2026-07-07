# Матрица каналов POWER_12V_BUS

| Канал | Тип | Назначение | Напряжение | Номинальный ток | Пиковый ток | Защита | Измерение тока | Fault | Статус |
|---|---|---|---:|---:|---:|---|---|---|---|
| CH1 | MCU-controlled | пользовательское имя в ПО | 12 В | 3 А | 5 А preliminary | individual | required | required | nominal fixed |
| CH2 | MCU-controlled | пользовательское имя в ПО | 12 В | 3 А | 5 А preliminary | individual | required | required | nominal fixed |
| CH3 | MCU-controlled | пользовательское имя в ПО | 12 В | 3 А | 5 А preliminary | individual | required | required | nominal fixed |
| CH4 | MCU-controlled | пользовательское имя в ПО | 12 В | 3 А | 5 А preliminary | individual | required | required | nominal fixed |
| CH5 | MCU-controlled | пользовательское имя в ПО | 12 В | 3 А | 5 А preliminary | individual | required | required | nominal fixed |
| CH6 | MCU-controlled | пользовательское имя в ПО | 12 В | 3 А | 5 А preliminary | individual | required | required | nominal fixed |
| CH7 | MCU-controlled | пользовательское имя в ПО | 12 В | 3 А | 5 А preliminary | individual | required | required | nominal fixed |
| CH8 | MCU-controlled | пользовательское имя в ПО | 12 В | 3 А | 5 А preliminary | individual | required | required | nominal fixed |
| CH9 | MCU-controlled | пользовательское имя в ПО | 12 В | 3 А | 5 А preliminary | individual | required | required | nominal fixed |
| CH10 | MCU-controlled | пользовательское имя в ПО | 12 В | 3 А | 5 А preliminary | individual | required | required | nominal fixed |
| CH11 | MCU-controlled | пользовательское имя в ПО | 12 В | 3 А | 5 А preliminary | individual | required | required | nominal fixed |
| CH12 | Always-On monitored | пользовательское имя в ПО | 12 В | 3 А | 5 А preliminary | individual | required | required | nominal fixed |
| CH13 | Always-On monitored | пользовательское имя в ПО | 12 В | 3 А | 5 А preliminary | individual | required | required | nominal fixed |
| CH14 | Always-On monitored | пользовательское имя в ПО | 12 В | 3 А | 5 А preliminary | individual | required | required | nominal fixed |

## Правила

1. Аппаратные имена всегда сохраняются как CH1...CH14.
2. Пользовательские назначения и названия хранятся в программе верхнего уровня.
3. CH12...CH14 включаются автоматически в штатном режиме, но могут отключаться защитой, SAFE и HARD_OFF.
4. Номинальный длительный ток одного канала — 3 А.
5. Пиковый ток 5 А является временным проектным допущением; длительность пика ещё не закрыта.
6. Возможность каждого канала выдавать 3 А не означает одновременное разрешение 14 × 3 А; общий лимит POWER_12V_BUS определяется энергетическим бюджетом и батарейными линиями СН-176А-12.
