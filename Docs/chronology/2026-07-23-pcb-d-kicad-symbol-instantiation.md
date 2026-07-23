# 2026-07-23 — PCB-D exact KiCad symbol instantiation and native ERC V1.9

## Base

```text
repository: Gonoboben/plataVM
branch: agent/pcb-d-lm5143design-calc-v1-9
base main: c513dbb3c9da57b8b5a26e755accc94e893e3ef3
PR: #45 draft
```

## Выполнено

1. Предварительный text-only `41_5V_DC_DC.kicad_sch` заменён реальным KiCad-10 symbol-core листом.
2. Создан exact LM5143A-Q1 RHA-40 symbol с 40 physical pins и exposed pad.
3. Инстанцированы controller, four MOSFETs, inductors, Kelvin shunts, timing, compensation, bootstrap, current-sense and capacitor positions.
4. После сверки split outputs `HO/HOL` и `LO/LOL` создано восемь gate-resistor positions вместо четырёх упрощённых.
5. Инстанцированы `U_UVLO` и direct-hardware `U_EN_GATE` placeholders; SAFE/HARD_OFF подключены к аппаратной границе.
6. Инстанцированы explicit fault/current-monitor placeholders.
7. Добавлен controlled `NT_AGND_PGND`; final copper/via pattern оставлен open.
8. Все 11 hierarchical interfaces получили электрическую привязку.
9. Добавлен deterministic generator и exact-symbol validator.
10. Добавлен GitHub Actions workflow для official KiCad 10 native ERC.
11. Исправлено преобразование symbol-local `Y` в sheet coordinates; устранены ошибочные pin-to-pin, EP, testpoint, PWR_FLAG и power-driver ERC faults.
12. Выполнен successful official KiCad 10.0.4 native ERC run с exact allowlist classification.

## Проверка deterministic и exact-symbol Gates

```text
controller pins including EP: 41
schematic instances: 50
split gate resistors: 8
hierarchical interfaces: 11
CALC_TBD markers: 38
UUID uniqueness: PASS
S-expression structure: PASS
symbol Gate: PASS
semantic manifest ERC: PASS
generator byte parity: PASS
```

## Native ERC result

```text
GitHub Actions run: 30028613180
job: exact-symbol-and-native-erc
head SHA tested: 0d741e46f0f817cbfa508ccfa0c92260a660f59b
native tool: KiCad 10.0.4
job conclusion: success
raw native exit code: 5
raw native violations: 14
expected root hierarchical boundaries: 11
expected parent-driven control inputs: 3
internal converter-core violations: 0
residual geometry faults: 0
native converter-core internal topology: PASS
```

Raw report не объявляется zero-error. Все 14 сообщений относятся только к standalone-проверке leaf sheet без родительского hierarchical context. Exact allowlist принимает только 11 именованных hierarchical boundaries и три входа `U_EN_GATE`; любое дополнительное нарушение блокирует CI.

Evidence:

```text
artifact: pcb-d-kicad-native-erc
artifact id: 8575877765
digest: sha256:fb661e874e79b833e84e2a8c4dd4f13694ef71c5df1ba2c4c80002703d5edf26
```

## Закрыто

```text
exact symbol instantiation: CLOSED
native KiCad parser/format Gate: CLOSED
native KiCad converter-core internal-topology ERC: CLOSED
```

## Ограничение

```text
owner KiCad 10 open/save and hierarchy-context visual/ERC review: OPEN
exact UVLO/EN, CS, gate, bootstrap and snubber calculations: OPEN
production footprint/BOM/layout: NOT FROZEN
```

## Architecture continuity

`K_MAIN` не добавлен; high current остаётся локальным PCB-D; `5V_SYS_BUS` не объединён с critical rails; SAFE/HARD_OFF остаются аппаратными; local MCU/CAN-FD/service override не получили bypass; hull thermal path не добавлен.
