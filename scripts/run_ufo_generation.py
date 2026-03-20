# scripts/run_ufo_generation.py
# Executed by Magnus blueprint `generate-ufo`.
# THIS IS NOT DEAD CODE.
import os
import re
import pwd
import json
import magnus
import argparse
import subprocess
import traceback
from typing import Any, Dict
from ref import ufo_generation_template


_LICENSE_ERROR_HINT = "not activated or is experiencing a license-related problem"


def _classify_license_error(stderr: str) -> dict | None:
    """Detect Wolfram Engine license errors. Returns None if not a license issue."""
    if _LICENSE_ERROR_HINT not in stderr:
        return None

    try:
        real_home = Path(pwd.getpwuid(os.getuid()).pw_dir)
    except KeyError:
        real_home = Path.home()

    license_exists = any(p.is_file() for p in [
        real_home / ".WolframEngine" / "Licensing" / "mathpass",
        Path("/root/.WolframEngine/Licensing/mathpass"),
    ])

    if license_exists:
        return {
            "license_issue": "concurrent_session_limit",
            "retryable": True,
            "message": (
                "Wolfram Engine license is valid but another session is currently active. "
                "The free developer license allows only one concurrent kernel. "
                "This is a TEMPORARY error — retry after a short wait (e.g. 30 seconds)."
            ),
        }
    else:
        return {
            "license_issue": "not_activated",
            "retryable": False,
            "message": (
                "Wolfram Engine is not activated on this machine. "
                "An administrator must run 'wolframscript -activate' inside the container."
            ),
        }


ufo_dir_name = "ufo_output"


def _validate_ufo(ufo_dir: str) -> list:
    """Check BSM particle mass references against parameter definitions. Returns warning list.

    We parse particles.py and parameters.py with regex rather than importing them,
    because these are FeynRules-generated code files from the user's model — executing
    arbitrary user code would be a security risk. The FeynRules UFO writer produces a
    highly stable format, so regex is both safe and reliable here.
    """
    warnings = []
    particles_path = os.path.join(ufo_dir, "particles.py")
    parameters_path = os.path.join(ufo_dir, "parameters.py")

    if not os.path.isfile(particles_path) or not os.path.isfile(parameters_path):
        return warnings

    with open(parameters_path) as f:
        params_text = f.read()
    with open(particles_path) as f:
        particles_text = f.read()

    # 1. From parameters.py: find all params with lhablock='MASS' → {pdg_code: param_name}
    mass_params = {}
    # Match parameter blocks: name = 'XXX' ... lhablock = 'MASS' ... lhacode = [ N ]
    for block in re.split(r'\n(?=\w+\s*=\s*Parameter\()', params_text):
        name_m = re.search(r"name\s*=\s*'(\w+)'", block)
        lha_m = re.search(r"lhablock\s*=\s*'MASS'", block)
        code_m = re.search(r"lhacode\s*=\s*\[\s*(\d+)\s*\]", block)
        if name_m and lha_m and code_m:
            mass_params[int(code_m.group(1))] = name_m.group(1)

    # 2. From particles.py: find all particles → {pdg_code: (name, mass_ref)}
    particles = {}
    for block in re.split(r'\n(?=\w+\s*=\s*Particle\()', particles_text):
        pdg_m = re.search(r"pdg_code\s*=\s*(\d+)", block)
        pname_m = re.search(r"name\s*=\s*'([^']+)'", block)
        mass_m = re.search(r"mass\s*=\s*Param\.(\w+)", block)
        if pdg_m and pname_m and mass_m:
            particles[int(pdg_m.group(1))] = (pname_m.group(1), mass_m.group(1))

    # 3. Cross-check: particle has mass=ZERO but MASS parameter exists for its PDG code
    for pdg, (pname, mass_ref) in particles.items():
        if mass_ref == "ZERO" and pdg in mass_params:
            warnings.append(
                f"Particle '{pname}' (pdg {pdg}) has mass=Param.ZERO "
                f"but MASS parameter '{mass_params[pdg]}' exists in parameters.py. "
                f"The particle may not pick up its intended mass at runtime."
            )

    return warnings


