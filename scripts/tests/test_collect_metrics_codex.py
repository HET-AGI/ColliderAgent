import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "bench" / "collect_metrics_codex.py"


def test_codex_metrics_from_events(tmp_path):
    sb = tmp_path / "sb"; sb.mkdir()
    (sb / "run.env").write_text("HARNESS=codex\nMODEL=gpt-5.5\nARXIV=1701.05379\nFIGURE=8\nLABEL=x\n")
    (sb / "status.json").write_text(json.dumps({"start_ts": 0, "end_ts": 7200, "exit_code": 0, "wall_clock_s": 7200}))
    ev = [
        {"type": "thread.started", "thread_id": "no-such-thread"},
        {"type": "item.completed", "item": {"type": "command_execution", "command": "magnus run madgraph-compile -- --process x"}},
        {"type": "item.completed", "item": {"type": "command_execution", "command": "ls && magnus run madgraph-launch -- --process y"}},
        {"type": "item.completed", "item": {"type": "file_change", "changes": [{"path": "/w/a.py", "kind": "add"}, {"path": "/w/b.py", "kind": "update"}]}},
        {"type": "item.completed", "item": {"type": "file_change", "changes": [{"path": "/w/a.py", "kind": "update"}]}},
        {"type": "item.completed", "item": {"type": "agent_message", "text": "done"}},
        {"type": "turn.completed", "usage": {"input_tokens": 1500000, "cached_input_tokens": 900000, "output_tokens": 12000, "reasoning_output_tokens": 3000}},
    ]
    (sb / "events.jsonl").write_text("\n".join(json.dumps(e) for e in ev) + "\n")
    r = subprocess.run([sys.executable, str(SCRIPT), str(sb)], capture_output=True, text=True, env={"CODEX_HOME": str(tmp_path / "nohome"), "PATH": "/usr/bin:/bin"})
    assert r.returncode == 0, r.stderr
    m = json.loads((sb / "metrics.json").read_text())
    assert m["magnus_jobs"] == 2 and m["files_written"] == 2 and m["subagent_calls"] == 0
    assert m["tokens_in_total"] == 1500000 and m["tokens_out_total"] == 12000 and m["cost_usd"] is None
    assert r.stdout.strip() == "| x | 2.00 | 0 | 2 | 2 | 1.50 | 12.0 |"
    assert (sb / "verdict.yaml").read_text().startswith("success: null")
