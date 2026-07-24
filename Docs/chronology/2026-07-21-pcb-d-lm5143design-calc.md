# 2026-07-21 — PCB-D LM5143DESIGN-CALC Gate V1.9

## Base

```text
main = c513dbb3c9da57b8b5a26e755accc94e893e3ef3
PR #44 = merged
```

## Выполнено

1. Прочитаны PROJECT_MASTER, ARCHITECTURE_BASELINE и PCB-D V1.9 calculation/component documents.
2. Выполнен official LM5143 family quick-start calculation для single-output two-phase FPWM.
3. Calculator result сопоставлен с independent manual ripple/OCP calculation.
4. Проверены RT, oscillator tolerance sweep, soft-start, OCP и slope-compensation relation.
5. Выявлено, что passive EN divider не обеспечивает требуемую UVLO hysteresis; external supervisor оставлен `CALC_TBD`.
6. Compensation calculator proposal `26,1 кОм /2,0 нФ /220 пФ` проверен отдельно.
7. После tolerance sweep принят более устойчивый prototype start `24,9 кОм /3,3 нФ /220 пФ`.
8. Получено nominal `fc≈29,18 кГц`, `PM≈73,55°`; modeled minimum PM ≈56,21°.
9. Подготовлен preliminary converter-core KiCad sheet с явными `CALC_TBD`.
10. Добавлен machine-readable manifest и выполнен semantic ERC: PASS.
11. Native KiCad ERC оставлен открытым, так как exact symbol/pin instantiation ещё не выполнен.

## Architecture continuity

Не изменены:

- отсутствие `K_MAIN`;
- PACK_BUS fanout;
- запрет high current через PCB-B;
- независимые SAFE/HARD_OFF;
- разделение 5V_SYS_BUS и critical rails;
- passive INTERCONNECT;
- no hull thermal contact;
- no production BOM/footprint freeze.

## Next

```text
exact controller/discrete symbols and pin mapping
→ owner KiCad 10.0 open
→ native ERC
→ Bode/load-step/OCP bench correlation
→ footprint/3D candidate review
→ prototype BOM Gate
```
