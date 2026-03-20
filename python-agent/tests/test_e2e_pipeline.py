#!/usr/bin/env python3
"""
End-to-end pipeline test: Natural Language → .fr → UFO → simulation.yaml → MadGraph5 files

This script tests the complete pipeline by calling each tool function directly,
logging every step's input/output for debugging.

Usage:
    python tests/test_e2e_pipeline.py 2>&1 | tee e2e_test.log
"""

import os
import sys
import json
import time
import shutil
import logging
from pathlib import Path

# Setup project root
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load environment
from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

# Setup logging
LOG_FILE = PROJECT_ROOT / "e2e_test.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("e2e_test")

# Import tools
from tools.file_tools import write, read
from tools.feynrules_to_ufo import generate_ufo_model
from tools.simulation_yaml_to_madgraph import generate_simulation_yaml, run_from_yaml
from tools.madgraph_tools import connect_to_madgraph


def banner(title: str):
    logger.info("")
    logger.info("=" * 80)
    logger.info(f"  {title}")
    logger.info("=" * 80)


def log_result(result: dict, max_stdout: int = 2000):
    """Pretty-print a tool result dict."""
    for k, v in result.items():
        if k in ("stdout", "stderr") and isinstance(v, str) and len(v) > max_stdout:
            logger.info(f"  {k}: ({len(v)} chars) ...last {max_stdout} chars...")
            logger.info(f"  {v[-max_stdout:]}")
        else:
            logger.info(f"  {k}: {v}")


# ============================================================================
# Test configuration
# ============================================================================
TEST_DIR = PROJECT_ROOT / "outputs" / "e2e_test"
FR_FILE = TEST_DIR / "ScalarLepton.fr"
UFO_NAME = "ScalarLepton_UFO"
YAML_PATH = TEST_DIR / "simulation.yaml"
PROCESS_NAME = "pp_to_ScaSca"
OUTPUT_DIR = TEST_DIR / "mg5_output"


# ============================================================================
# PHASE 1: Write the .fr model file (simulating agent's .fr generation)
# ============================================================================
def phase1_write_fr():
    """Write a simple BSM .fr file: scalar S coupled to leptons."""
    banner("PHASE 1: Generate FeynRules .fr Model File")

    # This is what the LLM agent would generate from natural language input like:
    # "Add a neutral scalar S with mass MS and Yukawa coupling yS to muons: L = -yS * S * mubar * mu"
    fr_content = r"""(* ============================================== *)
(* ScalarLepton Model                              *)
(* A simple neutral scalar S coupled to muons      *)
(* Lagrangian: L_NP = - yS S mubar mu              *)
(* ============================================== *)

M$ModelName = "ScalarLepton";

M$Information = {
  Authors      -> {"E2E Test"},
  Version      -> "1.0",
  Date         -> "2026-02-09",
  Institutions -> {"Test"},
  Emails       -> {"test@test.com"}
};

M$ClassesDescription = {

  (* New scalar particle S: neutral, color singlet *)
  S[100] == {
    ClassName        -> Sca,
    SelfConjugate    -> True,
    Mass             -> {MSca, 200.0},
    Width            -> {WSca, 1.0},
    PropagatorLabel  -> "Sca",
    PropagatorType   -> D,
    PropagatorArrow  -> None,
    ParticleName     -> "Sca",
    PDG              -> 9000001,
    FullName         -> "ScalarMediator"
  }
};

M$Parameters = {

  (* External: Yukawa coupling *)
  ySmu == {
    ParameterType    -> External,
    BlockName        -> NPINPUTS,
    OrderBlock       -> 1,
    Value            -> 0.1,
    InteractionOrder -> {NP, 1},
    TeX              -> Subscript[y, S\[Mu]],
    Description      -> "Scalar-muon Yukawa coupling"
  }
};

(* ============================================== *)
(* New Physics Lagrangian                          *)
(* L_NP = - ySmu * Sca * (mubar.mu)               *)
(* ============================================== *)

LSNP := - ySmu Sca mubar[sp1].mu[sp2] IndexDelta[sp1, sp2];
"""

    logger.info(f"Writing .fr file to: {FR_FILE}")
    logger.info(f"Natural language input (simulated):")
    logger.info(f'  "Add a neutral scalar S (mass=200 GeV) with Yukawa coupling yS=0.1 to muons"')
    logger.info(f'  L_NP = - yS * S * mubar * mu')
    logger.info(f"")

    # Use the write tool (same as agent would)
    result = write(str(FR_FILE), fr_content)
    log_result(result)

    # Verify file was created
    verify = read(str(FR_FILE))
    lines = verify.get("content", "").count("\n")
    logger.info(f"Verification: file has {lines} lines, {verify.get('size', 0)} bytes")

    return result.get("success", False)


