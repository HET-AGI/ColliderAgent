#!/usr/bin/env python3
"""Check the agent-runtime host: Magnus CLI and site, the Python analysis stack, optional tools.

Usage: check_env.py [--json] [--quiet]
Exit 0 when every required item is present, 1 otherwise. The table doubles as the "agent runtime"
rows of the paper's software-environment table.
"""
from __future__ import annotations

import importlib
import json
import shutil
import subprocess
import sys

REQUIRED_MODULES = ["numpy", "scipy", "matplotlib", "uproot", "awkward", "pyhf", "pylhe", "pyhepmc"]
OPTIONAL_TOOLS = {"pdftoppm": "judge.sh reference figures (poppler-utils)", "gs": "PostScript references (ghostscript)",
                  "tectonic": "compile docs/paper/*.tex", "pdflatex": "compile docs/paper/*.tex"}


def magnus_status() -> tuple[bool, str]:
    exe = shutil.which("magnus")
    if not exe:
        return False, "magnus CLI not on PATH (pip install 'magnus-sdk>=0.8')"
    try:
        out = subprocess.run([exe, "config"], capture_output=True, text=True, timeout=30).stdout
    except (OSError, subprocess.SubprocessError) as e:
        return False, f"magnus config failed: {e}"
    current = next((ln.split(":", 1)[1].strip() for ln in out.splitlines() if ln.strip().startswith("Current:")), "?")
    ok = current == "zhustation"
    return ok, f"magnus site = {current}" + ("" if ok else " (expected zhustation: run `magnus login`)")


def main(argv: list[str]) -> int:
    rows: list[dict] = []
    ok_all = True
    ok, msg = magnus_status()
    rows.append({"item": "magnus", "required": True, "ok": ok, "detail": msg})
    ok_all &= ok
    rows.append({"item": "python", "required": True, "ok": True, "detail": sys.version.split()[0]})
    for m in REQUIRED_MODULES:
        try:
            mod = importlib.import_module(m)
            rows.append({"item": m, "required": True, "ok": True, "detail": getattr(mod, "__version__", "?")})
        except Exception as e:  # noqa: BLE001
            rows.append({"item": m, "required": True, "ok": False, "detail": f"missing ({type(e).__name__}); pip install -r requirements.txt"})
            ok_all = False
    for tool, why in OPTIONAL_TOOLS.items():
        rows.append({"item": tool, "required": False, "ok": shutil.which(tool) is not None, "detail": why})
    if "--json" in argv:
        print(json.dumps({"ok": ok_all, "rows": rows}, indent=1))
    elif "--quiet" not in argv:
        for r in rows:
            flag = "OK " if r["ok"] else ("MISSING" if r["required"] else "absent ")
            print(f"{flag:8s} {r['item']:12s} {r['detail']}")
        print("environment:", "ready" if ok_all else "incomplete")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
