# Открытые вопросы ПДУ БНПА / PlataVM V1.9

Дата пересмотра: 2026-07-21  
Источник: решение владельца по форме V1.9 — `SERVICE_OVERRIDE`, вариант B  
Статус: `OWNER INPUT V1.9 APPLIED`; Q-SYS-007 закрыт, preliminary packaging boundary и physical interface count подготовлены.

## 1. Закрытые и зафиксированные решения

### 1.1 Battery Front-End и главная шина

| ID | Решение | Статус |
|---|---|---|
| Q-BFE-001 | Механическое соединение под нагрузкой не является штатной операцией | CLOSED |
| Q-BFE-002 | Обе исправные АКБ работают параллельно; межблочное выравнивание выполняется в DECK_BALANCE | CLOSED |
| Q-BFE-003A | Длина каждой батарейной кабельной сборки — 1 м | CLOSED |
| Q-BFE-004 | K_BAT1/K_BAT2 — однополюсные контакторы по плюсу | CLOSED |
| Q-BFE-005 | Центральный K_MAIN отсутствует; PACK_BUS — главная силовая шина | CLOSED |
| Q-BFE-006 | Штатный HARD_OFF: запрет новых команд → отключение тяжёлых нагрузок и электронных силовых трактов → журнал → разрыв hold loop → контроль токов и PACK_BUS | CLOSED |
| Q-BFE-007 | В корпусе АКБ не устанавливается дополнительная активная электроника | CLOSED |
| Q-BFE-008 | BMS работает автономно без обязательной цифровой телеметрии | CLOSED |
| Q-BFE-009 | RS-485/CAN/UART через батарейный соединитель не используются | CLOSED |

### 1.2 BMS и основные ячейки

| ID | Решение | Статус |
|---|---|---|
| Q-BMS-001 | BMS — закрытый двухполюсный защищённый источник BAT_PROT+ / BAT_PROT− | CLOSED |
| Q-BMS-002 | Raw-ветвь, внутренние точки и сигналы BMS не используются | CLOSED |
| Q-BMS-003 | Схема контактора не зависит от high-side/low-side topology BMS | CLOSED |
| Q-BMS-004 | Hunan Huaxing 32700-6000mAh LiFePO4, 3,2 В, 6 А·ч; 4S24P = 12,8 В, 144 А·ч | CLOSED |
| Q-BMS-005 | BMS LiFePO4 4S 12 V 30 A symmetric, supplier item 0102; изготовитель платы не идентифицирован | CLOSED_PRELIMINARY |
| Q-BMS-006 | Предварительно OV 3,65 В/cell, UV 2,3 В/cell; reconnect/delays проверяются отдельно | CLOSED_PARTIAL |
| Q-BMS-009 | 30 А continuous discharge, 40 А short, 60 А/1 с peak, 15 А charge, 30 мА balance | CLOSED_PRELIMINARY |

### 1.3 K_BATx

| ID | Решение | Статус |
|---|---|---|
| Q-KBAT-001 | Моностабильный normally-open SPST-NO контактор | CLOSED |
| Q-KBAT-002 | Одна катушка continuous duty | CLOSED |
| Q-KBAT-003 | При снятии питания пружиной возвращается в OPEN | CLOSED |
| Q-KBAT-004 | Self-hold через механически связанный K_BAT_AUX_NO | CLOSED |
| Q-KBAT-005 | Исчезновение BAT_PROT автоматически открывает K_BATx | CLOSED |
| Q-KBAT-006 | После BMS recovery требуется новый LOCAL_START | CLOSED |
| Q-KBAT-007 | Control range 0…16 В; normal coil range 9…14,6 В | CLOSED_PRELIMINARY |
| Q-KBAT-008 | Guaranteed pull-in 9…16 В | CLOSED_PRELIMINARY |
| Q-KBAT-009 | Guaranteed hold 7,5…16 В | CLOSED_PRELIMINARY |
| Q-KBAT-011 | Inrush ≤2 А / 150 мс | CLOSED_PRELIMINARY |
| Q-KBAT-012 | Hold target ≤0,15 А/2 Вт; limit ≤0,25 А/4 Вт | CLOSED_PRELIMINARY |
| Q-KBAT-013 | Economizer preferred; chatter/restart cycling запрещены | CLOSED_ARCHITECTURE |
| Q-KBAT-015 | Flyback diode без проверки не принимается; TVS/bidirectional TVS/diode+R анализируются | CLOSED_DIRECTION |
| Q-KBAT-016 | Main contact ≥30 А continuous; target class ≥50 А | CLOSED_PRELIMINARY |
| Q-KBAT-017 | DC breaking ≥30 А при 16 В DC | CLOSED_PRELIMINARY |
| Q-KBAT-018 | Contact resistance ≤2 мОм new, ≤5 мОм end-of-life | CLOSED_PRELIMINARY |
| Q-KBAT-019 | Work −20…+60 °C; storage −30…+70 °C; humidity/condensation; coating; life requirements | CLOSED_REQUIREMENT |
| Q-KBAT-020 | WELDED_CONTACT диагностируется и блокирует restart | CLOSED_REQUIREMENT |
| Q-KBAT-021 | Normal OFF: loads/MAIN_SW off → current decay → hold loop open; EXT_KILL immediate | CLOSED |
| Q-KBAT-028 | Vibration profile не задаётся владельцем; solder/screws primary, hot-melt adhesive auxiliary only | CLOSED_OWNER_SCOPE_WITH_DFM_RULES |

