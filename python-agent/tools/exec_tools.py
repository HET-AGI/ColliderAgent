"""
Code execution tools for the ADK agent: run a Python snippet or a shell command in the
working directory. Output is captured and truncated so it fits in the model context.
"""
import os
import subprocess
import sys
import time
import uuid
from typing import Any, Dict

MAX_OUTPUT_CHARS = 20000


def _truncate(text: str) -> str:
    if len(text) <= MAX_OUTPUT_CHARS:
        return text
    head = text[: MAX_OUTPUT_CHARS // 2]
    tail = text[-MAX_OUTPUT_CHARS // 2:]
    return f"{head}\n... [{len(text) - MAX_OUTPUT_CHARS} chars truncated] ...\n{tail}"


def run_shell(command: str, timeout_s: int = 900) -> Dict[str, Any]:
    """
    Run a shell command in the current working directory and return its output.

    Use it for file inspection (ls, grep, gunzip -c ... | head), unpacking downloads,
    and running scripts. Long jobs belong on Magnus, not here.

    Args:
        command: The bash command line to execute.
        timeout_s: Kill the command after this many seconds (default 900).

    Returns:
        dict: {"success": bool, "returncode": int, "stdout": str, "stderr": str,
               "elapsed_s": float, "message": str}
    """
    t0 = time.time()
    try:
        proc = subprocess.run(
            ["bash", "-lc", command], capture_output=True, text=True, timeout=timeout_s,
            cwd=os.getcwd(), env=os.environ.copy(),
        )
        return {
            "success": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": _truncate(proc.stdout),
            "stderr": _truncate(proc.stderr),
            "elapsed_s": round(time.time() - t0, 1),
            "message": "ok" if proc.returncode == 0 else f"exit code {proc.returncode}",
        }
    except subprocess.TimeoutExpired as e:
        return {
            "success": False, "returncode": -1,
            "stdout": _truncate((e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or "")),
            "stderr": _truncate((e.stderr or b"").decode() if isinstance(e.stderr, bytes) else (e.stderr or "")),
            "elapsed_s": round(time.time() - t0, 1),
            "message": f"timed out after {timeout_s}s",
        }
    except Exception as e:  # noqa: BLE001
        return {"success": False, "returncode": -1, "stdout": "", "stderr": str(e),
                "elapsed_s": round(time.time() - t0, 1), "message": f"failed to start: {e}"}


def run_python(code: str, timeout_s: int = 900) -> Dict[str, Any]:
    """
    Execute a Python snippet with the agent's interpreter (numpy, scipy, matplotlib, uproot,
    awkward, pyhf, pylhe, pyhepmc available) in the current working directory.

    Use it for post-processing of event files, cross-section tables, statistics and plots.
    Save figures to files (plt.savefig) — there is no display. Print what you need to see.

    Args:
        code: The Python source to run (a complete script, not an expression).
        timeout_s: Kill the script after this many seconds (default 900).

    Returns:
        dict: {"success": bool, "returncode": int, "stdout": str, "stderr": str,
               "script_path": str, "elapsed_s": float, "message": str}
    """
    scripts_dir = os.path.join(os.getcwd(), ".adk_scripts")
    os.makedirs(scripts_dir, exist_ok=True)
    path = os.path.join(scripts_dir, f"snippet_{time.strftime('%H%M%S')}_{uuid.uuid4().hex[:6]}.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    result = run_shell(f"{sys.executable} {path}", timeout_s=timeout_s)
    result["script_path"] = path
    return result
