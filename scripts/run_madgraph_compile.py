# scripts/run_madgraph_compile.py
# Executed by Magnus blueprint `madgraph-compile`.
# THIS IS NOT DEAD CODE.
import os
import re
import json
import shutil
import magnus
import argparse
import subprocess
import traceback
from typing import Any, Dict


process_output_name = "process_output"
ufo_model_name = "ufo_model"
mg5_executable = "mg5_aMC"  # /opt/MG5_aMC_v3_7_0/bin/mg5_aMC in collider container


def _compile(
    model_ref: str,
    processes: str,
    definitions: str = "",
)-> Dict[str, Any]:

    global process_output_name

    # Build MG5 script
    nb_core = len(os.sched_getaffinity(0))
    print(f"CPU cores (sched_getaffinity): {nb_core}")

    lines = [
        f"set nb_core {nb_core}",
        f"import model {model_ref}",
    ]

    if definitions.strip():
        for defn in definitions.strip().split("\n"):
            defn = defn.strip()
            if defn:
                lines.append(f"define {defn}")

    proc_list = [p.strip() for p in processes.strip().split("\n") if p.strip()]
    validate_only = len(proc_list) == 0

    if validate_only:
        lines.append("quit")
    else:
        lines.append(f"generate {proc_list[0]}")
        for proc in proc_list[1:]:
            lines.append(f"add process {proc}")
        lines.append(f"output {process_output_name}")

    script = "\n".join(lines) + "\n"

    script_filename = "compile.mg5"
    with open(script_filename, "w") as file_pointer:
        file_pointer.write(script)

    print("================ MG5 Compile Script ================")
    print(script, end="")
    print("=====================================================")

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

    # Check for errors: returncode, missing output dir, or stderr errors
    has_stderr_error = bool(re.search(r"(?i)^error\b", stderr_clean, re.MULTILINE))

    if validate_only:
        # Import-only: success = no errors
        if process_result.returncode != 0 or has_stderr_error:
            reason = []
            if process_result.returncode != 0:
                reason.append(f"return code {process_result.returncode}")
            if has_stderr_error:
                reason.append("errors detected in stderr")

            clean = stdout_clean + "\n" + stderr_clean
            result_dict = {
                "success": False,
                "message": f"Model import failed ({', '.join(reason)}).",
                "stdout": clean[-3000:],
                "script": script,
            }
        else:
            result_dict = {
                "success": True,
                "message": "Model imported successfully.",
            }
    elif process_result.returncode != 0 or not os.path.isdir(process_output_name) or has_stderr_error:
        reason = []
        if process_result.returncode != 0:
            reason.append(f"return code {process_result.returncode}")
        if not os.path.isdir(process_output_name):
            reason.append("output directory not created")
        if has_stderr_error:
            reason.append("errors detected in stderr")

        clean = stdout_clean + "\n" + stderr_clean

        result_dict = {
            "success": False,
            "message": f"Compilation failed ({', '.join(reason)}).",
            "stdout": clean[-3000:],
            "script": script,
        }
    else:
        result_dict = {
            "success": True,
            "message": "Process compiled successfully.",
        }

    return result_dict


def main():

    global process_output_name, ufo_model_name

    result_dict = {
        "success": False,
        "message": "Process compilation did not complete.",
    }

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--ufo_secret", type=str, default="")
        parser.add_argument("--model", type=str, default="")
        parser.add_argument("--process", type=str, default="")
        parser.add_argument("--definitions", type=str, default="")
        parser.add_argument("--target_path", type=str, default="")
        args = parser.parse_args()

        # Determine model reference: custom UFO upload or MG5 built-in model
        if args.ufo_secret:
            magnus.download_file(
                file_secret = args.ufo_secret,
                target_path = ufo_model_name,
            )
            model_ref = f"./{ufo_model_name}"
            print(f"Downloaded UFO model to {ufo_model_name}/")
        elif args.model:
            model_ref = args.model
            print(f"Using MG5 built-in model: {model_ref}")
        else:
            model_ref = "sm"
            print(f"No model specified, defaulting to: {model_ref}")

        print("\n\n\n")

        # Compile
        result_dict = _compile(
            model_ref = model_ref,
            processes = args.process,
            definitions = args.definitions,
        )

        # Embed UFO into process directory so launch can use DECAY Auto
        if result_dict.get("success") and os.path.isdir(process_output_name):
            if os.path.isdir(ufo_model_name):
                ufo_dest = os.path.join(process_output_name, "UFO_model")
                shutil.copytree(ufo_model_name, ufo_dest)
                print(f"Embedded UFO model into {ufo_dest}/")

            # Upload compiled process directory
            if args.target_path:
                file_secret = magnus.custody_file(process_output_name)
                download_target = args.target_path
                result_dict["process_dir"] = download_target

                action_path = os.environ.get("MAGNUS_ACTION")
                assert action_path is not None, "Environment variable MAGNUS_ACTION is not set."
                with open(action_path, "w", encoding="utf-8") as file_pointer:
                    file_pointer.write(f"magnus receive {file_secret} --output {download_target}")

        print("============ MG5 Compile Result ============")
        print(json.dumps(result_dict, ensure_ascii=False, indent=4))
        print("=============================================")

    except Exception as e:
        traceback.print_exc()
        result_dict = {
            "success": False,
            "message": f"Compilation crashed: {e}",
            "traceback": traceback.format_exc(),
        }

    # Write result — always reached
    result_path = os.environ.get("MAGNUS_RESULT")
    assert result_path is not None, "Environment variable MAGNUS_RESULT is not set."
    with open(result_path, "w", encoding="utf-8") as file_pointer:
        json.dump(result_dict, file_pointer, ensure_ascii=False, indent=4)


if __name__ == "__main__":

    main()
