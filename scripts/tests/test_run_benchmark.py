"""End-to-end test of scripts/bench/run_benchmark.sh with a fake `claude` binary (no network)."""
import json
import os
import subprocess
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RUN = REPO / "scripts" / "bench" / "run_benchmark.sh"
PROMPT = "# Target\n\nPlot $E_T^{\\text{miss}}$ for `p p > a w+ a` with $(echo injected) and \"quotes\" 'single' \\n done\n"

FAKE_CLAUDE = r'''#!/usr/bin/env bash
# fake claude for tests: records its arguments, writes a transcript, prints a result JSON
if [[ "${1:-}" == "--version" ]]; then echo "0.0.0-fake (Claude Code)"; exit 0; fi
if [[ "${1:-}" == "--help" ]]; then echo "usage: fake"; exit 0; fi
printf '%s\n' "$@" > claude_args.txt
: "${CLAUDE_CONFIG_DIR:?CLAUDE_CONFIG_DIR must be set}"
echo "$CLAUDE_CONFIG_DIR" > claude_config_dir.txt
sid="fake-session-0001"
slug="$(printf '%s' "$PWD" | sed 's/[^A-Za-z0-9]/-/g')"
mkdir -p "$CLAUDE_CONFIG_DIR/projects/$slug"
cat > "$CLAUDE_CONFIG_DIR/projects/$slug/$sid.jsonl" <<'J'
{"type":"assistant","requestId":"r1","message":{"role":"assistant","content":[{"type":"tool_use","name":"Bash","input":{"command":"magnus run madgraph-compile -- --process x"}},{"type":"tool_use","name":"Agent","input":{"prompt":"x"}}],"usage":{"input_tokens":1,"output_tokens":1}}}
{"type":"assistant","requestId":"r2","message":{"role":"assistant","content":[{"type":"tool_use","name":"Write","input":{"file_path":"/w/plot.py","content":"x"}}],"usage":{"input_tokens":1,"output_tokens":1}}}
J
mkdir -p output/figures && echo png > output/figures/fig.png
printf '{"type":"result","subtype":"success","is_error":false,"session_id":"%s","total_cost_usd":1.5,"num_turns":3,"duration_ms":1000,"usage":{"input_tokens":100,"cache_creation_input_tokens":200,"cache_read_input_tokens":300,"output_tokens":40}}\n' "$sid"
'''


def make_env(tmp_path):
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    (fake_bin / "claude").write_text(FAKE_CLAUDE)
    (fake_bin / "claude").chmod(0o755)
    cfg = tmp_path / "home-config"
    (cfg / "agent-memory" / "collider-simulator" / "lessons").mkdir(parents=True)
    (cfg / "agent-memory" / "collider-simulator" / "lessons" / "madgraph-x.md").write_text("---\nstage: madgraph\n---\n")
    (cfg / ".credentials.json").write_text('{"fake": true}')
    (cfg / "settings.json").write_text("{}")
    papers = tmp_path / "papers"
    (papers / "0000.00001" / "analysis" / "hepdata").mkdir(parents=True)
    (papers / "0000.00001" / "prompt_figure_2.md").write_text(PROMPT)
    (papers / "0000.00001" / "analysis" / "hepdata" / "table.yaml").write_text("a: 1\n")
    (papers / "0000.00001" / "data.yaml").write_text("b: 2\n")
    env = dict(os.environ,
               PATH=f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}",
               CLAUDE_CONFIG_DIR=str(cfg),
               BENCH_RUNS_DIR=str(tmp_path / "runs"),
               BENCH_PAPER_ROOT=str(papers),
               BENCH_POLL_S="1")
    return env


