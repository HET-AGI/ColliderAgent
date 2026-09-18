"""Tests for scripts/memory/distill.py (schema, merge, index cap, decay, propose, import, new)."""
import json
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
DISTILL = REPO / "scripts" / "memory" / "distill.py"
sys.path.insert(0, str(DISTILL.parent))
import distill  # noqa: E402

LINE_RE = re.compile(r"^- \[(\w+)\] (.+?) → (.+?) \(support (\d+), last (\d{4}-\d{2}-\d{2})\) \[lessons/([^\]]+\.md)\]$")
OVERFLOW_RE = re.compile(r"^- … (\d+) more lessons not indexed \(run distill\.py --propose or open lessons/\)$")


def run(*args):
    return subprocess.run([sys.executable, str(DISTILL), *map(str, args)], capture_output=True, text=True)


def lesson_text(stage="madgraph", symptom="job success but nevents wrong", fix="keep set lines above the final done",
                support=1, first="2026-09-01", last="2026-09-10", evidence=("job:abc",), generalizable=True,
                root_cause="set lines placed after the second done", blueprint="madgraph-launch", extra="",
                body="Body line."):
    ev = ", ".join(json.dumps(e) for e in evidence)
    return (
        "---\n"
        f"stage: {stage}\n"
        f"blueprint: {blueprint}\n"
        f"symptom: {json.dumps(symptom)}\n"
        f"root_cause: {json.dumps(root_cause)}\n"
        f"fix: {json.dumps(fix)}\n"
        f"evidence: [{ev}]\n"
        f"generalizable: {'true' if generalizable else 'false'}\n"
        f"support: {support}\n"
        f"first_seen: {first}\n"
        f"last_confirmed: {last}\n"
        f"{extra}---\n{body}\n"
    )


def write_lesson(root, agent, name, text):
    p = root / agent / "lessons" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


# --------------------------------------------------------------------------- parser / schema
def test_frontmatter_parser_handles_spec_example_and_edge_cases():
    text = (
        "---\n"
        "stage: madgraph        # feynrules | ufo | calchep | madgraph\n"
        "blueprint: madgraph-launch   # or \"none\"\n"
        'symptom: "job success=true but nevents=10000 instead of requested"\n'
        "root_cause: 'set lines placed after the second done'\n"
        'fix: "keep every set line above the final done # not a comment"\n'
        "evidence:\n"
        "  - job:ca68f501890c2786\n"
        '  - "progress/dy_14tev/step2_madgraph.md"\n'
        "generalizable: true    # false = specific to one model\n"
        "support: 1\n"
        "first_seen: 2026-09-16\n"
        "last_confirmed: 2026-09-16\n"
        'tags: ["mg5", "launch"]\n'
        "---\n"
        "body\n"
    )
    fm, body = distill.split_frontmatter(text)
    meta = distill.parse_frontmatter(fm)
    assert meta["stage"] == "madgraph"
    assert meta["blueprint"] == "madgraph-launch"
    assert meta["symptom"] == "job success=true but nevents=10000 instead of requested"
    assert meta["fix"].endswith("# not a comment")
    assert meta["evidence"] == ["job:ca68f501890c2786", "progress/dy_14tev/step2_madgraph.md"]
    assert meta["generalizable"] is True and meta["support"] == 1
    assert meta["first_seen"] == "2026-09-16"
    assert meta["tags"] == ["mg5", "launch"]
    assert body.strip() == "body"
    assert distill.validate(meta, distill.load_schema()) == []
    # round trip through the writer
    again = distill.parse_frontmatter(distill.split_frontmatter(distill.dump_frontmatter(meta) + "x\n")[0])
    assert again == meta


@pytest.mark.parametrize("bad, field", [
    ({"stage": "nope"}, "stage"),
    ({"symptom": "x" * 201}, "symptom"),
    ({"evidence": []}, "evidence"),
    ({"support": 0}, "support"),
    ({"generalizable": "yes"}, "generalizable"),
    ({"first_seen": "2026-13-40"}, "first_seen"),
    ({"extra_field": 1}, "extra_field"),
])
def test_schema_rejects_bad_values(bad, field):
    meta = distill.parse_frontmatter(distill.split_frontmatter(lesson_text())[0])
    meta.update(bad)
    errs = distill.validate(meta, distill.load_schema())
    assert errs and any(field in e for e in errs)


