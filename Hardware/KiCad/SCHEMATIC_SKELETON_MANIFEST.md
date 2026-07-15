# KiCad schematic skeleton manifest

Дата фиксации: 2026-07-14  
Дата обновления `00_SYSTEM_TOP`: 2026-07-15  
Дата обновления `02_INTERBOARD_POWER_AND_CONTROL`: 2026-07-15  
Дата обновления `01_EXTERNAL_BATTERIES_AND_HARNESS`: 2026-07-15  
Дата обновления PCB top-листов `10/20/30/40/50`: 2026-07-15  

Статус:

```text
ARCHITECTURE LEVEL A — all current top sheets converted to functional schematic sheets
```

## 1. Назначение

Этот пакет создаёт стартовый KiCad workspace для принятой многоплатной `SCHEMATIC ARCHITECTURE`. Он не выбирает компоненты, footprints или part numbers.

Источник истины:

```text
Docs/SCHEMATIC_ARCHITECTURE.md
Docs/INTERBOARD_INTERFACES.md
Docs/NET_NAMING_RULES.md
```

## 2. Созданные KiCad-файлы

```text
Hardware/KiCad/PlataVM.kicad_pro
Hardware/KiCad/PlataVM.kicad_sch
Hardware/KiCad/00_SYSTEM_TOP.kicad_sch
Hardware/KiCad/01_EXTERNAL_BATTERIES_AND_HARNESS.kicad_sch
Hardware/KiCad/02_INTERBOARD_POWER_AND_CONTROL.kicad_sch
Hardware/KiCad/10_BFE_POWER_TOP.kicad_sch
Hardware/KiCad/20_CTRL_RESERVE_TOP.kicad_sch
Hardware/KiCad/30_POWER_12V_TOP.kicad_sch
Hardware/KiCad/40_POWER_5V_TOP.kicad_sch
Hardware/KiCad/50_LIGHT_POWER_TOP.kicad_sch
```

## 3. Что уже зафиксировано

1. Корневой проект `PlataVM.kicad_pro`.
2. Корневой лист `PlataVM.kicad_sch`.
3. `00_SYSTEM_TOP.kicad_sch` — функциональный top-level обзор.
4. `01_EXTERNAL_BATTERIES_AND_HARNESS.kicad_sch` — внешние АКБ, СН-176А-12, `LOCAL_START`, `K_BATx` hold-loop.
5. `02_INTERBOARD_POWER_AND_CONTROL.kicad_sch` — логическая матрица межплатных power/control/diagnostics/safety интерфейсов.
6. `10_BFE_POWER_TOP.kicad_sch` — PCB-A / Battery Front-End, PACK_BUS, DECK_BALANCE, final HARD_OFF actuators.
7. `20_CTRL_RESERVE_TOP.kicad_sch` — PCB-B / MCU, critical power, EMG, RS-485, control/diagnostic IO.
8. `30_POWER_12V_TOP.kicad_sch` — PCB-C / 14-channel 12V distribution.
9. `40_POWER_5V_TOP.kicad_sch` — PCB-D / 5V_SYS DC/DC and ten protected outputs.
10. `50_LIGHT_POWER_TOP.kicad_sch` — PCB-E / six independent LED driver channels.

## 4. Системные top-level labels

```text
BAT1_TO_BFE
BAT2_TO_BFE
PACK_BUS_TO_P12
PACK_BUS_TO_P5
PACK_BUS_TO_LIGHT
PACK_BUS_TO_CRIT
CTRL_TO_BFE
CTRL_TO_P12
CTRL_TO_P5
CTRL_TO_LIGHT
EXT_KILL_HW
RS485_ISOLATED
```

## 5. Interboard labels

```text
PWR_A_TO_B_CRIT
PWR_A_TO_C_P12
PWR_A_TO_D_P5
PWR_A_TO_E_LIGHT
CTRL_B_TO_A
DIAG_A_TO_B
CTRL_B_TO_C_P12
DIAG_C_TO_B_P12
CTRL_B_TO_D_P5
DIAG_D_TO_B_P5
CTRL_B_TO_E_LIGHT
DIAG_E_TO_B_LIGHT
EXT_KILL_HW_CHAIN
```

## 6. Battery / harness labels

```text
BAT1_SN176_POWER
BAT1_REMOTE_OFF_LOOP
BAT1_LOCAL_START
BAT2_SN176_POWER
BAT2_REMOTE_OFF_LOOP
BAT2_LOCAL_START
K_BAT_HOLD_LOOP_RULE
```

## 7. PCB-A / BFE_POWER labels

