"""Tests for scripts/bench/pack_results.py."""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "bench" / "pack_results.py"
sys.path.insert(0, str(SCRIPT.parent))
import pack_results as pr  # noqa: E402


def sandbox(root, label, model, harness, success, fig=None, arxiv="1308.2209", figure="3"):
    d = root / label
    d.mkdir(parents=True)
    (d / "run.env").write_text(f"LABEL={label}\nARXIV={arxiv}\nFIGURE={figure}\nMODEL={model}\nHARNESS={harness}\nMEMORY=cold\n")
    (d / "metrics.json").write_text(json.dumps({"wall_clock_s": 3600, "magnus_jobs": 3, "tokens_in_total": 1e6, "tokens_out_total": 1e4}))
    produced = ""
    if fig:
        (d / "output").mkdir()
        (d / "output" / fig).write_bytes(b"png")
        produced = str(d / "output" / fig)
    (d / "verdict.yaml").write_text(f'success: {success}\nfailure_mode: null\nnotes: ""\nfootnote: ""\nproduced_figure: "{produced}"\n')
    return d


def test_pack(tmp_path):
    root = tmp_path / "runs"
    sandbox(root, "a1", "gemini-3.1-pro-preview", "adk", "true", "x.png")
    sandbox(root, "a2", "gemini-3.1-pro-preview", "adk", "false")
    sandbox(root, "b1", "gemini-3.1-pro-preview", "gemini", "true", "y.png")
    extra = tmp_path / "doc.json"
    extra.write_text(json.dumps({"runs": [{"label": "doc-1", "arxiv": "1308.2209", "figure": "3", "model": "claude-opus-4-6",
                                          "harness": "claude", "success": True, "metrics": {"wall_clock_s": 1800}}]}))
    out = tmp_path / "out"
    r = pr.pack(root, out, [extra])
    assert r["runs"] == 4 and r["no_figure"] == ["a2"]
    assert sorted(r["figures"]) == ["1308.2209_fig3__gemini-3.1-pro-preview-adk__a1.png",
                                    "1308.2209_fig3__gemini-3.1-pro-preview-gemini__a1.png"]
    assert (out / "tables.md").read_text().startswith("Runs found: 4")
    assert "| gemini-3.1-pro-preview / adk | gemini-3.1-pro-preview / gemini |" in (out / "tables.md").read_text()
    rows = (out / "runs.csv").read_text().splitlines()
    assert rows[0].startswith("attempt,benchmark,model") and len(rows) == 5
    r2 = subprocess.run([sys.executable, str(SCRIPT), str(root), str(out), "--extra", str(extra), "--no-figures"],
                        capture_output=True, text=True)
    assert r2.returncode == 0 and "packed 4 runs" in r2.stdout
    assert subprocess.run([sys.executable, str(SCRIPT), str(tmp_path / "missing"), str(out)], capture_output=True).returncode == 1
