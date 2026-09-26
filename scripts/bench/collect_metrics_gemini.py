#!/usr/bin/env python3
"""Collect benchmark metrics from a Gemini CLI sandbox made by run_benchmark_gemini.sh.

Parses events.jsonl (`gemini --output-format stream-json`): init, message, tool_use, tool_result and
the final result event with aggregated stats. Writes metrics.json with the same keys as the other
collectors (tokens_in_total, tokens_out_total, magnus_jobs, files_written, wall_clock_s, ...) plus
tool_calls, tool_errors, skills activated and the exit reason.

usage: collect_metrics_gemini.py <sandbox_dir>
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

MAGNUS_RE = re.compile(r"\bmagnus\s+(run|launch|blueprint\s+run)\b")
WRITE_TOOLS = {"write_file", "replace", "edit"}


def read_env(path: Path) -> dict:
    env = {}
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def read_events(path: Path) -> list[dict]:
    out = []
    if not path.is_file():
        return out
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


def collect(sandbox: Path) -> dict:
    env = read_env(sandbox / "run.env")
    status = json.loads((sandbox / "status.json").read_text()) if (sandbox / "status.json").is_file() else {}
    events = read_events(sandbox / "events.jsonl")

    result = next((e for e in reversed(events) if e.get("type") == "result"), None)
    stats = (result or {}).get("stats") or {}
    tool_uses = [e for e in events if e.get("type") == "tool_use"]
    tool_results = [e for e in events if e.get("type") == "tool_result"]
    errors = [e for e in events if e.get("type") == "error"]
    tool_counts = Counter(e.get("tool_name") for e in tool_uses)
    failed = [e for e in tool_results if e.get("status") not in (None, "success")]

    magnus_jobs = 0
    written = set()
    skills = []
    for e in tool_uses:
        p = e.get("parameters") or {}
        if e.get("tool_name") == "run_shell_command":
            magnus_jobs += len(MAGNUS_RE.findall(str(p.get("command", ""))))
        if e.get("tool_name") in WRITE_TOOLS and p.get("file_path"):
            written.add(str(p["file_path"]))
        if e.get("tool_name") == "activate_skill":
            skills.append(str(p.get("name") or p.get("skill") or p))
    figures = sorted(str(p.relative_to(sandbox)) for p in sandbox.rglob("*.png") if ".agents" not in p.parts)

    assistant_msgs = sum(1 for e in events if e.get("type") == "message" and e.get("role") == "assistant")
    # custom sub-agents (.gemini/agents, branch gemini-com) are called through the invoke_agent tool
    agent_calls = [e for e in tool_uses if e.get("tool_name") == "invoke_agent"]
    agents_used = [str((e.get("parameters") or {}).get("agent_name") or (e.get("parameters") or {}).get("agent")
                       or (e.get("parameters") or {}).get("name") or "?") for e in agent_calls]
    # sub-agents submit their Magnus jobs outside the main stream: count "Job submitted. ID: <id>" lines in the
    # sandbox files as well (the same signal job_provenance.py uses) and keep the larger count
    submitted_ids = set()
    for pth in sandbox.rglob("*"):
        if pth.is_file() and pth.suffix in (".jsonl", ".log", ".txt", ".md") and ".agents" not in pth.parts and pth.name != "metrics.json":
            try:
                submitted_ids.update(re.findall(r"Job submitted\.?\s*ID:\s*(?:\[green\])?([0-9a-f]{16})", pth.read_text(encoding="utf-8", errors="replace")))
            except OSError:
                pass
    magnus_jobs = max(magnus_jobs, len(submitted_ids))
    if status.get("exit_code") == 124:
        exit_reason = "wall_clock_limit"
    elif status.get("exit_code") == 53:
        exit_reason = "turn_limit"
    elif result is not None:
        exit_reason = "completed" if result.get("status") == "success" else f"result_{result.get('status')}"
    elif errors:
        exit_reason = "error: " + str(errors[-1].get("message") or errors[-1])[:120]
    else:
        exit_reason = f"exit_code_{status.get('exit_code')}"

    per_model = stats.get("models") or {}
    tokens_in = stats.get("input_tokens") or sum((m.get("input_tokens") or 0) for m in per_model.values())
    tokens_out = stats.get("output_tokens") or sum((m.get("output_tokens") or 0) for m in per_model.values())
    wall = status.get("wall_clock_s")
    metrics = {
        "label": env.get("LABEL") or sandbox.name,
        "harness": "gemini",
        "model": env.get("MODEL"),
        "effort": env.get("EFFORT") or None,
        "memory": env.get("MEMORY") or "cold",
        "arxiv": env.get("ARXIV"),
        "figure": env.get("FIGURE"),
        "git_commit": env.get("GIT_COMMIT"),
        "gemini_version": env.get("GEMINI_VERSION"),
        "sandbox": str(sandbox),
        "exit_code": status.get("exit_code"),
        "wall_clock_s": wall,
        "duration_ms": stats.get("duration_ms"),
        "exit_reason": exit_reason,
        "num_turns": assistant_msgs,
        "subagent_calls": len(agent_calls),
        "subagents_used": agents_used,
        "tool_calls": len(tool_uses),
        "tool_calls_by_name": dict(tool_counts),
        "tool_errors": len(failed),
        "skills_activated": skills,
        "magnus_jobs": magnus_jobs,
        "magnus_jobs_submitted_ids": len(submitted_ids),
        "files_written": len(written),
        "files_written_paths": sorted(written),
        "figures": figures,
        "tokens_in_total": tokens_in,
        "tokens_out_total": tokens_out,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "tokens_cached": stats.get("cached"),
        "tokens_scope": "gemini stream-json result.stats (all model calls of the session)",
        "cost_usd": None,
    }
    metrics["table_s3_row"] = (
        f"| {metrics['label']} | {(wall or 0) / 3600:.2f} | {len(agent_calls)} | {magnus_jobs} | {len(written)} | "
        f"{(tokens_in or 0) / 1e6:.2f} | {(tokens_out or 0) / 1e3:.1f} |"
    )
    return metrics


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    sandbox = Path(argv[0]).resolve()
    if not sandbox.is_dir():
        print(f"not a directory: {sandbox}", file=sys.stderr)
        return 1
    metrics = collect(sandbox)
    (sandbox / "metrics.json").write_text(json.dumps(metrics, indent=1, ensure_ascii=False), encoding="utf-8")
    if not (sandbox / "verdict.yaml").is_file():
        (sandbox / "verdict.yaml").write_text(
            'success: null\nfailure_mode: null\nnotes: ""\njudged_by: ""\n', encoding="utf-8")
    print(metrics["table_s3_row"])
    print(f"tool_calls={metrics['tool_calls']} tool_errors={metrics['tool_errors']} magnus_jobs={magnus_jobs_str(metrics)} "
          f"skills={metrics['skills_activated']} exit={metrics['exit_reason']}")
    return 0


def magnus_jobs_str(m: dict) -> str:
    return str(m["magnus_jobs"])


if __name__ == "__main__":
    sys.exit(main())
