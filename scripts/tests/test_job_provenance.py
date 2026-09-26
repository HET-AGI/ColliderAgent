"""Tests for scripts/bench/job_provenance.py."""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "bench" / "job_provenance.py"
sys.path.insert(0, str(SCRIPT.parent))
import job_provenance as jp  # noqa: E402


def test_valid_and_foreign(tmp_path):
    sb = tmp_path / "sb"
    (sb / ".agents" / "skills" / "x").mkdir(parents=True)
    (sb / ".agents" / "skills" / "x" / "SKILL.md").write_text("magnus logs ffffffffffffffff  # example in a skill, ignored\n")
    (sb / "events.jsonl").write_text(json.dumps({"item": {"type": "command_execution",
        "command": "magnus run madgraph-launch --process p.tar --output ev",
        "aggregated_output": "Job aaaaaaaaaaaaaaaa submitted. Waiting for completion..."}}) + "\n"
        + json.dumps({"item": {"type": "command_execution", "command": "magnus logs aaaaaaaaaaaaaaaa | tail -50"}}) + "\n")
    r = jp.scan(sb, check_server=False)
    assert r["submitted"] == ["aaaaaaaaaaaaaaaa"] and r["referenced"] == ["aaaaaaaaaaaaaaaa"] and r["valid"]
    (sb / "agent_stderr.log").write_text('{"job_id": "bbbbbbbbbbbbbbbb"}\nmagnus job status cccccccccccccccc\nmagnus download -o out dddddddddddddddd\n'
                                         'Job submitted. ID: [green]eeeeeeeeeeeeeeee[/green] (use -1 to reference)\nmagnus logs eeeeeeeeeeeeeeee\n')
    r = jp.scan(sb, check_server=False)
    assert set(r["submitted"]) == {"aaaaaaaaaaaaaaaa", "bbbbbbbbbbbbbbbb", "eeeeeeeeeeeeeeee"}
    assert set(r["foreign"]) == {"cccccccccccccccc", "dddddddddddddddd"} and not r["valid"]
    assert r["foreign"]["cccccccccccccccc"] == "agent_stderr.log"


def test_json_hash_not_linked_to_distant_command(tmp_path):
    sb = tmp_path / "sb"
    sb.mkdir()
    line = ('{"text": "run magnus job status later", "harnessSectionHash": "9908214ee726f4f0", '
            '"more": "' + "x" * 200 + '"}\n')
    (sb / "transcript.jsonl").write_text(line)
    r = jp.scan(sb, check_server=False)
    assert r["referenced"] == [] and r["valid"]


def test_cli(tmp_path):
    sb = tmp_path / "sb"
    sb.mkdir()
    (sb / "run.log").write_text("Job 1111111111111111 submitted\nmagnus logs 1111111111111111\n")
    r = subprocess.run([sys.executable, str(SCRIPT), str(sb), "--no-server"], capture_output=True, text=True)
    assert r.returncode == 0 and "VALID" in r.stdout and (sb / "provenance.json").is_file()
    (sb / "run.log").write_text("magnus logs 2222222222222222\n")
    r = subprocess.run([sys.executable, str(SCRIPT), str(sb), "--no-server"], capture_output=True, text=True)
    assert r.returncode == 3 and "INVALID" in r.stdout and "2222222222222222" in r.stdout
    assert subprocess.run([sys.executable, str(SCRIPT), str(tmp_path / "missing")], capture_output=True).returncode == 1


def test_creation_time_window(tmp_path, monkeypatch):
    sb = tmp_path / "sb"
    sb.mkdir()
    (sb / "run.log").write_text("magnus logs 3333333333333333\nmagnus logs 4444444444444444\n")
    (sb / "start.ts").write_text("1000000")
    (sb / "end.ts").write_text("1003600")
    monkeypatch.setattr(jp, "job_created_at", lambda jid: 1001800 if jid == "3333333333333333" else 900000)
    r = jp.scan(sb)
    assert list(r["own_by_creation_time"]) == ["3333333333333333"]
    assert list(r["foreign"]) == ["4444444444444444"] and not r["valid"]
