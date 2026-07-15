# PCB-E LIGHT_POWER interface consistency

Дата проверки: 2026-07-15

## 1. Область проверки

```text
Docs/INTERBOARD_INTERFACES.md
Hardware/KiCad/02_INTERBOARD_POWER_AND_CONTROL.kicad_sch
Hardware/KiCad/27_CONTROL_IO.kicad_sch
Hardware/KiCad/50_LIGHT_POWER_TOP.kicad_sch
Hardware/KiCad/51_LIGHT_INPUT_PROTECTION.kicad_sch
Hardware/KiCad/52_LED_DRIVER_TEMPLATE.kicad_sch
Hardware/KiCad/53_LED_DRIVER_1_3.kicad_sch
Hardware/KiCad/54_LED_DRIVER_4_6.kicad_sch
Hardware/KiCad/55_LIGHT_DIAGNOSTICS.kicad_sch
Hardware/KiCad/56_LIGHT_CONNECTORS.kicad_sch
```

## 2. Результат

```text
PCB-E LIGHT_POWER interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
```

Проверка фиксирует exact logical ports, directions и safe-state semantics. Driver topology, PWM electrical parameters, diagnostic transport, physical connectors, footprints, BOM и PCB layout не выбираются.

## 3. Питание PCB-E

```text
PCB-A -> PCB-E: PACK_BUS_LIGHT_IN
Return:          POWER_GND
Local node:      LIGHT_PROTECTED_BUS
```

LED load current не проходит через PCB-B. Две зоны по три канала остаются частями одной PCB-E.

## 4. Управление PCB-B → PCB-E

Канонические порты на `27_CONTROL_IO` и `50_LIGHT_POWER_TOP`:

```text
CTRL_B_TO_E_LIGHT
LIGHT_BRANCH_EN
LED_PWM[1..6]
LIGHT_GROUP_HARD_OFF
```

Local decomposition:

```text
LED_PWM_1_3
LED_PWM_4_6
```

Local groups не являются альтернативными interboard names.

## 5. Диагностика PCB-E → PCB-B

Канонические порты:

```text
DIAG_E_TO_B_LIGHT
LED_FAULT_N[1..6]
LED_ISENSE[1..6]
LIGHT_INPUT_VSENSE
LIGHT_BOARD_TEMP
LIGHT_BOARD_FAULT_N
```

Local source groups:

```text
LED_FAULT_N_1_3
LED_FAULT_N_4_6
LED_ISENSE_1_3
LED_ISENSE_4_6
LIGHT_INPUT_FAULT_N
LIGHT_INPUT_PRESENT
LIGHT_ZONE1_TEMP_SENSE_TBD
LIGHT_ZONE2_TEMP_SENSE_TBD
```

Они используются для aggregation на `55_LIGHT_DIAGNOSTICS`.

## 6. Directions

| Сигнал | PCB-B | PCB-E |
|---|---|---|
| `LIGHT_BRANCH_EN` | output | input |
| `LED_PWM[1..6]` | output | input |
| `LIGHT_GROUP_HARD_OFF` | output | input |
| `LED_FAULT_N[1..6]` | input | output |
| `LED_ISENSE[1..6]` | input | output |
| `LIGHT_INPUT_VSENSE` | input | output |
| `LIGHT_BOARD_TEMP` | input | output |
| `LIGHT_BOARD_FAULT_N` | input | output |

## 7. Safe-state semantics

1. Default safe state — все LED outputs OFF.
2. `LIGHT_GROUP_HARD_OFF` имеет приоритет над `LIGHT_BRANCH_EN` и всеми PWM inputs.
3. Lost firmware, reset, brownout и disconnected control не должны включать LED channels.
4. Driver recovery/retry не отменяет active HARD_OFF.
5. Diagnostic transport не участвует в shutdown.
6. Single-channel fault должен локализоваться, если thermal/group protection не требует wider shutdown.

## 8. Controlled placeholders

```text
LIGHT_INPUT_FAULT_N
LIGHT_INPUT_PRESENT
LED_CH_STATUS_TBD
LIGHT_ZONE1_TEMP_SENSE_TBD
LIGHT_ZONE2_TEMP_SENSE_TBD
SIGNAL_GND_REFERENCE_TBD
LIGHT_RETURN_GROUP_TBD
LIGHT_OUTPUT_CONNECTOR_CLASS_TBD
LIGHT_TP_LOW_ENERGY
LIGHT_TP_POWER_GUARDED
```

## 9. Архитектурные ограничения сохранены

- `K_MAIN` не добавлен.
- PCB-E остаётся одной функциональной платой.
- High-current LED power не проходит через PCB-B.
- Шесть каналов сохраняют электрическую и диагностическую независимость.
- Реальные library symbols не добавлены.
- LED-driver topology/controllers/switches/magnetics/sensors не выбраны.
- PWM level/frequency/dimming range не зафиксированы.
- Connectors, footprints, BOM и layout не создавались.
- Ground domains не объединялись.
- `.kicad_prl` не возвращён.

## 10. Следующий этап

```text
Run system-wide interface consistency audit
```
