"""Root conftest.py for pytest.

Pre-registers 'tools' package to prevent pytest from importing the root
__init__.py (which does `from . import agent` and fails outside package context).
"""
import sys
import importlib.util
from pathlib import Path

_tools_dir = Path(__file__).parent / "tools"

if "tools" not in sys.modules:
    spec = importlib.util.spec_from_file_location(
        "tools",
        str(_tools_dir / "__init__.py"),
        submodule_search_locations=[str(_tools_dir)],
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["tools"] = mod

    for name in ["file_tools", "mcp_mma", "feynrules_tools", "madgraph_tools", "simulation_workflow"]:
        sub_path = _tools_dir / f"{name}.py"
        if sub_path.exists():
            sub_spec = importlib.util.spec_from_file_location(
                f"tools.{name}", str(sub_path)
            )
            sub_mod = importlib.util.module_from_spec(sub_spec)
            sys.modules[f"tools.{name}"] = sub_mod
            sub_spec.loader.exec_module(sub_mod)

collect_ignore = ["__init__.py", "agent.py", "py.py"]
