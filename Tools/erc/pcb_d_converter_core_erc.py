#!/usr/bin/env python3
"""Semantic ERC for PCB-D converter-core manifest V1.9.

This is not a replacement for native KiCad ERC. It checks project architecture,
exact LM5143A-Q1 pin-contract references, required two-phase connectivity,
safety ownership, CALC_TBD visibility and controlled freeze state.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_TOP = {
    "document",
    "status",
    "source_main",
    "architecture",
    "controller",
    "pin_mapping",
    "timing",
    "compensation",
    "uvlo",
    "enable_logic",
    "phases",
    "capacitors",
    "safety",
    "freeze",
}
FORBIDDEN = {"K_MAIN", "MAIN_INPUT_BUS", "5V_CRIT", "3V3_CRIT", "EMG_4S2P"}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main(path: str) -> int:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []

    missing = REQUIRED_TOP - set(data)
    if missing:
        fail(f"missing top-level keys: {sorted(missing)}", errors)

    arch = data["architecture"]
    if arch.get("input") != "PACK_BUS_P5_IN":
        fail("wrong converter input boundary", errors)
    if arch.get("output") != "5V_SYS_BUS":
        fail("wrong converter output boundary", errors)
    if arch.get("phases") != 2:
        fail("converter must contain exactly two phases", errors)
    if arch.get("interleave_degrees") != 180:
        fail("phase shift must be 180 degrees", errors)
    if arch.get("high_current_forbidden_board") != "PCB-B":
        fail("PCB-B high-current prohibition missing", errors)
    if not FORBIDDEN.issubset(set(arch.get("forbidden_nets", []))):
        fail("forbidden-net list is incomplete", errors)

    controller = data["controller"]
    if controller.get("part") != "LM5143QRHARQ1":
        fail("controller candidate mismatch", errors)
    if controller.get("package") != "RHA VQFN-40":
        fail("controller package mismatch", errors)
    ties = controller.get("ties", {})
    required_ties = {
        "MODE": "VDDA",
        "FB1": "AGND",
        "FB2": "AGND",
        "COMP1": "COMP_COMMON",
        "COMP2": "COMP_COMMON",
        "SS1": "SS_COMMON",
        "SS2": "SS_COMMON",
        "DEMB": "VDDA",
        "DITH": "VDDA",
        "VOUT1": "5V_SYS_BUS_SENSE",
        "VOUT2": "5V_SYS_BUS_SENSE",
        "VCCX": "5V_SYS_BUS",
        "EN1": "EN_RUN",
        "EN2": "EN_RUN",
        "PG1": "P5_PGOOD_OD",
        "PG2": "NC_PG2_TESTPAD",
    }
    for pin, net in required_ties.items():
        if ties.get(pin) != net:
            fail(f"{pin} must connect to {net}", errors)

    pinmap = data["pin_mapping"]
    if pinmap.get("status") != "PASS":
        fail("exact pin-map Gate is not PASS", errors)
    if pinmap.get("physical_pins") != 40 or pinmap.get("exposed_pad") != 1:
        fail("RHA-40 pin/exposed-pad count mismatch", errors)
    expected_upper = {
        "31": "EN1", "32": "RES", "33": "DEMB", "34": "MODE",
        "35": "AGND", "36": "VDDA", "37": "RT", "38": "DITH",
        "39": "SYNCOUT", "40": "EN2",
    }
    if pinmap.get("upper_pin_group") != expected_upper:
        fail("LM5143A-Q1 pins 31..40 mismatch", errors)
    if pinmap.get("footprint_freeze") is not False:
        fail("footprint freeze was granted prematurely", errors)

    phases = data.get("phases", [])
    if len(phases) != 2:
        fail("phase list length is not two", errors)
    expected_phase_pins = [
        {"CS": 27, "VOUT": 26, "HB": 20, "SW": 21, "HO": 22,
         "HOL": 23, "LO": 18, "LOL": 19, "PGND": 17},
        {"CS": 4, "VOUT": 5, "HB": 11, "SW": 10, "HO": 9,
         "HOL": 8, "LO": 13, "LOL": 12, "PGND": 14},
    ]
    seen: set[str] = set()
    for index, phase in enumerate(phases, 1):
        name = phase.get("name")
        if name in seen:
            fail(f"duplicate phase {name}", errors)
        seen.add(name)
        for key in (
            "controller_pins",
            "high_side",
            "low_side",
            "inductor",
            "shunt",
            "switch_net",
            "cs_filter",
            "gate_resistors",
            "bootstrap",
            "snubber",
        ):
            if key not in phase:
                fail(f"phase {index} missing {key}", errors)
        if phase.get("controller_pins") != expected_phase_pins[index - 1]:
            fail(f"phase {index} controller pin map mismatch", errors)
        if phase.get("shunt", {}).get("value") != "5 mOhm 1% Kelvin":
            fail(f"phase {index} shunt value/Kelvin rule mismatch", errors)
        if "CALC_TBD" not in json.dumps(phase.get("cs_filter", {})):
            fail(f"phase {index} CS-filter CALC_TBD not explicit", errors)

    logic = data["enable_logic"]
    expected_inputs = {
        "5V_SYS_EN",
        "UVLO_OK",
        "P5_GROUP_SAFE_OFF",
        "P5_GROUP_HARD_OFF",
    }
    if set(logic.get("inputs", [])) != expected_inputs:
        fail("enable logic input set mismatch", errors)
    if logic.get("controller_pins") != [31, 40]:
        fail("EN_RUN must drive EN1 pin 31 and EN2 pin 40", errors)
    if not logic.get("must_be_hardware"):
        fail("enable logic is not marked hardware", errors)
    if data["uvlo"].get("value") != "CALC_TBD":
        fail("UVLO exact implementation must remain CALC_TBD", errors)

    safety = data["safety"]
    if set(safety.get("direct_inputs", [])) != {
        "P5_GROUP_SAFE_OFF",
        "P5_GROUP_HARD_OFF",
    }:
        fail("direct safety inputs incomplete", errors)
    if safety.get("power_good_source") != "PG1 pin 24":
        fail("single-output PGOOD must come from PG1 pin 24", errors)
    if safety.get("pg2_policy") != "testpad only; not aggregated":
        fail("PG2 isolation policy missing", errors)
    if not safety.get("local_mcu_bypass_prohibited"):
        fail("MCU bypass prohibition missing", errors)
    if not safety.get("service_override_bypass_prohibited"):
        fail("SERVICE_OVERRIDE bypass prohibition missing", errors)

    freeze = data["freeze"]
    required_freeze = {
        "calculation_gate": True,
        "pin_mapping": True,
        "kicad_symbol_instantiation": False,
        "native_kicad_erc": False,
        "production_bom": False,
        "footprints": False,
        "layout": False,
        "copper": False,
        "thermal_qualification": False,
    }
    if freeze != required_freeze:
        fail(f"freeze policy mismatch: {freeze!r}", errors)

    text = json.dumps(data)
    for forbidden in FORBIDDEN:
        count = text.count(forbidden)
        if count != 1:
            fail(
                f"forbidden token {forbidden} appears outside controlled declaration",
                errors,
            )

    tbd_count = text.count("CALC_TBD")
    if tbd_count < 8:
        warnings.append(
            f"low CALC_TBD count ({tbd_count}); review unresolved values"
        )

    print("PCB-D converter-core semantic ERC V1.9")
    print(f"manifest: {path}")
    print(f"phases: {len(phases)}")
    print("exact LM5143A-Q1 RHA-40 pin map: PASS")
    print(f"CALC_TBD markers: {tbd_count}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"RESULT: FAIL ({len(errors)} error(s))")
        return 1
    print("RESULT: PASS")
    print(
        "NOTE: native KiCad ERC remains mandatory after exact symbols are instantiated."
    )
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} MANIFEST.json", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
