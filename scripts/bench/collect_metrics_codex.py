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
    magnus = 0; cmds = 0; files: set[str] = set(); messages = 0; turns = 0; thread = None; errors = 0; spawns = 0; spawn_attempts = 0; child_ids: set[str] = set()
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
                elif kind == "collab_tool_call":
                    for cid in list((it.get("agents_states") or {}).keys()) + list(it.get("receiver_thread_ids") or []):
                        if isinstance(cid, str):
                            child_ids.add(cid)
                    if "spawn" in str(it.get("tool", "")).lower():
                        spawn_attempts += 1
                        if it.get("agents_states"):      # a spawn that produced a sub-agent thread
                            spawns += 1
                elif kind == "error":
                    errors += 1
    return {"usage": usage, "magnus_jobs": magnus, "commands": cmds, "files": sorted(files),
            "messages": messages, "turns": turns, "thread_id": thread, "errors": errors, "spawns": spawns, "spawn_attempts": spawn_attempts, "child_ids": child_ids}


def _rollout_path(thread_id: str) -> str | None:
    home = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    hits = glob.glob(str(home / "sessions" / "**" / f"*{thread_id}*.jsonl"), recursive=True)
    return hits[0] if hits else None


def scan_one_rollout(path: str) -> dict:
    """Per-thread totals from a Codex rollout: last token_count total, exec_command calls, magnus submissions,
    file patches, and the sub-agent threads it spawned."""
    magnus = cmds = patches = 0; last_tc = None; n = 0; children: set[str] = set()
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        n += 1
        p = d.get("payload") or {}
        t = p.get("type")
        if t in ("function_call", "custom_tool_call"):
            args = p.get("arguments") if isinstance(p.get("arguments"), str) else json.dumps(p.get("input") or p.get("arguments") or "")
            if p.get("name") in ("exec_command", "shell", "container.exec") or "cmd" in (args or "")[:40]:
                cmds += 1
                magnus += len(MAGNUS_RE.findall(args or ""))
            if p.get("name") == "apply_patch" or t == "custom_tool_call" and "patch" in str(p.get("name", "")).lower():
                patches += 1
        elif t == "token_count" and isinstance(p.get("info"), dict):
            last_tc = p["info"].get("total_token_usage") or last_tc
        elif t == "patch_apply_end":
            patches += 1
        if d.get("type") == "inter_agent_communication_metadata":
            for k in ("receiver_thread_ids", "child_thread_ids"):
                for c in (p.get(k) or d.get(k) or []):
                    if isinstance(c, str):
                        children.add(c)
    return {"path": path, "entries": n, "magnus_jobs": magnus, "commands": cmds, "patches": patches,
            "total_usage": last_tc, "children": children}


def scan_rollouts(thread_id: str | None, child_ids: set[str]) -> dict:
    """Main thread plus every sub-agent thread (ids from the events stream and from the rollouts themselves)."""
    out = {"path": None, "threads": [], "subagent_calls": 0, "total_usage": None, "entries": 0,
           "magnus_jobs": 0, "commands": 0, "patches": 0}
    if not thread_id:
        return out
    seen: set[str] = set(); queue = [thread_id]; usage_sum = {"input_tokens": 0, "cached_input_tokens": 0, "output_tokens": 0, "reasoning_output_tokens": 0}
    pending_children = set(child_ids)
    while queue or pending_children:
        tid = queue.pop(0) if queue else pending_children.pop()
        if tid in seen:
            continue
        seen.add(tid)
        path = _rollout_path(tid)
        if not path:
            continue
        r = scan_one_rollout(path)
        if tid == thread_id:
            out["path"] = path
        out["threads"].append({"thread_id": tid, "path": path, "magnus_jobs": r["magnus_jobs"], "commands": r["commands"], "usage": r["total_usage"]})
        out["entries"] += r["entries"]; out["magnus_jobs"] += r["magnus_jobs"]; out["commands"] += r["commands"]; out["patches"] += r["patches"]
        for k in usage_sum:
            usage_sum[k] += int((r["total_usage"] or {}).get(k, 0) or 0)
        queue.extend(c for c in r["children"] if c not in seen)
    out["subagent_calls"] = max(0, len(out["threads"]) - 1)
    out["total_usage"] = usage_sum if out["threads"] else None
    return out


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__); return 2
    sb = Path(argv[0]).resolve()
    env = read_env(sb / "run.env")
    status = json.loads((sb / "status.json").read_text()) if (sb / "status.json").is_file() else {}
    ev = scan_events(sb / "events.jsonl")
    ro = scan_rollouts(ev["thread_id"], ev["child_ids"])
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
        "tokens": u, "tokens_scope": "rollouts: main + %d sub-agent threads" % (ro["subagent_calls"] or 0) if ro["total_usage"] else "events turn.completed",
        "subagent_calls": max(ev["spawns"], ro["subagent_calls"] or 0),
        "magnus_jobs": max(ev["magnus_jobs"], ro["magnus_jobs"]), "files_written": max(len(ev["files"]), ro["patches"]),
        "files_written_paths": ev["files"], "threads": ro["threads"],
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
