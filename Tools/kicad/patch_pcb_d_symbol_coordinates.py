from __future__ import annotations

from pathlib import Path

GENERATOR = Path(__file__).with_name("generate_pcb_d_converter_core.py")


def replace_exact(text: str, old: str, new: str, expected: int) -> str:
    count = text.count(old)
    if count != expected:
        raise RuntimeError(
            f"Expected {expected} occurrence(s), found {count}: {old[:96]}"
        )
    return text.replace(old, new)


def main() -> None:
    text = GENERATOR.read_text(encoding="utf-8")
    replacements = (
        (
            "wire(x+5.08,y-1.27,x+7.62,y-1.27,f'{ref}:D'),label(drain,x+7.62,y-1.27,'left'),\n        wire(x+5.08,y+1.27,x+7.62,y+1.27,f'{ref}:S'),label(source,x+7.62,y+1.27,'left'),",
            "wire(x+5.08,y+1.27,x+7.62,y+1.27,f'{ref}:D'),label(drain,x+7.62,y+1.27,'left'),\n        wire(x+5.08,y-1.27,x+7.62,y-1.27,f'{ref}:S'),label(source,x+7.62,y-1.27,'left'),",
            1,
        ),
        (
            "objects.extend([wire(x,y+2.54,x,y+5.08,f'{ref}:1'),label(net,x,y+5.08,'left')])",
            "objects.extend([wire(x,y-2.54,x,y-5.08,f'{ref}:1'),label(net,x,y-5.08,'left')])",
            2,
        ),
        (
            "px,py=x-width/2-2.54,y+offset; ox=px-5.08",
            "px,py=x-width/2-2.54,y-offset; ox=px-5.08",
            1,
        ),
        (
            "px,py=x+width/2+2.54,y+offset; ox=px+5.08",
            "px,py=x+width/2+2.54,y-offset; ox=px+5.08",
            1,
        ),
        (
            "px,py=ux-15.24,uy+p.y; ox=px-5.08",
            "px,py=ux-15.24,uy-p.y; ox=px-5.08",
            1,
        ),
        (
            "px,py=ux+15.24,uy+p.y; ox=px+5.08",
            "px,py=ux+15.24,uy-p.y; ox=px+5.08",
            1,
        ),
        (
            "px,py=ux,uy+27.94; oy=py+5.08",
            "px,py=ux,uy-27.94; oy=py-5.08",
            1,
        ),
    )

    for old, new, expected in replacements:
        text = replace_exact(text, old, new, expected)

    GENERATOR.write_text(text, encoding="utf-8")
    print("PCB-D symbol coordinate transform patch: APPLIED")


if __name__ == "__main__":
    main()
