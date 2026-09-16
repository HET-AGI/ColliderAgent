"""Tests for scripts/bench/collect_metrics.py on a synthetic sandbox."""
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
COLLECT = REPO / "scripts" / "bench" / "collect_metrics.py"
sys.path.insert(0, str(COLLECT.parent))
import collect_metrics  # noqa: E402

SESSION = "11111111-2222-3333-4444-555555555555"


def _assistant(blocks, usage=None, req="r1"):
    return {"type": "assistant", "requestId": req,
            "message": {"role": "assistant", "content": blocks,
                        "usage": usage or {"input_tokens": 10, "cache_creation_input_tokens": 20,
                                           "cache_read_input_tokens": 30, "output_tokens": 5}}}


def _tool(name, **inp):
    return {"type": "tool_use", "id": f"toolu_{name}", "name": name, "input": inp}


def make_sandbox(tmp_path, slug_ok=True):
    sandbox = tmp_path / "bench_runs" / "20260916T120000Z_1701.05379_fig8_claude-opus-5"
    cfg = sandbox / ".claude-config"
    cfg.mkdir(parents=True)
    (sandbox / "result.json").write_text(json.dumps({
        "type": "result", "subtype": "success", "is_error": False, "session_id": SESSION,
        "total_cost_usd": 12.3456, "num_turns": 42, "duration_ms": 7_000_000,
        "usage": {"input_tokens": 1000, "cache_creation_input_tokens": 200000,
                  "cache_read_input_tokens": 1300000, "output_tokens": 12345},
    }))
    (sandbox / "status.json").write_text(json.dumps({"start_ts": 1000, "end_ts": 8200, "exit_code": 0}))
    (sandbox / "run.env").write_text(
        "LABEL=opus5-fig8\nARXIV=1701.05379\nFIGURE=8\nMODEL=claude-opus-5\nEFFORT=high\nMEMORY=cold\n"
        f"GIT_COMMIT=abc123\nCONFIG_DIR={cfg}\nEXTRA_ARGS=\n")
    slug = collect_metrics.path_slug(sandbox.resolve()) if slug_ok else "-some-other-slug"
    proj = cfg / "projects" / slug
    proj.mkdir(parents=True)
    main_lines = [
        json.dumps({"type": "user", "message": {"role": "user", "content": "go"}}),
        "this line is not json {",
        json.dumps(_assistant([_tool("Agent", prompt="build model", subagent_type="model-generator")], req="r1")),
        json.dumps(_assistant([_tool("Bash", command="magnus run madgraph-compile -- --process 'p p > e+ e-' --output x")], req="r2")),
        json.dumps(_assistant([_tool("Bash", command="ls -la && magnus job result abc")], req="r3")),
        json.dumps(_assistant([_tool("Write", file_path="/w/a.py", content="x")], req="r4")),
        json.dumps(_assistant([_tool("Edit", file_path="/w/a.py", old_string="x", new_string="y")], req="r4")),
        json.dumps(_assistant([_tool("Write", file_path="/w/b.md", content="x"),
                               _tool("Task", prompt="analyze", subagent_type="event-analyzer")], req="r5")),
        json.dumps({"type": "assistant", "message": {"role": "assistant", "content": "plain text"}}),
        json.dumps(["not", "a", "dict"]),
    ]
    (proj / f"{SESSION}.jsonl").write_text("\n".join(main_lines) + "\n")
    sub = proj / SESSION / "subagents"
    sub.mkdir(parents=True)
    (sub / "agent-abc.jsonl").write_text("\n".join([
        json.dumps(_assistant([_tool("Bash", command="cd x && magnus blueprint run madgraph-launch -- --process x")], req="s1")),
        json.dumps(_assistant([_tool("Bash", command="magnus launch validate-feynrules -- --model m.fr")], req="s2")),
        json.dumps(_assistant([_tool("Write", file_path="/w/c.mg5", content="x")], req="s3")),
        json.dumps(_assistant([_tool("Read", file_path="/w/c.mg5")], req="s4")),
    ]) + "\n")
    return sandbox