```text
BAT1_SN176_POWER
BAT2_SN176_POWER
BAT1_REMOTE_OFF_LOOP
BAT2_REMOTE_OFF_LOOP
EXT_KILL_HW_CHAIN
BFE_PACK_BUS_OUT
PACK_BUS_FANOUT
CTRL_B_TO_A
DIAG_A_TO_B
DECK_BALANCE_CTRL
POWER_GND_POLICY
```

## 8. PCB-B / CTRL_RESERVE labels

```text
PACK_BUS_CRIT_IN
5V_CRIT
3V3_CRIT
MCU_FAULT_MANAGER
RS485_ISOLATED
ISO_GND_POLICY
CTRL_B_TO_A
CTRL_B_TO_C_P12
CTRL_B_TO_D_P5
CTRL_B_TO_E_LIGHT
DIAG_A_TO_B
DIAG_C_TO_B_P12
DIAG_D_TO_B_P5
DIAG_E_TO_B_LIGHT
EXT_KILL_HW_CHAIN
SERVICE_DEBUG
```

## 9. PCB-C / POWER_12V labels

```text
PACK_BUS_P12_IN
POWER_GND_P12
CTRL_B_TO_C_P12
P12_CH_EN_1_11
P12_AON_CH12_14
P12_OUTPUTS_CH1_14
DIAG_C_TO_B_P12
P12_FAULT_SUMMARY
P12_SAFE_OFF
P12_THERMAL_MON
```

## 10. PCB-D / POWER_5V labels

```text
PACK_BUS_P5_IN
POWER_GND_P5
5V_SYS_BUS
CTRL_B_TO_D_P5
P5_OUT_EN_1_7
P5_AON_OUT8_10
5V_OUTPUTS_1_10
DIAG_D_TO_B_P5
P5_FAULT_SUMMARY
P5_SAFE_OFF
P5_THERMAL_MON
```

## 11. PCB-E / LIGHT_POWER labels

```text
PACK_BUS_LIGHT_IN
POWER_GND_LIGHT
CTRL_B_TO_E_LIGHT
LIGHT_BRANCH_EN
LED_PWM_1_6
LED_DRV1_3_ZONE
LED_DRV4_6_ZONE
DIAG_E_TO_B_LIGHT
LED_FAULT_SUMMARY
LED_OUTPUTS_1_6
LIGHT_SAFE_OFF
LIGHT_THERMAL_MON
```

## 12. Что пока не делается

1. Не выбирается контактор `K_BATx`.
2. Не выбираются `MAIN_SWx`.
3. Не выбираются датчики тока.
4. Не выбираются DC/DC, LED-драйверы, MCU и eFuse/high-side switches.
5. Не создаются footprints.
6. Не выполняется PCB layout.
7. Не объединяются автоматически `POWER_GND`, `SIGNAL_GND`, `ISO_GND` и `CHASSIS`.
8. Не назначаются физические межплатные разъёмы.
9. Не фиксируется окончательный pin-count.
10. Не фиксируются окончательные токи, thermal derating и connector families.

## 13. Проверка пользователем после пакета

Открыть локально:

```text
Hardware/KiCad/PlataVM.kicad_pro
```

Проверить каждый лист:

```text
00_SYSTEM_TOP
01_EXTERNAL_BATTERIES_AND_HARNESS
02_INTERBOARD_POWER_AND_CONTROL
10_BFE_POWER_TOP
20_CTRL_RESERVE_TOP
30_POWER_12V_TOP
40_POWER_5V_TOP
50_LIGHT_POWER_TOP
```

Минимальная проверка:

1. лист открывается без ошибки парсинга;
2. текстовые группы не перекрываются критично;
3. hierarchical labels видны;
4. KiCad не удаляет labels при сохранении;
5. `.kicad_prl` не появляется в Git changes из-за `.gitignore`.

## 14. Следующий инженерный этап

После визуальной проверки top-листов следующий этап:

```text
10_BFE_POWER detailed hierarchy
```

Разбить PCB-A на подлисты:

```text
11_BATTERY_INPUT_1
12_BATTERY_INPUT_2
13_MAIN_PATH_1
14_MAIN_PATH_2
15_DECK_BALANCE
16_PACK_BUS_AND_DISCHARGE
17_REMOTE_OFF_AND_EXT_KILL
18_BATTERY_MEASUREMENTS
19_BFE_CONNECTORS_TESTPOINTS
```

На этом этапе всё ещё допустимо использовать функциональные блоки `TBD`, если конкретные элементы не выбраны.