### 1.4 LOCAL_START и REMOTE_OFF

| ID | Решение | Статус |
|---|---|---|
| Q-LS-001 | LOCAL_START — отдельный двухконтактный connector | CLOSED |
| Q-LS-002 | Normally open, spring return, no latching | CLOSED |
| Q-LS-003 | Параллельно K_BAT_AUX_NO | CLOSED |
| Q-LS-004 | AUX ≥0,5 А при 16 В DC и ≥2 А /150 мс | CLOSED_PRELIMINARY |
| Q-LS-005 | LOCAL_START rating не ниже AUX | CLOSED_PRELIMINARY |
| Q-LS-006 | F_CTRL у ответвления BAT_PROT+ внутри battery housing | CLOSED |
| Q-LS-007 | Stuck LOCAL_START — fault; restart только после подтверждённого release | CLOSED_REQUIREMENT |
| Q-ROFF-001 | REMOTE_OFF разрывает hold loop единственной катушки | CLOSED |
| Q-ROFF-002 | Восстановление loop не включает K_BATx | CLOSED |
| Q-ROFF-003 | Pin 11: ≤0,25 А continuous и 2 А pulsed | CLOSED_PRELIMINARY |
| Q-ROFF-004 | Energize-to-run relay с physical NO run-contact | CLOSED_ARCHITECTURE |
| Q-ROFF-005 | Два независимых run-contact; EXT_KILL independent | CLOSED_ARCHITECTURE |
| Q-ROFF-006 | t_OFF ≥ max(250 мс; 5 × t_release_max) | CLOSED_PRELIMINARY |
| Q-ROFF-007 | Loop restore после выдержки и подтверждения OPEN | CLOSED |
| Q-ROFF-009 | HARD_OFF_FAILED при отсутствии OPEN; restart blocked | CLOSED_REQUIREMENT |
| Q-ROFF-010 | EXT_KILL последовательно после LOCAL_START ∥ AUX_NO | CLOSED_ARCHITECTURE |
| Q-ROFF-012 | Loss critical power/supervisor opens hold loop | CLOSED_ARCHITECTURE |

### 1.5 DECK_BALANCE

| ID | Решение | Статус |
|---|---|---|
| Q-DB-001 | BMS charge max 15 А; DECK_BALANCE отдельный limited mode | CLOSED_PRELIMINARY |
| Q-DB-002 | Nominal 2 А | CLOSED_PRELIMINARY |
| Q-DB-003 | Hard limit 3 А | CLOSED_PRELIMINARY |
| Q-DB-005 | Finish abs(ΔU) ≤50 мВ и abs(I) ≤0,2 А for 60 s | CLOSED_PRELIMINARY |
| Q-DB-006 | No new battery temperature sensors; allow only confirmed 0…45 °C | CLOSED_OWNER_DECISION |

### 1.6 PCB-C POWER_12V

| ID | Решение | Статус |
|---|---|---|
| Q-P12-001 | CH1…CH14 hardware names; assignments software-defined | CLOSED |
| Q-P12-002 | 3 А continuous/channel | CLOSED |
| Q-P12-003 | 5 А peak до 1 с; individual limit/protection | CLOSED_PRELIMINARY |
| Q-P12-004 | CH12…CH14 Always-On monitored but subject to protection/SAFE/HARD_OFF | CLOSED |
| Q-P12-005 | PCB-C hardware rating 30 А continuous; system budget limits simultaneous use | CLOSED_PRELIMINARY |
| Q-P12-006 | Local MCU/I/O/ADC + CAN-FD; direct SAFE/HARD_OFF | CLOSED_ARCHITECTURE |

### 1.7 PCB-D POWER_5V

