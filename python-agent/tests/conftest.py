"""Pytest configuration for collider-agent tests.

Pre-registers the 'tools' package via importlib to avoid the root __init__.py
(which does `from . import agent`) being triggered during test collection.
"""
import sys
import importlib.util
from pathlib import Path

_project_root = Path(__file__).parent.parent
_tools_dir = _project_root / "tools"

# Register 'tools' as a proper package before any test imports happen
if "tools" not in sys.modules:
    spec = importlib.util.spec_from_file_location(
        "tools",
        str(_tools_dir / "__init__.py"),
        submodule_search_locations=[str(_tools_dir)],
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["tools"] = mod

    # Pre-register submodules that simulation_workflow depends on
    for name in ["file_tools", "mcp_mma", "feynrules_tools", "madgraph_tools", "simulation_workflow"]:
        sub_path = _tools_dir / f"{name}.py"
        if sub_path.exists():
            sub_spec = importlib.util.spec_from_file_location(
                f"tools.{name}", str(sub_path)
            )
            sub_mod = importlib.util.module_from_spec(sub_spec)
            sys.modules[f"tools.{name}"] = sub_mod
            sub_spec.loader.exec_module(sub_mod)
