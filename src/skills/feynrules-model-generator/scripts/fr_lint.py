#!/usr/bin/env python3
"""Static checks on a FeynRules .fr file before it is sent to validate-feynrules.

Each check encodes a failure that cost a full cloud round-trip in earlier runs:
  E1  the literal token M$GaugeGroups anywhere in a BSM-extension file (comments included) makes the
      blueprints load it as a standalone model (substring test) -> validation aborts or 0 vertices
  E2  FSD[ ... ] used for a dual field strength -> unevaluated Mathematica leaks into the UFO
  E3  a class name shorter than two characters
  E4  unbalanced brackets / braces
  W1  the Lagrangian text mentions "h.c." but no HC[ ] appears (or HC[ ] appears with no h.c. mention)
  W2  Width -> 0 on a particle (MadGraph then ignores set param_card DECAY for it)
  W3  a Lagrangian symbol assigned with = instead of := (fine in FeynRules, but breaks the
      blueprint's symbol detection when it is the top-level Lagrangian)

Usage: fr_lint.py <model.fr> [--standalone]      (--standalone skips E1)
Exit 0 = no errors (warnings allowed), 1 = errors, 2 = usage.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def lint(text: str, standalone: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    lines = text.splitlines()

    if not standalone:
        for i, ln in enumerate(lines, 1):
            if "M$GaugeGroups" in ln:
                errors.append(f"E1 line {i}: literal 'M$GaugeGroups' (even in a comment) switches the blueprints to "
                              "standalone mode; reword it (e.g. 'the SM gauge group declarations')")
    for i, ln in enumerate(lines, 1):
        if re.search(r"\bFSD\[", ln):
            errors.append(f"E2 line {i}: FSD[ is not a FeynRules built-in; write the dual as (1/2)*Eps[mu,nu,rho,si]*FS[V,rho,si]")
    for m in re.finditer(r"ClassName\s*->\s*(\w+)", text):
        if len(m.group(1)) < 2:
            errors.append(f"E3: ClassName {m.group(1)!r} is a single character; use at least two")
    for open_c, close_c in (("[", "]"), ("{", "}"), ("(", ")")):
        code = re.sub(r"\(\*.*?\*\)", "", text, flags=re.S)
        if code.count(open_c) != code.count(close_c):
            errors.append(f"E4: unbalanced {open_c}{close_c}: {code.count(open_c)} vs {code.count(close_c)}")

    mentions_hc = re.search(r"h\.\s*c\.", text, re.I) is not None
    uses_hc = "HC[" in text
    if mentions_hc and not uses_hc:
        warnings.append("W1: the file mentions 'h.c.' but never uses HC[ ]; if the Lagrangian has + h.c., use the Ltmp + HC[Ltmp] pattern")
    if uses_hc and not mentions_hc:
        warnings.append("W1: HC[ ] is used but nothing says the Lagrangian has '+ h.c.'; make sure Hermitian terms are not doubled")
    for m in re.finditer(r"Width\s*->\s*0\b", text):
        warnings.append("W2: Width -> 0 marks the particle stable for MadGraph; use an external width parameter or Internal")
    for m in re.finditer(r"^\s*(L[A-Za-z0-9]*)\s*=\s*(?!=)", text, re.M):
        warnings.append(f"W3: '{m.group(1)} =' uses immediate assignment; := is the usual form for Lagrangians")
    return errors, warnings


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1 or not Path(args[0]).is_file():
        print(__doc__)
        return 2
    errors, warnings = lint(Path(args[0]).read_text(encoding="utf-8", errors="replace"), "--standalone" in argv)
    for w in warnings:
        print("WARN", w)
    for e in errors:
        print("ERROR", e)
    print(f"fr_lint: {args[0]} -> {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
