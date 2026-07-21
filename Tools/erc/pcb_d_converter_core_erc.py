#!/usr/bin/env python3
"""Preliminary semantic ERC for PCB-D converter-core manifest V1.9.

This is not a replacement for native KiCad ERC. It checks project architecture,
required two-phase connectivity, safety ownership, CALC_TBD visibility and
absence of forbidden power-domain substitutions before symbol instantiation.
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
    ties = controller.get("ties", {})
    required_ties = {
        "MODE": "VDDA",
        "FB1": "POWER_GND",
        "FB2": "POWER_GND",
        "COMP1": "COMP_COMMON",
        "COMP2": "COMP_COMMON",
        "SS1": "SS_COMMON",
        "SS2": "SS_COMMON",
        "DEMB": "VDDA",
        "DITH": "VDDA",
        "VOUT1": "5V_SYS_BUS",
        "VOUT2": "5V_SYS_BUS",
    }
    for pin, net in required_ties.items():
        if ties.get(pin) != net:
            fail(f"{pin} must connect to {net}", errors)

    phases = data.get("phases", [])
    if len(phases) != 2:
        fail("phase list length is not two", errors)
    seen: set[str] = set()
    for index, phase in enumerate(phases, 1):
        name = phase.get("name")
        if name in seen:
            fail(f"duplicate phase {name}", errors)
        seen.add(name)
        for key in (
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
        if phase.get("shunt", {}).get("value") != "5 mOhm 1% Kelvin":
            fail(f"phase {index} shunt value/Kelvin rule mismatch", errors)
        if "CALC_TBD" not in json.dumps(phase.get("cs_filter", {})):
            fail(f"phase {index} CS-filter CALC_TBD not explicit", errors)

    logic = data["enable_logic"]
    expected = {
        "5V_SYS_EN",
        "UVLO_OK",
        "P5_GROUP_SAFE_OFF",
        "P5_GROUP_HARD_OFF",
    }
    if set(logic.get("inputs", [])) != expected:
        fail("enable logic input set mismatch", errors)
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
    if not safety.get("local_mcu_bypass_prohibited"):
        fail("MCU bypass prohibition missing", errors)
    if not safety.get("service_override_bypass_prohibited"):
        fail("SERVICE_OVERRIDE bypass prohibition missing", errors)

    freeze = data["freeze"]
    for key, value in freeze.items():
        if value is not False:
            fail(f"premature freeze detected: {key}", errors)

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
        "NOTE: native KiCad ERC remains mandatory after exact symbols/pins are instantiated."
    )
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} MANIFEST.json", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
