#!/usr/bin/env python3
"""Check that a benchmark run only used Magnus jobs it submitted itself.

All harnesses share one Magnus account, so `magnus jobs` shows every job ever submitted, including
those of other benchmark runs. An agent that reads the logs or downloads the outputs of a job it did
not submit has not reproduced the paper; such a run is invalid. This script scans every text file a
sandbox produced (events.jsonl, transcript*.jsonl, agent_stderr.log, run.log, ...) for

  - job ids this run submitted: the "Job <id> submitted" / "job_id": "<id>" lines that `magnus run`
    and the python SDK print, and
  - job ids this run referenced: `magnus logs|job status|job logs|job result|job action|download <id>`
    and `magnus.get_job(<id>)`-style calls,

and reports the referenced ids that were never submitted here ("foreign"). It writes provenance.json
into the sandbox and exits 3 when foreign ids were used.

usage: job_provenance.py <sandbox_dir> [--quiet]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ID = r"([0-9a-f]{16})"
SUBMIT_RE = re.compile(r"Job submitted\.?\s*ID:\s*(?:\[green\])?" + ID      # magnus CLI: "Job submitted. ID: <id>"
                       + r"|Job\s+" + ID + r"\s+submitted"                    # python SDK: "Job <id> submitted."
                       + r"|\"job_id\":\s*\"" + ID + r"\"|job_id[=:]\s*'?" + ID
                       + r"|Submitted job\s+" + ID + r"|Job ID:\s*" + ID, re.I)
REF_RE = re.compile(r"magnus\s+(?:job\s+)?(?:logs?|status|result|action|download|fetch|kill|signal)\b[^\n|;&]*?\b" + ID + r"\b",
                    re.I)
SCAN_SUFFIXES = {".jsonl", ".log", ".txt", ".md", ".json", ".yaml", ".sh"}
SKIP_DIRS = {".agents", ".codex", ".claude-config", ".venv", "node_modules", ".adk_scripts"}
SKIP_FILES = {"provenance.json", "metrics.json"}


def extra_files(sandbox: Path) -> list[Path]:
    """Codex keeps the sub-agent threads' transcripts outside the sandbox (~/.codex/sessions); a Codex
    sandbox is scanned together with its main and sub-agent rollouts, found the way collect_metrics_codex does."""
    env = {}
    if (sandbox / "run.env").is_file():
        for line in (sandbox / "run.env").read_text(encoding="utf-8").splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    if env.get("HARNESS") != "codex" or not (sandbox / "events.jsonl").is_file():
        return []
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import collect_metrics_codex as cmc
        ev = cmc.scan_events(sandbox / "events.jsonl")
        ro = cmc.scan_rollouts(ev.get("thread_id"), set(ev.get("child_ids") or []))
        return [Path(t["path"]) for t in ro.get("threads", []) if t.get("path")]
    except Exception:  # noqa: BLE001
        return []


def scan(sandbox: Path) -> dict:
    submitted, referenced = set(), {}
    files = [p for p in sandbox.rglob("*")
             if p.is_file() and p.suffix in SCAN_SUFFIXES and p.name not in SKIP_FILES
             and not any(part in SKIP_DIRS for part in p.relative_to(sandbox).parts)]
    files += extra_files(sandbox)
    for p in files:
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in SUBMIT_RE.finditer(text):
            submitted.add(next(g for g in m.groups() if g))
        for m in REF_RE.finditer(text):
            referenced.setdefault(m.group(1), str(p.relative_to(sandbox)) if sandbox in p.parents else p.name)
    foreign = {jid: src for jid, src in referenced.items() if jid not in submitted}
    return {"submitted": sorted(submitted), "referenced": sorted(referenced),
            "foreign": foreign, "valid": not foreign, "files_scanned": len(files)}


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    quiet = "--quiet" in argv
    argv = [a for a in argv if a != "--quiet"]
    if len(argv) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    sandbox = Path(argv[0]).resolve()
    if not sandbox.is_dir():
        print(f"not a directory: {sandbox}", file=sys.stderr)
        return 1
    result = scan(sandbox)
    (sandbox / "provenance.json").write_text(json.dumps(result, indent=1), encoding="utf-8")
    if not quiet:
        print(f"{sandbox.name}: submitted {len(result['submitted'])}, referenced {len(result['referenced'])}, "
              f"foreign {len(result['foreign'])} -> {'VALID' if result['valid'] else 'INVALID'}")
        for jid, src in result["foreign"].items():
            print(f"  foreign job {jid} (first seen in {src})")
    return 0 if result["valid"] else 3


if __name__ == "__main__":
    sys.exit(main())
