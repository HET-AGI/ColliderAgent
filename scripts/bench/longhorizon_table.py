#!/usr/bin/env python3
"""Long-horizon indicators per model/harness from benchmark sandboxes (metrics.json + verdict.yaml).

For every (model / harness) column it prints the number of runs, successes, and the means over runs of:
wall-clock, LLM calls, tool errors, error-refine cycles and the largest prompt (context) the run reached
(all four only for the ADK harness, whose event log records every model call and every tool's success flag),
tool calls, Magnus jobs, input tokens, and how the run ended (ADK exit_reason).

usage: longhorizon_table.py <runs_dir> [--benchmarks 1308.2209,1701.05379,...]
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import aggregate  # noqa: E402


def _mean(vals):
    vals = [v for v in vals if isinstance(v, (int, float)) and not isinstance(v, bool)]
    return sum(vals) / len(vals) if vals else None


def _f(v, spec):
    return "-" if v is None else format(v, spec)


def rows(runs_dir: Path, benchmarks: set[str] | None = None) -> list[dict]:
    runs = [r for r in aggregate.load_runs(runs_dir) if r["metrics"]]
    if benchmarks:
        runs = [r for r in runs if r["benchmark"].split(" ")[0] in benchmarks]
    groups: dict[str, list[dict]] = defaultdict(list)
    for r in runs:
        groups[r["model_label"]].append(r)
    out = []
    for label, rs in sorted(groups.items()):
        ms = [r["metrics"] for r in rs]
        adk = [r["metrics"] for r in rs if r.get("harness") == "adk"]
        exits = Counter(m.get("exit_reason") for m in ms if m.get("exit_reason"))
        out.append({
            "column": label,
            "runs": len(rs),
            "success": sum(1 for r in rs if r["success"] is True),
            "wall_h": _mean((m.get("wall_clock_s") or 0) / 3600 for m in ms),
            "llm_calls": _mean(m.get("llm_calls") for m in adk),
            "tool_calls": _mean(m.get("tool_calls") for m in ms),
            "tool_errors": _mean(m.get("tool_errors") for m in adk),
            "refine_cycles": _mean(m.get("error_refine_cycles") for m in adk),
            "magnus_jobs": _mean(m.get("magnus_jobs") for m in ms),
            "max_context_k": _mean((m.get("max_context_tokens") or 0) / 1e3 for m in ms if m.get("max_context_tokens")),
            "tokens_in_M": _mean((m.get("tokens_in_total") or m.get("tokens_in") or 0) / 1e6 for m in ms),
            "exit_reasons": dict(exits),
        })
    return out


def render(table: list[dict]) -> str:
    lines = ["| Column | Runs | Success | Wall (h) | LLM calls | Tool calls | Tool errors | Error-refine cycles | Magnus jobs | Max context (k tok) | Tokens in (M) | Exit reasons |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    for t in table:
        ex = ", ".join(f"{k} ({v})" for k, v in sorted(t["exit_reasons"].items())) or "-"
        lines.append(f"| {t['column']} | {t['runs']} | {t['success']} | {_f(t['wall_h'], '.2f')} | {_f(t['llm_calls'], '.0f')} | "
                     f"{_f(t['tool_calls'], '.0f')} | {_f(t['tool_errors'], '.0f')} | {_f(t['refine_cycles'], '.0f')} | "
                     f"{_f(t['magnus_jobs'], '.0f')} | {_f(t['max_context_k'], '.0f')} | {_f(t['tokens_in_M'], '.1f')} | {ex} |")
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs_dir")
    ap.add_argument("--benchmarks", help="comma-separated arXiv ids to keep (default: all)")
    a = ap.parse_args(argv)
    runs_dir = Path(a.runs_dir)
    if not runs_dir.is_dir():
        print(f"longhorizon_table.py: not a directory: {runs_dir}", file=sys.stderr)
        return 1
    bm = set(a.benchmarks.split(",")) if a.benchmarks else None
    sys.stdout.write(render(rows(runs_dir, bm)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