def test_compute_counts_and_row(tmp_path):
    sandbox = make_sandbox(tmp_path)
    m = collect_metrics.compute(sandbox)
    assert m["subagent_calls"] == 2
    assert m["magnus_jobs"] == 3
    assert m["files_written"] == 3
    assert m["files_written_paths"] == ["/w/a.py", "/w/b.md", "/w/c.mg5"]
    assert m["tokens_in"] == 1000 + 200000 + 1300000
    assert m["tokens_out"] == 12345
    assert m["cost_usd"] == 12.3456 and m["num_turns"] == 42
    assert m["wall_clock_s"] == 7200
    assert m["label"] == "opus5-fig8" and m["model"] == "claude-opus-5" and m["session_id"] == SESSION
    assert m["tool_calls"] == {"Agent": 1, "Bash": 4, "Edit": 1, "Read": 1, "Task": 1, "Write": 3}
    assert m["table_s3_row"] == "| opus5-fig8 | 2.00 | 2 | 3 | 3 | 1.50 | 12.3 |"
    assert m["transcript"]["found"] and m["transcript"]["subagent_files"] == 1
    # usage cross-check sums each requestId once (r4 appears on two lines)
    assert m["transcript"]["usage_crosscheck"]["input_tokens"] == 10 * (5 + 4)
    assert (sandbox / "transcript.jsonl").is_file()
    assert (sandbox / "transcript_subagents" / "agent-abc.jsonl").is_file()


def test_cli_writes_metrics_and_verdict_template(tmp_path):
    sandbox = make_sandbox(tmp_path)
    r = subprocess.run([sys.executable, str(COLLECT), str(sandbox)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "| opus5-fig8 | 2.00 | 2 | 3 | 3 | 1.50 | 12.3 |"
    metrics = json.loads((sandbox / "metrics.json").read_text())
    assert metrics["magnus_jobs"] == 3 and metrics["table_s3_row"] == r.stdout.strip()
    verdict = (sandbox / "verdict.yaml").read_text()
    assert verdict == 'success: null\nfailure_mode: null\nnotes: ""\njudged_by: ""\n'
    # an existing verdict is never overwritten
    (sandbox / "verdict.yaml").write_text("success: true\n")
    subprocess.run([sys.executable, str(COLLECT), str(sandbox)], capture_output=True, text=True, check=True)
    assert (sandbox / "verdict.yaml").read_text() == "success: true\n"


def test_transcript_found_by_glob_when_slug_misses(tmp_path):
    sandbox = make_sandbox(tmp_path, slug_ok=False)
    m = collect_metrics.compute(sandbox)
    assert m["transcript"]["found"] and m["magnus_jobs"] == 3 and m["subagent_calls"] == 2


def test_missing_transcript_and_result_degrade_to_unknown(tmp_path):
    sandbox = tmp_path / "s"
    sandbox.mkdir()
    (sandbox / "run.env").write_text("LABEL=empty\nMODEL=m\n")
    m = collect_metrics.compute(sandbox)
    assert m["subagent_calls"] is None and m["tokens_in"] is None and m["wall_clock_s"] is None
    assert m["table_s3_row"] == "| empty | ? | ? | ? | ? | ? | ? |"
    r = subprocess.run([sys.executable, str(COLLECT), str(sandbox)], capture_output=True, text=True)
    assert r.returncode == 0 and "transcript not found" in r.stderr


def test_slug_rule():
    assert collect_metrics.path_slug(Path("/home/u/ColliderAgent/bench_runs/x_1.2")) == \
        "-home-u-ColliderAgent-bench-runs-x-1-2"
    assert re.fullmatch(r"[A-Za-z0-9-]+", collect_metrics.path_slug(Path("/a b/c.d")))


def test_help():
    assert subprocess.run([sys.executable, str(COLLECT), "--help"], capture_output=True).returncode == 0
