"""Tests for scripts/bench/aggregate.py on fixture sandboxes."""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
AGGREGATE = REPO / "scripts" / "bench" / "aggregate.py"
sys.path.insert(0, str(AGGREGATE.parent))
import aggregate  # noqa: E402


def sandbox(root, label, model, memory="cold", verdict=None, metrics=None, arxiv="1701.05379", figure="8"):
    d = root / label
    d.mkdir(parents=True)
    (d / "run.env").write_text(f"LABEL={label}\nARXIV={arxiv}\nFIGURE={figure}\nMODEL={model}\nMEMORY={memory}\n")
    if metrics is not None:
        (d / "metrics.json").write_text(json.dumps(metrics))
    if verdict is not None:
        (d / "verdict.yaml").write_text(verdict)
    return d


def metrics(wall, sub, mag, files, tin, tout, cost):
    return {"wall_clock_s": wall, "subagent_calls": sub, "magnus_jobs": mag, "files_written": files,
            "tokens_in": tin, "tokens_out": tout, "cost_usd": cost}


def build(tmp_path):
    root = tmp_path / "bench_runs"
    sandbox(root, "a1", "claude-opus-5", verdict='success: true\nfailure_mode: null\nnotes: "ok"\njudged_by: "x"\n',
            metrics=metrics(3600, 4, 6, 10, 2_000_000, 20_000, 10.0))
    sandbox(root, "a2", "claude-opus-5", verdict='success: true\nfailure_mode: null\nnotes: ""\njudged_by: "x"\n',
            metrics=metrics(7200, 6, 8, 14, 4_000_000, 30_000, 20.0))
    sandbox(root, "a3", "claude-opus-5", verdict='success: null\nfailure_mode: null\nnotes: ""\njudged_by: ""\n',
            metrics=metrics(999, 99, 99, 99, 9e9, 9e9, 999.0))
    sandbox(root, "b1", "claude-sonnet-5", verdict='success: false\nfailure_mode: generation\nnotes: "bad"\njudged_by: "x"\n',
            metrics=metrics(100, 1, 1, 1, 1, 1, 1.0))
    sandbox(root, "b2", "claude-sonnet-5", memory="warm", verdict='success: false\nfailure_mode: analysis\nnotes: ""\njudged_by: "x"\n',
            metrics=metrics(100, 1, 1, 1, 1, 1, 1.0))
    sandbox(root, "c1", "claude-opus-5", arxiv="1811.07920", figure="3", metrics=metrics(10, 1, 1, 1, 1, 1, 1.0))
    (root / "not-a-run").mkdir()
    (root / "stray.txt").write_text("x")
    return root


def test_tables(tmp_path):
    root = build(tmp_path)
    out = aggregate.render(aggregate.load_runs(root))
    assert "Runs found: 6 (successful 2, failed 2, unjudged 2)" in out
    # S3: only the two successful opus runs, averaged
    assert "| 1701.05379 Fig. 8 | claude-opus-5 | 2 | 1.50 | 5.0 | 7.0 | 12.0 | 3.00 | 25.0 | 15.00 |" in out
    assert "claude-sonnet-5 |" not in out.split("### Table S4")[0]
    # S4: success/attempted per benchmark x model, unjudged shown with ?
    s4 = out.split("### Table S4")[1].split("### Table S5")[0]
    assert "| Benchmark | claude-opus-5 | claude-sonnet-5 | claude-sonnet-5 (warm) |" in s4
    assert "| 1701.05379 Fig. 8 | 2/3 (1 ?) | 0/1 | 0/1 |" in s4
    assert "| 1811.07920 Fig. 3 | 0/1 (1 ?) | - | - |" in s4
    # S5: per benchmark with failure modes
    s5 = out.split("### Table S5")[1]
    assert "| 1701.05379 Fig. 8 | 2/5 (1 ?) | analysis (1), generation (1), unjudged ? (1) |" in s5
    assert "| 1811.07920 Fig. 3 | 0/1 (1 ?) | unjudged ? (1) |" in s5


def test_cli(tmp_path):
    root = build(tmp_path)
    r = subprocess.run([sys.executable, str(AGGREGATE), str(root)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "### Table S3" in r.stdout and "### Table S4" in r.stdout and "### Table S5" in r.stdout
    assert subprocess.run([sys.executable, str(AGGREGATE), str(tmp_path / "missing")], capture_output=True).returncode == 1
    assert subprocess.run([sys.executable, str(AGGREGATE), "--help"], capture_output=True).returncode == 0


def test_empty_dir(tmp_path):
    out = aggregate.render(aggregate.load_runs(tmp_path))
    assert "Runs found: 0" in out and "(no successful runs yet)" in out and "(no runs)" in out


def test_parse_simple_yaml():
    d = aggregate.parse_simple_yaml('success: true\nfailure_mode: null\nnotes: "a: b \\"q\\""\njudged_by: x\n# c\n')
    assert d == {"success": True, "failure_mode": None, "notes": 'a: b "q"', "judged_by": "x"}
