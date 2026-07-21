# Предварительное решение по физической топологии интерфейсов — PlataVM V1.9

Дата: 2026-07-21  
Статус: `PRELIMINARY TOPOLOGY ACCEPTED; CONNECTOR FAMILY OPEN`

## 1. PCB-A ↔ PCB-B

Рассмотрены варианты:

```text
A: один 32-position signal connector
B: два 16-position connectors — CTRL и DIAG
```

Принят рабочий вариант:

```text
B: 16 CTRL + 16 DIAG
```

## 2. Обоснование 16+16

Преимущества:

1. меньше mating-volume одного корпуса;
2. функциональное разделение command и diagnostic groups;
3. упрощённая сервисная локализация;
4. возможность разнести sensitive measurements и switching control;
5. меньший риск полной потери интерфейса при повреждении одного корпуса;
6. проще разместить на PCB-A 110 × 94 мм и PCB-B 180 × 94 мм;
7. сохраняется суммарный резерв 32-position allocation.

Недостатки:

1. два корпуса и два ответных разъёма;
2. больше операций сборки;
3. требуется исключить перепутывание CTRL/DIAG;
4. требуется отдельное ключевание и маркировка;
5. увеличивается число cable exits.

Меры:

- механически несовместимое ключевание либо разные coding keys;
- разные обозначения и маркировка;
- запрет одинакового свободного переставляемого pinout;
- отдельные shield/return assignments после pinout review.

## 3. PCB-B ↔ PCB-C/D/E

Сохраняется единый предварительный класс:

```text
8 signal positions per destination board
```

Назначения включают:

- CAN_INT_H;
- CAN_INT_L;
- direct SAFE/HARD_OFF;
- board-fault summary;
- signal returns/reserve.

Конкретный pinout и connector family остаются открытыми.

## 4. CAN-FD physical order

Продольный floorplan:

```text
L0: крышка → PCB-A → PCB-C
L1: крышка → PCB-D → PCB-E
L2: крышка → PCB-B
```

Принят предварительный порядок:

```text
PCB-B → PCB-D → PCB-E → PCB-C
```

Обоснование:

1. PCB-B и PCB-D находятся ближе к крышке;
2. PCB-D и PCB-E соседствуют на L1;
3. PCB-E и PCB-C находятся в задней части своих уровней;
4. исключается возврат магистрали от PCB-C к PCB-D;
5. минимизируется trunk length для текущего floorplan;
6. PCB-A не включается как обязательный CAN node;
7. direct safety/fault lines сохраняются независимо.

## 5. Termination

Предварительные физические концы CAN-FD:

```text
end 1: PCB-B
end 2: PCB-C
```

Следствие:

- termination на PCB-B и PCB-C;
- PCB-D и PCB-E — промежуточные nodes;
- stubs должны быть минимальными;
- termination должна быть конфигурируемой до final harness freeze;
- на промежуточных платах допускаются DNP footprints только после schematic decision.

## 6. Ограничения

Решение не фиксирует:

- CAN transceiver;
- разъём;
- cable impedance;
- bitrate;
- termination resistor part number;
- common-mode choke;
- ESD network;
- окончательную длину жгута.

## 7. Gate

```text
A↔B topology 16+16: PRELIMINARY PASS
CAN order B-D-E-C: PRELIMINARY PASS
termination ends B/C: PRELIMINARY PASS
connector family: OPEN
physical pinout: OPEN
mating clearance: OPEN
```

Решение пересматривается только если реальные connector volumes или component-height audit делают текущую компоновку невозможной.
