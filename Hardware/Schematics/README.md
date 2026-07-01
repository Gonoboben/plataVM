# Schematics

Схемотехника ПДУ БНПА V1.5 делится на следующие функциональные листы:

1. `01_Battery_Front_End` — входы АКБ_1/АКБ_2.
2. `02_Battery_Disconnect_Precharge` — BATTERY_DISCONNECT и PRECHARGE.
3. `03_Main_Input_Bus` — MAIN_INPUT_BUS.
4. `04_Power_12V_Bus` — POWER_12V_BUS CH1...CH14.
5. `05_5V_Sys_Bus` — внешняя 5V_SYS_BUS.
6. `06_Light_Branch` — onboard LED drivers для Epistar XY-J45.
7. `07_Reserve_Keep_Alive` — RESERVE_BRANCH, EMG, 5V_CRIT, 3V3_CRIT.
8. `08_MCU_Control` — MCU, watchdog, fault manager.
9. `09_Interfaces` — RS-485, UART, SWD, optional CAN footprint.

Перед созданием схемы свериться с `Docs/PROJECT_MASTER.md`, `Docs/ARCHITECTURE_BASELINE.md` и `Docs/OPEN_QUESTIONS.md`.