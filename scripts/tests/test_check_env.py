import json
import subprocess
import sys
from pathlib import Path

CHECK = Path(__file__).resolve().parents[1] / "check_env.py"


def test_check_env_json_lists_required_modules():
    r = subprocess.run([sys.executable, str(CHECK), "--json"], capture_output=True, text=True)
    data = json.loads(r.stdout)
    items = {row["item"]: row for row in data["rows"]}
    for m in ("numpy", "scipy", "matplotlib", "uproot", "awkward", "pyhf", "pylhe", "pyhepmc", "magnus"):
        assert m in items and items[m]["required"]
    assert r.returncode == (0 if data["ok"] else 1)