| ID | Решение | Статус |
|---|---|---|
| Q-5V-001 | 10 external 5V_OUT | CLOSED |
| Q-5V-002 | Up to 3 А/output | CLOSED |
| Q-5V-003 | Three Always-On monitored outputs | CLOSED |
| Q-5V-004 | Per-output current diagnostics mandatory | CLOSED |
| Q-5V-005 | 15 А continuous / 20 А short total | CLOSED_ASSUMPTION |
| Q-5V-006 | OUT8…OUT10 assignment software-defined | CLOSED |
| Q-5V-007 | Preliminary two-phase synchronous buck; thermal contact to hull prohibited; low-loss/internal-convection design | CLOSED_TOPOLOGY_PRELIMINARY_UPDATED_V1_8 |
| Q-5V-008 | Local MCU/I/O/ADC + CAN-FD; hard-off direct | CLOSED_ARCHITECTURE |

### 1.8 PCB-E LIGHT_POWER

| ID | Решение | Статус |
|---|---|---|
| Q-LGT-001 | Six logically independent channels | CLOSED |
| Q-LGT-002 | LED current calculation maximum 1,05 А/matrix | CLOSED_ASSUMPTION |
| Q-LGT-003 | Per-channel diagnostics mandatory | CLOSED |
| Q-LGT-004 | Two symmetric zones 2×3 | CLOSED |
| Q-LGT-005 | Functional input 8…16 В; protected range preliminary 9,2…14,6 В | CLOSED_PRELIMINARY |
| Q-LGT-006 | No separate brightness limit in SINGLE_PACK_MODE; general system budget applies | CLOSED_OWNER_DECISION |
| Q-LGT-007 | PWM 3,3 В active-high, default 1 кГц, configurable 100…1000 Гц | CLOSED_PRELIMINARY |

### 1.9 Interfaces, MCU и grounds

| ID | Решение | Статус |
|---|---|---|
| Q-IF-001 | External CAN optional/DNP; external baseline RS-485 | CLOSED |
| Q-IF-002 | RS-485 115200, half-duplex, 8N1, addressed binary, CRC-16, sequence, timeout/heartbeat | CLOSED_PRELIMINARY |
| Q-IF-003 | External isolated RS-485 | CLOSED |
| Q-MCU-001 | STM32G4 family; packages after pin count | CLOSED_FAMILY |
| Q-SCH-001 | Accepted schematic hierarchy | CLOSED |
| Q-SCH-002 | Logical interfaces before physical connectors | CLOSED |
| Q-SCH-003 | High currents distributed from PCB-A, not through PCB-B | CLOSED |
| Q-SCH-004 | Owner verified opening root project and sheets 00…56 | CLOSED_OWNER_VERIFICATION |
| Q-SCH-005 | Internal CAN-FD for normal traffic; direct safety/fault wires | CLOSED_ARCHITECTURE |
| Q-SCH-007 | One SIGNAL_GND–POWER_GND controlled point on PCB-B | CLOSED_ARCHITECTURE |
| Q-SCH-008 | Shields to CHASSIS at entry; ISO_GND isolated | CLOSED_ARCHITECTURE |
| Q-SCH-009 | Passive INTERCONNECT; power paths separated | CLOSED |
| Q-SCH-010 | PCB-A near power entry; PCB-B low-noise placement; C/D/E near loads where possible | CLOSED_ARCHITECTURE |
| Q-SCH-011 | Refdes ranges A100, B200, C300, D400, E500 | CLOSED |

### 1.10 Механика и environment

| ID | Решение | Статус |
|---|---|---|
| Q-MECH-001 | Maximum width 100 мм | CLOSED |
| Q-MECH-002 | Electronics in dry sealed enclosure; internal connectors need no separate external sealing | CLOSED_SCOPE |
| Q-MECH-003 | Five PCB modules + passive INTERCONNECT | CLOSED |
| Q-MECH-004 | Cylinder, removable connector lid, service from lid side | CLOSED |
| Q-MECH-005 | Separate power wiring + passive signal INTERCONNECT | CLOSED_ARCHITECTURE |
| Q-MECH-006 | Owner-defined internal cylinder Ø130 × 1000 мм; wall/material outside PCB scope | CLOSED_OWNER_DEFINED_ENVELOPE |
| Q-MECH-007 | Multilevel electronic assembly ≤100 × 250 × 80 мм; connector-lid map owner-controlled | CLOSED_OWNER_ENVELOPE_PRELIMINARY_LENGTH |
| Q-MECH-008 | Entire assembly removed with lid; boards screwed to owner-selected standoffs; PCB mounting holes required | CLOSED_OWNER_MECHANICAL_CONCEPT |
| Q-MECH-009 | Pressure hull outside electronics scope; hot-melt adhesive auxiliary only | CLOSED_OWNER_SCOPE_WITH_DFM_RULES |
| Q-MECH-010 | No thermal contact to hull; internal natural convection and low-loss design | CLOSED_OWNER_THERMAL_CONSTRAINT |
| Q-MECH-011 | PACKAGING-P1: L0 A+C, L1 D+E, L2 B; preliminary area budgets fit 100 × 250 × 80 мм | CLOSED_PRELIMINARY_FLOORPLAN |
| Q-MECH-012 | Logical power/signal interface count completed; physical connector placement remains separate | CLOSED_PARTIAL_PIN_COUNT |

