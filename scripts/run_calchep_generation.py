# scripts/run_calchep_generation.py
# Executed by Magnus blueprint `generate-calchep`.
# THIS IS NOT DEAD CODE.
import os
import pwd
import json
import magnus
import argparse
import subprocess
import traceback
from pathlib import Path
from typing import Any, Dict
from ref import calchep_generation_template


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


calchep_dir_name = "calchep_output"


def _generate(
    model_path: str,
    lagrangian_symbol: str,
    restriction_path: str = "",
)-> Dict[str, Any]:

    global calchep_dir_name

    start_marker = "__JSON_START__"
    end_marker = "__JSON_END__"
    wolfram_script_content = calchep_generation_template(
        model_path = model_path,
        lagrangian_symbol = lagrangian_symbol,
        calchep_output_name = calchep_dir_name,
        restriction_path = restriction_path,
        start_marker = start_marker,
        end_marker = end_marker,
    )
    script_filename = "generate_calchep.m"
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

    global calchep_dir_name

    result_dict = {
        "success": False,
        "message": "CalcHEP generation did not complete.",
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

        print("================ FeynRules Model for CalcHEP Generation ================")
        with open(model_path) as file_pointer:
            print(file_pointer.read(), end="")
        print("\n========================================================================")

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

        # Generate CalcHEP
        result_dict = _generate(
            model_path = model_path,
            lagrangian_symbol = args.lagrangian,
            restriction_path = restriction_path,
        )

        # If successful, upload CalcHEP directory and set action for download
        if result_dict.get("success") and os.path.isdir(calchep_dir_name):
            calchep_file_secret = magnus.custody_file(calchep_dir_name)
            download_target = args.target_path
            result_dict["calchep_path"] = download_target

            action_path = os.environ.get("MAGNUS_ACTION")
            assert action_path is not None, "Environment variable MAGNUS_ACTION is not set."
            with open(action_path, "w", encoding="utf-8") as file_pointer:
                file_pointer.write(f"magnus receive {calchep_file_secret} --output {download_target}")

        print("============ CalcHEP Generation Result ============")
        print(json.dumps(result_dict, ensure_ascii=False, indent=4))
        print("====================================================")

    except Exception as e:
        traceback.print_exc()
        result_dict = {
            "success": False,
            "message": f"CalcHEP generation crashed: {e}",
            "traceback": traceback.format_exc(),
        }

    # Write result — always reached
    result_path = os.environ.get("MAGNUS_RESULT")
    assert result_path is not None, "Environment variable MAGNUS_RESULT is not set."
    with open(result_path, "w", encoding="utf-8") as file_pointer:
        json.dump(result_dict, file_pointer, ensure_ascii=False, indent=4)


if __name__ == "__main__":

    main()
