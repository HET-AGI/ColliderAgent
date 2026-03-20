# tools/madgraph_tools.py
import json
import traceback
from typing import Any, Dict
from dotenv import load_dotenv; load_dotenv()
import magnus


__all__ = [
    "madgraph_compile",
    "madgraph_launch",
]


def madgraph_compile(
    ufo_model_path: str,
    process: str,
    target_path: str,
    definitions: str = "",
)-> Dict[str, Any]:
    """
    Compile a MadGraph5 process: enumerate Feynman diagrams, compute matrix
    elements, and produce a compiled process directory ready for event generation.

    Args:
        ufo_model_path: Path to the UFO model directory (from FeynRules/UFO
            generation). This directory is uploaded to the cloud for compilation.
        process: Process definition, one per line.
            First line becomes `generate`, the rest become `add process`.
            Example: "p p > t t~\\np p > t t~ j"
        target_path: Where to download the compiled process directory
            (e.g., "tmp/pp_ttbar").
        definitions: Multiparticle definitions, one per line (without the
            `define` keyword). Example: "l+ = e+ mu+\\nl- = e- mu-"

    Returns:
        dict with keys:
            - success (bool): Whether compilation succeeded
            - process_dir (str): Path to compiled process directory (if success)
            - message (str): Human-readable status message

    Example:
        >>> result = madgraph_compile(
        ...     ufo_model_path="tools/assets/NP_S_UFO",
        ...     process="p p > t t~",
        ...     target_path="tmp/pp_ttbar",
        ... )
        >>> if result["success"]:
        ...     print(f"Process directory at: {result['process_dir']}")
    """

    try:
        args = {
            "ufo": ufo_model_path,
            "process": process,
            "output": target_path,
        }
        if definitions:
            args["definitions"] = definitions

        result = magnus.run_blueprint("madgraph-compile", args=args)
        assert result is not None
        return json.loads(result)
    except:
        return {
            "success": False,
            "error": traceback.format_exc(),
        }


def madgraph_launch(
    process_dir: str,
    launch_commands: str,
    target_path: str,
    pdf_set: str = "",
)-> Dict[str, Any]:
    """
    Launch MadGraph5 event generation on a compiled process directory.

    Takes the process directory produced by madgraph_compile(), runs Monte
    Carlo event generation with the specified settings, and returns the
    output directory containing the generated events.

    Args:
        process_dir: Path to the compiled process directory (from
            madgraph_compile). This directory is uploaded for execution.
        launch_commands: MG5 launch body — everything after `launch <dir>`.
            MG5 processes this as a state machine:
              1. shower/detector? → setting lines or `done` to skip
              2. edit cards? → `done` to skip, enters parameter-setting mode
              3. `set` commands for parameters
              4. `done` to start the run
            **NEVER** put two consecutive `done` before `set` commands —
            the second `done` ends parameter editing and starts the run.
            Parton-level example:
                "done\\nset nevents 1000\\nset ebeam1 7000\\ndone"
            With Pythia8+Delphes example:
                "shower=Pythia8\\ndetector=Delphes\\ndone\\nCMS\\ndone\\n"
                "set nevents 1000\\nset ebeam1 7000\\ndone"
        target_path: Where to download the output directory (process dir
            with generated events in Events/run_XX/).
        pdf_set: LHAPDF PDF set name to install before running MG5
            (e.g. "LUXlep-NNPDF31_nlo_as_0118_luxqed"). Downloaded from
            CERN if not already present. Leave empty to skip.

    Returns:
        dict with keys:
            - success (bool): Whether event generation succeeded
            - output_dir (str): Path to output directory (if success)
            - message (str): Human-readable status message

    Example:
        >>> result = madgraph_launch(
        ...     process_dir="tmp/pp_ttbar",
        ...     launch_commands="done\\nset nevents 1000\\nset ebeam1 7000\\nset ebeam2 7000\\ndone",
        ...     target_path="tmp/pp_ttbar",
        ... )
        >>> if result["success"]:
        ...     print(f"Events at: {result['output_dir']}/Events/")
    """

    try:
        args = {
            "process": process_dir,
            "commands": launch_commands,
            "output": target_path,
        }
        if pdf_set:
            args["pdf"] = pdf_set

        result = magnus.run_blueprint("madgraph-launch", args=args)
        assert result is not None
        return json.loads(result)
    except:
        return {
            "success": False,
            "error": traceback.format_exc(),
        }
