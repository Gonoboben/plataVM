# Хронология: datasheet correction review PCB-D prototype components

Дата: 2026-07-21

До открытия PR выполнена повторная проверка exact manufacturer data.

Исправлено:

```text
LM5143A-Q1 VCS max:
82 мВ ошибочно
→ 80 мВ по exact datasheet

maximum equivalent OCP:
31,158 А ошибочно
→ 30,350 А
```

Минимальный OCP threshold и запас 20-А режима не изменились:

```text
minimum equivalent threshold: 22,522 А
minimum phase peak margin: 10,7 %
```

Также по Bourns ordering scheme закрыт exact prototype order code:

```text
PWR263S-35-R100FE
0,10 Ом /1 % /tape and reel
```

Application-specific pulse curve and hot-plug test remain open.

Результат:

```text
datasheet value correction: PASS
cross-document synchronization: PASS
architecture change: NONE
production freeze: NOT GRANTED
```