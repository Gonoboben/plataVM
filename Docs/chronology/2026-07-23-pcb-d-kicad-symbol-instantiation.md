# 2026-07-23 — PCB-D exact KiCad symbol instantiation V1.9

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

## Проверка до native ERC

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
```

## Ограничение

```text
native kicad-cli ERC: OPEN until CI run
owner KiCad open/save: OPEN
production footprint/BOM/layout: NOT FROZEN
```

## Architecture continuity

`K_MAIN` не добавлен; high current остаётся локальным PCB-D; `5V_SYS_BUS` не объединён с critical rails; SAFE/HARD_OFF остаются аппаратными; local MCU/CAN-FD/service override не получили bypass; hull thermal path не добавлен.
