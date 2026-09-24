#!/usr/bin/env python3
"""Metrics for a Codex sandbox (run_benchmark_codex.sh), in the same shape as collect_metrics.py.

Sources: events.jsonl (codex exec --json): turn.completed usage, command_execution and file_change items;
the rollout log ~/.codex/sessions/**/rollout-*-<thread_id>.jsonl: last token_count (authoritative totals,
sub-agent threads included) and sub_agent_activity events (sub-agent spawns). Cost is null for a ChatGPT
plan login. Writes metrics.json and a verdict.yaml template; prints the Table S3 row.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys
from pathlib import Path

MAGNUS_RE = re.compile(r"magnus (?:run|launch|blueprint run)\b")
VERDICT_TEMPLATE = 'success: null\nfailure_mode: null\nnotes: ""\nfootnote: ""\njudged_by: ""\n'


def read_env(p: Path) -> dict:
    env = {}
    if p.is_file():
        for ln in p.read_text().splitlines():
            if "=" in ln:
                k, v = ln.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def scan_events(p: Path) -> dict:
    usage = {"input_tokens": 0, "cached_input_tokens": 0, "output_tokens": 0, "reasoning_output_tokens": 0}
    magnus = 0; cmds = 0; files: set[str] = set(); messages = 0; turns = 0; thread = None; errors = 0; spawns = 0; spawn_attempts = 0
    if p.is_file():
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                d = json.loads(line)
            except ValueError:
                continue
            t = d.get("type")
            if t == "thread.started":
                thread = d.get("thread_id")
            elif t == "turn.completed":
                turns += 1
                for k in usage:
                    v = (d.get("usage") or {}).get(k)
                    if isinstance(v, (int, float)):
                        usage[k] += int(v)
            elif t == "item.completed":
                it = d.get("item") or {}
                kind = it.get("type")
                if kind == "command_execution":
                    cmds += 1
                    magnus += len(MAGNUS_RE.findall(it.get("command") or ""))
                elif kind == "file_change":
                    for ch in it.get("changes") or []:
                        if isinstance(ch, dict) and ch.get("path"):
                            files.add(ch["path"])
                elif kind == "agent_message":
                    messages += 1
                elif kind == "collab_tool_call" and "spawn" in str(it.get("tool", "")).lower():
                    spawn_attempts += 1
                    if it.get("agents_states"):      # a spawn that produced a sub-agent thread
                        spawns += 1
                elif kind == "error":
                    errors += 1
    return {"usage": usage, "magnus_jobs": magnus, "commands": cmds, "files": sorted(files),
            "messages": messages, "turns": turns, "thread_id": thread, "errors": errors, "spawns": spawns, "spawn_attempts": spawn_attempts}


def scan_rollout(thread_id: str | None) -> dict:
    out = {"path": None, "subagent_calls": None, "total_usage": None, "entries": 0}
    if not thread_id:
        return out
    home = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    hits = glob.glob(str(home / "sessions" / "**" / f"*{thread_id}*.jsonl"), recursive=True)
    if not hits:
        return out
    out["path"] = hits[0]
    sub = 0; last_tc = None; n = 0
    for line in open(hits[0], encoding="utf-8", errors="replace"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        n += 1
        p = d.get("payload") or {}
        if p.get("type") == "sub_agent_activity" or d.get("type") == "inter_agent_communication_metadata":
            sub += 1
        if p.get("type") == "token_count" and isinstance(p.get("info"), dict):
            last_tc = p["info"].get("total_token_usage") or last_tc
    out.update({"subagent_calls": sub, "total_usage": last_tc, "entries": n})
    return out


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__); return 2
    sb = Path(argv[0]).resolve()
    env = read_env(sb / "run.env")
    status = json.loads((sb / "status.json").read_text()) if (sb / "status.json").is_file() else {}
    ev = scan_events(sb / "events.jsonl")
    ro = scan_rollout(ev["thread_id"])
    u = ro["total_usage"] or ev["usage"]
    tokens_in = int(u.get("input_tokens", 0))        # Codex reports cached tokens inside input_tokens
    tokens_out = int(u.get("output_tokens", 0))
    wall = status.get("wall_clock_s")
    m = {
        "label": env.get("LABEL") or sb.name, "sandbox": str(sb), "harness": "codex",
        "model": env.get("MODEL"), "effort": env.get("EFFORT") or None, "memory": "cold",
        "arxiv": env.get("ARXIV"), "figure": env.get("FIGURE"), "git_commit": env.get("GIT_COMMIT"),
        "codex_version": env.get("CODEX_VERSION"), "thread_id": ev["thread_id"],
        "exit_code": status.get("exit_code"), "wall_clock_s": wall, "num_turns": ev["turns"],
        "cost_usd": None,
        "tokens_in": tokens_in, "tokens_out": tokens_out, "tokens_in_total": tokens_in, "tokens_out_total": tokens_out,
        "tokens": u, "tokens_scope": "rollout total" if ro["total_usage"] else "events turn.completed",
        "subagent_calls": max(ev["spawns"], ro["subagent_calls"] or 0),
        "magnus_jobs": ev["magnus_jobs"], "files_written": len(ev["files"]), "files_written_paths": ev["files"],
        "tool_calls": {"command_execution": ev["commands"], "file_change": len(ev["files"]), "agent_message": ev["messages"]},
        "errors": ev["errors"], "subagent_spawn_attempts": ev["spawn_attempts"], "transcript": {"found": ro["path"] is not None, "source": ro["path"], "entries": ro["entries"]},
    }
    f = lambda v, s: "?" if v is None else s.format(v)
    m["table_s3_row"] = (f"| {m['label']} | {f(wall and wall/3600, '{:.2f}')} | {m['subagent_calls']} | {m['magnus_jobs']} | "
                         f"{m['files_written']} | {tokens_in/1e6:.2f} | {tokens_out/1e3:.1f} |")
    (sb / "metrics.json").write_text(json.dumps(m, indent=1))
    if not (sb / "verdict.yaml").exists():
        (sb / "verdict.yaml").write_text(VERDICT_TEMPLATE)
    print(m["table_s3_row"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