def test_rebuild_rejects_invalid_file_with_exit_2(tmp_path):
    good = write_lesson(tmp_path, "collider-simulator", "madgraph-good.md", lesson_text())
    bad = write_lesson(tmp_path, "collider-simulator", "madgraph-bad.md", lesson_text(stage="mg5"))
    r = run("rebuild", "--root", tmp_path)
    assert r.returncode == 2, r.stderr
    assert str(bad) in r.stderr and "stage" in r.stderr
    assert not (tmp_path / "collider-simulator" / "MEMORY.md").exists()
    assert good.exists() and bad.exists()


# --------------------------------------------------------------------------- rebuild / index
def test_rebuild_index_format(tmp_path):
    write_lesson(tmp_path, "collider-simulator", "madgraph-a.md",
                 lesson_text(symptom="A symptom", fix="A fix", support=2, last="2026-09-10"))
    write_lesson(tmp_path, "collider-simulator", "madgraph-b.md",
                 lesson_text(symptom="B symptom", fix="B fix", support=5, last="2026-09-01"))
    write_lesson(tmp_path, "collider-simulator", "madanalysis-c.md",
                 lesson_text(stage="madanalysis", symptom="C symptom", fix="C fix", support=2, last="2026-09-12"))
    r = run("rebuild", "--root", tmp_path)
    assert r.returncode == 0, r.stderr
    lines = (tmp_path / "collider-simulator" / "MEMORY.md").read_text(encoding="utf-8").splitlines()
    assert lines[0].startswith("# ") and "collider-simulator" in lines[0]
    assert "injected into the subagent prompt" in lines[1]
    assert lines[2:] == [
        "- [madgraph] B symptom → B fix (support 5, last 2026-09-01) [lessons/madgraph-b.md]",
        "- [madanalysis] C symptom → C fix (support 2, last 2026-09-12) [lessons/madanalysis-c.md]",
        "- [madgraph] A symptom → A fix (support 2, last 2026-09-10) [lessons/madgraph-a.md]",
    ]
    assert all(LINE_RE.match(ln) for ln in lines[2:])


def test_duplicate_merge(tmp_path):
    write_lesson(tmp_path, "collider-simulator", "madgraph-one.md",
                 lesson_text(symptom="Job success but NEVENTS wrong!", fix="short fix", support=1,
                             first="2026-09-05", last="2026-09-05", evidence=("job:a",)))
    write_lesson(tmp_path, "collider-simulator", "madgraph-two.md",
                 lesson_text(symptom="job success, but nevents wrong", fix="a much longer fix text", support=2,
                             first="2026-09-01", last="2026-09-10", evidence=("job:b", "job:a")))
    r = run("rebuild", "--root", tmp_path)
    assert r.returncode == 0, r.stderr
    files = sorted(p.name for p in (tmp_path / "collider-simulator" / "lessons").glob("*.md"))
    assert files == ["madgraph-two.md"]  # higher support wins the path
    les, _ = distill.load_lesson(tmp_path / "collider-simulator" / "lessons" / "madgraph-two.md")
    assert les.meta["support"] == 3
    assert les.meta["evidence"] == ["job:b", "job:a"]
    assert les.meta["first_seen"] == "2026-09-01" and les.meta["last_confirmed"] == "2026-09-10"
    assert les.meta["fix"] == "a much longer fix text"
    index = (tmp_path / "collider-simulator" / "MEMORY.md").read_text(encoding="utf-8")
    assert index.count("\n- [") == 1 and "(support 3, last 2026-09-10)" in index


