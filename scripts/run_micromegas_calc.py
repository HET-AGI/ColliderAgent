# scripts/run_micromegas_calc.py
# Executed by Magnus blueprint `micromegas-calc`.
# THIS IS NOT DEAD CODE.
import os
import re
import json
import shutil
import magnus
import argparse
import subprocess
import traceback
from typing import Any, Dict, List, Tuple


project_name = "dm_project"
slha_input_name = "params.slha"
output_dir_name = "dm_run_output"

# Convention: user-supplied main.c is expected to write structured results to
# a file named `results.json` inside its working directory. If present, we
# surface its contents in MAGNUS_RESULT for downstream skills to consume.
RESULTS_FILENAME = "results.json"

# `make main=main.c` bakes the compile-time absolute path of <project>/work/
# into <project>/work/path.c as:
#     char * WORK="/opt/micromegas_6.2.3/<project>/work";
# ./main reads this at runtime to locate CalcHEP's symbolic-compile workspace.
# After a custody round-trip between containers the path has to be recreated
# verbatim or dynamic subprocess compilation silently fails (Omega=NAN).
_WORK_LINE_RE = re.compile(r'^\s*char\s*\*\s*WORK\s*=\s*"([^"]+)"\s*;', re.MULTILINE)

# Hard failure markers that appear on stdout even when ./main exits 0.
# Keep this list tight — only patterns that genuinely indicate garbage output.
_FAILURE_PATTERNS = (
    "Can not compile",
    "Omega=NAN",
    "Omega=nan",
)


def _resolve_install_path(project_path: str) -> Tuple[str, str]:
    """Parse <project>/work/path.c and return (install_path, work_value).

    install_path is the directory the project must live at when ./main runs.
    Raises FileNotFoundError / ValueError with a specific diagnostic if the
    file is missing or its contents don't match the expected format.
    """
    path_c = os.path.join(project_path, "work", "path.c")
    if not os.path.isfile(path_c):
        raise FileNotFoundError(
            f"Expected {path_c} in the downloaded project; micromegas-compile "
            "should have produced it. Was the project compiled with a recent "
            "micrOmegas release?"
        )

    with open(path_c) as file_pointer:
        content = file_pointer.read()

    match = _WORK_LINE_RE.search(content)
    if match is None:
        raise ValueError(
            f"Could not parse WORK=\"…\" from {path_c}. File contents begin: "
            f"{content[:200]!r}. The micrOmegas path.c format may have changed."
        )

    work_value = match.group(1)
    if not work_value.endswith("/work"):
        raise ValueError(
            f"WORK value {work_value!r} from {path_c} does not end in '/work'; "
            "cannot derive project install path."
        )

    install_path = work_value[: -len("/work")]
    if not os.path.isabs(install_path):
        raise ValueError(
            f"Derived install path {install_path!r} is not absolute; refusing "
            "to proceed."
        )
    return install_path, work_value


def _relocate_project(downloaded_path: str, install_path: str) -> str:
    """Move the downloaded project to its compile-time absolute path.

    Returns the final absolute location of the project directory.
    """
    downloaded_abs = os.path.abspath(downloaded_path)
    install_abs = os.path.abspath(install_path)

    if downloaded_abs == install_abs:
        return install_abs

    if os.path.exists(install_abs):
        # Magnus runs each job in a fresh container, so wiping a pre-existing
        # directory at the install path is safe.
        print(f"  removing stale {install_abs} before relocation")
        shutil.rmtree(install_abs)

    os.makedirs(os.path.dirname(install_abs), exist_ok = True)
    shutil.move(downloaded_abs, install_abs)
    print(f"  relocated project: {downloaded_abs} -> {install_abs}")
    return install_abs


def _detect_stdout_failures(stdout_content: str) -> List[str]:
    """Return the list of failure markers present in ./main stdout.

    Empty list means stdout looks clean.
    """
    hits: List[str] = []
    for pattern in _FAILURE_PATTERNS:
        if pattern in stdout_content:
            hits.append(pattern)
    return hits


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

    failure_markers = _detect_stdout_failures(stdout_content)
    if failure_markers:
        return {
            "success": False,
            "message": (
                "./main exited 0 but stdout contains failure markers "
                f"{failure_markers}; physics output is not trustworthy. This "
                "usually means micrOmegas could not dynamically compile an "
                "annihilation subprocess (check that <project>/work/ is at the "
                "absolute path baked into path.c)."
            ),
            "failure_markers": failure_markers,
            "stdout_tail": stdout_content[-4000:],
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
        downloaded_path = os.path.abspath(project_name)
        print(f"Downloaded compiled project to {downloaded_path}/")

        # ./main hard-codes the compile-time absolute path of work/ via
        # work/path.c. Recreate that path before invocation, otherwise
        # CalcHEP's dynamic subprocess compiler silently fails (Omega=NAN).
        install_path, work_value = _resolve_install_path(downloaded_path)
        print(f"path.c WORK = {work_value}")
        project_path = _relocate_project(downloaded_path, install_path)

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
