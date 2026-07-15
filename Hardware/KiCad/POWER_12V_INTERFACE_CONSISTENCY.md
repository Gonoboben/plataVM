# PCB-C POWER_12V interface consistency

Дата проверки: 2026-07-15  
Область проверки:

```text
Docs/INTERBOARD_INTERFACES.md
Hardware/KiCad/02_INTERBOARD_POWER_AND_CONTROL.kicad_sch
Hardware/KiCad/27_CONTROL_IO.kicad_sch
Hardware/KiCad/30_POWER_12V_TOP.kicad_sch
Hardware/KiCad/31_POWER_12V_INPUT_PROTECTION.kicad_sch
Hardware/KiCad/32_POWER_12V_CHANNEL_TEMPLATE.kicad_sch
Hardware/KiCad/33_POWER_12V_CH1_CH7.kicad_sch
Hardware/KiCad/34_POWER_12V_CH8_CH14.kicad_sch
Hardware/KiCad/35_POWER_12V_DIAGNOSTICS.kicad_sch
Hardware/KiCad/36_POWER_12V_CONNECTORS.kicad_sch
```

## 1. Результат

```text
PCB-C POWER_12V interface consistency: PASS WITH CONTROLLED PLACEHOLDERS
```

Проверка фиксирует точные логические bus names, направления и safe-state semantics. Она не выбирает electrical transport, component topology, physical connectors, footprints, BOM или PCB layout.

## 2. Питание PCB-C

```text
PCB-A -> PCB-C: PACK_BUS_P12_IN
Return:          POWER_GND
Local node:      P12_PROTECTED_BUS
```

Токи CH1…CH14 не проходят через PCB-B.

## 3. Управление PCB-B → PCB-C

Канонические внешние порты на `27_CONTROL_IO` и `30_POWER_12V_TOP`:

```text
P12_CH_EN[1..11]
P12_GROUP_SAFE_OFF
P12_GROUP_HARD_OFF
CTRL_B_TO_C_P12
```

Исправлено:

```text
P12_CH_EN_1_11 -> P12_CH_EN[1..11]  (external boundary)
```

Внутреннее разложение на PCB-C сохранено:

```text
P12_CH_EN_1_7
P12_CH_EN_8_11
```

Это локальные sub-sheet groups, а не альтернативные межплатные имена.

## 4. Always-On monitored channels

```text
CH12..CH14 = Always-On monitored during normal RUN
```

При этом они обязательно подчиняются:

```text
P12_GROUP_SAFE_OFF
P12_GROUP_HARD_OFF
board-level protection
individual channel protection
```

`P12_AON_CH12_14` и `P12_AON_POLICY_CH12_14` являются local architecture placeholders до выбора способа физического always-enabled управления.

## 5. Диагностика PCB-C → PCB-B

Канонические внешние порты на `35_POWER_12V_DIAGNOSTICS`, `30_POWER_12V_TOP` и `27_CONTROL_IO`:

```text
P12_CH_FAULT_N[1..14]
P12_CH_ISENSE[1..14]
P12_BOARD_TEMP
P12_INPUT_VSENSE
P12_BOARD_FAULT_N
DIAG_C_TO_B_P12
```

Исправлено:

```text
P12_CH_FAULT_N_1_14 -> P12_CH_FAULT_N[1..14]  (external boundary)
P12_CH_ISENSE_1_14  -> P12_CH_ISENSE[1..14]   (external boundary)
```

Внутренние source groups сохранены:

```text
P12_CH_FAULT_N_1_7
P12_CH_FAULT_N_8_14
P12_CH_ISENSE_1_7
P12_CH_ISENSE_8_14
P12_INPUT_FAULT_N
P12_INPUT_PRESENT
P12_BOARD_TEMP_SENSE_TBD
```

Они используются для local aggregation и не являются альтернативными межплатными nets.

## 6. Направления

| Сигнал | PCB-B `27_CONTROL_IO` | PCB-C | Назначение |
|---|---|---|---|
| `P12_CH_EN[1..11]` | output | input | normal channel enables |
| `P12_GROUP_SAFE_OFF` | output | input | controlled safe-state request |
| `P12_GROUP_HARD_OFF` | output | input | hardware-priority group OFF |
| `P12_CH_FAULT_N[1..14]` | input | output | individual channel faults |
| `P12_CH_ISENSE[1..14]` | input | output | individual current diagnostics |
| `P12_BOARD_TEMP` | input | output | board thermal observation |
| `P12_INPUT_VSENSE` | input | output | PCB-C branch input voltage |
| `P12_BOARD_FAULT_N` | input | output | conditioned board fault summary |

## 7. Safe-state semantics

1. CH1…CH11 default OFF during reset, brownout, lost firmware and disconnected control.
2. `P12_GROUP_HARD_OFF` overrides normal enables and Always-On policy.
3. `P12_GROUP_SAFE_OFF` requests the defined controlled safe state.
4. CH12…CH14 are not uncontrolled; they remain protected and shut down under SAFE/HARD_OFF.
5. Diagnostic transport cannot block or delay HARD_OFF.
6. A single channel fault should remain contained where upstream protection coordination permits.

## 8. Controlled placeholders

```text
P12_INPUT_FAULT_N
P12_INPUT_PRESENT
P12_CH_STATUS_TBD
P12_AON_CH12_14
P12_AON_POLICY_CH12_14
P12_BOARD_TEMP_SENSE_TBD
SIGNAL_GND_REFERENCE_TBD
P12_RETURN_GROUP_TBD
P12_OUTPUT_CONNECTOR_CLASS_TBD
P12_TP_LOW_ENERGY
P12_TP_POWER_GUARDED
```

Причины:

- component topology не выбрана;
- analog reference/transport не выбран;
- physical output returns, harness and connector mechanics требуют нагрузочных данных;
- temperature sensor location требует thermal design;
- Always-On implementation требует отдельного electrical decision.

## 9. Что не изменено

- `K_MAIN` не добавлен.
- PCB-C получает отдельную силовую ветвь от PCB-A.
- High-current power не проходит через PCB-B.
- CH1…CH14 сохраняют индивидуальную идентичность.
- Реальные library symbols не добавлены.
- eFuse/high-side switches, fuses, sensors, TVS и suppression не выбраны.
- Connectors, footprints, BOM и layout не создавались.
- Ground domains не объединялись.
- `.kicad_prl` не возвращён.

## 10. Следующий этап

```text
Start PCB-D_POWER_5V detailed hierarchy
```

После создания листов `41…46` требуется отдельная проверка PCB-B ↔ PCB-D interfaces.