def test_index_cap_with_250_lessons(tmp_path):
    base = date(2026, 1, 1)
    for i in range(250):
        write_lesson(tmp_path, "event-analyzer", f"madanalysis-s{i:03d}.md",
                     lesson_text(stage="madanalysis", symptom=f"symptom number {i} " + "x" * 40,
                                 fix=f"fix number {i} " + "y" * 40, support=(i % 7) + 1,
                                 last=(base + timedelta(days=i % 50)).isoformat(),
                                 evidence=(f"job:{i}",)))
    r = run("rebuild", "--root", tmp_path)
    assert r.returncode == 0, r.stderr
    text = (tmp_path / "event-analyzer" / "MEMORY.md").read_text(encoding="utf-8")
    lines = text.splitlines()
    assert len(lines) <= 200 and len(text.encode("utf-8")) <= 25_000
    m = OVERFLOW_RE.match(lines[-1])
    assert m, lines[-1]
    entries = lines[2:-1]
    assert all(LINE_RE.match(ln) for ln in entries)
    assert int(m.group(1)) == 250 - len(entries)
    keys = [(int(LINE_RE.match(ln).group(4)), LINE_RE.match(ln).group(5)) for ln in entries]
    # support desc, then last_confirmed desc
    assert keys == sorted(keys, key=lambda k: (-k[0], tuple(-int(p) for p in k[1].split("-"))))
    assert keys[0][0] == 7
    assert len(list((tmp_path / "event-analyzer" / "lessons").glob("*.md"))) == 250


# --------------------------------------------------------------------------- decay
def test_decay_archives_only_stale_support_one(tmp_path):
    today = date(2026, 9, 16)
    write_lesson(tmp_path, "model-generator", "feynrules-stale.md",
                 lesson_text(stage="feynrules", symptom="stale one", support=1, last="2020-01-01", first="2020-01-01"))
    write_lesson(tmp_path, "model-generator", "feynrules-stale-strong.md",
                 lesson_text(stage="feynrules", symptom="stale but confirmed twice", support=2,
                             last="2020-01-01", first="2020-01-01"))
    write_lesson(tmp_path, "model-generator", "feynrules-fresh.md",
                 lesson_text(stage="feynrules", symptom="fresh one", support=1,
                             last=(today - timedelta(days=10)).isoformat(), first="2026-09-01"))
    r = run("decay", "--root", tmp_path, "--stale-days", 90, "--today", today.isoformat())
    assert r.returncode == 0, r.stderr
    agent = tmp_path / "model-generator"
    assert (agent / "archive" / "feynrules-stale.md").exists()
    assert not (agent / "lessons" / "feynrules-stale.md").exists()
    assert (agent / "lessons" / "feynrules-stale-strong.md").exists()
    assert (agent / "lessons" / "feynrules-fresh.md").exists()
    index = (agent / "MEMORY.md").read_text(encoding="utf-8")
    assert "stale one" not in index and "fresh one" in index and "confirmed twice" in index


# --------------------------------------------------------------------------- propose
def test_propose_threshold_and_target_skill(tmp_path):
    write_lesson(tmp_path, "collider-simulator", "madgraph-yes.md",
                 lesson_text(symptom="promote me", support=3, generalizable=True))
    write_lesson(tmp_path, "collider-simulator", "madgraph-low.md",
                 lesson_text(symptom="too little support", support=2, generalizable=True))
    write_lesson(tmp_path, "collider-simulator", "madgraph-specific.md",
                 lesson_text(symptom="paper specific", support=9, generalizable=False))
    write_lesson(tmp_path, "pheno-analyzer", "pheno-yes.md",
                 lesson_text(stage="pheno", blueprint="none", symptom="pheno lesson", support=4, generalizable=True))
    r = run("propose", "--root", tmp_path)
    assert r.returncode == 0, r.stderr
    assert "promote me" in r.stdout and "pheno lesson" in r.stdout
    assert "too little support" not in r.stdout and "paper specific" not in r.stdout
    data = json.loads((tmp_path / "proposals.json").read_text(encoding="utf-8"))
    cands = {c["symptom"]: c for c in data["candidates"]}
    assert set(cands) == {"promote me", "pheno lesson"}
    assert cands["promote me"]["target_skill"] == "madgraph-simulator"
    assert cands["promote me"]["target_skill_file"] == "src/skills/madgraph-simulator/SKILL.md"
    assert cands["pheno lesson"]["target_skill"] == "pheno-pipeline-orchestrator"
    assert [c["support"] for c in data["candidates"]] == [4, 3]
    r2 = run("propose", "--root", tmp_path, "--min-support", 2)
    assert "too little support" in r2.stdout


