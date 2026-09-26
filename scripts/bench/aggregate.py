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
import io
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


def model_label(model: str, harness, memory) -> str:
    """Column label: the model, plus the harness when it is not Claude Code (so that the same model run
    through Codex, the ADK python-agent or Gemini CLI is never averaged with its Claude Code runs)."""
    label = model
    if harness and harness not in ("claude", "claude-code"):
        label += f" / {harness}"
    if memory == "warm":
        label += " (warm)"
    return label


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
        harness = env.get("HARNESS") or m.get("harness") or ("claude" if env.get("CLAUDE_VERSION") else None)
        runs.append({
            "label": env.get("LABEL") or m.get("label") or d.name,
            "benchmark": f"{arxiv} Fig. {figure}" if arxiv and figure else d.name,
            "model": model,
            "model_label": model_label(model, harness, memory),
            "success": success,
            "failure_mode": failure_mode,
            "footnote": footnote,
            "metrics": metrics,
            "effort": env.get("EFFORT") or m.get("effort") or None,
            "harness": harness,
            "source": "sandbox",
        })
    return runs


def load_extra(path: Path) -> list[dict]:
    """Runs recorded only in documents (their sandboxes are gone): a JSON file holding either a list
    of run records or {"runs": [...]}. Each record carries arxiv, figure, model, success, failure_mode,
    footnote, and a metrics dict with the collect_metrics.py keys (see docs/paper/results-*/documented_runs.json)."""
    data = read_json(path)
    if isinstance(data, dict):
        data = data.get("runs")
    if not isinstance(data, list):
        raise SystemExit(f"aggregate.py: {path} must hold a list of run records (or {{'runs': [...]}})")
    runs = []
    for rec in data:
        if not isinstance(rec, dict):
            continue
        arxiv, figure = rec.get("arxiv"), rec.get("figure")
        model = rec.get("model") or "?"
        memory = rec.get("memory") or "cold"
        success = rec.get("success")
        footnote = rec.get("footnote")
        failure_mode = rec.get("failure_mode")
        metrics = rec.get("metrics")
        runs.append({
            "label": rec.get("label") or f"documented_{arxiv}_fig{figure}_{model}",
            "benchmark": f"{arxiv} Fig. {figure}" if arxiv and figure else str(rec.get("label")),
            "model": model,
            "model_label": model_label(model, rec.get("harness"), memory),
            "success": success if isinstance(success, bool) else None,
            "failure_mode": failure_mode if isinstance(failure_mode, str) and failure_mode else None,
            "footnote": footnote if isinstance(footnote, str) and footnote.strip() else None,
            "metrics": metrics if isinstance(metrics, dict) else None,
            "effort": rec.get("effort"),
            "harness": rec.get("harness"),
            "source": "documented",
        })
    return runs


CSV_FIELDS = ["attempt", "benchmark", "model", "harness", "effort", "label", "source", "success", "failure_mode",
              "wall_clock_h", "subagent_calls", "magnus_jobs", "files_written", "tokens_in_M", "tokens_out_k",
              "cost_usd", "llm_share_of_wall", "footnote"]


def runs_csv(runs: list[dict]) -> str:
    """One row per run, attempts numbered per (benchmark, model) in label order (documented rows first)."""
    import csv

    def key(r):
        return (r["benchmark"], r["model_label"], 0 if r.get("source") == "documented" else 1, r["label"])

    counter: Counter = Counter()
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=CSV_FIELDS, lineterminator="\n")
    w.writeheader()
    for r in sorted(runs, key=key):
        counter[(r["benchmark"], r["model_label"])] += 1
        m = r.get("metrics") or {}
        wall = m.get("wall_clock_s")
        tin = m.get("tokens_in_total", m.get("tokens_in"))
        tout = m.get("tokens_out_total", m.get("tokens_out"))
        w.writerow({
            "attempt": counter[(r["benchmark"], r["model_label"])],
            "benchmark": r["benchmark"], "model": r["model_label"],
            "harness": r.get("harness") or "", "effort": r.get("effort") or "",
            "label": r["label"], "source": r.get("source") or "sandbox",
            "success": {True: "yes", False: "no"}.get(r["success"], "TBD"),
            "failure_mode": r["failure_mode"] or "",
            "wall_clock_h": "" if wall is None else f"{wall / 3600:.2f}",
            "subagent_calls": m.get("subagent_calls", ""), "magnus_jobs": m.get("magnus_jobs", ""),
            "files_written": m.get("files_written", ""),
            "tokens_in_M": "" if tin is None else f"{tin / 1e6:.2f}",
            "tokens_out_k": "" if tout is None else f"{tout / 1e3:.1f}",
            "cost_usd": "" if m.get("cost_usd") is None else f"{m['cost_usd']:.2f}",
            "llm_share_of_wall": "" if m.get("llm_share_of_wall") is None else f"{m['llm_share_of_wall']:.2f}",
            "footnote": r["footnote"] or "",
        })
    return buf.getvalue()


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
    ap.add_argument("--extra", action="append", default=[], metavar="JSON",
                    help="JSON file of documented runs (sandbox gone) to merge; may be repeated")
    ap.add_argument("--csv", metavar="PATH", help="also write one CSV row per run (attempt-numbered) to PATH")
    args = ap.parse_args(argv)
    root = Path(args.runs_dir)
    if not root.is_dir():
        print(f"aggregate.py: not a directory: {root}", file=sys.stderr)
        return 1
    runs = load_runs(root)
    for extra in args.extra:
        runs += load_extra(Path(extra))
    if args.csv:
        Path(args.csv).write_text(runs_csv(runs), encoding="utf-8")
    sys.stdout.write(render(runs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
