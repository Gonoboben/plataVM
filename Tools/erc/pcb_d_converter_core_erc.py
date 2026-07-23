#!/usr/bin/env python3
"""Semantic ERC for PCB-D converter-core manifest V1.9.

This check enforces the frozen system architecture, exact LM5143A-Q1 pin and
phase contracts, split-gate topology, direct fail-safe control boundaries,
CALC_TBD visibility, and controlled freeze state. Native KiCad ERC remains a
separate mandatory tool check.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

FORBIDDEN = {"K_MAIN", "MAIN_INPUT_BUS", "5V_CRIT", "3V3_CRIT", "EMG_4S2P"}
REQUIRED_TOP = {
    "document", "status", "source_main", "architecture", "kicad_artifacts",
    "controller", "pin_mapping", "timing", "compensation", "uvlo",
    "enable_logic", "grounding", "diagnostics", "phases", "capacitors",
    "safety", "freeze",
}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main(path: str) -> int:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    errors: list[str] = []

    missing = REQUIRED_TOP - set(data)
    if missing:
        fail(f"missing top-level keys: {sorted(missing)}", errors)

    arch = data["architecture"]
    if arch.get("input") != "PACK_BUS_P5_IN" or arch.get("output") != "5V_SYS_BUS":
        fail("converter input/output boundary mismatch", errors)
    if arch.get("phases") != 2 or arch.get("interleave_degrees") != 180:
        fail("converter must remain two-phase and 180-degree interleaved", errors)
    if arch.get("high_current_owner") != "PCB-D":
        fail("PCB-D high-current ownership missing", errors)
    if arch.get("high_current_forbidden_board") != "PCB-B":
        fail("PCB-B high-current prohibition missing", errors)
    if set(arch.get("forbidden_nets", [])) != FORBIDDEN:
        fail("forbidden-net declaration mismatch", errors)

    artifacts = data["kicad_artifacts"]
    expected_artifacts = {
        "schematic": "Hardware/KiCad/41_5V_DC_DC.kicad_sch",
        "symbol_library": "Hardware/KiCad/plataVM_symbols.kicad_sym",
        "generator": "Tools/kicad/generate_pcb_d_converter_core.py",
        "symbol_validator": "Tools/erc/pcb_d_kicad_symbol_gate.py",
    }
    for key, value in expected_artifacts.items():
        if artifacts.get(key) != value:
            fail(f"KiCad artifact path mismatch for {key}", errors)
    if artifacts.get("generator_identity") != "plataVM_symbol_gate":
        fail("third-party KiCad generator identity mismatch", errors)
    if artifacts.get("controller_instances") != 1:
        fail("exact controller must be instantiated once", errors)
    if artifacts.get("power_mosfet_instances") != 4:
        fail("four power MOSFET symbols are required", errors)
    if artifacts.get("split_gate_resistor_positions") != 8:
        fail("eight split gate-resistor positions are required", errors)
    if artifacts.get("footprints_assigned") != 0:
        fail("premature footprint assignment detected", errors)
    if artifacts.get("native_erc") != "OPEN_CI_AND_OWNER_KICAD":
        fail("native ERC status is not explicitly open", errors)

    controller = data["controller"]
    if controller.get("part") != "LM5143QRHARQ1" or controller.get("package") != "RHA VQFN-40":
        fail("controller candidate/package mismatch", errors)
    expected_ties = {
        "MODE": "VDDA", "FB1": "AGND", "FB2": "AGND",
        "COMP1": "COMP_COMMON", "COMP2": "COMP_COMMON",
        "SS1": "SS_COMMON", "SS2": "SS_COMMON", "DEMB": "VDDA",
        "DITH": "VDDA", "VOUT1": "5V_SYS_BUS", "VOUT2": "5V_SYS_BUS",
        "VOUT_route_class": "KELVIN_SENSE", "VCCX": "5V_SYS_BUS",
        "EN1": "EN_RUN", "EN2": "EN_RUN", "PG1": "P5_PGOOD_OD",
        "PG2": "NC_PG2_TESTPAD",
    }
    if controller.get("ties") != expected_ties:
        fail("single-output interleaved controller tie contract mismatch", errors)

    pinmap = data["pin_mapping"]
    expected_upper = {
        "31": "EN1", "32": "RES", "33": "DEMB", "34": "MODE",
        "35": "AGND", "36": "VDDA", "37": "RT", "38": "DITH",
        "39": "SYNCOUT", "40": "EN2",
    }
    if pinmap.get("status") != "PASS" or pinmap.get("upper_pin_group") != expected_upper:
        fail("exact LM5143A-Q1 pin-map Gate mismatch", errors)
    if pinmap.get("physical_pins") != 40 or pinmap.get("exposed_pad") != 1:
        fail("RHA-40 pin/exposed-pad count mismatch", errors)
    if pinmap.get("symbol_definition") != "PASS" or pinmap.get("symbol_instantiation") != "PASS":
        fail("exact symbol definition/instantiation is not closed", errors)
    if pinmap.get("footprint_freeze") is not False:
        fail("footprint freeze granted prematurely", errors)

    expected_phase_pins = [
        {"CS": 27, "VOUT": 26, "HB": 20, "SW": 21, "HO": 22,
         "HOL": 23, "LO": 18, "LOL": 19, "PGND": 17},
        {"CS": 4, "VOUT": 5, "HB": 11, "SW": 10, "HO": 9,
         "HOL": 8, "LO": 13, "LOL": 12, "PGND": 14},
    ]
    phases = data.get("phases", [])
    if len(phases) != 2:
        fail("phase list length is not two", errors)
    for index, phase in enumerate(phases, 1):
        if phase.get("name") != f"PHASE{index}":
            fail(f"phase {index} identity mismatch", errors)
        if phase.get("controller_pins") != expected_phase_pins[index - 1]:
            fail(f"phase {index} controller pin allocation mismatch", errors)
        if phase.get("shunt", {}).get("value") != "5 mOhm 1% Kelvin":
            fail(f"phase {index} Kelvin shunt contract mismatch", errors)
        gate = phase.get("gate_resistors", {})
        expected_gate_keys = {"HS_ON", "HS_OFF", "LS_ON", "LS_OFF"}
        if set(gate) != expected_gate_keys or any("CALC_TBD" not in str(v) for v in gate.values()):
            fail(f"phase {index} split gate-resistor boundary mismatch", errors)
        if "CALC_TBD" not in json.dumps(phase.get("cs_filter", {})):
            fail(f"phase {index} CS filter is not explicit CALC_TBD", errors)
        if "CALC_TBD" not in json.dumps(phase.get("bootstrap", {})):
            fail(f"phase {index} bootstrap is not explicit CALC_TBD", errors)
        if "DNP_CALC_TBD" not in str(phase.get("snubber")):
            fail(f"phase {index} snubber must remain DNP_CALC_TBD", errors)

    uvlo = data["uvlo"]
    if uvlo.get("ref") != "U_UVLO" or uvlo.get("value") != "CALC_TBD":
        fail("UVLO placeholder/value mismatch", errors)
    if uvlo.get("rise_target_V") != 8.9 or uvlo.get("fall_target_V") != 8.35:
        fail("UVLO target mismatch", errors)

    logic = data["enable_logic"]
    expected_inputs = {"5V_SYS_EN", "UVLO_OK", "P5_GROUP_SAFE_OFF", "P5_GROUP_HARD_OFF"}
    if logic.get("ref") != "U_EN_GATE" or set(logic.get("inputs", [])) != expected_inputs:
        fail("hardware enable-gate input contract mismatch", errors)
    if logic.get("controller_pins") != [31, 40] or not logic.get("must_be_hardware"):
        fail("EN_RUN hardware ownership mismatch", errors)
    if not logic.get("fail_safe_required") or logic.get("implementation") != "CALC_TBD":
        fail("fail-safe hardware gate must remain explicit CALC_TBD", errors)

    grounding = data["grounding"]
    if grounding.get("controller_ep_net") != "AGND":
        fail("controller exposed pad must terminate on AGND side", errors)
    if grounding.get("controlled_join_ref") != "NT_AGND_PGND":
        fail("controlled AGND/PGND join missing", errors)
    if grounding.get("copper_and_via_pattern") != "OPEN_LAYOUT_GATE":
        fail("ground copper/via Gate was closed prematurely", errors)

    diagnostics = data["diagnostics"]
    if diagnostics.get("fault_ref") != "U_FAULT":
        fail("fault export placeholder missing", errors)
    if diagnostics.get("phase_monitor_refs") != ["U_ISENSE1", "U_ISENSE2"]:
        fail("phase-monitor placeholders mismatch", errors)
    if diagnostics.get("total_monitor_ref") != "U_ISUM":
        fail("total-current monitor placeholder mismatch", errors)
    if diagnostics.get("monitor_implementation") != "CALC_TBD":
        fail("diagnostic implementation frozen prematurely", errors)

    safety = data["safety"]
    if set(safety.get("direct_inputs", [])) != {"P5_GROUP_SAFE_OFF", "P5_GROUP_HARD_OFF"}:
        fail("direct SAFE/HARD_OFF set mismatch", errors)
    if not safety.get("local_mcu_bypass_prohibited") or not safety.get("service_override_bypass_prohibited"):
        fail("hardware safety bypass prohibition missing", errors)

    required_freeze = {
        "calculation_gate": True, "pin_mapping": True,
        "kicad_symbol_definition": True, "kicad_symbol_instantiation": True,
        "native_kicad_erc": False, "owner_kicad_open_save": False,
        "production_bom": False, "footprints": False, "layout": False,
        "copper": False, "thermal_qualification": False,
    }
    if data["freeze"] != required_freeze:
        fail(f"controlled freeze state mismatch: {data['freeze']!r}", errors)

    text = json.dumps(data)
    for forbidden in FORBIDDEN:
        if text.count(forbidden) != 1:
            fail(f"forbidden token {forbidden} appears outside controlled declaration", errors)
    tbd_count = text.count("CALC_TBD")
    if tbd_count < 20:
        fail(f"CALC_TBD visibility too low: {tbd_count}", errors)

    print("PCB-D converter-core semantic ERC V1.9")
    print(f"manifest: {path}")
    print(f"phases: {len(phases)}")
    print("exact LM5143A-Q1 RHA-40 symbol instantiation: PASS")
    print(f"split gate-resistor positions: {artifacts.get('split_gate_resistor_positions')}")
    print(f"CALC_TBD markers: {tbd_count}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"RESULT: FAIL ({len(errors)} error(s))")
        return 1
    print("RESULT: PASS")
    print("NOTE: native KiCad ERC and owner KiCad open/save remain mandatory.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} MANIFEST.json", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