def test_target_skill_map_is_complete():
    assert set(distill.TARGET_SKILL) == set(distill.STAGES)
    for skill in set(distill.TARGET_SKILL.values()):
        assert (REPO / "src" / "skills" / skill / "SKILL.md").exists(), skill


# --------------------------------------------------------------------------- import
def test_import_merges_and_never_lowers_support(tmp_path):
    central = tmp_path / "central"
    other = tmp_path / "sandbox-config" / "agent-memory"
    write_lesson(central, "collider-simulator", "madgraph-known.md",
                 lesson_text(symptom="known symptom", support=5, evidence=("job:c1", "job:c2"),
                             first="2026-08-01", last="2026-09-01", fix="central fix"))
    write_lesson(central, "collider-simulator", "madgraph-clash.md",
                 lesson_text(symptom="central clash symptom", support=2, evidence=("job:c3",)))
    # independent confirmation (disjoint evidence) -> support summed
    write_lesson(other, "collider-simulator", "madgraph-known.md",
                 lesson_text(symptom="Known symptom.", support=1, evidence=("job:x",), first="2026-09-10",
                             last="2026-09-10", fix="central fix"))
    # same file name, different symptom -> added under a new name, central file untouched
    write_lesson(other, "collider-simulator", "madgraph-clash.md",
                 lesson_text(symptom="a different sandbox symptom", support=1, evidence=("job:y",)))
    # brand-new agent
    write_lesson(other, "event-analyzer", "madanalysis-new.md",
                 lesson_text(stage="madanalysis", symptom="new lesson", support=1, evidence=("job:z",)))
    r = run("import", "--from", tmp_path / "sandbox-config", "--root", central)
    assert r.returncode == 0, r.stderr
    known, _ = distill.load_lesson(central / "collider-simulator" / "lessons" / "madgraph-known.md")
    assert known.meta["support"] == 6
    assert known.meta["evidence"] == ["job:c1", "job:c2", "job:x"]
    assert known.meta["first_seen"] == "2026-08-01" and known.meta["last_confirmed"] == "2026-09-10"
    clash, _ = distill.load_lesson(central / "collider-simulator" / "lessons" / "madgraph-clash.md")
    assert clash.meta["symptom"] == "central clash symptom" and clash.meta["support"] == 2
    names = sorted(p.name for p in (central / "collider-simulator" / "lessons").glob("*.md"))
    assert names == ["madgraph-clash-2.md", "madgraph-clash.md", "madgraph-known.md"]
    assert (central / "event-analyzer" / "lessons" / "madanalysis-new.md").exists()
    assert (central / "event-analyzer" / "MEMORY.md").exists()
    assert other.exists()  # source untouched

    # warm-sandbox copy (evidence superset) -> max, not sum; lower-support subset never lowers
    warm = tmp_path / "warm" / "agent-memory"
    write_lesson(warm, "collider-simulator", "madgraph-known.md",
                 lesson_text(symptom="known symptom", support=7, evidence=("job:c1", "job:c2", "job:x", "job:w"),
                             first="2026-08-01", last="2026-09-15", fix="central fix"))
    assert run("import", "--from", warm, "--root", central).returncode == 0
    known, _ = distill.load_lesson(central / "collider-simulator" / "lessons" / "madgraph-known.md")
    assert known.meta["support"] == 7 and known.meta["last_confirmed"] == "2026-09-15"
    stale = tmp_path / "stale" / "agent-memory"
    write_lesson(stale, "collider-simulator", "madgraph-known.md",
                 lesson_text(symptom="known symptom", support=1, evidence=("job:c1",), fix="central fix"))
    assert run("import", "--from", stale, "--root", central).returncode == 0
    known, _ = distill.load_lesson(central / "collider-simulator" / "lessons" / "madgraph-known.md")
    assert known.meta["support"] == 7
    # importing the same source twice is idempotent
    assert run("import", "--from", warm, "--root", central).returncode == 0
    known, _ = distill.load_lesson(central / "collider-simulator" / "lessons" / "madgraph-known.md")
    assert known.meta["support"] == 7


