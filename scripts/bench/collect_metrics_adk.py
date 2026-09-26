#!/usr/bin/env python3
"""Collect benchmark metrics from a python-agent (Google ADK) sandbox made by run_benchmark_adk.sh.

Reads run.env, status.json, events.jsonl (one record per ADK runner event, written by agent.py),
agent_stdout.log and the sandbox tree, and writes metrics.json with the same keys as
collect_metrics.py / collect_metrics_codex.py plus the long-horizon indicators that Table S4's
Model C discussion needs: LLM calls, tool calls, tool errors, error-refine cycles, context growth,
the pipeline stage reached and why the run ended.

usage: collect_metrics_adk.py <sandbox_dir>
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

MAGNUS_TOOLS = {"validate_feynrules", "generate_ufo_model", "madgraph_compile", "madgraph_launch",
                "run_from_yaml", "madanalysis_process"}
STAGE_ORDER = ["model_written", "validated", "ufo", "compiled", "events", "analysis", "figure"]
STAGE_OF_TOOL = {"validate_feynrules": "validated", "generate_ufo_model": "ufo", "madgraph_compile": "compiled",
                 "madgraph_launch": "events", "run_from_yaml": "events", "madanalysis_process": "analysis"}


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
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


def exit_reason(sandbox: Path, status: dict, events: list[dict]) -> str:
    log = (sandbox / "agent_stdout.log").read_text(encoding="utf-8", errors="replace") if (sandbox / "agent_stdout.log").is_file() else ""
    err = (sandbox / "agent_stderr.log").read_text(encoding="utf-8", errors="replace") if (sandbox / "agent_stderr.log").is_file() else ""
    if status.get("exit_code") == 124:
        return "wall_clock_limit"
    m = re.search(r"^Error: (.*)$", log, re.M)
    if m:  # agent.run() raised: classify by the exception text (stderr tail as a hint)
        text = m.group(1) + " " + err[-3000:]
        if "LlmCallsLimitExceeded" in text or "max_llm_calls" in text or "Max number of llm calls" in text:
            return "max_llm_calls"
        if re.search(r"context.length|context_length|maximum context|too many tokens|input token count", text, re.I):
            return "context_length"
        if re.search(r"RateLimit|(?<![\d,:.])429(?!\d)|rate limit", text):
            return "rate_limit"
        return "exception: " + m.group(1)[:120]
    if re.search(r"^Response:", log, re.M):
        return "completed"  # the agent ended its turn with a final answer (whether or not the task succeeded)
    if any(e.get("error") for e in events):
        last = [e for e in events if e.get("error")][-1]["error"]
        return "llm_error: " + str(last.get("message") or last.get("code"))[:120]
    return "completed" if status.get("exit_code") == 0 else f"exit_code_{status.get('exit_code')}"


def collect(sandbox: Path) -> dict:
    env = read_env(sandbox / "run.env")
    status = json.loads((sandbox / "status.json").read_text()) if (sandbox / "status.json").is_file() else {}
    events = read_events(sandbox / "events.jsonl")

    usages = [e["usage"] for e in events if isinstance(e.get("usage"), dict) and e["usage"].get("prompt_tokens") is not None]
    llm_calls = len(usages)
    tokens_in = sum(u.get("prompt_tokens") or 0 for u in usages)
    tokens_out = sum((u.get("candidates_tokens") or 0) + (u.get("thoughts_tokens") or 0) for u in usages)
    final_ctx = usages[-1].get("prompt_tokens") if usages else None
    max_ctx = max((u.get("prompt_tokens") or 0) for u in usages) if usages else None

    calls = [c for e in events for c in e.get("function_calls", [])]
    responses = [r for e in events for r in e.get("function_responses", [])]
    tool_counts = Counter(c["name"] for c in calls)
    tool_errors = [r for r in responses if r.get("success") is False]
    error_counts = Counter(r["name"] for r in tool_errors)
    # an error-refine cycle: a failed tool call that is followed later by another call of the same tool
    refine_cycles = 0
    seq = []
    for e in events:
        for r in e.get("function_responses", []):
            seq.append(("resp", r["name"], r.get("success")))
        for c in e.get("function_calls", []):
            seq.append(("call", c["name"], None))
    for i, (kind, name, ok) in enumerate(seq):
        if kind == "resp" and ok is False and any(k == "call" and n == name for k, n, _ in seq[i + 1:]):
            refine_cycles += 1

    magnus_jobs = sum(tool_counts[t] for t in MAGNUS_TOOLS)
    magnus_ok = sum(1 for r in responses if r["name"] in MAGNUS_TOOLS and r.get("success") is True)

    written = set()
    for c in calls:
        if c["name"] in ("write", "edit") and c["args"].get("file_path"):
            written.add(str(c["args"]["file_path"]))
    figures = sorted(str(p.relative_to(sandbox)) for p in sandbox.rglob("*.png")
                     if ".adk_scripts" not in p.parts and "outputs" not in p.parts)
    figures += sorted(str(p.relative_to(sandbox)) for p in sandbox.rglob("*.pdf")
                      if ".adk_scripts" not in p.parts and "Output" in p.parts)  # MA5 report plots

    stage = None
    if any(c["name"] == "write" and str(c["args"].get("file_path", "")).endswith(".fr") for c in calls):
        stage = "model_written"
    for r in responses:
        if r.get("success") is True and r["name"] in STAGE_OF_TOOL:
            s = STAGE_OF_TOOL[r["name"]]
            if stage is None or STAGE_ORDER.index(s) > STAGE_ORDER.index(stage):
                stage = s
    if figures:
        stage = "figure"

    wall = status.get("wall_clock_s")
    first_ts = events[0].get("ts") if events else None
    last_ts = events[-1].get("ts") if events else None
    metrics = {
        "label": env.get("LABEL") or sandbox.name,
        "harness": "adk",
        "model": env.get("MODEL"),
        "effort": env.get("EFFORT") or None,
        "memory": env.get("MEMORY") or "cold",
        "arxiv": env.get("ARXIV"),
        "figure": env.get("FIGURE"),
        "git_commit": env.get("GIT_COMMIT"),
        "adk_version": env.get("ADK_VERSION"),
        "max_turns": int(env["MAX_TURNS"]) if env.get("MAX_TURNS", "").isdigit() else None,
        "sandbox": str(sandbox),
        "exit_code": status.get("exit_code"),
        "wall_clock_s": wall,
        "agent_active_s": round(last_ts - first_ts, 1) if first_ts and last_ts else None,
        "exit_reason": exit_reason(sandbox, status, events),
        "llm_calls": llm_calls,
        "num_turns": llm_calls,
        "subagent_calls": 0,
        "tool_calls": len(calls),
        "tool_calls_by_name": dict(tool_counts),
        "tool_errors": len(tool_errors),
        "tool_errors_by_name": dict(error_counts),
        "error_refine_cycles": refine_cycles,
        "magnus_jobs": magnus_jobs,
        "magnus_jobs_ok": magnus_ok,
        "files_written": len(written),
        "files_written_paths": sorted(written),
        "figures": figures,
        "stage_reached": stage,
        "tokens_in_total": tokens_in,
        "tokens_out_total": tokens_out,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "tokens_scope": "all LLM calls of the single ADK agent (prompt + candidates + thoughts)",
        "final_context_tokens": final_ctx,
        "max_context_tokens": max_ctx,
        "cost_usd": None,
    }
    metrics["table_s3_row"] = (
        f"| {metrics['label']} | {(wall or 0) / 3600:.2f} | 0 | {magnus_jobs} | {len(written)} | "
        f"{tokens_in / 1e6:.2f} | {tokens_out / 1e3:.1f} |"
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
    print(f"llm_calls={metrics['llm_calls']} tool_calls={metrics['tool_calls']} tool_errors={metrics['tool_errors']} "
          f"refine_cycles={metrics['error_refine_cycles']} stage={metrics['stage_reached']} "
          f"final_ctx={metrics['final_context_tokens']} exit={metrics['exit_reason']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
