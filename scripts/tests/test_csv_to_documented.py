import csv, json, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bench"))
import csv_to_documented as c2d  # noqa: E402

ROWS = [
    {"attempt": "2", "benchmark": "1605.02910 Fig. 1", "model": "gpt-5.5 / codex", "harness": "codex", "effort": "",
     "label": "20260926T1_1605.02910_fig1_codex-gpt-5.5", "source": "sandbox", "success": "yes", "failure_mode": "",
     "wall_clock_h": "1.03", "subagent_calls": "2", "magnus_jobs": "21", "files_written": "11", "tokens_in_M": "11.05",
     "tokens_out_k": "51.0", "cost_usd": "", "llm_share_of_wall": "", "footnote": "ok"},
    {"attempt": "1", "benchmark": "2005.06475 Fig. 2", "model": "claude-opus-4-6", "harness": "claude", "effort": "xhigh",
     "label": "doc-x", "source": "documented", "success": "TBD", "failure_mode": "", "wall_clock_h": "6.41",
     "subagent_calls": "2", "magnus_jobs": "42", "files_written": "28", "tokens_in_M": "214", "tokens_out_k": "220",
     "cost_usd": "", "llm_share_of_wall": "0.65", "footnote": ""},
    {"attempt": "1", "benchmark": "2005.06475 Fig. 2", "model": "gemini-3.1-pro-preview / adk", "harness": "adk", "effort": "",
     "label": "20260926T2_2005.06475_fig2_adk-gemini", "source": "sandbox", "success": "no", "failure_mode": "generation",
     "wall_clock_h": "2.80", "subagent_calls": "0", "magnus_jobs": "35", "files_written": "0", "tokens_in_M": "31.56",
     "tokens_out_k": "91.9", "cost_usd": "", "llm_share_of_wall": "", "footnote": ""},
]


def test_convert_splits_label_and_scales_metrics():
    recs = c2d.convert(ROWS, "note")
    assert [r["label"] for r in recs] == [ROWS[0]["label"], ROWS[2]["label"]]  # documented row skipped
    r = recs[0]
    assert (r["arxiv"], r["figure"], r["model"], r["harness"]) == ("1605.02910", "1", "gpt-5.5", "codex")
    assert r["success"] is True and r["failure_mode"] is None and r["effort"] is None
    assert r["metrics"]["wall_clock_s"] == 3708 and r["metrics"]["tokens_in_total"] == 11050000
    assert r["metrics"]["tokens_out_total"] == 51000 and r["metrics"]["cost_usd"] is None
    g = recs[1]
    assert g["success"] is False and g["failure_mode"] == "generation" and g["footnote"] is None
    assert g["model"] == "gemini-3.1-pro-preview" and g["source_note"] == "note"


def test_roundtrip_through_aggregate(tmp_path):
    src = tmp_path / "runs.csv"
    with src.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(ROWS[0].keys())); w.writeheader(); w.writerows(ROWS)
    out = tmp_path / "doc.json"
    subprocess.run([sys.executable, str(Path(__file__).resolve().parents[1] / "bench" / "csv_to_documented.py"),
                    str(src), str(out)], check=True, capture_output=True)
    runs = json.loads(out.read_text())["runs"]
    assert len(runs) == 2
    empty = tmp_path / "runs"; empty.mkdir()
    out_csv = tmp_path / "out.csv"
    subprocess.run([sys.executable, str(Path(__file__).resolve().parents[1] / "bench" / "aggregate.py"),
                    str(empty), "--extra", str(out), "--csv", str(out_csv)], check=True, capture_output=True, text=True)
    rows = list(csv.DictReader(out_csv.open()))
    by = {r["label"]: r for r in rows}
    assert by[ROWS[0]["label"]]["model"] == "gpt-5.5 / codex" and by[ROWS[0]["label"]]["wall_clock_h"] == "1.03"
    assert by[ROWS[2]["label"]]["tokens_in_M"] == "31.56" and by[ROWS[2]["label"]]["success"] == "no"
