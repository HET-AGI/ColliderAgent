"""Tests for scripts/bench/longhorizon_table.py."""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "bench" / "longhorizon_table.py"
sys.path.insert(0, str(SCRIPT.parent))
import longhorizon_table as lh  # noqa: E402


def sandbox(root, label, model, harness, success, metrics, arxiv="1308.2209"):
    d = root / label
    d.mkdir(parents=True)
    (d / "run.env").write_text(f"LABEL={label}\nARXIV={arxiv}\nFIGURE=3\nMODEL={model}\nHARNESS={harness}\nMEMORY=cold\n")
    (d / "metrics.json").write_text(json.dumps(metrics))
    (d / "verdict.yaml").write_text(f"success: {success}\nfailure_mode: null\nnotes: \"\"\n")


def test_rows_and_render(tmp_path):
    root = tmp_path / "runs"
    sandbox(root, "a1", "gemini", "adk", "false", {"wall_clock_s": 3600, "llm_calls": 150, "tool_calls": 150, "tool_errors": 50,
                                                    "error_refine_cycles": 48, "magnus_jobs": 20, "max_context_tokens": 100000,
                                                    "tokens_in_total": 9e6, "exit_reason": "max_llm_calls"})
    sandbox(root, "a2", "gemini", "adk", "true", {"wall_clock_s": 1800, "llm_calls": 30, "tool_calls": 30, "tool_errors": 2,
                                                   "error_refine_cycles": 2, "magnus_jobs": 6, "max_context_tokens": 40000,
                                                   "tokens_in_total": 1e6, "exit_reason": "completed"})
    sandbox(root, "b1", "gemini", "gemini", "true", {"wall_clock_s": 1800, "tool_calls": 60, "tool_errors": 0, "magnus_jobs": 8,
                                                      "tokens_in_total": 2e6}, arxiv="2103.02708")
    table = lh.rows(root)
    assert [t["column"] for t in table] == ["gemini / adk", "gemini / gemini"]
    adk = table[0]
    assert adk["runs"] == 2 and adk["success"] == 1 and adk["llm_calls"] == 90 and adk["tool_errors"] == 26
    assert adk["refine_cycles"] == 25 and adk["max_context_k"] == 70 and adk["tokens_in_M"] == 5
    assert adk["exit_reasons"] == {"max_llm_calls": 1, "completed": 1}
    gem = table[1]
    assert gem["llm_calls"] is None and gem["tool_errors"] is None and gem["refine_cycles"] is None and gem["max_context_k"] is None
    text = lh.render(table)
    assert "| gemini / adk | 2 | 1 | 0.75 | 90 | 90 | 26 | 25 | 13 | 70 | 5.0 | completed (1), max_llm_calls (1) |" in text
    assert "| gemini / gemini | 1 | 1 | 0.50 | - | 60 | - | - | 8 | - | 2.0 | - |" in text
    assert [t["column"] for t in lh.rows(root, {"2103.02708"})] == ["gemini / gemini"]
    r = subprocess.run([sys.executable, str(SCRIPT), str(root), "--benchmarks", "1308.2209"], capture_output=True, text=True)
    assert r.returncode == 0 and "gemini / adk" in r.stdout and "gemini / gemini" not in r.stdout
    assert subprocess.run([sys.executable, str(SCRIPT), str(tmp_path / "missing")], capture_output=True).returncode == 1