def test_cold_run_end_to_end(tmp_path):
    env = make_env(tmp_path)
    r = subprocess.run([str(RUN), "0000.00001", "2", "claude-opus-5", "--effort", "high", "--label", "cold1",
                        "--extra-args", "--verbose --foo bar"], capture_output=True, text=True, env=env, timeout=120)
    assert r.returncode == 0, r.stdout + r.stderr
    sb = tmp_path / "runs" / "cold1"
    assert (tmp_path / "runs" / ".gitignore").read_text() == "*\n!.gitignore\n"
    assert (sb / "prompt.md").read_text() == PROMPT
    assert (sb / "analysis" / "hepdata" / "table.yaml").is_file() and (sb / "data.yaml").is_file()
    cfg = sb / ".claude-config"
    assert (cfg / "skills" / "magnus" / "SKILL.md").is_file() and (cfg / "agents" / "model-generator.md").is_file()
    assert (cfg / ".credentials.json").read_text() == '{"fake": true}' and (cfg / "settings.json").is_file()
    assert (cfg / "agent-memory").is_dir() and not any((cfg / "agent-memory").iterdir())  # cold = empty
    env_text = (sb / "run.env").read_text()
    for key in ("MODEL=claude-opus-5", "EFFORT=high", "MEMORY=cold", "ARXIV=0000.00001", "FIGURE=2",
                "GIT_COMMIT=", "START_UTC=", "LABEL=cold1", "EXTRA_ARGS=--verbose --foo bar"):
        assert key in env_text, key
    # the prompt reached claude as one argument, byte-for-byte (minus the trailing newline), un-evaluated
    args = (sb / "claude_args.txt").read_text().split("\n")
    assert args[0] == "-p"
    prompt_lines = PROMPT.rstrip("\n").split("\n")
    assert args[1:1 + len(prompt_lines)] == prompt_lines
    rest = args[1 + len(prompt_lines):]
    assert rest[:5] == ["--model", "claude-opus-5", "--output-format", "json", "--dangerously-skip-permissions"]
    assert rest[5:10] == ["--effort", "high", "--verbose", "--foo", "bar"]
    assert "injected" not in "".join(rest)
    assert (sb / "claude_config_dir.txt").read_text().strip() == str(cfg)
    status = json.loads((sb / "status.json").read_text())
    assert status["exit_code"] == 0 and status["end_ts"] >= status["start_ts"]
    assert (sb / "start.ts").is_file() and (sb / "end.ts").is_file() and (sb / "stderr.log").is_file()
    assert json.loads((sb / "result.json").read_text())["session_id"] == "fake-session-0001"
    metrics = json.loads((sb / "metrics.json").read_text())
    assert metrics["magnus_jobs"] == 1 and metrics["subagent_calls"] == 1 and metrics["files_written"] == 1
    assert metrics["tokens_in"] == 600 and metrics["tokens_out"] == 40 and metrics["cost_usd"] == 1.5
    assert metrics["model"] == "claude-opus-5" and metrics["effort"] == "high"
    assert (sb / "transcript.jsonl").is_file() and (sb / "verdict.yaml").is_file()
    assert metrics["table_s3_row"] in r.stdout
    # refuses to reuse a sandbox
    r2 = subprocess.run([str(RUN), "0000.00001", "2", "claude-opus-5", "--label", "cold1"],
                        capture_output=True, text=True, env=env)
    assert r2.returncode == 2 and "already exists" in r2.stderr


def test_warm_run_no_wait(tmp_path):
    env = make_env(tmp_path)
    r = subprocess.run([str(RUN), "0000.00001", "2", "claude-sonnet-5", "--memory", "warm", "--no-wait"],
                       capture_output=True, text=True, env=env, timeout=60)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "pid:" in r.stdout and "sandbox:" in r.stdout
    sb = Path(r.stdout.split("sandbox:", 1)[1].split("\n", 1)[0].strip())
    assert sb.parent == tmp_path / "runs" and sb.name.endswith("_0000.00001_fig2_claude-sonnet-5")
    assert (sb / ".claude-config" / "agent-memory" / "collider-simulator" / "lessons" / "madgraph-x.md").is_file()
    for _ in range(60):
        if (sb / "metrics.json").is_file():
            break
        time.sleep(0.5)
    assert (sb / "status.json").is_file() and (sb / "metrics.json").is_file()
    assert "MEMORY=warm" in (sb / "run.env").read_text()
    assert "EFFORT=\n" in (sb / "run.env").read_text()
    args = (sb / "claude_args.txt").read_text().split("\n")
    assert "--effort" not in args


def test_rejects_bad_memory_mode(tmp_path):
    env = make_env(tmp_path)
    r = subprocess.run([str(RUN), "0000.00001", "2", "m", "--memory", "hot"], capture_output=True, text=True, env=env)
    assert r.returncode == 2 and "cold or warm" in r.stderr