# ============================================================================
# PHASE 2: Generate UFO model from .fr file
# ============================================================================
def phase2_generate_ufo():
    """Generate UFO model using generate_ufo_model tool."""
    banner("PHASE 2: Generate UFO Model (FeynRules → UFO)")

    # The path must be relative to project root for generate_ufo_model
    fr_rel_path = str(FR_FILE.relative_to(PROJECT_ROOT))
    logger.info(f"Input .fr file: {fr_rel_path}")
    logger.info(f"Lagrangian symbol: LSNP")
    logger.info(f"UFO output name: {UFO_NAME}")
    logger.info(f"")

    t0 = time.time()
    result = generate_ufo_model(
        fr_model_path=fr_rel_path,
        lagrangian="LSNP",
        ufo_output_name=UFO_NAME,
        timeout=300,
    )
    elapsed = time.time() - t0

    logger.info(f"Elapsed: {elapsed:.1f}s")
    log_result(result)

    if result.get("success"):
        ufo_path = result["ufo_path"]
        logger.info(f"UFO model generated at: {ufo_path}")
        # List UFO contents
        ufo_dir = Path(ufo_path)
        if ufo_dir.exists():
            for f in sorted(ufo_dir.iterdir()):
                logger.info(f"  {f.name} ({f.stat().st_size} bytes)")
    else:
        logger.warning(f"UFO generation failed (wolframscript may not be available)")
        logger.warning(f"Will fall back to SM model for remaining phases")

    return result


# ============================================================================
# PHASE 3: Generate simulation.yaml
# ============================================================================
def phase3_generate_yaml(model_path: str):
    """Generate simulation.yaml from the UFO model (or SM fallback)."""
    banner("PHASE 3: Generate simulation.yaml")

    logger.info(f"Model path: {model_path}")
    logger.info(f"Process: p p > mu+ mu- (Drell-Yan like)")
    logger.info(f"YAML output: {YAML_PATH}")
    logger.info(f"")

    # Determine process based on model
    if model_path == "sm":
        processes = ["p p > mu+ mu-"]
        model_params = {}
    else:
        processes = ["p p > Sca Sca"]  # Pair production of the new scalar
        model_params = {"MSca": 200.0, "ySmu": 0.1}

    result = generate_simulation_yaml(
        yaml_path=str(YAML_PATH),
        process_name=PROCESS_NAME,
        model=model_path,
        processes=processes,
        output_dir=str(OUTPUT_DIR),
        event_set_name="13TeV",
        run_settings={
            "shower": "OFF",
            "detector": "OFF",
            "analysis": "OFF",
            "nevents": 100,  # Small number for quick test
        },
        physics_params={
            "ebeam1": 6500.0,
            "ebeam2": 6500.0,
        },
        model_params=model_params,
    )

    log_result(result)

    if result.get("success"):
        # Show the generated YAML
        logger.info(f"")
        logger.info(f"Generated YAML content:")
        logger.info(f"-" * 40)
        yaml_read = read(str(YAML_PATH))
        logger.info(yaml_read.get("content", ""))
        logger.info(f"-" * 40)

    return result.get("success", False)


# ============================================================================
# PHASE 4: Run MadGraph5 from simulation.yaml
# ============================================================================
def phase4_run_madgraph():
    """Run MadGraph5 simulation from YAML configuration."""
    banner("PHASE 4: Run MadGraph5 Simulation (simulation.yaml → Events)")

    logger.info(f"YAML path: {YAML_PATH}")
    logger.info(f"Process name: {PROCESS_NAME}")
    logger.info(f"Event set: 13TeV")
    logger.info(f"Mode: first_run")
    logger.info(f"")

    t0 = time.time()
    result = run_from_yaml(
        yaml_path=str(YAML_PATH),
        process_name=PROCESS_NAME,
        event_set_name="13TeV",
        mode="first_run",
        timeout=600,
    )
    elapsed = time.time() - t0

    logger.info(f"Elapsed: {elapsed:.1f}s")
    log_result(result)

    return result


