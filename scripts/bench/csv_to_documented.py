#!/usr/bin/env python3
"""Turn the runs.csv written by aggregate.py --csv into documented-run records (the --extra input of
aggregate.py / pack_results.py), for batches whose sandboxes have been deleted.

usage: csv_to_documented.py <runs.csv> <out.json> [--note TEXT] [--skip-source documented]

Rows whose `source` column equals a --skip-source value (default: documented, i.e. rows that already come
from another documented_runs.json) are left out. The model column of runs.csv is the aggregate label
"<model> / <harness>" for non-Claude harnesses; it is split back into model and harness.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

SUCCESS = {"yes": True, "no": False}


def _num(v: str, scale: float = 1.0, integer: bool = False):
    v = (v or "").strip()
    if v in ("", "-", "--"):
        return None
    x = float(v) * scale
    return int(round(x)) if integer else x


def convert(rows: list[dict], note: str, skip_source=("documented",)) -> list[dict]:
    out = []
    for r in rows:
        if r.get("source") in skip_source:
            continue
        arxiv, _, fig = (r.get("benchmark") or "").partition(" Fig. ")
        model = (r.get("model") or "").split(" / ")[0].strip()
        rec = {
            "label": r["label"],
            "arxiv": arxiv.strip(),
            "figure": fig.strip(),
            "model": model,
            "effort": (r.get("effort") or None) or None,
            "harness": r.get("harness") or None,
            "memory": "cold",
            "attempt": _num(r.get("attempt"), integer=True),
            "success": SUCCESS.get((r.get("success") or "").strip().lower()),
            "failure_mode": (r.get("failure_mode") or "").strip() or None,
            "footnote": (r.get("footnote") or "").strip() or None,
            "metrics": {
                "wall_clock_s": _num(r.get("wall_clock_h"), 3600, integer=True),
                "subagent_calls": _num(r.get("subagent_calls"), integer=True),
                "magnus_jobs": _num(r.get("magnus_jobs"), integer=True),
                "files_written": _num(r.get("files_written"), integer=True),
                "tokens_in_total": _num(r.get("tokens_in_M"), 1e6, integer=True),
                "tokens_out_total": _num(r.get("tokens_out_k"), 1e3, integer=True),
                "cost_usd": _num(r.get("cost_usd")),
                "llm_share_of_wall": _num(r.get("llm_share_of_wall")),
            },
            "source_note": note,
        }
        out.append(rec)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("csv", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--note", default="sandbox deleted; numbers from runs.csv of that batch")
    ap.add_argument("--skip-source", action="append", default=None)
    a = ap.parse_args(argv)
    with a.csv.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    recs = convert(rows, a.note, tuple(a.skip_source) if a.skip_source else ("documented",))
    a.out.write_text(json.dumps({"runs": recs}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(recs)} documented runs to {a.out} (from {len(rows)} csv rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
