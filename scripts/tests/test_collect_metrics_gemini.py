"""Tests for scripts/bench/collect_metrics_gemini.py on a synthetic Gemini CLI sandbox."""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "bench" / "collect_metrics_gemini.py"
sys.path.insert(0, str(SCRIPT.parent))
import collect_metrics_gemini as cm  # noqa: E402


def build(tmp_path, exit_code=0, with_result=True):
    sb = tmp_path / "20260926T000000Z_1308.2209_fig3_gemini-gemini-3.1-pro-preview"
    sb.mkdir(parents=True)
    (sb / "run.env").write_text("HARNESS=gemini\nMODEL=gemini-3.1-pro-preview\nARXIV=1308.2209\nFIGURE=3\nLABEL=lab\n")
    (sb / "status.json").write_text(json.dumps({"start_ts": 0, "end_ts": 1800, "exit_code": exit_code, "wall_clock_s": 1800}))
    events = [
        {"type": "init", "session_id": "s", "model": "gemini-3.1-pro-preview"},
        {"type": "message", "role": "user", "content": "task"},
        {"type": "tool_use", "tool_name": "activate_skill", "tool_id": "t1", "parameters": {"name": "feynrules-model-generator"}},
        {"type": "tool_result", "tool_id": "t1", "status": "success", "output": ""},
        {"type": "tool_use", "tool_name": "write_file", "tool_id": "t2", "parameters": {"file_path": "/sb/models/HeavyN.fr", "content": "x"}},
        {"type": "tool_result", "tool_id": "t2", "status": "success", "output": ""},
        {"type": "tool_use", "tool_name": "run_shell_command", "tool_id": "t3",
         "parameters": {"command": "magnus run validate-feynrules --model models/HeavyN.fr --lagrangian LN"}},
        {"type": "tool_result", "tool_id": "t3", "status": "error", "output": "symbol not found"},
        {"type": "tool_use", "tool_name": "replace", "tool_id": "t4", "parameters": {"file_path": "/sb/models/HeavyN.fr", "old_string": "a", "new_string": "b"}},
        {"type": "tool_result", "tool_id": "t4", "status": "success", "output": ""},
        {"type": "tool_use", "tool_name": "run_shell_command", "tool_id": "t5",
         "parameters": {"command": "magnus run validate-feynrules --model models/HeavyN.fr --lagrangian LHeavyN && magnus run generate-ufo --model models/HeavyN.fr"}},
        {"type": "tool_result", "tool_id": "t5", "status": "success", "output": "ok"},
        {"type": "tool_use", "tool_name": "invoke_agent", "tool_id": "t6", "parameters": {"agent": "model-generator", "task": "build the model"}},
        {"type": "tool_result", "tool_id": "t6", "status": "success", "output": "done"},
        {"type": "message", "role": "assistant", "content": "The figure is at output/figures/xsec.png", "delta": True},
    ]
    if with_result:
        events.append({"type": "result", "status": "success",
                       "stats": {"total_tokens": 300000, "input_tokens": 290000, "output_tokens": 10000, "cached": 1000,
                                 "duration_ms": 1700000, "tool_calls": 5,
                                 "models": {"gemini-3.1-pro-preview": {"input_tokens": 290000, "output_tokens": 10000}}}})
    (sb / "events.jsonl").write_text("YOLO mode is enabled.\n" + "\n".join(json.dumps(e) for e in events) + "\n")
    return sb


def test_metrics(tmp_path):
    sb = build(tmp_path)
    (sb / "output" / "figures").mkdir(parents=True)
    (sb / "output" / "figures" / "xsec.png").write_bytes(b"png")
    m = cm.collect(sb)
    assert m["tool_calls"] == 6 and m["tool_errors"] == 1
    assert m["subagent_calls"] == 1 and m["subagents_used"] == ["model-generator"]
    assert m["magnus_jobs"] == 3
    assert m["files_written"] == 1 and m["files_written_paths"] == ["/sb/models/HeavyN.fr"]
    assert m["skills_activated"] == ["feynrules-model-generator"]
    assert m["tokens_in_total"] == 290000 and m["tokens_out_total"] == 10000 and m["tokens_cached"] == 1000
    assert m["figures"] == ["output/figures/xsec.png"] and m["num_turns"] == 1
    assert m["exit_reason"] == "completed" and m["cost_usd"] is None
    assert m["table_s3_row"] == "| lab | 0.50 | 1 | 3 | 1 | 0.29 | 10.0 |"


def test_exit_reasons(tmp_path):
    assert cm.collect(build(tmp_path / "a", exit_code=124))["exit_reason"] == "wall_clock_limit"
    assert cm.collect(build(tmp_path / "b", exit_code=53))["exit_reason"] == "turn_limit"
    m = cm.collect(build(tmp_path / "c", exit_code=1, with_result=False))
    assert m["exit_reason"] == "exit_code_1" and m["tokens_in_total"] == 0


def test_cli(tmp_path):
    sb = build(tmp_path)
    r = subprocess.run([sys.executable, str(SCRIPT), str(sb)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert (sb / "metrics.json").is_file() and (sb / "verdict.yaml").read_text().startswith("success: null")
    assert "magnus_jobs=3" in r.stdout
