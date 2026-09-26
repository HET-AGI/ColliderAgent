"""Tests for scripts/bench/collect_metrics_adk.py on a synthetic ADK sandbox."""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "bench" / "collect_metrics_adk.py"
sys.path.insert(0, str(SCRIPT.parent))
import collect_metrics_adk as cm  # noqa: E402


def ev(turn, **kw):
    d = {"turn": turn, "ts": 1000.0 + turn, "author": "feynrules_agent", "type": "Event"}
    d.update(kw)
    return d


def build(tmp_path, exit_code=0, stdout="Response: done\nTurns: 9\n"):
    sb = tmp_path / "20260926T000000Z_1308.2209_fig3_adk-gemini-3.1-pro-preview"
    sb.mkdir(parents=True)
    (sb / "run.env").write_text("HARNESS=adk\nMODEL=gemini-3.1-pro-preview\nARXIV=1308.2209\nFIGURE=3\n"
                                "LABEL=lab\nMAX_TURNS=150\nADK_VERSION=2.10.0 litellm 1.0\n")
    (sb / "status.json").write_text(json.dumps({"start_ts": 0, "end_ts": 3600, "exit_code": exit_code, "wall_clock_s": 3600}))
    (sb / "agent_stdout.log").write_text(stdout)
    events = [
        ev(1, usage={"prompt_tokens": 5000, "candidates_tokens": 100, "thoughts_tokens": 50, "total_tokens": 5150},
           function_calls=[{"name": "write", "args": {"file_path": "/sb/models/HeavyN.fr", "content": "..."}}]),
        ev(2, function_responses=[{"name": "write", "success": True, "message": "ok", "size": 40}]),
        ev(3, usage={"prompt_tokens": 6000, "candidates_tokens": 80, "thoughts_tokens": 0, "total_tokens": 6080},
           function_calls=[{"name": "validate_feynrules", "args": {"feynrules_model_path": "/sb/models/HeavyN.fr", "lagrangian_symbol": "LN"}}]),
        ev(4, function_responses=[{"name": "validate_feynrules", "success": False, "message": "symbol not found", "size": 200}]),
        ev(5, usage={"prompt_tokens": 7000, "candidates_tokens": 60, "thoughts_tokens": 10, "total_tokens": 7070},
           function_calls=[{"name": "edit", "args": {"file_path": "/sb/models/HeavyN.fr", "old_string": "a", "new_string": "b"}},
                           {"name": "validate_feynrules", "args": {"feynrules_model_path": "/sb/models/HeavyN.fr", "lagrangian_symbol": "LHeavyN"}}]),
        ev(6, function_responses=[{"name": "edit", "success": True, "message": "", "size": 30},
                                  {"name": "validate_feynrules", "success": True, "message": "", "size": 900}]),
        ev(7, usage={"prompt_tokens": 9000, "candidates_tokens": 40, "thoughts_tokens": 0, "total_tokens": 9040},
           function_calls=[{"name": "madgraph_compile", "args": {"ufo_model_path": "/sb/ufo", "process": "p p > mu+ n1", "target_path": "/sb/proc"}}]),
        ev(8, function_responses=[{"name": "madgraph_compile", "success": True, "message": "", "size": 100}]),
        ev(9, usage={"prompt_tokens": 12000, "candidates_tokens": 200, "thoughts_tokens": 0, "total_tokens": 12200},
           text=["The figure is at /sb/output/figures/xsec.png"]),
    ]
    (sb / "events.jsonl").write_text("\n".join(json.dumps(e) for e in events) + "\n")
    return sb


def test_metrics(tmp_path):
    sb = build(tmp_path)
    m = cm.collect(sb)
    assert m["llm_calls"] == 5 and m["num_turns"] == 5
    assert m["tokens_in_total"] == 5000 + 6000 + 7000 + 9000 + 12000
    assert m["tokens_out_total"] == (100 + 50) + 80 + (60 + 10) + 40 + 200
    assert m["final_context_tokens"] == 12000 and m["max_context_tokens"] == 12000
    assert m["tool_calls"] == 5 and m["tool_calls_by_name"]["validate_feynrules"] == 2
    assert m["tool_errors"] == 1 and m["error_refine_cycles"] == 1
    assert m["magnus_jobs"] == 3 and m["magnus_jobs_ok"] == 2
    assert m["files_written"] == 1 and m["files_written_paths"] == ["/sb/models/HeavyN.fr"]
    assert m["stage_reached"] == "compiled" and m["figures"] == []
    assert m["exit_reason"] == "completed" and m["subagent_calls"] == 0 and m["cost_usd"] is None
    assert m["table_s3_row"] == "| lab | 1.00 | 0 | 3 | 1 | 0.04 | 0.5 |"


def test_stage_figure_and_exit_reasons(tmp_path):
    sb = build(tmp_path, exit_code=0, stdout="Error: LlmCallsLimitExceededError: Max number of llm calls limit of `150` exceeded\n")
    (sb / "output" / "figures").mkdir(parents=True)
    (sb / "output" / "figures" / "xsec.png").write_bytes(b"png")
    (sb / ".adk_scripts").mkdir()
    (sb / ".adk_scripts" / "ignored.png").write_bytes(b"png")
    m = cm.collect(sb)
    assert m["stage_reached"] == "figure" and m["figures"] == ["output/figures/xsec.png"]
    assert m["exit_reason"] == "max_llm_calls"
    sb2 = build(tmp_path / "b", exit_code=124)
    assert cm.collect(sb2)["exit_reason"] == "wall_clock_limit"
    sb3 = build(tmp_path / "c", stdout="Error: BadRequestError: This model's maximum context length is 1048576 tokens\n")
    assert cm.collect(sb3)["exit_reason"] == "context_length"
    # a transient 429 in stderr does not change a run that ended with a final answer
    sb4 = build(tmp_path / "d", stdout="Response:\nI could not validate the model.\nTurns: 67\n")
    (sb4 / "agent_stderr.log").write_text("LiteLLM: RateLimitError 429 ... Retrying\n")
    assert cm.collect(sb4)["exit_reason"] == "completed"
    sb5 = build(tmp_path / "e", stdout="Error: RateLimitError: 429 Too Many Requests\n")
    assert cm.collect(sb5)["exit_reason"] == "rate_limit"


def test_cli(tmp_path):
    sb = build(tmp_path)
    r = subprocess.run([sys.executable, str(SCRIPT), str(sb)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert (sb / "metrics.json").is_file() and (sb / "verdict.yaml").read_text().startswith("success: null")
    assert "llm_calls=5" in r.stdout
    assert subprocess.run([sys.executable, str(SCRIPT), str(tmp_path / "missing")], capture_output=True).returncode == 1