def test_import_skips_invalid_source_files(tmp_path):
    central = tmp_path / "central"
    other = tmp_path / "other"
    write_lesson(other, "collider-simulator", "madgraph-bad.md", lesson_text(stage="bogus"))
    write_lesson(other, "collider-simulator", "madgraph-ok.md", lesson_text(symptom="ok"))
    r = run("import", "--from", other, "--root", central)
    assert r.returncode == 0, r.stderr
    assert "skipping invalid" in r.stderr
    assert (central / "collider-simulator" / "lessons" / "madgraph-ok.md").exists()
    assert not (central / "collider-simulator" / "lessons" / "madgraph-bad.md").exists()


# --------------------------------------------------------------------------- new
def test_new_writes_valid_lesson_and_index(tmp_path):
    r = run("new", "--root", tmp_path, "--agent", "collider-simulator", "--stage", "madgraph",
            "--blueprint", "madgraph-launch", "--symptom", "Job success=true but nevents=10000 instead of requested",
            "--root-cause", "set lines after the second done", "--fix", "keep set lines above the final done",
            "--evidence", "job:ca68f501890c2786", "--evidence", "progress/dy/step2_madgraph.md",
            "--generalizable", "--date", "2026-09-16")
    assert r.returncode == 0, r.stderr
    path = tmp_path / "collider-simulator" / "lessons" / "madgraph-job-success-true-but-nevents-10000-instead-of-requested.md"
    assert path.exists(), list((tmp_path / "collider-simulator" / "lessons").iterdir())
    les, warnings = distill.load_lesson(path)
    assert warnings == []
    assert les.meta["support"] == 1 and les.meta["generalizable"] is True
    assert les.meta["first_seen"] == les.meta["last_confirmed"] == "2026-09-16"
    assert les.meta["evidence"] == ["job:ca68f501890c2786", "progress/dy/step2_madgraph.md"]
    index = (tmp_path / "collider-simulator" / "MEMORY.md").read_text(encoding="utf-8")
    assert "[madgraph] Job success=true but nevents=10000 instead of requested → keep set lines above the final done (support 1, last 2026-09-16) [lessons/" in index
    # recording the same symptom again counts as a confirmation once rebuilt
    r2 = run("new", "--root", tmp_path, "--agent", "collider-simulator", "--stage", "madgraph",
             "--symptom", "job success=true but nevents=10000 instead of requested", "--root-cause", "same",
             "--fix", "same", "--evidence", "job:other", "--date", "2026-09-17")
    assert r2.returncode == 0, r2.stderr
    les, _ = distill.load_lesson(path)
    assert les.meta["support"] == 2 and les.meta["last_confirmed"] == "2026-09-17"
    assert len(list((tmp_path / "collider-simulator" / "lessons").glob("*.md"))) == 1


def test_help_and_flag_aliases(tmp_path):
    assert run("--help").returncode == 0
    for cmd in ("rebuild", "decay", "propose", "import", "new"):
        assert run(cmd, "--help").returncode == 0, cmd
    write_lesson(tmp_path, "a", "madgraph-x.md", lesson_text(support=3))
    assert run("--propose", "--root", tmp_path).returncode == 0


