"""
YAML-Based Simulation Workflow for Collider Agent

Provides two high-level tools:
1. generate_simulation_yaml() - Create/append simulation YAML configuration
2. run_from_yaml() - Execute MadGraph5 simulation from YAML configuration

The YAML format is compatible with the Workflow-Example project's simulation.yaml schema.

Usage:
    # Step 1: Generate configuration
    result = generate_simulation_yaml(
        yaml_path="simulation.yaml",
        process_name="pp_to_tt",
        model="sm",
        processes=["p p > t t~"],
        output_dir="outputs/pp_to_tt",
    )

    # Step 2: Run simulation
    result = run_from_yaml(
        yaml_path="simulation.yaml",
        process_name="pp_to_tt",
    )
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

import yaml

from .madgraph_tools import madgraph_compile, madgraph_launch


__all__ = [
    "generate_simulation_yaml",
    "run_from_yaml",
]


logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Environment-driven defaults
# ---------------------------------------------------------------------------

def _env_float(key: str, default: float) -> float:
    val = os.environ.get(key)
    return float(val) if val else default

def _env_int(key: str, default: int) -> int:
    val = os.environ.get(key)
    return int(val) if val else default

DEFAULT_RUN_SETTINGS = {
    "shower": "OFF",
    "detector": "OFF",
    "analysis": "OFF",
    "nevents": _env_int("DEFAULT_NEVENTS", 10000),
}

DEFAULT_PHYSICS_PARAMS = {
    "ebeam1": _env_float("DEFAULT_EBEAM1", 6500.0),
    "ebeam2": _env_float("DEFAULT_EBEAM2", 6500.0),
}


# ---------------------------------------------------------------------------
# Tool 1: generate_simulation_yaml
# ---------------------------------------------------------------------------

def generate_simulation_yaml(
    yaml_path: str,
    process_name: str,
    model: str,
    processes: List[str],
    output_dir: str,
    event_set_name: str = "14TeV",
    definitions: Optional[List[str]] = None,
    run_settings: Optional[Dict[str, Any]] = None,
    physics_params: Optional[Dict[str, Any]] = None,
    model_params: Optional[Dict[str, Any]] = None,
    scan_params: Optional[Dict[str, Any]] = None,
    extra_commands: Optional[List[str]] = None,
    card: Optional[Dict[str, Any]] = None,
    append: bool = False,
) -> Dict[str, Any]:
    """
    Generate a simulation YAML configuration file compatible with the
    Workflow-Example simulation.yaml schema.

    Args:
        yaml_path: Path to write the YAML file
        process_name: Name for the process block (e.g. "pp_to_tt")
        model: Model name ("sm", "mssm") or UFO model path
        processes: List of MG5 process strings (e.g. ["p p > t t~"])
        output_dir: Output directory for MadGraph results
        event_set_name: Label for this event set (default "14TeV")
        definitions: Multi-particle definitions (e.g. ["p = p b b~"])
        run_settings: Dict with shower/detector/analysis/nevents settings
        physics_params: Dict with beam energies, masses, etc.
        model_params: Dict with BSM param_card parameters
        scan_params: Dict with parameter scan ranges (e.g. {"mH0": [20,40,60]})
        extra_commands: Additional MG5 commands to append
        card: Dict with card paths (e.g. {"delphes": "path/to/card.dat"})
        append: If True and file exists, append new process to existing YAML

    Returns:
        dict: {"success": bool, "yaml_path": str, "process_name": str, "message": str}
    """
    try:
        # Build the event set configuration
        config = {
            "model": model,
            "processes": list(processes),
            "output_dir": output_dir,
            "run_settings": {**DEFAULT_RUN_SETTINGS, **(run_settings or {})},
            "physics_params": {**DEFAULT_PHYSICS_PARAMS, **(physics_params or {})},
            "model_params": dict(model_params) if model_params else {},
            "scan_params": dict(scan_params) if scan_params else {},
            "extra_commands": list(extra_commands) if extra_commands else [],
        }

        if definitions:
            config["definitions"] = list(definitions)

        if card:
            config["card"] = dict(card)

        # Build the process entry in list-of-single-key-dicts format
        event_set_entry = {event_set_name: config}

        # Load existing or create new YAML data
        yaml_file = Path(yaml_path)
        data = {}

        if append and yaml_file.exists():
            with open(yaml_file, "r") as f:
                data = yaml.safe_load(f) or {}

        # Add/update the process
        if process_name in data and isinstance(data[process_name], list):
            # Check if event_set_name already exists - replace if so
            replaced = False
            for i, entry in enumerate(data[process_name]):
                if isinstance(entry, dict) and event_set_name in entry:
                    data[process_name][i] = event_set_entry
                    replaced = True
                    break
            if not replaced:
                data[process_name].append(event_set_entry)
        else:
            data[process_name] = [event_set_entry]

        # Write YAML
        yaml_file.parent.mkdir(parents=True, exist_ok=True)
        with open(yaml_file, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

        msg = f"YAML configuration written to {yaml_path} (process: {process_name}/{event_set_name})"
        logger.info(msg)
        return {
            "success": True,
            "yaml_path": str(yaml_file.resolve()),
            "process_name": process_name,
            "message": msg,
        }

    except Exception as e:
        msg = f"Failed to generate YAML: {e}"
        logger.error(msg, exc_info=True)
        return {
            "success": False,
            "yaml_path": yaml_path,
            "process_name": process_name,
            "message": msg,
        }


# ---------------------------------------------------------------------------
# Tool 2: run_from_yaml
# ---------------------------------------------------------------------------

def run_from_yaml(
    yaml_path: str,
    process_name: str,
    event_set_name: str = "14TeV",
    nevents: Optional[int] = None,
    mode: str = "auto",
) -> Dict[str, Any]:
    """
    Run a MadGraph5 simulation from a YAML configuration file.

    The YAML file should follow the Workflow-Example simulation.yaml schema.
    This function reads the configuration, calls madgraph_compile() to compile
    the process, then calls madgraph_launch() to generate events.

    Args:
        yaml_path: Path to the simulation YAML file
        process_name: Which process block to run (e.g. "pp_to_tt")
        event_set_name: Which event set within the process (default "14TeV")
        nevents: Override number of events (optional)
        mode: "auto" (detect first-run vs add-events), "first_run", or "add_events"

    Returns:
        dict: {"success": bool, "output_dir": str, "message": str}
    """
    result = {
        "success": False,
        "output_dir": "",
        "message": "",
    }

    try:
        # 1. Load & validate YAML
        config = _load_config(yaml_path, process_name, event_set_name)
        _validate_config(config)

        # Resolve output_dir to absolute path
        output_dir = str(Path(config["output_dir"]).resolve())
        result["output_dir"] = output_dir

        # Override nevents if provided
        if nevents is not None:
            config.setdefault("run_settings", {})["nevents"] = nevents

        # 2. Determine run mode
        if mode == "auto":
            mode = "add_events" if not _is_first_run(output_dir) else "first_run"

        logger.info(f"Running {process_name}/{event_set_name} in mode={mode}")

        # 3. Execute based on mode
        if mode == "first_run":
            # Step A: Compile (import/generate/output)
            _, ufo_path = _resolve_model(config["model"])
            processes_str = "\n".join(config["processes"])
            definitions_str = "\n".join(config.get("definitions", []))

            compile_result = madgraph_compile(
                ufo_model_path = ufo_path,
                process = processes_str,
                target_path = output_dir,
                definitions = definitions_str,
            )

            if not compile_result.get("success"):
                result["message"] = f"Compile phase failed: {compile_result.get('message', '')}"
                return result

            # Step B: Launch (set params, shower, detector, etc.)
            launch_commands = _build_launch_commands(config)

            launch_result = madgraph_launch(
                process_dir = output_dir,
                launch_commands = launch_commands,
                target_path = output_dir,
            )

            if not launch_result.get("success"):
                result["message"] = f"Launch phase failed: {launch_result.get('message', '')}"
                return result

        elif mode == "add_events":
            # Only launch (process dir already exists)
            launch_commands = _build_launch_commands(config)

            launch_result = madgraph_launch(
                process_dir = output_dir,
                launch_commands = launch_commands,
                target_path = output_dir,
            )

            if not launch_result.get("success"):
                result["message"] = f"Add-events phase failed: {launch_result.get('message', '')}"
                return result

        else:
            result["message"] = f"Unknown mode: {mode}. Use 'auto', 'first_run', or 'add_events'."
            return result

        result["success"] = True
        result["message"] = (
            f"Simulation completed for {process_name}/{event_set_name}. "
            f"Output: {output_dir}"
        )
        logger.info(result["message"])
        return result

    except Exception as e:
        result["message"] = f"Simulation error: {e}"
        logger.error(result["message"], exc_info=True)
        return result


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _load_config(
    yaml_path: str, process_name: str, event_set_name: str
) -> Dict[str, Any]:
    """Load and extract a specific event set configuration from YAML."""
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)

    if not data or process_name not in data:
        raise ValueError(
            f"Process '{process_name}' not found in {yaml_path}. "
            f"Available: {list(data.keys()) if data else []}"
        )

    process_block = data[process_name]
    if not isinstance(process_block, list):
        raise ValueError(
            f"Process '{process_name}' should be a list of event set dicts, "
            f"got {type(process_block).__name__}"
        )

    # Find the matching event set
    for entry in process_block:
        if isinstance(entry, dict) and event_set_name in entry:
            return entry[event_set_name]

    available = []
    for entry in process_block:
        if isinstance(entry, dict):
            available.extend(entry.keys())

    raise ValueError(
        f"Event set '{event_set_name}' not found in process '{process_name}'. "
        f"Available: {available}"
    )


def _validate_config(config: Dict[str, Any]) -> None:
    """Validate required fields in event set configuration."""
    required = ["model", "processes", "output_dir"]
    missing = [k for k in required if k not in config]
    if missing:
        raise ValueError(f"Missing required config fields: {missing}")

    if not config["processes"]:
        raise ValueError("'processes' list cannot be empty")


def _resolve_model(model: str):
    """Determine if model is a built-in name or a UFO path.

    Returns (model_name, ufo_model_path):
        - Built-in: ("sm", None)
        - UFO path: ("sm", "/path/to/UFO")  # model_name is ignored when ufo_path is set
    """
    if "/" not in model and "\\" not in model:
        return model, None
    # It's a path — resolve relative paths
    p = Path(model)
    if not p.is_absolute():
        p = p.resolve()
    return "sm", str(p)


def _is_first_run(output_dir: str) -> bool:
    """Check if this is the first run (no Events/run_* directories)."""
    events_dir = Path(output_dir) / "Events"
    if not events_dir.exists():
        return True
    run_dirs = list(events_dir.glob("run_*"))
    return len(run_dirs) == 0


def _build_launch_commands(config: Dict[str, Any]) -> str:
    """Build MG5 launch body: shower/detector settings, params, done markers.

    Returns everything that goes AFTER `launch <dir>` — the cloud script
    prepends the `launch` command itself.
    """
    lines = []

    run_settings = config.get("run_settings", {})
    physics_params = config.get("physics_params", {})
    model_params = config.get("model_params", {})
    scan_params = config.get("scan_params", {})
    extra_commands = config.get("extra_commands", [])
    card = config.get("card", {})

    # Shower / detector / analysis switches
    for key in ("shower", "detector", "analysis"):
        if key in run_settings:
            val = run_settings[key]
            lines.append(f"{key}={val}")

    # Done with switch selection
    lines.append("done")

    # Delphes card selection (between first and second done)
    if card.get("delphes"):
        lines.append(str(card["delphes"]))
        lines.append("done")

    # Physics params (run_card): set <param> <value>
    for param, value in physics_params.items():
        lines.append(f"set {param} {value}")

    # nevents from run_settings
    if "nevents" in run_settings:
        lines.append(f"set nevents {run_settings['nevents']}")

    # Model params (param_card): set param_card <param> <value>
    for param, value in model_params.items():
        lines.append(f"set param_card {param} {value}")

    # Scan params: set param_card <param> scan:[v1,v2,...]
    for param, values in scan_params.items():
        scan_str = "scan:[" + ",".join(str(v) for v in values) + "]"
        lines.append(f"set param_card {param} {scan_str}")

    # Extra commands
    for cmd in extra_commands:
        lines.append(cmd)

    # Final done to start the run
    lines.append("done")

    return "\n".join(lines) + "\n"