def _generate(
    model_path: str,
    lagrangian_symbol: str,
    restriction_path: str = "",
)-> Dict[str, Any]:

    global ufo_dir_name
    
    start_marker = "__JSON_START__"
    end_marker = "__JSON_END__"
    wolfram_script_content = ufo_generation_template(
        model_path = model_path,
        lagrangian_symbol = lagrangian_symbol,
        ufo_output_name = ufo_dir_name,
        restriction_path = restriction_path,
        start_marker = start_marker,
        end_marker = end_marker,
    )
    script_filename = "generate_ufo.m"
    with open(script_filename, "w") as file_pointer:
        file_pointer.write(wolfram_script_content)

    process_result = subprocess.run(
        ["wolframscript", "-file", script_filename],
        capture_output = True,
        text = True,
    )

    try:
        stdout_content = process_result.stdout
        stderr_content = process_result.stderr

        if start_marker in stdout_content and end_marker in stdout_content:
            json_str = stdout_content.split(start_marker)[1].split(end_marker)[0].strip()
            result_dict = json.loads(json_str)
        else:
            result_dict = {
                "success": False,
                "message": "WolframScript did not produce valid output.",
                "wolframscript": {
                    "returncode": process_result.returncode,
                    "stdout": stdout_content[:2000],
                    "stderr": stderr_content[:2000],
                    "script_head": wolfram_script_content[:500],
                },
            }
            license_info = _classify_license_error(stderr_content)
            if license_info:
                result_dict["license_info"] = license_info
                result_dict["message"] = license_info["message"]
    except Exception as e:
        result_dict = {
            "success": False,
            "message": f"Python parsing failed: {str(e)}",
            "wolframscript": {
                "returncode": process_result.returncode,
                "stdout": process_result.stdout[:2000],
                "stderr": process_result.stderr[:2000],
            },
        }

    return result_dict


def main():

    global ufo_dir_name

    result_dict = {
        "success": False,
        "message": "UFO generation did not complete.",
    }

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--secret", type=str, required=True)
        parser.add_argument("--lagrangian", type=str, required=True)
        parser.add_argument("--target_path", type=str, required=True)
        parser.add_argument("--restriction_secret", type=str, default="")
        args = parser.parse_args()

        # Download model file
        model_path = "model.fr"
        magnus.download_file(
            file_secret = args.secret,
            target_path = model_path,
        )

        print("================ FeynRules Model for UFO Generation ================")
        with open(model_path) as file_pointer:
            print(file_pointer.read(), end="")
        print("\n====================================================================")

        # Download restriction file if provided
        restriction_path = ""
        if args.restriction_secret:
            restriction_path = "restriction.rst"
            magnus.download_file(
                file_secret = args.restriction_secret,
                target_path = restriction_path,
            )
            print("\n================ Restriction File ================")
            with open(restriction_path) as file_pointer:
                print(file_pointer.read(), end="")
            print("\n==================================================")

        print("\n\n\n")

        # Generate UFO
        result_dict = _generate(
            model_path = model_path,
            lagrangian_symbol = args.lagrangian,
            restriction_path = restriction_path,
        )

        # If successful, upload UFO directory and set action for download
        if result_dict.get("success") and os.path.isdir(ufo_dir_name):
            # Validate UFO: cross-check particle masses vs parameter definitions
            ufo_warnings = _validate_ufo(ufo_dir_name)
            if ufo_warnings:
                result_dict["warnings"] = ufo_warnings

            ufo_file_secret = magnus.custody_file(ufo_dir_name)
            download_target = args.target_path
            result_dict["ufo_path"] = download_target

            action_path = os.environ.get("MAGNUS_ACTION")
            assert action_path is not None, "Environment variable MAGNUS_ACTION is not set."
            with open(action_path, "w", encoding="utf-8") as file_pointer:
                file_pointer.write(f"magnus receive {ufo_file_secret} --output {download_target}")

        print("============ UFO Generation Result ============")
        print(json.dumps(result_dict, ensure_ascii=False, indent=4))
        print("================================================")

    except Exception as e:
        traceback.print_exc()
        result_dict = {
            "success": False,
            "message": f"UFO generation crashed: {e}",
            "traceback": traceback.format_exc(),
        }

    # Write result — always reached
    result_path = os.environ.get("MAGNUS_RESULT")
    assert result_path is not None, "Environment variable MAGNUS_RESULT is not set."
    with open(result_path, "w", encoding="utf-8") as file_pointer:
        json.dump(result_dict, file_pointer, ensure_ascii=False, indent=4)


if __name__ == "__main__":

    main()
