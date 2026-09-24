"""Tests for the deterministic FeynRules/UFO helpers shipped inside the skills."""
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
UFO_FIX = REPO / "src/skills/ufo-generator/scripts/ufo_fix.py"
FR_LINT = REPO / "src/skills/feynrules-model-generator/scripts/fr_lint.py"


def run(script, *args):
    return subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True)


def make_ufo(tmp_path, raise_py2=True, leak=False, empty_lorentz=False):
    ufo = tmp_path / "X_UFO"
    ufo.mkdir()
    ol = "class UFOError(Exception):\n    pass\n\ndef f(x):\n    if x:\n        raise UFOError, \"bad\"\n    return 1\n"
    if not raise_py2:
        ol = ol.replace('raise UFOError, "bad"', 'raise UFOError("bad")')
    (ufo / "object_library.py").write_text(ol)
    (ufo / "couplings.py").write_text("GC_1 = Coupling(name='GC_1', value='-(ee*complex(0,1))', order={'QED':1})\n"
                                      + ("GC_2 = Coupling(name='GC_2', value='CreateObjectParticleName[PartNameMG[Wi]]', order={'NP':1})\n" if leak else ""))
    (ufo / "lorentz.py").write_text("" if empty_lorentz else "FFV1 = Lorentz(name='FFV1', spins=[2,2,3], structure='Gamma(3,2,1)')\n")
    (ufo / "vertices.py").write_text("V_1 = Vertex(name='V_1', particles=[], color=['1'], lorentz=[L.FFV1], couplings={(0,0):C.GC_1})\n")
    return ufo


def test_ufo_fix_repairs_python2_raise_and_reports_clean(tmp_path):
    ufo = make_ufo(tmp_path)
    r = run(UFO_FIX, str(ufo), "--check")
    assert r.returncode == 1 and "Python-2 raise" in r.stdout
    r = run(UFO_FIX, str(ufo))
    assert r.returncode == 0, r.stdout
    assert 'raise UFOError("bad")' in (ufo / "object_library.py").read_text()
    assert run(UFO_FIX, str(ufo), "--check").returncode == 0


def test_ufo_fix_reports_mathematica_leak_and_empty_lorentz(tmp_path):
    ufo = make_ufo(tmp_path, raise_py2=False, leak=True, empty_lorentz=True)
    r = run(UFO_FIX, str(ufo))
    assert r.returncode == 1
    assert "CreateObjectParticleName" in r.stdout and "no Lorentz structure" in r.stdout


def test_fr_lint_flags_token_fsd_and_short_classname(tmp_path):
    fr = tmp_path / "m.fr"
    fr.write_text("(* uses M$GaugeGroups in a comment *)\nM$ClassesDescription = { S[100] == { ClassName -> a, Width -> 0 } };\n"
                  "L1 := FSD[B, mu, nu] * FS[B, mu, nu];\n")
    r = run(FR_LINT, str(fr))
    assert r.returncode == 1
    assert "E1" in r.stdout and "E2" in r.stdout and "E3" in r.stdout and "W2" in r.stdout
    assert run(FR_LINT, str(fr), "--standalone").stdout.count("E1") == 0


def test_fr_lint_clean_file_passes(tmp_path):
    fr = tmp_path / "m.fr"
    fr.write_text("M$ClassesDescription = { V[100] == { ClassName -> Zp, Width -> {WZp, 1.0} } };\n"
                  "LNPtmp := Block[{mu}, gzp * Zp[mu] * ebar.Ga[mu].e];\nLNP := LNPtmp + HC[LNPtmp]; (* + h.c. *)\n")
    r = run(FR_LINT, str(fr))
    assert r.returncode == 0, r.stdout