# ============================================================================
# PHASE 5: Verify output files
# ============================================================================
def phase5_verify_outputs(mg5_result: dict):
    """Verify MadGraph5 generated the expected output files."""
    banner("PHASE 5: Verify Output Files")

    output_dir = Path(mg5_result.get("output_dir", str(OUTPUT_DIR)))
    logger.info(f"Checking output directory: {output_dir}")

    if not output_dir.exists():
        logger.error(f"Output directory does not exist!")
        return False

    # Check directory structure
    expected_items = ["Cards", "SubProcesses", "Events", "HTML"]
    for item in expected_items:
        path = output_dir / item
        exists = path.exists()
        status = "OK" if exists else "MISSING"
        logger.info(f"  [{status}] {item}/")

    # Check Cards
    cards_dir = output_dir / "Cards"
    if cards_dir.exists():
        logger.info(f"")
        logger.info(f"Cards directory contents:")
        for f in sorted(cards_dir.iterdir()):
            if f.is_file():
                logger.info(f"  {f.name} ({f.stat().st_size} bytes)")

    # Check Events
    events_dir = output_dir / "Events"
    if events_dir.exists():
        logger.info(f"")
        logger.info(f"Events directory contents:")
        for run_dir in sorted(events_dir.iterdir()):
            if run_dir.is_dir():
                logger.info(f"  {run_dir.name}/")
                for f in sorted(run_dir.iterdir()):
                    logger.info(f"    {f.name} ({f.stat().st_size} bytes)")

        # Find LHE file
        lhe_files = list(events_dir.glob("run_*/unweighted_events.lhe*"))
        if lhe_files:
            logger.info(f"")
            logger.info(f"SUCCESS: Found event files:")
            for lhe in lhe_files:
                logger.info(f"  {lhe}")
            return True
        else:
            logger.warning(f"No LHE event files found")
    else:
        logger.warning(f"Events directory not found")

    return False


# ============================================================================
# Main
# ============================================================================
def main():
    banner("COLLIDER-AGENT END-TO-END PIPELINE TEST")
    logger.info(f"Project root: {PROJECT_ROOT}")
    logger.info(f"Test directory: {TEST_DIR}")
    logger.info(f"Log file: {LOG_FILE}")
    logger.info(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"")
    logger.info(f"MG5_PATH: {os.environ.get('MG5_PATH', 'NOT SET')}")
    logger.info(f"wolframscript: {shutil.which('wolframscript') or 'NOT FOUND'}")

    # Clean up previous test
    if TEST_DIR.exists():
        logger.info(f"Cleaning previous test directory: {TEST_DIR}")
        shutil.rmtree(TEST_DIR)
    TEST_DIR.mkdir(parents=True, exist_ok=True)

    results = {}
    overall_success = True

    # --- Phase 1: Write .fr ---
    try:
        results["phase1"] = phase1_write_fr()
    except Exception as e:
        logger.error(f"Phase 1 EXCEPTION: {e}", exc_info=True)
        results["phase1"] = False
        overall_success = False

    if not results["phase1"]:
        logger.error("Phase 1 failed, cannot continue")
        return

    # --- Phase 2: Generate UFO ---
    ufo_result = None
    try:
        ufo_result = phase2_generate_ufo()
        results["phase2"] = ufo_result.get("success", False)
    except Exception as e:
        logger.error(f"Phase 2 EXCEPTION: {e}", exc_info=True)
        results["phase2"] = False

    # Determine model path for remaining phases
    if results["phase2"] and ufo_result and ufo_result.get("ufo_path"):
        model_path = ufo_result["ufo_path"]
        logger.info(f"Using generated UFO model: {model_path}")
    else:
        model_path = "sm"
        logger.info(f"Falling back to SM model for pipeline test")

    # --- Phase 3: Generate YAML ---
    try:
        results["phase3"] = phase3_generate_yaml(model_path)
    except Exception as e:
        logger.error(f"Phase 3 EXCEPTION: {e}", exc_info=True)
        results["phase3"] = False
        overall_success = False

    if not results["phase3"]:
        logger.error("Phase 3 failed, cannot continue to MadGraph")
        return

    # --- Phase 4: Run MadGraph ---
    mg5_result = None
    try:
        mg5_result = phase4_run_madgraph()
        results["phase4"] = mg5_result.get("success", False)
    except Exception as e:
        logger.error(f"Phase 4 EXCEPTION: {e}", exc_info=True)
        results["phase4"] = False

    # --- Phase 5: Verify outputs ---
    if mg5_result:
        try:
            results["phase5"] = phase5_verify_outputs(mg5_result)
        except Exception as e:
            logger.error(f"Phase 5 EXCEPTION: {e}", exc_info=True)
            results["phase5"] = False
    else:
        results["phase5"] = False

    # --- Summary ---
    banner("TEST SUMMARY")
    phase_names = {
        "phase1": "Write .fr model file",
        "phase2": "Generate UFO model (wolframscript)",
        "phase3": "Generate simulation.yaml",
        "phase4": "Run MadGraph5 simulation",
        "phase5": "Verify output files",
    }
    for phase, passed in results.items():
        status = "PASS" if passed else "FAIL"
        logger.info(f"  [{status}] {phase_names.get(phase, phase)}")

    logger.info(f"")
    if all(results.values()):
        logger.info(f"  OVERALL: ALL PHASES PASSED")
    elif results.get("phase4") and results.get("phase5"):
        logger.info(f"  OVERALL: PIPELINE WORKS (some optional steps skipped)")
    else:
        failed = [k for k, v in results.items() if not v]
        logger.info(f"  OVERALL: FAILED phases: {failed}")

    logger.info(f"")
    logger.info(f"Full log saved to: {LOG_FILE}")


if __name__ == "__main__":
    main()