### 1.11 System power budget, SINGLE_PACK_MODE и service

| ID | Решение | Статус |
|---|---|---|
| Q-SYS-001 | DUAL 40/44 А; SINGLE 20/22 А | CLOSED_SYSTEM_LIMIT_PRELIMINARY |
| Q-SYS-002 | SINGLE_PACK_MODE degraded functional; no category-based automatic shutdown; DECK_BALANCE prohibited | CLOSED_OWNER_DECISION |
| Q-SYS-003 | Warning 85 %; reject new noncritical at 100 %; no software shedding of running loads | CLOSED_OWNER_DECISION |
| Q-SYS-004 | Short ≤1 с; repeat interval ≥10 с; I²t/thermal accumulator | CLOSED_PRELIMINARY_TIMING |
| Q-SYS-005 | Low-pass 100 мс; warning 85 %/250 мс; clear 80 %/2 с; re-enable 90 %/2 с | CLOSED_PRELIMINARY_FIRMWARE_POLICY |
| Q-SYS-006 | Critical only PCB-B critical domain; external CH/5V/LED noncritical; load profiles required | CLOSED_OWNER_CLASSIFICATION |
| Q-SYS-007 | Guarded SERVICE_OVERRIDE: SERVICE_MODE, authorization, double confirmation, one output, 60 с lease, short limits unchanged, full logging | CLOSED_OWNER_DECISION |

### 1.12 СН-176А-12 owner-controlled scope

| ID | Решение владельца / внешнее ограничение | Статус |
|---|---|---|
| Q-CON-001 | Only working battery inter-housing connector | CLOSED |
| Q-CON-002 | Pins 1–5 BAT+, 6–10 BAT− | CLOSED |
| Q-CON-003 | 20 А continuous / 22 А short target; 17,5 А air limit until confirmation | OWNER_CONTROLLED_PRELIMINARY |
| Q-CON-004 | Cable composition accepted by owner | OWNER_CONFIRMED |
| Q-CON-005 | Pin 11 REMOTE_OFF / K_BAT_HOLD_RETURN | CLOSED |
| Q-CON-006 | Pin numbering confirmed | OWNER_CONFIRMED |
| Q-CON-007 | Current sharing assumption accepted by owner | OWNER_ACCEPTED_ASSUMPTION |
| Q-CON-008 | Contact/cable thermal qualification outside current engineering scope | OWNER_SCOPE_EXTERNAL |
| Q-CON-009 | Pin 12 RESERVE | CLOSED |
| Q-CON-010 | Pin 11 ≤0,25 А continuous / 2 А 150 мс | CLOSED_PRELIMINARY |
| Q-CON-011 | Pin 11 suitability accepted; F_CTRL/hold limits remain | OWNER_ACCEPTED_ASSUMPTION |

## 2. KiCad и physical interfaces

| ID | Открытый вопрос | Статус |
|---|---|---|
| Q-SCH-006 | Select physical interboard connector families after current, height and mating-cycle calculations | OPEN_COMPONENT_SELECTION |
| Q-SCH-012 | Record KiCad version and ERC report for release commit before schematic freeze | OPEN_RELEASE_VERIFICATION |
| Q-IF-004 | Confirm one 32-position A↔B signal connector or split into 16-position CTRL + 16-position DIAG | OPEN_PACKAGING_DECISION |
| Q-IF-005 | Select standardized 8-position signal connector class for PCB-C/D/E | OPEN_COMPONENT_SELECTION |
| Q-IF-006 | Define final CAN-FD physical node order and termination positions | OPEN_LAYOUT_DECISION |

## 3. Фактическое поведение BMS

