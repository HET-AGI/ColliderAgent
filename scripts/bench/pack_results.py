#!/usr/bin/env python3
"""Build a results package from benchmark sandboxes: tables.md, runs.csv and one figure per attempt.

usage: pack_results.py <runs_dir> <out_dir> [--extra documented_runs.json ...] [--no-figures]

- tables.md / runs.csv come from aggregate.py (documented runs merged with --extra).
- figures/<arxiv>_fig<N>__<model-label>__a<attempt>[-FAILED|-TBD].<ext> is the judged figure of every
  sandbox run (verdict.yaml: produced_figure); documented runs keep whatever figures the package already has.
- provenance: runs whose provenance.json says valid=false are listed in tables.md and skipped in the tables
  by moving nothing — quarantine them under <runs_dir>/invalid/ before packing (aggregate.py only reads the
  top-level sandboxes).
"""
from __future__ import annotations

import argparse
import csv
import io
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import aggregate  # noqa: E402


def figure_name(row: dict, src: Path) -> str:
    bench = row["benchmark"].replace(" Fig. ", "_fig")
    model = row["model"].replace(" / ", "-").replace(" ", "")
    tag = {"yes": "", "no": "-FAILED", "TBD": "-TBD"}.get(row["success"], "")
    return f"{bench}__{model}__a{row['attempt']}{tag}{src.suffix.lower()}"


def pack(runs_dir: Path, out_dir: Path, extras: list[Path], figures: bool = True) -> dict:
    runs = aggregate.load_runs(runs_dir)
    for e in extras:
        runs += aggregate.load_extra(e)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "tables.md").write_text(aggregate.render(runs), encoding="utf-8")
    csv_text = aggregate.runs_csv(runs)
    (out_dir / "runs.csv").write_text(csv_text, encoding="utf-8")
    copied, missing = [], []
    if figures:
        fig_dir = out_dir / "figures"
        fig_dir.mkdir(exist_ok=True)
        for row in csv.DictReader(io.StringIO(csv_text)):
            if row["source"] != "sandbox":
                continue
            sb = runs_dir / row["label"]
            v = (sb / "verdict.yaml").read_text(encoding="utf-8") if (sb / "verdict.yaml").is_file() else ""
            m = re.search(r'^produced_figure:\s*"?([^"\n]+)"?', v, re.M)
            src = Path(m.group(1)) if m else None
            if not src or not src.is_file() or src.suffix.lower() not in (".png", ".jpg", ".jpeg", ".pdf"):
                missing.append(row["label"])
                continue
            dst = fig_dir / figure_name(row, src)
            shutil.copyfile(src, dst)
            copied.append(dst.name)
    return {"runs": len(runs), "figures": copied, "no_figure": missing}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs_dir")
    ap.add_argument("out_dir")
    ap.add_argument("--extra", action="append", default=[], metavar="JSON")
    ap.add_argument("--no-figures", action="store_true")
    a = ap.parse_args(argv)
    runs_dir = Path(a.runs_dir)
    if not runs_dir.is_dir():
        print(f"pack_results.py: not a directory: {runs_dir}", file=sys.stderr)
        return 1
    r = pack(runs_dir, Path(a.out_dir), [Path(e) for e in a.extra], figures=not a.no_figures)
    print(f"packed {r['runs']} runs -> {a.out_dir}: {len(r['figures'])} figures, {len(r['no_figure'])} runs without a figure")
    for lab in r["no_figure"]:
        print("  no figure:", lab)
    return 0


if __name__ == "__main__":
    sys.exit(main())
