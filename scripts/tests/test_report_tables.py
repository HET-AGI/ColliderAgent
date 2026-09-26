"""Smoke test for scripts/bench/report_tables.py on a minimal results package."""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "bench" / "report_tables.py"
sys.path.insert(0, str(SCRIPT.parent))
import report_tables as rt  # noqa: E402

HEADER = "attempt,benchmark,model,harness,effort,label,source,success,failure_mode,wall_clock_h,subagent_calls,magnus_jobs,files_written,tokens_in_M,tokens_out_k,cost_usd,llm_share_of_wall,footnote\n"


def build(tmp_path):
    res = tmp_path / "res"
    res.mkdir()
    rows = [
        "1,1308.2209 Fig. 3,claude-opus-4-6,claude,xhigh,doc-20260916T2200Z_a,documented,yes,,0.40,3,7,18,3.2,13.3,4.16,0.72,",
        "1,1308.2209 Fig. 3,claude-opus-4-6,claude,xhigh,20260924T182320Z_b,documented,yes,,0.37,2,7,13,2.7,16.3,3.61,0.54,dev",
        "1,1308.2209 Fig. 3,gemini-3.1-pro-preview / adk,adk,,20260926T080037Z_c,sandbox,no,model,1.17,0,24,1,9.1,26.1,,,",
        "2,1308.2209 Fig. 3,gemini-3.1-pro-preview / adk,adk,,20260926T110026Z_d,sandbox,yes,,1.63,0,38,1,3.9,17.2,,,dev2",
        "1,1701.05379 Fig. 8,claude-opus-5,claude,default,doc-20260916T1500Z_e,documented,yes,,0.87,3,5,17,5.7,37.5,9.06,0.38,",
        "1,2005.06475 Fig. 2,claude-opus-4-6,claude,xhigh,doc-20260916T2200Z_f,documented,TBD,,6.41,2,42,28,214.0,220.0,,0.65,tbd note",
    ]
    (res / "runs.csv").write_text(HEADER + "\n".join(rows) + "\n")
    (res / "tables.md").write_text("Footnotes (quantitative deviations of runs counted as successful):\n\n1. 1308.2209 Fig. 3, claude-opus-4-6: dev & 10% off\n2. 1308.2209 Fig. 3, gemini: dev2\n")
    (res / "adk_runs.json").write_text(json.dumps({"runs": [
        {"label": "c", "model": "gemini-3.1-pro-preview", "benchmark": "1308.2209 Fig. 3", "attempt": 1, "llm_calls": 150, "tool_errors": 51,
         "refine_cycles": 50, "ctx_max_k": 98, "exit": "max_llm_calls", "stage": "model_written", "result": "fail:model"}]}))
    (res / "longhorizon_light.md").write_text("| Column | Runs | Success | Exit reasons |\n|---|---:|---:|---|\n| gemini-3.1-pro-preview / adk | 2 | 1 | max_llm_calls (1) |\n")
    return res


def test_fragments(tmp_path):
    res = build(tmp_path)
    out = tmp_path / "out"
    r = subprocess.run([sys.executable, str(SCRIPT), str(res), str(out)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    s4 = (out / "s4_matrix.tex").read_text()
    assert "Heavy N & 2/2 & -- & 1/2 \\\\" in s4 and "Opus 4.8" not in s4
    assert "Scalar LQ $m_{ej}$ (Delphes) & 0/1 (1 TBD) & -- & -- \\\\" in s4
    s5 = (out / "s5_attempts.tex").read_text()
    assert "Heavy N & ok / ok$^{*}$ & m / ok$^{*}$ \\\\" in s5          # attempts renumbered chronologically
    fm = (out / "failure_modes.tex").read_text()
    assert "Gemini 3.1 Pro / ADK & 2 & 1 & 0 & 1 & 0 & 0 & 0 \\\\" in fm
    fn = (out / "footnotes.tex").read_text()
    assert r"\item \textbf{1308.2209 Fig. 3, claude-opus-4-6}: dev \& 10\% off" in fn
    lh = (out / "longhorizon_light.tex").read_text()
    assert "Gemini 3.1 Pro / ADK & 2 & 1 & max\\_llm\\_calls (1) \\\\" in lh
    assert "150 & 51 & 50 & 98" in (out / "adk_runs.tex").read_text()
    assert subprocess.run([sys.executable, str(SCRIPT), str(tmp_path / "missing"), str(out)], capture_output=True).returncode == 1