| ID | Открытый вопрос | Статус |
|---|---|---|
| Q-BMS-007 | BAT_PROT fall shape/speed at UV/OC/SCP | OPEN_TEST |
| Q-BMS-008 | BAT_PROT recovery and external charge/reset requirement | OPEN_TEST |

## 4. K_BATx selection and tests

| ID | Открытый вопрос | Статус |
|---|---|---|
| Q-KBAT-010 | Guaranteed dropout range | OPEN_CANDIDATE |
| Q-KBAT-014 | Slow voltage fall/recovery behavior | OPEN_TEST |
| Q-KBAT-022 | Coil inductance and stored energy | OPEN_MEASUREMENT |
| Q-KBAT-023 | Economizer repeated-start/brownout behavior | OPEN_TEST |
| Q-KBAT-024 | Coil temperature at 16 В and Tmax | OPEN_THERMAL_TEST |
| Q-KBAT-025 | Suppression providing release ≤100 мс | OPEN_CALC_TEST |
| Q-KBAT-026 | 30 А/16 В DC breaking for actual L/R load | OPEN_CANDIDATE_TEST |
| Q-KBAT-027 | Contact resistance/temperature after life | OPEN_LIFE_TEST |

## 5. LOCAL_START, REMOTE_OFF and fault injection

| ID | Открытый вопрос | Статус |
|---|---|---|
| Q-LS-008 | K_BAT_AUX_NO weld diagnostics | OPEN_DESIGN |
| Q-LS-009 | LOCAL_START bounce test 5…20 мс | OPEN_TEST |
| Q-LS-010 | AUX minimum wetting current | OPEN_CANDIDATE |
| Q-LS-011 | Final F_CTRL by time-current and I²t | OPEN_CALC |
| Q-ROFF-008 | Pin 11 short-to-BAT_PROT− FMEA and EXT_KILL bypass protection | OPEN_FMEA_TEST |
| Q-ROFF-011 | Energize-to-run relay candidate and DC/transient rating | OPEN_CANDIDATE |

## 6. DECK_BALANCE

| ID | Открытый вопрос | Статус |
|---|---|---|
| Q-DB-004 | Maximum timeout and no-progress criterion | OPEN_CALC_TEST |

## 7. PCB packaging, current calculation and thermal verification

| ID | Открытый вопрос | Статус |
|---|---|---|
| Q-PKG-001 | Create preliminary KiCad board outlines from V1.9 area budgets | OPEN_MECHANICAL_DESIGN |
| Q-PKG-002 | Define mounting-hole coordinates after owner selects screw/standoff class | OPEN_OWNER_COMPONENT_INPUT |
| Q-PKG-003 | Perform component-height audit and 3D inter-level clearance review | OPEN_COMPONENT_LAYOUT |
| Q-PKG-004 | Confirm PACKAGING-P1 or revise level allocation after thermal/component audit | OPEN_REVIEW |
| Q-PWR-001 | Calculate maximum PCB-B critical branch current and A↔B power connector rating | OPEN_CALC |
| Q-PWR-002 | Calculate PCB-D input current, efficiency and branch connector rating | OPEN_CALC |
| Q-PWR-003 | Calculate PCB-E worst-case branch current and connector rating | OPEN_CALC |
| Q-THERM-001 | PCB-A…PCB-E loss budget and thermal test at +60 °C without hull contact | OPEN_CALC_TEST |
| Q-THERM-002 | Confirm continuous ratings or derating after sealed-volume thermal test | OPEN_TEST_DECISION |

## 8. Текущий Gate G-R

Закрыты owner-level входы V1.9:

1. internal/assembly envelope;
2. multilevel mounting and extraction;
3. pressure-hull scope boundary;
4. thermal-path constraint;
5. short duration/cooldown/I²t;
6. filtering/hysteresis;
7. load classification/profiles;
8. guarded SERVICE_OVERRIDE;
9. preliminary packaging boundary;
10. preliminary physical interface count.

Полный Gate G-R остаётся открыт до:

1. BMS BAT_PROT fault/recovery tests;
2. K_BATx and REMOTE_OFF candidate selection/tests;
3. preliminary KiCad outlines and mounting review;
4. current/thermal calculations;
5. connector class comparison and selection;
6. release ERC.

Подробности V1.9:

```text
Docs/SERVICE_OVERRIDE_POLICY.md
Docs/PCB_PACKAGING_BOUNDARY_V1_9.md
Docs/PCB_MODULE_AREA_BUDGET_V1_9.md
Docs/PHYSICAL_INTERFACE_COUNT_V1_9.md
Docs/adr/ADR-2026-07-21-service-override-v1-9.md
Docs/chronology/2026-07-21-service-override-v1-9.md
```
