# Предварительная компоновочная граница PCB-A…PCB-E — PlataVM V1.9

Дата: 2026-07-21  
Основание: owner-defined envelope V1.8 и закрытие Q-SYS-007  
Статус: `PRELIMINARY PACKAGING BOUNDARY — NO PCB OUTLINE FREEZE`

## 1. Назначение

Документ переводит принятый общий envelope электронной сборки в контролируемую основу для:

1. предварительных контуров PCB-A…PCB-E;
2. распределения плат по уровням;
3. оценки высоты компонентов;
4. подготовки mounting-hole zones;
5. трассировки силовых и сигнальных жгутов;
6. physical pin count;
7. последующего выбора межплатных разъёмов.

Документ не фиксирует окончательные размеры плат, координаты отверстий, диаметр крепежа, компоненты, footprints или 3D-модель.

## 2. Общий envelope

```text
X — продольное направление от крышки внутрь корпуса
Y — ширина электронной сборки
Z — общая высота многоуровневой сборки
```

Предельная граница:

```text
Y_MAX = 100 мм
X_TARGET = 250 мм
Z_MAX = 80 мм
```

Вся сборка:

- крепится к съёмной крышке;
- извлекается вместе с крышкой;
- не имеет штатного теплового контакта с цилиндрическим корпусом;
- не опирается на стенку цилиндра;
- использует стойки и винты, выбираемые владельцем;
- должна иметь доступные mounting holes и tool-access zones.

## 3. Расчётная внутренняя граница

Для исключения выхода платы, пайки и компонентов за assembly envelope вводится проектная внутренняя граница:

```text
PCB width target: ≤94 мм
absolute PCB width: ≤100 мм
assembly length target: ≤240 мм
absolute assembly length: ≤250 мм
component/fastener height: в пределах 80 мм всей сборки
```

Запас `6 мм` по ширине и `10 мм` по длине является предварительным технологическим резервом, а не свойством корпуса.

Выход за target допускается только после общей 3D-проверки.

## 4. Принцип разбиения по уровням

Базовый кандидат `PACKAGING-P1` использует три функциональных уровня.

### Уровень L0 — Battery Front-End / high-current distribution

Предварительно:

```text
PCB-A_BFE_POWER
PCB-C_POWER_12V
```

Назначение уровня:

- батарейные вводы;
- BFE_1/BFE_2;
- MAIN_SW/BALANCE paths;
- PACK_BUS distribution;
- 12 В high-current channels;
- минимальная длина силовых токовых петель.

Требования:

- силовые клеммы и шины обращены к краям сборки;
- PCB-B не размещается в этом уровне между силовыми токовыми путями;
- тяжёлые и высокие элементы имеют механическую опору;
- вокруг токовых шунтов и измерительных узлов предусматривается thermal/EMI separation.

### Уровень L1 — преобразование и свет

Предварительно:

```text
PCB-D_POWER_5V
PCB-E_LIGHT_POWER
```

Назначение уровня:

- 12→5 В conversion;
- 5V_SYS_BUS distribution;
- LED current regulation;
- local high-frequency switching.

Требования:

- PCB-D и PCB-E не располагаются непосредственно над чувствительными analog sections PCB-B;
- switching nodes имеют локальные экраны/keepout по необходимости;
- дроссели и другие тяжёлые компоненты фиксируются механически;
- создаются проходы для внутренней естественной конвекции.

### Уровень L2 — critical control

Предварительно:

```text
PCB-B_CTRL_RESERVE
```

Назначение уровня:

- MCU;
- 5V_CRIT/3V3_CRIT;
- supervisor/watchdog/fault manager;
- внешний isolated RS-485;
- внутренний CAN-FD;
- direct safety lines;
- service/debug.

Требования:

- максимальное удаление от BFE switching nodes и DC/DC power loops;
- доступ к service/debug после снятия сборки;
- отсутствие силового транзита пользовательских нагрузок;
- единственная controlled SIGNAL_GND–POWER_GND point остаётся на PCB-B.

## 5. Предварительный размерный бюджет уровней

Размеры ниже являются не контурами плат, а area budget для начала floorplanning.

| Уровень | Состав | Бюджет по X | Бюджет по Y | Бюджет по Z |
|---|---|---:|---:|---:|
| L0 | PCB-A + PCB-C | ≤240 мм суммарно | ≤94 мм target | ≤25 мм от plane L0 |
| L1 | PCB-D + PCB-E | ≤240 мм суммарно | ≤94 мм target | ≤25 мм от plane L1 |
| L2 | PCB-B | ≤220 мм | ≤94 мм target | ≤18 мм от plane L2 |

Предварительный вертикальный бюджет:

```text
base/mount allowance       3 мм
L0 PCB + components       26 мм
inter-level clearance      3 мм
L1 PCB + components       26 мм
inter-level clearance      3 мм
L2 PCB + components       18 мм
--------------------------------
total                     79 мм
```

Это проверочный envelope, а не требование использовать максимальную высоту каждого уровня одновременно.

Если выбранный дроссель, трансформатор, разъём или защитный компонент не укладывается, сначала пересматриваются расположение и topology, а не общий envelope.

## 6. Предварительный продольный floorplan

Для L0:

```text
крышка
→ PCB-A_BFE_POWER
→ PCB-C_POWER_12V
→ внутренний конец сборки
```

Обоснование:

- PCB-A располагается ближе к батарейным вводам;
- PCB-C получает короткое ответвление PACK_BUS_P12_IN;
- ток пользовательских 12 В нагрузок не проходит через PCB-B.

