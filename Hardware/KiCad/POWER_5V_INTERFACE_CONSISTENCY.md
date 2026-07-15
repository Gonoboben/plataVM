# PCB-D POWER_5V interface consistency

Дата проверки: 2026-07-15

## 1. Область проверки

```text
Docs/INTERBOARD_INTERFACES.md
Hardware/KiCad/02_INTERBOARD_POWER_AND_CONTROL.kicad_sch
Hardware/KiCad/27_CONTROL_IO.kicad_sch
Hardware/KiCad/40_POWER_5V_TOP.kicad_sch
Hardware/KiCad/41_5V_DC_DC.kicad_sch
Hardware/KiCad/42_5V_OUTPUT_TEMPLATE.kicad_sch
Hardware/KiCad/43_5V_OUT1_OUT5.kicad_sch
Hardware/KiCad/44_5V_OUT6_OUT10.kicad_sch
Hardware/KiCad/45_5V_DIAGNOSTICS.kicad_sch
Hardware/KiCad/46_5V_CONNECTORS.kicad_sch
```

## 2. Результат

```text
PCB-D POWER_5V interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
```

Проверка фиксирует logical ports, directions и safe-state semantics. Она не выбирает converter/output topology, diagnostic transport, physical connectors, footprints, BOM или PCB layout.

## 3. Питание PCB-D

```text
PCB-A -> PCB-D: PACK_BUS_P5_IN
Return:          POWER_GND
Converted rail:  5V_SYS_BUS
Budget:          15 A continuous / 20 A short peak
```

`5V_SYS_BUS` не питает `5V_CRIT/3V3_CRIT` и не питается от EMG.

## 4. Управление PCB-B → PCB-D

Канонические порты на `27_CONTROL_IO` и `40_POWER_5V_TOP`:

```text
CTRL_B_TO_D_P5
5V_SYS_EN
P5_OUT_EN[1..7]
P5_GROUP_SAFE_OFF
P5_GROUP_HARD_OFF
```

Local decomposition:

```text
P5_OUT_EN_1_5
P5_OUT_EN_6_7
```

Local groups не являются альтернативными межплатными names.

## 5. Диагностика PCB-D → PCB-B

Канонические порты:

```text
DIAG_D_TO_B_P5
P5_OUT_FAULT_N[1..10]
P5_OUT_ISENSE[1..10]
5V_SYS_VSENSE
5V_SYS_TOTAL_ISENSE
P5_BOARD_TEMP
P5_BOARD_FAULT_N
```

Local source groups:

```text
P5_OUT_FAULT_N_1_5
P5_OUT_FAULT_N_6_10
P5_OUT_ISENSE_1_5
P5_OUT_ISENSE_6_10
P5_DC_DC_FAULT_N
P5_BOARD_TEMP_SENSE_TBD
```

Они используются для aggregation на `45_5V_DIAGNOSTICS`.

## 6. Directions

| Сигнал | PCB-B | PCB-D |
|---|---|---|
| `5V_SYS_EN` | output | input |
| `P5_OUT_EN[1..7]` | output | input |
| `P5_GROUP_SAFE_OFF` | output | input |
| `P5_GROUP_HARD_OFF` | output | input |
| `P5_OUT_FAULT_N[1..10]` | input | output |
| `P5_OUT_ISENSE[1..10]` | input | output |
| `5V_SYS_VSENSE` | input | output |
| `5V_SYS_TOTAL_ISENSE` | input | output |
| `P5_BOARD_TEMP` | input | output |
| `P5_BOARD_FAULT_N` | input | output |

## 7. Always-On monitored outputs

```text
5V_OUT8..5V_OUT10 = Always-On monitored during normal RUN
```

Always-On не отменяет:

```text
individual protection
P5_GROUP_SAFE_OFF
P5_GROUP_HARD_OFF
board-level protection
fault/current diagnostics
```

`P5_AON_OUT8_10` и `P5_AON_POLICY_OUT8_10` остаются local placeholders до выбора physical implementation.

## 8. Safe-state semantics

1. `5V_SYS_EN` defaults OFF при lost control, если иной startup policy не утверждён отдельно.
2. `P5_GROUP_HARD_OFF` имеет приоритет над converter enable, output enables и Always-On policy.
3. `P5_GROUP_SAFE_OFF` запрашивает controlled safe state.
4. Converter recovery не отменяет HARD_OFF.
5. Diagnostic transport не участвует в аппаратном shutdown.
6. Faulted output должен изолироваться без destabilization `5V_SYS_BUS`, где это допускает protection coordination.

## 9. Controlled placeholders

```text
P5_DC_DC_FAULT_N
P5_OUT_STATUS_TBD
P5_AON_OUT8_10
P5_AON_POLICY_OUT8_10
P5_BOARD_TEMP_SENSE_TBD
SIGNAL_GND_REFERENCE_TBD
P5_RETURN_GROUP_TBD
P5_OUTPUT_CONNECTOR_CLASS_TBD
P5_TP_LOW_ENERGY
P5_TP_POWER_GUARDED
```

## 10. Архитектурные ограничения сохранены

- `K_MAIN` не добавлен.
- High-current outputs не проходят через PCB-B.
- `5V_SYS_BUS` отделён от critical domain.
- Реальные library symbols не добавлены.
- DC/DC, magnetics, load switches, sensors, TVS и filters не выбраны.
- Connectors, footprints, BOM и layout не создавались.
- Ground domains не объединялись.
- `.kicad_prl` не возвращён.

## 11. Следующий этап

```text
Start PCB-E_LIGHT_POWER detailed hierarchy
```