def test_import_repairs_extra_keys_and_long_symptom(tmp_path):
    """Files written in the harness auto-memory format (name/description/metadata) or with an over-long
    symptom are repaired on import instead of being skipped."""
    import subprocess, sys
    src = tmp_path / "sandbox_mem" / "model-generator" / "lessons"
    src.mkdir(parents=True)
    long_symptom = "generate-ufo " + "x" * 260
    (src / "drift.md").write_text(
        "---\n"
        "name: drift\n"
        "description: harness auto-memory style header\n"
        "metadata:\n"
        "  type: feedback\n"
        "stage: ufo\n"
        "blueprint: generate-ufo\n"
        f"symptom: \"{long_symptom}\"\n"
        "root_cause: \"flaky export\"\n"
        "fix: \"retry once\"\n"
        "evidence: [\"job:abc\"]\n"
        "generalizable: true\n"
        "support: 1\n"
        "first_seen: 2026-09-16\n"
        "last_confirmed: 2026-09-16\n"
        "---\n"
        "body line\n")
    root = tmp_path / "central"
    root.mkdir()
    r = subprocess.run([sys.executable, str(DISTILL), "import", "--from", str(tmp_path / "sandbox_mem"),
                        "--root", str(root)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr + r.stdout
    assert "repaired" in r.stderr and "1 added" in r.stdout
    imported = list((root / "model-generator" / "lessons").glob("*.md"))
    assert len(imported) == 1
    text = imported[0].read_text()
    assert "metadata" not in text.split("---")[1]
    assert "Full symptom: generate-ufo xxx" in text
    assert len(text.split("symptom: ")[1].split("\n")[0]) <= 205



def test_dedupe_merges_reworded_symptoms_and_route_moves_by_stage(tmp_path):
    """Four independent runs wrote the same Python-2 raise lesson in different words; rebuild must merge them
    into one lesson with support 4, and route must move a ufo-stage lesson written by collider-simulator
    into model-generator's store."""
    import subprocess, sys
    root = tmp_path / "mem"
    def lesson(agent, name, symptom, stage="ufo", blueprint="generate-ufo", extra=""):
        d = root / agent / "lessons"; d.mkdir(parents=True, exist_ok=True)
        (d / name).write_text(
            f"---\nstage: {stage}\nblueprint: {blueprint}\nsymptom: \"{symptom}\"\nroot_cause: \"FeynRules 2.3.49 emits Python 2 raise\"\n"
            f"fix: \"replace raise UFOError, msg with raise UFOError(msg)\"\nevidence: [\"job:{name}\"]\ngeneralizable: true\n"
            f"support: 1\nfirst_seen: 2026-09-16\nlast_confirmed: 2026-09-16\n{extra}---\nbody\n")
    lesson("model-generator", "a.md", "Python 2 raise UFOError, msg syntax in object_library.py causes SyntaxError on MG5 import")
    lesson("model-generator", "b.md", "object_library.py SyntaxError: raise UFOError, msg (Python 2 syntax)")
    lesson("model-generator", "c.md", "FeynRules 2.3.49 object_library.py contains Python 2 raise UFOError, msg syntax that breaks MG5 3.x import")
    lesson("collider-simulator", "d.md", "FeynRules 2.3.49 object_library.py has Python 2 raise UFOError syntax which breaks MG5 import", extra="contradictions: 1\n")
    lesson("collider-simulator", "e.md", "cut_decays default False skips lepton cuts on decay products", stage="madgraph", blueprint="madgraph-launch")
    r = subprocess.run([sys.executable, str(DISTILL), "route", "--root", str(root)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr + r.stdout
    assert "routed d.md: collider-simulator -> model-generator" in r.stdout
    files = sorted(p.name for p in (root / "model-generator" / "lessons").glob("*.md"))
    assert len(files) == 1, files  # a, b, c and the routed d merged into one lesson
    text = (root / "model-generator" / "lessons" / files[0]).read_text()
    assert "support: 4" in text and "contradictions: 1" in text
    index = (root / "model-generator" / "MEMORY.md").read_text()
    assert "support 4, contradicted 1" in index
    assert (root / "collider-simulator" / "lessons" / "e.md").is_file()  # madgraph lesson stays
    r = subprocess.run([sys.executable, str(DISTILL), "propose", "--root", str(root), "--min-support", "3"],
                       capture_output=True, text=True)
    assert "support   4" in r.stdout and "ufo-generator" in r.stdout
