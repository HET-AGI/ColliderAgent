#!/usr/bin/env python3
"""Emit the LaTeX table fragments of the experiment report from a results package.

Inputs (a results package directory such as docs/paper/results-2026-09-26/):
  runs.csv            one row per attempt (aggregate.py --csv), documented and sandbox runs alike
  tables.md           aggregate.py output; only its "Footnotes" list is used
  adk_runs.json       per-run long-horizon indicators of the ADK runs (optional)

Outputs (<out_dir>/*.tex, each a bare tabular/longtable to be \\input):
  s4_matrix.tex        benchmark x column, successful/attempted
  s5_attempts.tex      per-attempt results (ok / m / g / a / i) for every column with more than one attempt
  failure_modes.tex    per column: runs, successes, failure-mode counts
  resources.tex        per column: mean wall-clock, sub-agents, jobs, files, tokens, cost over successful runs
  opus46_attempts.tex  every Opus 4.6 attempt with its resource numbers (Table S3 detail)
  crossmodel.tex       the single 2026-09-16 runs of Opus 4.8 / Opus 5 / Sonnet 5
  all_runs.tex         longtable of every attempt (date, benchmark, column, wall, jobs, tokens, cost, result)
  adk_runs.tex         per-run ADK indicators (from adk_runs.json)
  footnotes.tex        itemised deviations of the successful runs (from tables.md)

usage: report_tables.py <results_dir> <out_dir>
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

BENCH_ORDER = ["1308.2209 Fig. 3", "1605.02910 Fig. 1", "1701.05379 Fig. 8", "2103.02708 Fig. 4", "9909255 Fig. 2",
               "2104.05720 Fig. 11", "2104.05720 Fig. 12", "2005.06475 Fig. 2", "1811.07920 Fig. 3"]
BENCH_NAME = {"1308.2209 Fig. 3": "Heavy N", "1605.02910 Fig. 1": "U(1)$'$ scan", "1701.05379 Fig. 8": "ALP EFT",
              "2103.02708 Fig. 4": "General $Z'$", "9909255 Fig. 2": "KK graviton", "2104.05720 Fig. 11": "U1 LQ at MuC, $\\eta$",
              "2104.05720 Fig. 12": "U1 LQ at MuC, reach", "2005.06475 Fig. 2": "Scalar LQ $m_{ej}$ (Delphes)",
              "1811.07920 Fig. 3": "U1 LQ mono-$\\tau$ (Delphes)"}
COLUMN_ORDER = ["claude-opus-4-6", "claude-opus-5", "claude-opus-4-8", "claude-sonnet-5", "gpt-5.3-codex / codex",
                "gpt-5.5 / codex", "gemini-3.1-pro-preview / adk", "gemini-3.1-pro-preview / gemini", "gpt-5.5 / adk"]
COLUMN_NAME = {"claude-opus-4-6": "Opus 4.6 / Claude Code", "claude-opus-5": "Opus 5 / Claude Code",
               "claude-opus-4-8": "Opus 4.8 / Claude Code", "claude-sonnet-5": "Sonnet 5 / Claude Code",
               "gpt-5.3-codex / codex": "GPT-5.3-Codex / Codex", "gpt-5.5 / codex": "GPT-5.5 / Codex",
               "gemini-3.1-pro-preview / adk": "Gemini 3.1 Pro / ADK", "gemini-3.1-pro-preview / gemini": "Gemini 3.1 Pro / Gemini CLI",
               "gpt-5.5 / adk": "GPT-5.5 / ADK"}
MODE_LETTER = {"model": "m", "generation": "g", "analysis": "a", "infrastructure": "i"}


def tex(s: str) -> str:
    s = str(s).replace("\\", r"\textbackslash{}")
    for a, b in [("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}"),
                 ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}")]:
        s = s.replace(a, b)
    return s


def num(v, spec, dash="--"):
    if v in (None, ""):
        return dash
    try:
        return format(float(v), spec)
    except ValueError:
        return dash


def read_runs(path: Path) -> list[dict]:
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    for r in rows:
        stamp = r["label"].replace("doc-", "")[:8]
        r["date"] = f"{stamp[:4]}-{stamp[4:6]}-{stamp[6:8]}" if stamp.isdigit() else "?"
    # attempts: chronological within (benchmark, column), whatever the CSV says
    groups: dict = defaultdict(list)
    for r in rows:
        groups[(r["benchmark"], r["model"])].append(r)
    for rs in groups.values():
        for i, r in enumerate(sorted(rs, key=lambda r: r["label"].replace("doc-", "")), 1):
            r["attempt"] = str(i)
    return rows


def column_key(r: dict) -> str:
    return r["model"]


def cell(rs: list[dict]) -> str:
    if not rs:
        return "--"
    ok = sum(1 for r in rs if r["success"] == "yes")
    tbd = sum(1 for r in rs if r["success"] == "TBD")
    return f"{ok}/{len(rs)}" + (f" ({tbd} TBD)" if tbd else "")


def result_letter(r: dict) -> str:
    if r["success"] == "yes":
        return "ok" + ("$^{*}$" if r.get("footnote") else "")
    if r["success"] == "TBD":
        return "TBD"
    return MODE_LETTER.get(r["failure_mode"], "?")


COLUMN_TWO_LINE = {"claude-opus-4-6": ("Opus 4.6", "Claude Code"), "claude-opus-5": ("Opus 5", "Claude Code"),
                   "claude-opus-4-8": ("Opus 4.8", "Claude Code"), "claude-sonnet-5": ("Sonnet 5", "Claude Code"),
                   "gpt-5.3-codex / codex": ("GPT-5.3-Codex", "Codex"), "gpt-5.5 / codex": ("GPT-5.5", "Codex"),
                   "gemini-3.1-pro-preview / adk": ("Gemini 3.1 Pro", "ADK"), "gemini-3.1-pro-preview / gemini": ("Gemini 3.1 Pro", "Gemini CLI"),
                   "gpt-5.5 / adk": ("GPT-5.5", "ADK")}


def s4_matrix(rows, exclude=("claude-opus-4-8", "claude-sonnet-5")):
    """Single-run 2026-09-16 columns (Opus 4.8, Sonnet 5) are left to the cross-model table to keep the matrix legible."""
    cols = [c for c in COLUMN_ORDER if c not in exclude and any(column_key(r) == c for r in rows)]
    lines = [r"\begin{tabular}{l" + "c" * len(cols) + "}", r"\toprule",
             "Benchmark & " + " & ".join(COLUMN_TWO_LINE[c][0] for c in cols) + r" \\",
             " & " + " & ".join(COLUMN_TWO_LINE[c][1] for c in cols) + r" \\", r"\midrule"]
    for b in BENCH_ORDER:
        if not any(r["benchmark"] == b for r in rows):
            continue
        if b == "2005.06475 Fig. 2":
            lines.append(r"\midrule")
        lines.append(BENCH_NAME[b] + " & "
                     + " & ".join(cell([r for r in rows if r["benchmark"] == b and column_key(r) == c]) for c in cols) + r" \\")
    light = [b for b in BENCH_ORDER[:7]]
    lines.append(r"\midrule")
    lines.append("figure benchmarks & " + " & ".join(cell([r for r in rows if r["benchmark"] in light and column_key(r) == c]) for c in cols) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def s5_attempts(rows):
    cols = [c for c in COLUMN_ORDER if any(column_key(r) == c for r in rows)]
    multi = [c for c in cols if max(Counter((r["benchmark"], column_key(r)) for r in rows if column_key(r) == c).values()) > 1]
    lines = [r"\begin{tabular}{l" + "c" * len(multi) + "}", r"\toprule",
             "Benchmark & " + " & ".join(COLUMN_NAME[c] + " (a1 / a2 / a3)" for c in multi) + r" \\", r"\midrule"]
    for b in BENCH_ORDER:
        cells = []
        for c in multi:
            rs = sorted([r for r in rows if r["benchmark"] == b and column_key(r) == c], key=lambda r: int(r["attempt"]))
            cells.append(" / ".join(result_letter(r) for r in rs) if rs else "--")
        if all(x == "--" for x in cells):
            continue
        lines.append(BENCH_NAME[b] + " & " + " & ".join(cells) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def failure_modes(rows):
    lines = [r"\begin{tabular}{lrrrrrrr}", r"\toprule",
             r"Column & runs & ok & TBD & model & generation & analysis & infrastructure \\", r"\midrule"]
    for c in COLUMN_ORDER:
        rs = [r for r in rows if column_key(r) == c]
        if not rs:
            continue
        cnt = Counter(r["failure_mode"] for r in rs if r["success"] == "no")
        lines.append(f"{COLUMN_NAME[c]} & {len(rs)} & {sum(r['success'] == 'yes' for r in rs)} & {sum(r['success'] == 'TBD' for r in rs)} & "
                     f"{cnt.get('model', 0)} & {cnt.get('generation', 0)} & {cnt.get('analysis', 0)} & {cnt.get('infrastructure', 0)} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def mean(vals):
    vals = [float(v) for v in vals if v not in (None, "")]
    return sum(vals) / len(vals) if vals else None


def resources(rows):
    lines = [r"\begin{tabular}{lrrrrrrrr}", r"\toprule",
             r"Column & ok runs & wall [h] & sub-agents & Magnus jobs & files & tokens in [M] & tokens out [k] & USD \\", r"\midrule"]
    for c in COLUMN_ORDER:
        rs = [r for r in rows if column_key(r) == c and r["success"] == "yes" and r["benchmark"] in BENCH_ORDER[:7]]
        if not rs:
            continue
        lines.append(f"{COLUMN_NAME[c]} & {len(rs)} & {num(mean(r['wall_clock_h'] for r in rs), '.2f')} & "
                     f"{num(mean(r['subagent_calls'] for r in rs), '.1f')} & {num(mean(r['magnus_jobs'] for r in rs), '.1f')} & "
                     f"{num(mean(r['files_written'] for r in rs), '.1f')} & {num(mean(r['tokens_in_M'] for r in rs), '.1f')} & "
                     f"{num(mean(r['tokens_out_k'] for r in rs), '.0f')} & {num(mean(r['cost_usd'] for r in rs), '.1f')} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def opus46_attempts(rows):
    lines = [r"\begin{tabular}{llrrrrrrrrl}", r"\toprule",
             r"Benchmark & attempt & wall [h] & sub-agents & jobs & files & tok in [M] & tok out [k] & USD & model share & result \\", r"\midrule"]
    for b in BENCH_ORDER:
        rs = sorted([r for r in rows if r["benchmark"] == b and column_key(r) == "claude-opus-4-6"], key=lambda r: int(r["attempt"]))
        for i, r in enumerate(rs):
            lines.append(f"{BENCH_NAME[b] if i == 0 else ''} & {r['attempt']} ({r['date'][5:]}) & {num(r['wall_clock_h'], '.2f')} & "
                         f"{r['subagent_calls'] or '--'} & {r['magnus_jobs'] or '--'} & {r['files_written'] or '--'} & "
                         f"{num(r['tokens_in_M'], '.1f')} & {num(r['tokens_out_k'], '.0f')} & {num(r['cost_usd'], '.1f')} & "
                         f"{num(r['llm_share_of_wall'], '.2f')} & {result_letter(r)} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def crossmodel(rows):
    rs = [r for r in rows if column_key(r) in ("claude-opus-5", "claude-opus-4-8", "claude-sonnet-5") and r["date"] == "2026-09-16"]
    lines = [r"\begin{tabular}{llrrrrrrl}", r"\toprule",
             r"Benchmark & model & wall [h] & sub-agents & jobs & files & tok in [M] & USD & result \\", r"\midrule"]
    for r in sorted(rs, key=lambda r: (BENCH_ORDER.index(r["benchmark"]), r["model"])):
        lines.append(f"{BENCH_NAME[r['benchmark']]} & {COLUMN_NAME[r['model']]} & {num(r['wall_clock_h'], '.2f')} & {r['subagent_calls']} & "
                     f"{r['magnus_jobs']} & {r['files_written']} & {num(r['tokens_in_M'], '.1f')} & {num(r['cost_usd'], '.2f')} & {result_letter(r)} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def all_runs(rows):
    lines = [r"\begin{longtable}{llllrrrrl}", r"\toprule",
             r"date & benchmark & column & att. & wall [h] & jobs & tok in [M] & USD & result \\", r"\midrule", r"\endhead"]
    for r in sorted(rows, key=lambda r: (r["date"], BENCH_ORDER.index(r["benchmark"]), COLUMN_ORDER.index(column_key(r)) if column_key(r) in COLUMN_ORDER else 99, int(r["attempt"]))):
        lines.append(f"{r['date']} & {BENCH_NAME[r['benchmark']]} & {COLUMN_NAME.get(column_key(r), tex(column_key(r)))} & {r['attempt']} & "
                     f"{num(r['wall_clock_h'], '.2f')} & {r['magnus_jobs'] or '--'} & {num(r['tokens_in_M'], '.1f')} & {num(r['cost_usd'], '.1f')} & {result_letter(r)} \\\\")
    lines += [r"\bottomrule", r"\end{longtable}"]
    return "\n".join(lines) + "\n"


def adk_runs(path: Path):
    if not path.is_file():
        return "% no adk_runs.json\n"
    data = json.loads(path.read_text(encoding="utf-8"))["runs"]
    lines = [r"\begin{tabular}{llrrrrrll}", r"\toprule",
             r"Model & benchmark & att. & LLM calls & tool errors & refine cycles & max ctx [k] & exit & stage / result \\", r"\midrule"]
    for r in sorted(data, key=lambda r: (r["model"], BENCH_ORDER.index(r["benchmark"]), r["attempt"])):
        res = r["result"].replace("fail:", "fail (") + (")" if r["result"].startswith("fail") else "")
        lines.append(f"{tex(r['model'])} & {BENCH_NAME[r['benchmark']]} & {r['attempt']} & {r['llm_calls']} & {r['tool_errors']} & "
                     f"{r['refine_cycles']} & {r['ctx_max_k']} & {tex(r['exit'])} & {tex(r['stage'])}; {res} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def md_table(path: Path, align: str | None = None) -> str:
    """A Markdown pipe table (longhorizon_table.py output) as a booktabs tabular."""
    if not path.is_file():
        return f"% missing {path.name}\n"
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in path.read_text(encoding="utf-8").splitlines()
            if ln.startswith("|") and not set(ln.replace("|", "").strip()) <= set(":- ")]
    if not rows:
        return "% empty table\n"
    n = len(rows[0])
    short = {"Runs": "n", "Success": "ok", "Wall (h)": "wall [h]", "LLM calls": "LLM calls", "Tool calls": "tool calls",
             "Tool errors": "tool err.", "Error-refine cycles": "refine cyc.", "Magnus jobs": "jobs",
             "Max context (k tok)": "max ctx [k]", "Tokens in (M)": "tok in [M]", "Exit reasons": "exit"}
    lines = [r"\begin{tabular}{" + (align or "l" + "r" * (n - 2) + "l") + "}", r"\toprule",
             " & ".join(tex(short.get(c, c)) for c in rows[0]) + r" \\", r"\midrule"]
    for row in rows[1:]:
        row = [COLUMN_NAME.get(row[0], row[0])] + row[1:]
        lines.append(" & ".join(tex(c) for c in row) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def footnotes(tables_md: Path):
    if not tables_md.is_file():
        return "% no tables.md\n"
    text = tables_md.read_text(encoding="utf-8")
    m = re.search(r"Footnotes \(quantitative deviations of runs counted as successful\):\s*\n(.*)", text, re.S)
    if not m:
        return "% no footnotes\n"
    items = re.findall(r"^\d+\.\s+(.*?)(?=^\d+\.\s|\Z)", m.group(1), re.S | re.M)
    lines = [r"\begin{enumerate}\setlength{\itemsep}{1pt}"]
    for it in items:
        it = " ".join(it.split())
        head, _, body = it.partition(": ")
        lines.append(r"\item \textbf{" + tex(head) + "}: " + tex(body))
    lines.append(r"\end{enumerate}")
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    res, out = Path(argv[0]), Path(argv[1])
    if not (res / "runs.csv").is_file():
        print(f"missing {res / 'runs.csv'}", file=sys.stderr)
        return 1
    out.mkdir(parents=True, exist_ok=True)
    rows = read_runs(res / "runs.csv")
    frags = {"s4_matrix.tex": s4_matrix(rows), "s5_attempts.tex": s5_attempts(rows), "failure_modes.tex": failure_modes(rows),
             "resources.tex": resources(rows), "opus46_attempts.tex": opus46_attempts(rows), "crossmodel.tex": crossmodel(rows),
             "all_runs.tex": all_runs(rows), "adk_runs.tex": adk_runs(res / "adk_runs.json"), "footnotes.tex": footnotes(res / "tables.md"),
             "longhorizon_light.tex": md_table(res / "longhorizon_light.md"), "longhorizon_heavy.tex": md_table(res / "longhorizon_heavy.md")}
    for name, body in frags.items():
        (out / name).write_text(body, encoding="utf-8")
    print(f"wrote {len(frags)} fragments to {out} from {len(rows)} runs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
