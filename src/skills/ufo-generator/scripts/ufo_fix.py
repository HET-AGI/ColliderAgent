#!/usr/bin/env python3
"""Check and repair a downloaded UFO directory before the MadGraph5 import test.

Known FeynRules 2.3.49 export defects are mechanical, so they are fixed here instead of by hand:
  * Python 2 ``raise UFOError, "msg"`` in object_library.py  -> ``raise UFOError("msg")``
  * leaked, unevaluated Mathematica in couplings.py / vertices.py / lorentz.py
    (``Slot(``, ``CreateObjectParticleName``, ``FSD[``, ``MapAt[``, ``PRIVATE```, ``[[``)  -> reported, not fixable here
  * a ``lorentz.py`` with no Lorentz structures, or ``vertices.py`` with no vertices          -> reported
  * every .py must byte-compile                                                              -> reported

Usage:  ufo_fix.py <UFO_DIR> [--check | --fix]      (default: --fix)
Exit 0 = clean (after fixes), 1 = defects remain that need the .fr file regenerated, 2 = usage error.
Prints one line per finding; the last line is a summary.
"""
from __future__ import annotations

import py_compile
import re
import shutil
import sys
from pathlib import Path

LEAK_PATTERNS = [
    (re.compile(r"Slot\("), "Mathematica Slot( in generated code"),
    (re.compile(r"CreateObjectParticleName|PartNameMG"), "unevaluated CreateObjectParticleName/PartNameMG"),
    (re.compile(r"\bFSD\["), "FSD[ (dual field strength written with a non-built-in)"),
    (re.compile(r"MapAt\[|PRIVATE`|FR\$"), "unevaluated Mathematica (MapAt/PRIVATE`/FR$)"),
    (re.compile(r"\[\[\s*\d+\s*,\s*\d+\s*\]\]"), "Mathematica Part [[i,j]] in Python"),
]
PY2_RAISE = re.compile(r"^(\s*)raise\s+(\w+)\s*,\s*(.+?)\s*$", re.M)


def find_py2_raise(text: str) -> list[str]:
    return [m.group(0).strip() for m in PY2_RAISE.finditer(text)]


def fix_py2_raise(text: str) -> tuple[str, int]:
    return PY2_RAISE.subn(lambda m: f"{m.group(1)}raise {m.group(2)}({m.group(3)})", text)


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    mode = "check" if "--check" in argv else "fix"
    if len(args) != 1 or not Path(args[0]).is_dir():
        print(__doc__)
        return 2
    ufo = Path(args[0])
    findings: list[str] = []
    fixed = 0
    remaining = 0

    for py in sorted(ufo.glob("*.py")):
        text = py.read_text(encoding="utf-8", errors="replace")
        hits = find_py2_raise(text)
        if hits:
            if mode == "fix":
                new, n = fix_py2_raise(text)
                py.write_text(new, encoding="utf-8")
                fixed += n
                findings.append(f"fixed {n} Python-2 raise statement(s) in {py.name}")
                text = new
            else:
                remaining += len(hits)
                findings.append(f"{py.name}: Python-2 raise syntax: {hits[0]}")
        if py.name in ("couplings.py", "vertices.py", "lorentz.py", "parameters.py", "coupling_orders.py"):
            for pat, label in LEAK_PATTERNS:
                m = pat.search(text)
                if m:
                    remaining += 1
                    line = text.count("\n", 0, m.start()) + 1
                    findings.append(f"{py.name}:{line}: {label} -> regenerate from a corrected .fr")
                    break

    for name, needle, what in (("lorentz.py", "Lorentz(", "Lorentz structure"), ("vertices.py", "Vertex(", "vertex")):
        f = ufo / name
        if f.is_file() and needle not in f.read_text(encoding="utf-8", errors="replace"):
            remaining += 1
            findings.append(f"{name}: no {what} written -> the .fr produced no interactions; regenerate")

    pycache = ufo / "__pycache__"
    if pycache.is_dir() and mode == "fix":
        shutil.rmtree(pycache)
    for py in sorted(ufo.glob("*.py")):
        try:
            py_compile.compile(str(py), doraise=True, cfile=str(Path("/tmp") / f"ufo_fix_{py.stem}.pyc"))
        except py_compile.PyCompileError as e:
            remaining += 1
            findings.append(f"{py.name}: does not byte-compile: {str(e).splitlines()[-1][:120]}")

    for line in findings:
        print(line)
    status = "clean" if remaining == 0 else "defects remain"
    print(f"ufo_fix: {ufo} -> {status} (fixed {fixed}, remaining {remaining}, mode {mode})")
    return 0 if remaining == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
