"""Tests for scripts/install.sh and syntax/--help of the shell scripts (no network, no ~/.claude)."""
import os
import re
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
INSTALL = REPO / "scripts" / "install.sh"
SHELL_SCRIPTS = [INSTALL, REPO / "scripts" / "bench" / "run_benchmark.sh",
                 REPO / "scripts" / "bench" / "judge.sh", REPO / "scripts" / "bench" / "smoke.sh"]


def sh(*args, env=None):
    return subprocess.run([str(a) for a in args], capture_output=True, text=True, env=env)


def test_install_then_check_then_drift(tmp_path):
    r = sh(INSTALL, "--target", tmp_path)
    assert r.returncode == 0, r.stderr
    assert (tmp_path / "skills" / "magnus" / "SKILL.md").is_file()
    assert (tmp_path / "skills" / "madgraph-simulator" / "references").is_dir()
    assert (tmp_path / "agents" / "model-generator.md").is_file()
    assert not (tmp_path / "skills" / "README.md").exists()  # loose files are not skills
    src_skills = sorted(p.name for p in (REPO / "src" / "skills").iterdir() if (p / "SKILL.md").is_file())
    assert sorted(p.name for p in (tmp_path / "skills").iterdir()) == src_skills

    r = sh(INSTALL, "--check", "--target", tmp_path)
    assert r.returncode == 0, r.stderr

    with open(tmp_path / "skills" / "magnus" / "SKILL.md", "a") as fh:
        fh.write("\ndrift\n")
    r = sh(INSTALL, "--check", "--target", tmp_path)
    assert r.returncode == 1
    assert "skills/magnus" in r.stderr

    # re-install replaces the skill dir wholesale (stray files vanish) and restores parity
    (tmp_path / "skills" / "magnus" / "stray.txt").write_text("x")
    assert sh(INSTALL, "--target", tmp_path).returncode == 0
    assert not (tmp_path / "skills" / "magnus" / "stray.txt").exists()
    assert sh(INSTALL, "--check", "--target", tmp_path).returncode == 0

    # a foreign skill under the target is left alone and does not count as drift
    (tmp_path / "skills" / "user-skill").mkdir()
    (tmp_path / "skills" / "user-skill" / "SKILL.md").write_text("mine")
    assert sh(INSTALL, "--check", "--target", tmp_path).returncode == 0
    assert sh(INSTALL, "--target", tmp_path).returncode == 0
    assert (tmp_path / "skills" / "user-skill" / "SKILL.md").exists()

    os.remove(tmp_path / "agents" / "model-generator.md")
    r = sh(INSTALL, "--check", "--target", tmp_path)
    assert r.returncode == 1 and "agents/model-generator.md: not installed" in r.stderr


def test_check_against_empty_target_fails(tmp_path):
    r = sh(INSTALL, "--check", "--target", tmp_path / "nothing")
    assert r.returncode == 1 and "not installed" in r.stderr


def test_target_from_claude_config_dir_env(tmp_path):
    env = dict(os.environ, CLAUDE_CONFIG_DIR=str(tmp_path / "cfg"))
    assert sh(INSTALL, env=env).returncode == 0
    assert (tmp_path / "cfg" / "skills" / "magnus" / "SKILL.md").is_file()
    assert sh(INSTALL, "--check", env=env).returncode == 0


@pytest.mark.parametrize("script", SHELL_SCRIPTS, ids=lambda p: p.name)
def test_shell_script_parses_and_has_help(script):
    assert os.access(script, os.X_OK), f"{script} is not executable"
    assert sh("bash", "-n", script).returncode == 0
    r = sh(script, "--help")
    assert r.returncode == 0 and "Usage:" in r.stdout


def test_bad_arguments_exit_2(tmp_path):
    assert sh(INSTALL, "--bogus").returncode == 2
    assert sh(REPO / "scripts" / "bench" / "run_benchmark.sh").returncode == 2
    assert sh(REPO / "scripts" / "bench" / "run_benchmark.sh", "0000.00000", "1", "m").returncode == 2  # no prompt
    assert sh(REPO / "scripts" / "bench" / "judge.sh", tmp_path).returncode == 2
    assert sh(REPO / "scripts" / "bench" / "smoke.sh", "--bogus").returncode == 2


def test_smoke_dry_run_never_calls_magnus(tmp_path):
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    (fake_bin / "magnus").write_text("#!/usr/bin/env bash\necho 'magnus must not run in --dry-run' >&2\nexit 99\n")
    (fake_bin / "magnus").chmod(0o755)
    env = dict(os.environ, PATH=f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}",
               SMOKE_DIR=str(tmp_path / "smoke"))
    r = sh(REPO / "scripts" / "bench" / "smoke.sh", "--dry-run", env=env)
    assert r.returncode == 0, r.stderr
    assert "must not run" not in r.stderr
    # same rule as smoke.sh: first line of the asset starting with L<alnum> (LYuk on 2026-09-16; the
    # earlier " LGauge = ..." line has a leading space and is deliberately not matched)
    fr = (REPO / "python-agent" / "tests" / "assets" / "minimal_Zp.fr").read_text(errors="replace")
    symbol = next(re.match(r"^L[A-Za-z0-9]+", ln).group(0) for ln in fr.splitlines() if re.match(r"^L[A-Za-z0-9]+", ln))
    assert f"--lagrangian {symbol}" in r.stdout
    assert "madgraph-compile" in r.stdout and "madanalysis-process" in r.stdout and "validate-feynrules" in r.stdout
    assert r.stdout.count("| DRY |") == 5
    assert "p\\ p\\ \\>\\ e+\\ e-" in r.stdout  # printf %q of the process string
    launch = next(ln for ln in r.stdout.splitlines() if ln.startswith("== launch:"))
    assert "--commands $'done\\nset nevents 500\\nset ebeam1 7000\\nset ebeam2 7000\\nset use_syst False\\ndone'" in launch
    ma5 = next(ln for ln in r.stdout.splitlines() if ln.startswith("== ma5:"))
    assert "--script $'import {EVENTS_DIR}/Events/run_01/unweighted_events.lhe.gz as sample\\nset sample.type = signal\\nplot M(e+ e-) 50 0 500\\nselect N(e+) >= 1'" in ma5
    assert "--level parton" in ma5
    q = sh(REPO / "scripts" / "bench" / "smoke.sh", "--dry-run", "--quick", env=env)
    assert q.returncode == 0 and q.stdout.count("| DRY |") == 3 and "madgraph-launch" not in q.stdout


def test_smoke_fails_when_site_is_not_zhustation(tmp_path):
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    (fake_bin / "magnus").write_text(
        "#!/usr/bin/env bash\nif [[ $1 == config ]]; then printf '\\n  Current:  local\\n  Token: sk-abcdef123\\n'; exit 0; fi\n"
        "echo 'unexpected magnus call' >&2; exit 99\n")
    (fake_bin / "magnus").chmod(0o755)
    env = dict(os.environ, PATH=f"{fake_bin}{os.pathsep}{os.environ.get('PATH', '')}",
               SMOKE_DIR=str(tmp_path / "smoke"))
    r = sh(REPO / "scripts" / "bench" / "smoke.sh", "--quick", env=env)
    assert r.returncode == 1
    assert "| config | FAIL |" in r.stdout
    assert "sk-abcdef123" not in r.stdout + r.stderr and "sk-***" in r.stdout
    assert "unexpected magnus call" not in r.stderr
