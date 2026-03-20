# scripts/run_feynrules_validation.py
# Executed by Magnus blueprint `validate-feynrules`.
# THIS IS NOT DEAD CODE.
import os
import pwd
import json
import magnus
import argparse
import subprocess
import traceback
from typing import Any, Dict
from ref import feynrules_validation_template


_LICENSE_ERROR_HINT = "not activated or is experiencing a license-related problem"


def _classify_license_error(stderr: str) -> dict | None:
    """Detect Wolfram Engine license errors. Returns None if not a license issue."""
    if _LICENSE_ERROR_HINT not in stderr:
        return None

    # If a mathpass file exists, the license is valid but likely occupied by another session.
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


def _validate(
    feynrules_model_path: str,
    lagrangian_symbol: str,
)-> Dict[str, Any]:
    
    start_marker = "__JSON_START__"
    end_marker = "__JSON_END__"
    wolfram_script_content = feynrules_validation_template(
        feynrules_model_path = feynrules_model_path,
        lagrangian_symbol = lagrangian_symbol,
        start_marker = start_marker,
        end_marker = end_marker,
    )
    script_filename = "validate.m"
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
            # Fallback if Mathematica crashed or failed completely
            result_dict = {
                "success": False,
                "model_loading": {
                    "status": False,
                    "message": "WolframScript did not produce valid output.",
                },
                "wolframscript": {
                    "returncode": process_result.returncode,
                    "stdout": stdout_content[:2000],
                    "stderr": stderr_content[:2000],
                    "script_head": wolfram_script_content[:500],
                }
            }
            license_info = _classify_license_error(stderr_content)
            if license_info:
                result_dict["license_info"] = license_info
                result_dict["model_loading"]["message"] = license_info["message"]
    except Exception as e:
        result_dict = {
            "success": False,
            "model_loading": {
                "status": False,
                "message": f"Python parsing failed: {str(e)}",
            },
            "wolframscript": {
                "returncode": process_result.returncode,
                "stdout": process_result.stdout[:2000],
                "stderr": process_result.stderr[:2000],
            }
        }

    return result_dict


def main():

    result_dict = {
        "success": False,
        "model_loading": {
            "status": False,
            "message": "Validation did not complete.",
        },
    }

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--secret", type=str, required=True)
        parser.add_argument("--symbol", type=str, required=True)
        args = parser.parse_args()

        fr_path = "undertest.fr"
        magnus.download_file(
            file_secret = args.secret,
            target_path = fr_path,
        )

        print("================ FeynRules Model Undertest ================")
        with open(fr_path) as file_pointer:
            print(file_pointer.read(), end="")
        print("\n===========================================================")

        print("\n\n\n")

        result_dict = _validate(
            feynrules_model_path = fr_path,
            lagrangian_symbol = args.symbol,
        )

        print("============ FeynRules Model Validation Result ============")
        print(json.dumps(result_dict, ensure_ascii=False, indent=4))
        print("===========================================================")

    except Exception as e:
        traceback.print_exc()
        result_dict = {
            "success": False,
            "message": f"Validation crashed: {e}",
            "traceback": traceback.format_exc(),
        }

    # Write result — always reached
    result_path = os.environ.get("MAGNUS_RESULT")
    assert result_path is not None, "Environment variable MAGNUS_RESULT is not set."
    with open(result_path, "w", encoding="utf-8") as file_pointer:
        json.dump(result_dict, file_pointer, ensure_ascii=False, indent=4)

    
if __name__ == "__main__":
    
    main()