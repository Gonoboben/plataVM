#!/usr/bin/env python3
"""Validate PCB-D KiCad 10 symbol instantiation before native ERC.

This deterministic gate checks the generated S-expression, exact LM5143A-Q1
RHA-40 pin contract, converter-core instances, direct safety-control boundaries,
explicit CALC_TBD visibility, and the absence of premature footprint/layout
freezes. It does not replace ``kicad-cli sch erc``.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

EXPECTED_PINS = {
    "1": ("SS2", "passive"), "2": ("COMP2", "passive"),
    "3": ("FB2", "input"), "4": ("CS2", "input"),
    "5": ("VOUT2", "input"), "6": ("VCCX", "power_in"),
    "7": ("PG2", "open_collector"), "8": ("HOL2", "output"),
    "9": ("HO2", "output"), "10": ("SW2", "passive"),
    "11": ("HB2", "passive"), "12": ("LOL2", "output"),
    "13": ("LO2", "output"), "14": ("PGND2", "power_in"),
    "15": ("VCC", "power_out"), "16": ("VCC", "passive"),
    "17": ("PGND1", "power_in"), "18": ("LO1", "output"),
    "19": ("LOL1", "output"), "20": ("HB1", "passive"),
    "21": ("SW1", "passive"), "22": ("HO1", "output"),
    "23": ("HOL1", "output"), "24": ("PG1", "open_collector"),
    "25": ("VIN", "power_in"), "26": ("VOUT1", "input"),
    "27": ("CS1", "input"), "28": ("FB1", "input"),
    "29": ("COMP1", "output"), "30": ("SS1", "input"),
    "31": ("EN1", "input"), "32": ("RES", "output"),
    "33": ("DEMB", "input"), "34": ("MODE", "input"),
    "35": ("AGND", "power_in"), "36": ("VDDA", "power_out"),
    "37": ("RT", "input"), "38": ("DITH", "input"),
    "39": ("SYNCOUT", "output"), "40": ("EN2", "input"),
    "EP": ("EXPOSED_PAD", "passive"),
}

REQUIRED_REFS = {
    "U_DCDC", "Q_HS1", "Q_LS1", "Q_HS2", "Q_LS2", "L1", "L2",
    "RSH1", "RSH2", "R_GH1_ON", "R_GH1_OFF", "R_GL1_ON",
    "R_GL1_OFF", "R_GH2_ON", "R_GH2_OFF", "R_GL2_ON", "R_GL2_OFF",
    "D_BOOT1", "C_BOOT1", "D_BOOT2", "C_BOOT2", "R_CS1", "C_CS1",
    "R_CS2", "C_CS2", "R_RT", "C_SS", "C_RES", "R_COMP", "C_COMP",
    "C_HF", "U_UVLO", "U_EN_GATE", "U_FAULT", "U_ISENSE1",
    "U_ISENSE2", "U_ISUM", "NT_AGND_PGND", "R_PG1_PULLUP",
}

REQUIRED_HLABELS = {
    "PACK_BUS_P5_IN", "POWER_GND", "5V_SYS_EN", "P5_GROUP_SAFE_OFF",
    "P5_GROUP_HARD_OFF", "5V_SYS_BUS", "5V_SYS_VSENSE",
    "5V_SYS_TOTAL_ISENSE", "P5_DC_DC_FAULT_N", "P5_PHASE1_ISENSE",
    "P5_PHASE2_ISENSE",
}

FORBIDDEN = {"K_MAIN", "MAIN_INPUT_BUS", "5V_CRIT", "3V3_CRIT", "EMG_4S2P"}


def balanced(text: str) -> bool:
    depth = 0
    quoted = False
    escaped = False
    for char in text:
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        else:
            if char == '"':
                quoted = True
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth < 0:
                    return False
    return depth == 0 and not quoted


def extract_block(text: str, marker: str) -> str:
    start = text.find(marker)
    if start < 0:
        raise ValueError(f"missing block marker: {marker}")
    depth = 0
    quoted = False
    escaped = False
    began = False
    for index in range(start, len(text)):
        char = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        else:
            if char == '"':
                quoted = True
            elif char == "(":
                depth += 1
                began = True
            elif char == ")":
                depth -= 1
                if began and depth == 0:
                    return text[start:index + 1]
    raise ValueError(f"unterminated block: {marker}")


def controller_pins(symbol_text: str) -> dict[str, tuple[str, str]]:
    block = extract_block(symbol_text, '(symbol "LM5143A_Q1_RHA40"')
    result: dict[str, tuple[str, str]] = {}
    pattern = re.compile(
        r'\(pin\s+(\w+)\s+\w+.*?'
        r'\(name\s+"([^"]+)".*?\)\s*'
        r'\(number\s+"([^"]+)"',
        re.DOTALL,
    )
    for electrical_type, name, number in pattern.findall(block):
        if number in result:
            raise ValueError(f"duplicate controller pin number {number}")
        result[number] = (name, electrical_type)
    return result


def instance_refs(schematic: str) -> set[str]:
    # Instance symbols uniquely include a lib_id before their Reference property.
    return set(re.findall(
        r'\(symbol\s+\(lib_id\s+"[^"]+"\).*?'
        r'\(property\s+"Reference"\s+"([^"]+)"',
        schematic,
        re.DOTALL,
    ))


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main(schematic_path: str, symbol_path: str) -> int:
    schematic = Path(schematic_path).read_text(encoding="utf-8")
    symbols = Path(symbol_path).read_text(encoding="utf-8")
    errors: list[str] = []

    for name, text in (("schematic", schematic), ("symbol library", symbols)):
        if not balanced(text):
            fail(f"{name} S-expression is unbalanced", errors)
        if '(generator "eeschema")' in text:
            fail(f"{name} falsely identifies third-party generator as eeschema", errors)
        if '(generator "plataVM_symbol_gate")' not in text:
            fail(f"{name} generator identity mismatch", errors)
        if "\\t" in text or "\\n" in text:
            fail(f"{name} contains literal escaped whitespace tokens", errors)

    if '(version 20260101)' not in schematic:
        fail("schematic format must match the KiCad 10.0 supported 20260101 format", errors)
    if schematic.count('(embedded_fonts no)') != 15:
        fail("schematic embedded-font metadata count mismatch", errors)
    if symbols.count('(embedded_fonts no)') != 14:
        fail("symbol-library embedded-font metadata count mismatch", errors)
    if schematic.count('(in_pos_files yes)') < 50:
        fail("schematic instances/lib symbols are missing in_pos_files metadata", errors)
    if schematic.count('(duplicate_pin_numbers_are_jumpers no)') != 14:
        fail("embedded library symbol jumper metadata count mismatch", errors)
    if schematic.count('(body_style 1)') != 50:
        fail("schematic symbol body-style metadata count mismatch", errors)
    if schematic.count('(show_name no)') < 250 or schematic.count('(do_not_autoplace no)') < 250:
        fail("schematic property metadata is incomplete", errors)

    uuids = re.findall(r'\(uuid\s+"([^"]+)"\)', schematic)
    if len(uuids) != len(set(uuids)):
        fail("schematic contains duplicate UUIDs", errors)

    try:
        actual_pins = controller_pins(symbols)
        if actual_pins != EXPECTED_PINS:
            missing = sorted(set(EXPECTED_PINS) - set(actual_pins))
            extra = sorted(set(actual_pins) - set(EXPECTED_PINS))
            mismatched = {
                key: (EXPECTED_PINS[key], actual_pins.get(key))
                for key in EXPECTED_PINS
                if key in actual_pins and EXPECTED_PINS[key] != actual_pins[key]
            }
            fail(
                f"controller pin contract mismatch; missing={missing}, extra={extra}, "
                f"mismatched={mismatched}",
                errors,
            )
    except ValueError as exc:
        fail(str(exc), errors)
        actual_pins = {}

    refs = instance_refs(schematic)
    missing_refs = sorted(REQUIRED_REFS - refs)
    if missing_refs:
        fail(f"required converter-core instances missing: {missing_refs}", errors)

    gate_refs = {ref for ref in refs if re.fullmatch(r"R_G[HL][12]_(ON|OFF)", ref)}
    if len(gate_refs) != 8:
        fail(f"expected eight split gate-resistor positions, got {sorted(gate_refs)}", errors)

    hlabels = set(re.findall(r'\(hierarchical_label\s+"([^"]+)"', schematic))
    if hlabels != REQUIRED_HLABELS:
        fail(
            f"hierarchical interface mismatch; missing={sorted(REQUIRED_HLABELS-hlabels)}, "
            f"extra={sorted(hlabels-REQUIRED_HLABELS)}",
            errors,
        )

    required_tokens = {
        "UVLO_OK", "EN_RUN", "P5_GROUP_SAFE_OFF", "P5_GROUP_HARD_OFF",
        "AGND_PGND_STAR_LAYOUT_TBD", "P5_PGOOD_OD", "P5_DC_DC_FAULT_N",
        "P5_PHASE1_ISENSE", "P5_PHASE2_ISENSE", "5V_SYS_TOTAL_ISENSE",
        "PHASE1_L_OUT", "PHASE2_L_OUT", "CS1_FILTERED", "CS2_FILTERED",
    }
    for token in sorted(required_tokens):
        if token not in schematic:
            fail(f"required safety/diagnostic net missing: {token}", errors)

    for forbidden in sorted(FORBIDDEN):
        if forbidden in schematic or forbidden in symbols:
            fail(f"forbidden architecture token appears in KiCad artifacts: {forbidden}", errors)

    nonempty_footprints = re.findall(r'\(property\s+"Footprint"\s+"([^"]+)"', schematic)
    if nonempty_footprints:
        fail(f"premature footprint assignment detected: {nonempty_footprints[:5]}", errors)

    if schematic.count("CALC_TBD") < 30:
        fail("unresolved symbol-core values are not explicitly visible", errors)

    if schematic.count('(lib_id "plataVM:LM5143A_Q1_RHA40")') != 1:
        fail("exact controller symbol must be instantiated exactly once", errors)
    if schematic.count('(lib_id "plataVM:NMOS_POWER")') != 4:
        fail("four power MOSFET symbols are required", errors)

    print("PCB-D KiCad exact-symbol Gate V1.9")
    print(f"schematic: {schematic_path}")
    print(f"symbol library: {symbol_path}")
    print(f"controller pins: {len(actual_pins)} including exposed pad")
    print(f"schematic instances: {len(refs)}")
    print(f"split gate resistors: {len(gate_refs)}")
    print(f"hierarchical interfaces: {len(hlabels)}")
    print(f"CALC_TBD markers: {schematic.count('CALC_TBD')}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"RESULT: FAIL ({len(errors)} error(s))")
        return 1
    print("RESULT: PASS")
    print("NOTE: native KiCad ERC remains a separate mandatory check.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            f"usage: {Path(sys.argv[0]).name} SCHEMATIC.kicad_sch SYMBOLS.kicad_sym",
            file=sys.stderr,
        )
        raise SystemExit(2)
    try:
        raise SystemExit(main(sys.argv[1], sys.argv[2]))
    except (OSError, ValueError) as exc:
        print(f"PCB-D KiCad exact-symbol Gate V1.9: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
