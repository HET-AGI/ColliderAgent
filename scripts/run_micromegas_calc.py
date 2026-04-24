# scripts/run_micromegas_calc.py
# Executed by Magnus blueprint `micromegas-calc`.
# THIS IS NOT DEAD CODE.
import os
import json
import shutil
import magnus
import argparse
import subprocess
import traceback
from typing import Any, Dict, List


project_name = "dm_project"
slha_input_name = "params.slha"
output_dir_name = "dm_run_output"

# Convention: user-supplied main.c is expected to write structured results to
# a file named `results.json` inside its working directory. If present, we
# surface its contents in MAGNUS_RESULT for downstream skills to consume.
RESULTS_FILENAME = "results.json"


def _run(project_path: str, main_args: List[str])-> Dict[str, Any]:

    binary_path = os.path.join(project_path, "main")
    if not os.path.isfile(binary_path):
        return {
            "success": False,
            "message": f"No ./main binary in {project_path}. Was the project produced by micromegas-compile?",
        }

    cmd = [binary_path] + main_args
    print(f"=== invoking: {' '.join(cmd)} ===\n")

    run_result = subprocess.run(
        cmd,
        cwd = project_path,
        capture_output = True,
        text = True,
    )
    stdout_content = run_result.stdout
    stderr_content = run_result.stderr

    print(stdout_content)
    if stderr_content.strip():
        print("=== STDERR ===")
        print(stderr_content)

    if run_result.returncode != 0:
        return {
            "success": False,
            "message": f"./main returned non-zero exit code {run_result.returncode}.",
            "stdout_tail": stdout_content[-3000:],
            "stderr_tail": stderr_content[-2000:],
        }

    result_dict: Dict[str, Any] = {
        "success": True,
        "message": "micrOmegas calculation completed.",
        "stdout_tail": stdout_content[-4000:],
    }

    # Surface results.json if the user's main.c wrote one
    results_path = os.path.join(project_path, RESULTS_FILENAME)
    if os.path.isfile(results_path):
        try:
            with open(results_path) as file_pointer:
                result_dict["results"] = json.load(file_pointer)
        except json.JSONDecodeError as e:
            result_dict["results_parse_error"] = f"{results_path} is not valid JSON: {e}"

    return result_dict


def _collect_outputs(project_path: str)-> str:
    """Collect files the user's main.c may have written (results.json, plots, etc.)
    into a single directory for upload to Magnus custody."""
    global output_dir_name

    if os.path.isdir(output_dir_name):
        shutil.rmtree(output_dir_name)
    os.makedirs(output_dir_name)

    # Preserve every non-build artifact produced by ./main
    skip_names = {"main", "work", "lib", "Makefile", "README", "main.c", "main.cpp", "data.par"}
    for entry in os.listdir(project_path):
        if entry in skip_names or entry.startswith("."):
            continue
        src = os.path.join(project_path, entry)
        dst = os.path.join(output_dir_name, entry)
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy(src, dst)
        except Exception as e:
            print(f"  warning: could not copy {entry}: {e}")

    return output_dir_name


def main():

    global project_name, slha_input_name

    result_dict = {
        "success": False,
        "message": "micrOmegas calculation did not complete.",
    }

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--project_secret", type=str, required=True)
        parser.add_argument("--target_path", type=str, required=True)
        parser.add_argument("--slha_secret", type=str, default="")
        parser.add_argument("--extra_args", type=str, default="")
        args = parser.parse_args()

        # Download the compiled project directory
        magnus.download_file(
            file_secret = args.project_secret,
            target_path = project_name,
        )
        project_path = os.path.abspath(project_name)
        print(f"Downloaded compiled project to {project_path}/")

        # Compiled binaries come off Magnus custody without the executable bit;
        # restore it so ./main is runnable.
        binary_path = os.path.join(project_path, "main")
        if os.path.isfile(binary_path):
            os.chmod(binary_path, 0o755)

        # Assemble ./main arguments: [slha_path?] + extra positional args
        main_args: List[str] = []
        if args.slha_secret:
            slha_abs = os.path.abspath(slha_input_name)
            magnus.download_file(
                file_secret = args.slha_secret,
                target_path = slha_abs,
            )
            print(f"Downloaded SLHA file to {slha_abs}")
            main_args.append(slha_abs)

        if args.extra_args.strip():
            main_args.extend(args.extra_args.strip().split())

        result_dict = _run(project_path = project_path, main_args = main_args)

        # Always try to upload outputs, even on failure — stdout / partial results
        # often carry the diagnostic the user needs.
        try:
            collected = _collect_outputs(project_path)
            file_secret = magnus.custody_file(collected)
            result_dict["output_dir"] = args.target_path

            action_path = os.environ.get("MAGNUS_ACTION")
            assert action_path is not None, "Environment variable MAGNUS_ACTION is not set."
            with open(action_path, "w", encoding="utf-8") as file_pointer:
                file_pointer.write(f"magnus receive {file_secret} --output {args.target_path}")
        except Exception as upload_err:
            print(f"Warning: output upload failed: {upload_err}")

        print("============ micrOmegas Calc Result ============")
        print(json.dumps(result_dict, ensure_ascii=False, indent=4))
        print("=================================================")

    except Exception as e:
        traceback.print_exc()
        result_dict = {
            "success": False,
            "message": f"Calculation crashed: {e}",
            "traceback": traceback.format_exc(),
        }

    # Write result — always reached
    result_path = os.environ.get("MAGNUS_RESULT")
    assert result_path is not None, "Environment variable MAGNUS_RESULT is not set."
    with open(result_path, "w", encoding="utf-8") as file_pointer:
        json.dump(result_dict, file_pointer, ensure_ascii=False, indent=4)


if __name__ == "__main__":

    main()
