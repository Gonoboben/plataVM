# 2026-07-24 — PCB-D exact discrete physical pin map V1.9

## Основание

Owner screenshots подтвердили логическую корректность converter core, но выявили generic 3-pin NMOS symbol и generic 2-pin resistor symbol для физически многовыводных компонентов.

## Выполнено

1. Зафиксирован BUK9Y6R0-60E LFPAK56 contract: `1/2/3=S`, `4=G`, `mb=D`.
2. Зафиксирован WSK2512 contract: `I1/I2` current, `E1/E2` voltage sense.
3. Созданы exact KiCad symbols и заменены 4 MOSFET + 2 shunt instances.
4. Введены отдельные `RSHx_SENSE_HI/LO` nets.
5. Обновлены controller VOUTx, CS filters and monitor boundaries.
6. Добавлены machine-readable exact discrete checks.
7. Footprints и layout намеренно не заморожены.

## Архитектура

PACK_BUS, two-phase buck, 5V_SYS_BUS, direct SAFE/HARD_OFF and AGND/PGND boundaries unchanged.