Для L1:

```text
крышка
→ PCB-D_POWER_5V
→ PCB-E_LIGHT_POWER
→ внутренний конец сборки
```

Порядок D/E остаётся предварительным и может быть изменён после оценки потерь, разъёмных групп и высоты магнитных компонентов.

PCB-B на L2 может перекрывать несколько нижних модулей по X, но не должен исключать доступ к их креплению без контролируемой разборки уровня.

## 7. Mounting-hole zones

Поскольку тип винтов и стоек выбирает владелец, окончательный drill не фиксируется.

Для каждого PCB-модуля требуется:

1. не менее четырёх основных mounting-hole zones;
2. дополнительные zones для длинной платы или тяжёлых компонентов;
3. центр основной зоны не ближе 5 мм от края платы;
4. component/copper keepout вокруг зоны — не менее 5 мм до выбора крепежа;
5. доступ инструмента по оси винта;
6. отсутствие разъёмов, высоких компонентов и жгутов над зоной;
7. отдельные опоры тяжёлых дросселей, трансформаторов, шин и массивных разъёмов.

До выбора крепежа в KiCad применяется placeholder:

```text
MOUNT_HOLE_TBD
NO FINAL DRILL
MECHANICAL KEEPOUT ONLY
```

## 8. Межуровневые соединения

INTERCONNECT остаётся пассивным.

Разрешены:

- отдельные силовые шины/жгуты PACK_BUS и POWER_GND;
- отдельные ответвления к PCB-C/D/E;
- signal harness или пассивная backplane;
- CAN_INT_H/L;
- direct SAFE/HARD_OFF/fault lines;
- service/debug harness.

Запрещено:

- проводить high current через PCB-B;
- использовать PCB-B как силовую последовательную перемычку;
- объединять все земли без доменной маркировки;
- размещать активные repeaters или protection logic на INTERCONNECT без нового ADR.

## 9. CAN-FD physical order

Предварительный порядок nodes должен следовать фактическому расположению и минимизировать stubs.

Кандидат для `PACKAGING-P1`:

```text
PCB-B — PCB-D — PCB-E — PCB-C
```

или при другом продольном порядке:

```text
PCB-B — PCB-C — PCB-D — PCB-E
```

PCB-A не обязан быть обычным CAN-FD node; его critical control остаётся прямым через PCB-B.

Окончательный node order и termination выбираются после physical floorplan и connector placement.

## 10. Тепловая граница

Принято:

```text
нет штатного thermal contact с корпусом
охлаждение — внутренняя natural convection + PCB copper + локальные радиаторы
T_AMBIENT_INTERNAL_TEST = +60 °C
```

Для packaging:

1. не перекрывать полностью поперечное сечение сплошными платами и жгутами;
2. предусмотреть продольные воздушные проходы;
3. не размещать основные источники тепла строго друг над другом;
4. не направлять горячий воздух PCB-D на PCB-B;
5. распределять силовые потери по длине;
6. предусмотреть temperature sensors PCB-C/D/E;
7. ограничить применение hot-melt adhesive около горячих элементов.

## 11. EMC и измерительные зоны

1. PCB-B располагается вдали от switching nodes PCB-D/E;
2. battery-current sense и PACK_BUS sensing не трассируются рядом с gate-drive loops;
3. CAN-FD pair идёт совместно и отдельно от high dI/dt paths;
4. direct hardware safety lines не объединяются с PWM/switching bundles;
5. cable shields завершаются на CHASSIS около крышки;
6. SIGNAL_GND–POWER_GND connection остаётся только в controlled point PCB-B.

## 12. DFM/сборка

Обязательные требования:

- все разъёмы имеют strain relief;
- нельзя передавать усилие крышки и внешнего кабеля на пайку PCB;
- платы снимаются в определённой последовательности;
- винты верхнего уровня не закрывают крепёж нижнего без описанной операции;
- маркировка PCB-A…PCB-E видима после извлечения;
- polarity и connector-keying исключают перестановку силовых ветвей;
- conformal coating mask учитывает разъёмы, test points и thermal surfaces;
- hot-melt adhesive применяется после функционального теста и визуального контроля.

## 13. Что разрешено делать дальше

На основании этой границы разрешено:

1. создать preliminary board outlines в отдельных mechanical branches;
2. ввести mounting-hole zones без final drill;
3. сделать component-area blocks без выбора part number;
4. оценить количество силовых, CAN-FD и direct safety contacts;
5. сформировать connector classes;
6. начать thermal-loss budget PCB-D/PCB-E;
7. подготовить 3D placeholder model assembly.

## 14. Что пока запрещено

До расчётов и выбора компонентов запрещено:

1. замораживать точные размеры каждой платы;
2. выпускать final mounting holes;
3. выбирать межплатные connector families;
4. утверждать CAN termination location;
5. фиксировать высоту уровней без component-height audit;
6. утверждать thermal compliance без расчёта/испытания при +60 °C;
7. выпускать production PCB layout.

## 15. Следующие инженерные задачи

```text
PKG-001 — component-area budget PCB-A
PKG-002 — component-area budget PCB-B
PKG-003 — component-area budget PCB-C
PKG-004 — component-area budget PCB-D
PKG-005 — component-area budget PCB-E
PKG-006 — mounting-hole zones and stack access
PKG-007 — physical power/hard-line/CAN pin count
PKG-008 — connector class selection
PKG-009 — thermal-loss budget without hull contact
```
