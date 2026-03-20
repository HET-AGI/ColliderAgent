# scripts/on_magnus/run_madgraph_launch.py
# Executed by Magnus blueprint `madgraph-launch`.
# THIS IS NOT DEAD CODE.
import os
import re
import json
import magnus
import argparse
import subprocess
import traceback
from typing import Any, Dict


process_dir_name = "process_output"
mg5_executable = "mg5_aMC"  # /opt/MG5_aMC_v3_7_0/bin/mg5_aMC in collider container


def _install_pdf_set(name: str) -> None:
    """Download and install a LHAPDF PDF set from CERN if not already present.

    Uses `lhapdf-config --datadir` to locate the LHAPDF data directory,
    then downloads and extracts the tarball from the CERN repository.
    """
    # Determine LHAPDF data directory
    result = subprocess.run(
        ["lhapdf-config", "--datadir"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"lhapdf-config --datadir failed (rc={result.returncode}): {result.stderr.strip()}"
        )
    datadir = result.stdout.strip()
    print(f"LHAPDF data directory: {datadir}")

    # Skip if already installed
    pdf_dir = os.path.join(datadir, name)
    if os.path.isdir(pdf_dir):
        print(f"PDF set '{name}' already installed at {pdf_dir}, skipping download.")
        return

    # Download tarball
    url = f"https://lhapdfsets.web.cern.ch/current/{name}.tar.gz"
    tarball = f"{name}.tar.gz"
    print(f"Downloading PDF set: {url}")
    dl = subprocess.run(
        ["curl", "-fSL", "-o", tarball, url],
        capture_output=True, text=True,
    )
    if dl.returncode != 0:
        raise RuntimeError(
            f"Failed to download PDF set '{name}' (rc={dl.returncode}): {dl.stderr.strip()}"
        )

    # Extract into data directory
    subprocess.run(
        ["tar", "xzf", tarball, "-C", datadir],
        check=True,
    )
    os.remove(tarball)

    # Verify
    if not os.path.isdir(pdf_dir):
        raise RuntimeError(
            f"PDF set directory {pdf_dir} not found after extraction."
        )
    print(f"PDF set '{name}' installed successfully at {pdf_dir}")


def _check_param_card(process_dir: str) -> list:
    """Check param_card.dat for duplicate PDG entries in MASS block and DECAY declarations.

    param_card format has two distinct structures:
      - `Block mass` is a block header followed by `<pdg> <value>` entries
      - `DECAY <pdg> <width>` are individual declarations, one per line

    Returns warning list (empty if clean).
    """
    warnings = []
    card_path = os.path.join(process_dir, "Cards", "param_card.dat")
    if not os.path.isfile(card_path):
        return warnings

    with open(card_path) as f:
        lines = f.readlines()

    # --- Check 1: duplicate PDG codes within Block mass ---
    in_mass_block = False
    mass_entries = {}  # pdg -> [line_numbers]

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        # Any Block/DECAY header ends the current block
        block_match = re.match(r'(?i)^block\s+(\S+)', stripped)
        decay_match = re.match(r'(?i)^decay\s+', stripped)
        if block_match:
            in_mass_block = block_match.group(1).upper() == "MASS"
            continue
        if decay_match:
            in_mass_block = False
            # Don't continue — fall through to DECAY collection below

        if in_mass_block:
            pdg_match = re.match(r'\s*(\d+)\s+', stripped)
            if pdg_match:
                pdg = int(pdg_match.group(1))
                mass_entries.setdefault(pdg, []).append(i)

    for pdg, line_nums in mass_entries.items():
        if len(line_nums) > 1:
            warnings.append(
                f"Block MASS: PDG {pdg} appears {len(line_nums)} times "
                f"(lines {line_nums}). MG5 may error with "
                f"'mass ({pdg},) is already define'. "
                f"Check the UFO model's parameters.py for duplicate external/dependent entries."
            )

    # --- Check 2: duplicate DECAY declarations ---
    decay_entries = {}  # pdg -> [line_numbers]

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        decay_match = re.match(r'(?i)^decay\s+(\d+)\s+', stripped)
        if decay_match:
            pdg = int(decay_match.group(1))
            decay_entries.setdefault(pdg, []).append(i)

    for pdg, line_nums in decay_entries.items():
        if len(line_nums) > 1:
            warnings.append(
                f"DECAY: PDG {pdg} declared {len(line_nums)} times "
                f"(lines {line_nums}). MG5 may error with a duplicate definition."
            )

    return warnings


def _parse_results_summary(stdout: str)-> Dict[str, Any]:
    """Extract cross-section, nevents, and run name from MG5 stdout."""
    summary = {}

    run_match = re.search(
        r"Results Summary for run:\s+(\S+)\s+tag:\s+(\S+)",
        stdout,
    )
    if run_match:
        summary["run_name"] = run_match.group(1)
        summary["tag"] = run_match.group(2)

    xs_match = re.search(
        r"Cross-section\s*:\s*([\d.eE+-]+)\s*\+-\s*([\d.eE+-]+)\s*(\w+)",
        stdout,
    )
    if xs_match:
        summary["cross_section"] = f"{xs_match.group(1)} +- {xs_match.group(2)} {xs_match.group(3)}"

    nev_match = re.search(
        r"Nb of events\s*:\s*(\d+)",
        stdout,
    )
    if nev_match:
        summary["nevents"] = int(nev_match.group(1))

    return summary


def _launch(
    process_dir: str,
    launch_commands: str,
)-> Dict[str, Any]:

    # Build MG5 script
    nb_core = len(os.sched_getaffinity(0))
    print(f"CPU cores (sched_getaffinity): {nb_core}")

    script = f"set nb_core {nb_core}\nlaunch {process_dir}\n{launch_commands}\n"

    script_filename = "launch.mg5"
    with open(script_filename, "w") as file_pointer:
        file_pointer.write(script)

    print("================ MG5 Launch Script ================")
    print(script, end="")
    print("====================================================")

    process_result = subprocess.run(
        [mg5_executable, script_filename],
        capture_output = True,
        text = True,
        stdin = subprocess.DEVNULL,
    )

    stdout_content = process_result.stdout
    stderr_content = process_result.stderr

    # Print full output to Magnus job logs (stdout/stderr → Magnus log)
    print(stdout_content)
    if stderr_content.strip():
        print("=== STDERR ===")
        print(stderr_content)

    # Strip ANSI escape codes before error detection
    stdout_clean = re.sub(r"\x1b\[[0-9;]*m", "", stdout_content)
    stderr_clean = re.sub(r"\x1b\[[0-9;]*m", "", stderr_content)

    # Parse Results Summary first — this is the authoritative success signal
    summary = _parse_results_summary(stdout_content)

    if "cross_section" in summary:
        # Results Summary found → events were generated successfully
        result_dict = {
            "success": True,
            "message": "Event generation completed successfully.",
        }
        result_dict.update(summary)

        # Attach warnings for non-fatal issues (e.g. LHAPDF systematics fail)
        warnings = []
        if bool(re.search(r"(?i)^error\b", stderr_clean, re.MULTILINE)):
            warnings.append("errors detected in stderr (non-fatal)")
        if bool(re.search(r"^\s*fail\s*$", stdout_clean, re.MULTILINE)):
            warnings.append("'fail' detected in stdout (non-fatal, e.g. LHAPDF systematics)")
        if warnings:
            result_dict["warnings"] = warnings
    else:
        # No Results Summary → check error signals
        has_stderr_error = bool(re.search(r"(?i)^error\b", stderr_clean, re.MULTILINE))
        has_stdout_fail = bool(re.search(r"^\s*fail\s*$", stdout_clean, re.MULTILINE))

        reason = []
        if process_result.returncode != 0:
            reason.append(f"return code {process_result.returncode}")
        if has_stderr_error:
            reason.append("errors detected in stderr")
        if has_stdout_fail:
            reason.append("MG5 reported 'fail' in stdout")

        clean = stdout_clean + "\n" + stderr_clean

        if reason:
            result_dict = {
                "success": False,
                "message": f"Event generation failed ({', '.join(reason)}).",
                "stdout": clean[-3000:],
            }
        else:
            result_dict = {
                "success": False,
                "message": "No Results Summary found in MG5 output. Run did not complete normally.",
                "stdout": clean[-2000:],
            }

    return result_dict


def main():

    global process_dir_name

    result_dict = {
        "success": False,
        "message": "Event generation did not complete.",
    }

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--process_secret", type=str, required=True)
        parser.add_argument("--launch_commands", type=str, required=True)
        parser.add_argument("--target_path", type=str, required=True)
        parser.add_argument("--pdf", type=str, default="")
        args = parser.parse_args()

        # Download compiled process directory
        magnus.download_file(
            file_secret = args.process_secret,
            target_path = process_dir_name,
        )
        print(f"Downloaded process directory to {process_dir_name}/")

        # Restore UFO model if embedded by compile step (needed for DECAY Auto)
        ufo_in_process = os.path.join(process_dir_name, "UFO_model")
        if os.path.isdir(ufo_in_process):
            os.symlink(os.path.abspath(ufo_in_process), "ufo_model")
            print(f"Linked embedded UFO model: ufo_model -> {ufo_in_process}/")

        # Check param_card for duplicate PDG entries
        card_warnings = _check_param_card(process_dir_name)

        # Install PDF set if requested
        if args.pdf:
            _install_pdf_set(args.pdf)

        print("\n\n\n")

        # Launch
        result_dict = _launch(
            process_dir = process_dir_name,
            launch_commands = args.launch_commands,
        )

        # Attach param_card warnings (if any) to result
        if card_warnings:
            result_dict["param_card_warnings"] = card_warnings

        # Upload output directory and set download action
        # Upload even on failure so partial results (e.g. generated events) are recoverable
        if os.path.isdir(process_dir_name):
            file_secret = magnus.custody_file(process_dir_name)
            download_target = args.target_path
            result_dict["output_dir"] = download_target

            action_path = os.environ.get("MAGNUS_ACTION")
            assert action_path is not None, "Environment variable MAGNUS_ACTION is not set."
            with open(action_path, "w", encoding="utf-8") as file_pointer:
                file_pointer.write(f"magnus receive {file_secret} --output {download_target}")

        print("============ MG5 Launch Result ============")
        print(json.dumps(result_dict, ensure_ascii=False, indent=4))
        print("============================================")

    except Exception as e:
        traceback.print_exc()
        result_dict = {
            "success": False,
            "message": f"Event generation crashed: {e}",
            "traceback": traceback.format_exc(),
        }

    # Write result — always reached
    result_path = os.environ.get("MAGNUS_RESULT")
    assert result_path is not None, "Environment variable MAGNUS_RESULT is not set."
    with open(result_path, "w", encoding="utf-8") as file_pointer:
        json.dump(result_dict, file_pointer, ensure_ascii=False, indent=4)


if __name__ == "__main__":

    main()
