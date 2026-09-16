#!/usr/bin/env python3
"""Collect resource metrics for one benchmark sandbox created by run_benchmark.sh.

Reads result.json (authoritative for cost and turns; its usage covers the main session only, so token totals come from the main + subagent transcripts when available), status.json (timing, exit code)
and run.env, locates the session transcript under the sandbox's private config dir
(<config>/projects/<slug>/<session_id>.jsonl, slug = sandbox path with every
non-alphanumeric character replaced by '-') plus its subagent transcripts
(<slug>/<session_id>/subagents/*.jsonl), copies them next to the sandbox, and writes
metrics.json plus one Markdown row for Table S3. Transcript parsing is tolerant: bad
lines are skipped, and every transcript-derived count is null when no transcript exists.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

MAGNUS_RE = re.compile(r"\bmagnus\s+(?:run|launch|blueprint\s+run)\b")
SUBAGENT_TOOLS = {"Agent", "Task"}
WRITE_TOOLS = {"Write", "Edit", "NotebookEdit"}
TOKEN_KEYS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")
VERDICT_TEMPLATE = 'success: null\nfailure_mode: null\nnotes: ""\njudged_by: ""\n'


def read_json(path: Path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def parse_run_env(path: Path) -> dict:
    """KEY=value lines; surrounding quotes are stripped."""
    env: dict = {}
    try:
        text = Path(path).read_text(encoding="utf-8")
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


def path_slug(path: Path) -> str:
    return re.sub(r"[^A-Za-z0-9]", "-", str(path))


def find_transcript(config_dir: Path, sandbox: Path, session_id) -> Path | None:
    if not session_id or not isinstance(session_id, str):
        return None
    projects = Path(config_dir) / "projects"
    guess = projects / path_slug(Path(sandbox).resolve()) / f"{session_id}.jsonl"
    if guess.is_file():
        return guess
    if not projects.is_dir():
        return None
    hits = sorted(p for p in projects.glob(f"**/{session_id}.jsonl") if p.is_file())
    return hits[0] if hits else None


def subagent_transcripts(main_path: Path) -> list[Path]:
    d = main_path.with_suffix("")
    return sorted(d.glob("subagents/*.jsonl")) if d.is_dir() else []


def iter_entries(path: Path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if isinstance(d, dict):
                yield d


def scan_transcripts(paths: list[Path]) -> dict:
    """Count tool_use blocks over all transcript files; sum assistant usage once per request."""
    counts: dict[str, int] = {}
    files: set[str] = set()
    magnus = subagents = entries = 0
    usage = {k: 0 for k in TOKEN_KEYS}
    seen_requests: set = set()
    for path in paths:
        for n, d in enumerate(iter_entries(path)):
            msg = d.get("message")
            if not isinstance(msg, dict):
                continue
            entries += 1
            if d.get("type") == "assistant" and isinstance(msg.get("usage"), dict):
                req = d.get("requestId") or d.get("uuid") or (str(path), n)
                if req not in seen_requests:
                    seen_requests.add(req)
                    for k in TOKEN_KEYS:
                        v = msg["usage"].get(k)
                        if isinstance(v, (int, float)) and not isinstance(v, bool):
                            usage[k] += int(v)
            content = msg.get("content")
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict) or block.get("type") != "tool_use":
                    continue
                name = block.get("name")
                if not isinstance(name, str):
                    continue
                counts[name] = counts.get(name, 0) + 1
                inp = block.get("input") if isinstance(block.get("input"), dict) else {}
                if name in SUBAGENT_TOOLS:
                    subagents += 1
                elif name == "Bash":
                    cmd = inp.get("command")
                    if isinstance(cmd, str):
                        magnus += len(MAGNUS_RE.findall(cmd))
                elif name in WRITE_TOOLS:
                    fp = inp.get("file_path") or inp.get("notebook_path")
                    if isinstance(fp, str) and fp:
                        files.add(fp)
    return {
        "tool_calls": dict(sorted(counts.items())),
        "subagent_calls": subagents,
        "magnus_jobs": magnus,
        "files_written": len(files),
        "files_written_paths": sorted(files),
        "usage_crosscheck": usage,
        "entries": entries,
    }


def _num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def _fmt(v, spec: str) -> str:
    return "?" if v is None else format(v, spec)


def table_row(m: dict) -> str:
    wall_h = None if m.get("wall_clock_s") is None else m["wall_clock_s"] / 3600.0
    tin_v = m.get("tokens_in_total", m.get("tokens_in"))
    tout_v = m.get("tokens_out_total", m.get("tokens_out"))
    tin = None if tin_v is None else tin_v / 1e6
    tout = None if tout_v is None else tout_v / 1e3
    return (f"| {m['label']} | {_fmt(wall_h, '.2f')} | {_fmt(m.get('subagent_calls'), 'd')} | "
            f"{_fmt(m.get('magnus_jobs'), 'd')} | {_fmt(m.get('files_written'), 'd')} | "
            f"{_fmt(tin, '.2f')} | {_fmt(tout, '.1f')} |")


def compute(sandbox: Path, config_dir: Path | None = None) -> dict:
    sandbox = Path(sandbox).resolve()
    env = parse_run_env(sandbox / "run.env")
    result = read_json(sandbox / "result.json")
    result = result if isinstance(result, dict) else {}
    status = read_json(sandbox / "status.json")
    status = status if isinstance(status, dict) else {}
    cfg = Path(config_dir) if config_dir else Path(env.get("CONFIG_DIR") or ".claude-config")
    if not cfg.is_absolute():
        cfg = sandbox / cfg

    usage = result.get("usage") if isinstance(result.get("usage"), dict) else None
    tokens = {k: int(_num(usage.get(k)) or 0) for k in TOKEN_KEYS} if usage is not None else None
    tokens_in = None if tokens is None else (tokens["input_tokens"] + tokens["cache_creation_input_tokens"]
                                              + tokens["cache_read_input_tokens"])
    tokens_out = None if tokens is None else tokens["output_tokens"]

    start, end = _num(status.get("start_ts")), _num(status.get("end_ts"))
    if start is not None and end is not None:
        wall = end - start
    else:
        wall = _num(status.get("wall_clock_s"))
        if wall is None and _num(result.get("duration_ms")) is not None:
            wall = result["duration_ms"] / 1000.0

    session_id = result.get("session_id")
    local_main = sandbox / "transcript.jsonl"
    sub_dir = sandbox / "transcript_subagents"
    src = find_transcript(cfg, sandbox, session_id)
    if src is not None:
        if src.resolve() != local_main.resolve():
            shutil.copy2(src, local_main)
        subs = subagent_transcripts(src)
        if subs:
            sub_dir.mkdir(exist_ok=True)
            for s in subs:
                shutil.copy2(s, sub_dir / s.name)
    paths = [local_main] if local_main.is_file() else []
    paths += sorted(sub_dir.glob("*.jsonl")) if sub_dir.is_dir() else []
    scan = scan_transcripts(paths) if paths else None

    m = {
        "label": env.get("LABEL") or sandbox.name,
        "sandbox": str(sandbox),
        "session_id": session_id,
        "model": env.get("MODEL"),
        "effort": env.get("EFFORT") or None,
        "memory": env.get("MEMORY") or "cold",
        "arxiv": env.get("ARXIV"),
        "figure": env.get("FIGURE"),
        "git_commit": env.get("GIT_COMMIT"),
        "exit_code": _num(status.get("exit_code")),
        "is_error": result.get("is_error"),
        "wall_clock_s": wall,
        "duration_ms": _num(result.get("duration_ms")),
        "num_turns": _num(result.get("num_turns")),
        "cost_usd": _num(result.get("total_cost_usd")),
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "tokens": tokens,
        "subagent_calls": scan["subagent_calls"] if scan else None,
        "magnus_jobs": scan["magnus_jobs"] if scan else None,
        "files_written": scan["files_written"] if scan else None,
        "files_written_paths": scan["files_written_paths"] if scan else [],
        "tool_calls": scan["tool_calls"] if scan else {},
        "transcript": {
            "found": src is not None or local_main.is_file(),
            "source": str(src) if src else None,
            "path": str(local_main) if local_main.is_file() else None,
            "subagent_files": len(paths) - 1 if paths else 0,
            "entries": scan["entries"] if scan else 0,
            "usage_crosscheck": scan["usage_crosscheck"] if scan else None,
        },
    }
    # result.json's usage covers the main session only; subagent stages (where most tokens are spent)
    # are visible only in their transcripts. When the transcript scan covers subagent files and its
    # per-request sums exceed the main-session numbers, report those totals in the S3 row.
    xc = scan["usage_crosscheck"] if scan else None
    m["tokens_scope"] = "main_session"
    m["tokens_in_total"], m["tokens_out_total"] = tokens_in, tokens_out
    if xc and m["transcript"]["subagent_files"] > 0:
        xin = int(xc.get("input_tokens", 0) + xc.get("cache_creation_input_tokens", 0)
                  + xc.get("cache_read_input_tokens", 0))
        xout = int(xc.get("output_tokens", 0))
        if tokens_in is None or xin >= tokens_in:
            m["tokens_in_total"], m["tokens_out_total"], m["tokens_scope"] = xin, xout, "main+subagents"
    m["table_s3_row"] = table_row(m)
    return m


def ensure_verdict(sandbox: Path) -> None:
    p = Path(sandbox) / "verdict.yaml"
    if not p.exists():
        p.write_text(VERDICT_TEMPLATE, encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sandbox", help="bench_runs/<label> directory")
    ap.add_argument("--config-dir", help="CLAUDE_CONFIG_DIR used for the run (default: run.env CONFIG_DIR "
                                         "or <sandbox>/.claude-config)")
    args = ap.parse_args(argv)
    sandbox = Path(args.sandbox)
    if not sandbox.is_dir():
        print(f"collect_metrics.py: not a directory: {sandbox}", file=sys.stderr)
        return 1
    if not (sandbox / "result.json").is_file():
        print(f"collect_metrics.py: warning: {sandbox / 'result.json'} missing; token/cost fields will be null",
              file=sys.stderr)
    metrics = compute(sandbox, Path(args.config_dir) if args.config_dir else None)
    (sandbox / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    ensure_verdict(sandbox)
    if not metrics["transcript"]["found"]:
        print("collect_metrics.py: warning: transcript not found; tool counts are null", file=sys.stderr)
    print(metrics["table_s3_row"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
