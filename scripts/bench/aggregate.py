#!/usr/bin/env python3
"""Aggregate benchmark sandboxes (bench_runs/<label>/) into Markdown Tables S3, S4 and S5.

Each sandbox contributes metrics.json (from collect_metrics.py), verdict.yaml (from judge.sh
and/or a human) and run.env (from run_benchmark.sh). A run whose verdict.yaml has
`success: true` is successful, `success: false` failed, anything else is attempted but
unjudged and is shown as `?`. Warm-memory runs are listed as a separate model column
("<model> (warm)") so they are never averaged with cold runs.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def parse_run_env(path: Path) -> dict:
    env: dict = {}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return env
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        env[k.strip()] = v
    return env


def parse_simple_yaml(text: str) -> dict:
    """`key: scalar` lines only (what judge.sh / collect_metrics.py write)."""
    out: dict = {}
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        v = v.strip()
        if v[:1] == '"':
            try:
                v = json.loads(v)
            except ValueError:
                v = v.strip('"')
        elif v[:1] == "'":
            v = v.strip("'")
        elif v in ("null", "~", ""):
            v = None
        elif v in ("true", "True"):
            v = True
        elif v in ("false", "False"):
            v = False
        out[k.strip()] = v
    return out


def load_runs(root: Path) -> list[dict]:
    runs = []
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        env = parse_run_env(d / "run.env")
        metrics = read_json(d / "metrics.json")
        metrics = metrics if isinstance(metrics, dict) else None
        if not env and metrics is None:
            continue
        verdict = {}
        if (d / "verdict.yaml").is_file():
            verdict = parse_simple_yaml((d / "verdict.yaml").read_text(encoding="utf-8"))
        success = verdict.get("success")
        success = success if isinstance(success, bool) else None
        failure_mode = verdict.get("failure_mode")
        failure_mode = failure_mode if isinstance(failure_mode, str) and failure_mode else None
        footnote = verdict.get("footnote")
        footnote = footnote if isinstance(footnote, str) and footnote.strip() else None
        m = metrics or {}
        arxiv = env.get("ARXIV") or m.get("arxiv")
        figure = env.get("FIGURE") or m.get("figure")
        model = env.get("MODEL") or m.get("model") or "?"
        memory = env.get("MEMORY") or m.get("memory") or "cold"
        runs.append({
            "label": env.get("LABEL") or m.get("label") or d.name,
            "benchmark": f"{arxiv} Fig. {figure}" if arxiv and figure else d.name,
            "model": model,
            "model_label": model + (" (warm)" if memory == "warm" else ""),
            "success": success,
            "failure_mode": failure_mode,
            "footnote": footnote,
            "metrics": metrics,
        })
    return runs


def _mean(values):
    vals = [v for v in values if isinstance(v, (int, float)) and not isinstance(v, bool)]
    return sum(vals) / len(vals) if vals else None


def _fmt(v, spec: str) -> str:
    return "?" if v is None else format(v, spec)


def table_s3(runs: list[dict]) -> str:
    groups: dict[tuple[str, str], list[dict]] = {}
    for r in runs:
        if r["success"] is True and r["metrics"]:
            groups.setdefault((r["benchmark"], r["model_label"]), []).append(r["metrics"])
    lines = ["### Table S3: resource usage (successful runs, mean over runs)", "",
             "| Benchmark | Model | Runs | Wall-clock (h) | Subagent calls | Magnus jobs | Files written "
             "| Tokens in (M) | Tokens out (k) | Cost (USD) |",
             "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for (bench, model), ms in sorted(groups.items()):
        wall = _mean(m.get("wall_clock_s") for m in ms)
        # prefer main+subagent totals (collect_metrics.py) over the main-session-only usage
        tin = _mean(m.get("tokens_in_total", m.get("tokens_in")) for m in ms)
        tout = _mean(m.get("tokens_out_total", m.get("tokens_out")) for m in ms)
        lines.append(
            f"| {bench} | {model} | {len(ms)} | {_fmt(None if wall is None else wall / 3600, '.2f')} | "
            f"{_fmt(_mean(m.get('subagent_calls') for m in ms), '.1f')} | "
            f"{_fmt(_mean(m.get('magnus_jobs') for m in ms), '.1f')} | "
            f"{_fmt(_mean(m.get('files_written') for m in ms), '.1f')} | "
            f"{_fmt(None if tin is None else tin / 1e6, '.2f')} | "
            f"{_fmt(None if tout is None else tout / 1e3, '.1f')} | "
            f"{_fmt(_mean(m.get('cost_usd') for m in ms), '.2f')} |")
    if not groups:
        lines.append("| (no successful runs yet) | | | | | | | | | |")
    return "\n".join(lines)


def _cell(rs: list[dict]) -> str:
    if not rs:
        return "-"
    succ = sum(1 for r in rs if r["success"] is True)
    unjudged = sum(1 for r in rs if r["success"] is None)
    cell = f"{succ}/{len(rs)}"
    return cell + (f" ({unjudged} ?)" if unjudged else "")


def table_s4(runs: list[dict]) -> str:
    benchmarks = sorted({r["benchmark"] for r in runs})
    models = sorted({r["model_label"] for r in runs})
    lines = ["### Table S4: successful/attempted per benchmark and model (`?` = attempted, not yet judged)", "",
             "| Benchmark | " + " | ".join(models) + " |",
             "|---|" + "---:|" * len(models)]
    for b in benchmarks:
        cells = [_cell([r for r in runs if r["benchmark"] == b and r["model_label"] == m]) for m in models]
        lines.append(f"| {b} | " + " | ".join(cells) + " |")
    if not benchmarks:
        lines.append("| (no runs) |")
    return "\n".join(lines)


def table_s5(runs: list[dict]) -> str:
    benchmarks = sorted({r["benchmark"] for r in runs})
    lines = ["### Table S5: successful/attempted per benchmark with failure modes", "",
             "| Benchmark | Successful/attempted | Failure modes |", "|---|---:|---|"]
    for b in benchmarks:
        rs = [r for r in runs if r["benchmark"] == b]
        modes = Counter((r["failure_mode"] or "unclassified") for r in rs if r["success"] is False)
        unjudged = sum(1 for r in rs if r["success"] is None)
        if unjudged:
            modes["unjudged ?"] = unjudged
        text = ", ".join(f"{k} ({v})" for k, v in sorted(modes.items())) or "-"
        lines.append(f"| {b} | {_cell(rs)} | {text} |")
    if not benchmarks:
        lines.append("| (no runs) | | |")
    notes = [(r["benchmark"], r["model_label"], r["footnote"]) for r in runs if r.get("footnote")]
    if notes:
        lines += ["", "Footnotes (quantitative deviations of runs counted as successful):", ""]
        for i, (b, ml, fn) in enumerate(notes, 1):
            lines.append(f"{i}. {b}, {ml}: {fn}")
    return "\n".join(lines)


def render(runs: list[dict]) -> str:
    succ = sum(1 for r in runs if r["success"] is True)
    fail = sum(1 for r in runs if r["success"] is False)
    unj = sum(1 for r in runs if r["success"] is None)
    head = f"Runs found: {len(runs)} (successful {succ}, failed {fail}, unjudged {unj})"
    return "\n\n".join([head, table_s3(runs), table_s4(runs), table_s5(runs)]) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs_dir", nargs="?", default="bench_runs", help="directory of sandboxes (default: bench_runs)")
    args = ap.parse_args(argv)
    root = Path(args.runs_dir)
    if not root.is_dir():
        print(f"aggregate.py: not a directory: {root}", file=sys.stderr)
        return 1
    sys.stdout.write(render(load_runs(root)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
