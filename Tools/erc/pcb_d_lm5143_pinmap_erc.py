#!/usr/bin/env python3
"""Validate the exact LM5143A-Q1 RHA-40 pin map used by PCB-D.

This is a deterministic source/pin contract check. It is not a replacement for
KiCad's native electrical-rules check after symbols are instantiated.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

EXPECTED = {
    "1": "SS2", "2": "COMP2", "3": "FB2", "4": "CS2", "5": "VOUT2",
    "6": "VCCX", "7": "PG2", "8": "HOL2", "9": "HO2", "10": "SW2",
    "11": "HB2", "12": "LOL2", "13": "LO2", "14": "PGND2",
    "15": "VCC", "16": "VCC", "17": "PGND1", "18": "LO1",
    "19": "LOL1", "20": "HB1", "21": "SW1", "22": "HO1",
    "23": "HOL1", "24": "PG1", "25": "VIN", "26": "VOUT1",
    "27": "CS1", "28": "FB1", "29": "COMP1", "30": "SS1",
    "31": "EN1", "32": "RES", "33": "DEMB", "34": "MODE",
    "35": "AGND", "36": "VDDA", "37": "RT", "38": "DITH",
    "39": "SYNCOUT", "40": "EN2", "EP": "EXPOSED_PAD",
}

REQUIRED_NETS = {
    "MODE": "VDDA",
    "FB2": "AGND",
    "FB1": "AGND",
    "DEMB": "VDDA",
    "DITH": "VDDA",
    "EN1": "EN_RUN",
    "EN2": "EN_RUN",
    "COMP1": "COMP_COMMON",
    "COMP2": "COMP_COMMON",
    "SS1": "SS_COMMON",
    "SS2": "SS_COMMON",
    "PG1": "P5_PGOOD_OD",
    "PG2": "NC_PG2_TESTPAD",
}


def fail(message: str) -> None:
    raise ValueError(message)


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <pinmap.json>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    pins = data.get("pins")
    if not isinstance(pins, list):
        fail("pins must be a list")

    by_number: dict[str, dict[str, object]] = {}
    by_name: dict[str, list[dict[str, object]]] = {}
    for pin in pins:
        number = str(pin.get("number"))
        name = str(pin.get("name"))
        if number in by_number:
            fail(f"duplicate pin number: {number}")
        by_number[number] = pin
        by_name.setdefault(name, []).append(pin)

    if set(by_number) != set(EXPECTED):
        missing = sorted(set(EXPECTED) - set(by_number))
        extra = sorted(set(by_number) - set(EXPECTED))
        fail(f"pin-number set mismatch; missing={missing}, extra={extra}")

    for number, expected_name in EXPECTED.items():
        actual_name = str(by_number[number].get("name"))
        if actual_name != expected_name:
            fail(f"pin {number}: expected {expected_name}, got {actual_name}")

    for name, required_net in REQUIRED_NETS.items():
        matching = by_name.get(name, [])
        if len(matching) != 1:
            fail(f"expected exactly one {name} pin, got {len(matching)}")
        actual_net = str(matching[0].get("pcb_d_net"))
        if actual_net != required_net:
            fail(f"{name}: expected net {required_net}, got {actual_net}")

    vcc_pins = by_name.get("VCC", [])
    if sorted(str(pin["number"]) for pin in vcc_pins) != ["15", "16"]:
        fail("VCC must be pins 15 and 16")
    if {str(pin.get("pcb_d_net")) for pin in vcc_pins} != {"VCC_BIAS"}:
        fail("VCC pins 15 and 16 must share VCC_BIAS")

    ties = data.get("required_single_output_ties", {})
    expected_ties = {
        "MODE": "VDDA",
        "FB2": "AGND",
        "FB1": "AGND",
        "COMP1_COMP2": "CONNECTED",
        "SS1_SS2": "CONNECTED",
        "DEMB": "VDDA",
        "EN1_EN2": "EN_RUN",
    }
    if ties != expected_ties:
        fail(f"single-output tie contract mismatch: {ties!r}")

    freeze = data.get("freeze", {})
    if freeze.get("pin_mapping") is not True:
        fail("pin_mapping must be frozen after verification")
    for key in ("symbol_geometry", "footprint", "layout", "production_bom"):
        if freeze.get(key) is not False:
            fail(f"{key} must remain false")

    print("LM5143A-Q1 RHA-40 pin-map ERC: PASS")
    print(f"physical pins: {len(EXPECTED) - 1}")
    print("exposed pad: 1")
    print("single-output interleaved ties: PASS")
    print("PG1/PG2 role separation: PASS")
    print("production footprint/BOM freeze: NOT GRANTED")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"LM5143A-Q1 RHA-40 pin-map ERC: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
