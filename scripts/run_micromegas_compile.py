# scripts/run_micromegas_compile.py
# Executed by Magnus blueprint `micromegas-compile`.
# THIS IS NOT DEAD CODE.
import os
import json
import glob
import shutil
import magnus
import argparse
import subprocess
import traceback
from typing import Any, Dict


project_name = "dm_project"
calchep_input_name = "calchep_input"
main_source_name = "main.c"

# Resolved at container build time; see src/images/micromegas/Dockerfile.
_DEFAULT_MICROMEGAS_ROOT = "/opt/micromegas_6.2.3"


def _find_mdl_files(calchep_dir: str) -> list:
    """Locate the four CalcHEP .mdl files.

    `generate-calchep` places them at the top level of its output directory,
    but we also look one level down to tolerate layouts like `<dir>/work/models/`.
    """
    required = ["vars1.mdl", "func1.mdl", "prtcls1.mdl", "lgrng1.mdl"]
    candidates = [calchep_dir] + [
        d for d in glob.glob(os.path.join(calchep_dir, "*")) if os.path.isdir(d)
    ]
    for root in candidates:
        found = [os.path.join(root, name) for name in required]
        if all(os.path.isfile(p) for p in found):
            return found
    raise FileNotFoundError(
        f"Could not locate vars1.mdl/func1.mdl/prtcls1.mdl/lgrng1.mdl under {calchep_dir}"
    )


def _compile(micromegas_root: str)-> Dict[str, Any]:

    global project_name

    # 1. Create the project skeleton via `newProject`
    project_path = os.path.join(micromegas_root, project_name)
    if os.path.isdir(project_path):
        shutil.rmtree(project_path)

    newproject_result = subprocess.run(
        [os.path.join(micromegas_root, "newProject"), project_name],
        cwd = micromegas_root,
        capture_output = True,
        text = True,
    )
    print("=== newProject stdout ===")
    print(newproject_result.stdout)
    if newproject_result.returncode != 0:
        return {
            "success": False,
            "message": f"newProject failed (return code {newproject_result.returncode}).",
            "stderr": newproject_result.stderr[:2000],
        }

    # 2. Install CalcHEP model files into work/models/
    mdl_files = _find_mdl_files(calchep_input_name)
    models_dir = os.path.join(project_path, "work", "models")
    os.makedirs(models_dir, exist_ok = True)
    for src in mdl_files:
        shutil.copy(src, models_dir)
        print(f"  installed {os.path.basename(src)} → work/models/")

    # 3. Install user-supplied main.c (overwrites the newProject template)
    shutil.copy(main_source_name, os.path.join(project_path, "main.c"))
    print(f"  installed main.c → {project_name}/main.c")

    # 4. Compile. First invocation generates annihilation / scattering amplitudes
    # via the pre-built CalcHEP engine, then compiles the user project.
    nb_core = len(os.sched_getaffinity(0))
    print(f"\nCPU cores (sched_getaffinity): {nb_core}\n")

    make_result = subprocess.run(
        ["make", "main=main.c", f"-j{nb_core}"],
        cwd = project_path,
        capture_output = True,
        text = True,
    )

    print("=== make stdout ===")
    print(make_result.stdout)
    if make_result.stderr.strip():
        print("=== make stderr ===")
        print(make_result.stderr)

    binary_path = os.path.join(project_path, "main")
    if make_result.returncode != 0 or not os.path.isfile(binary_path):
        tail = (make_result.stdout + "\n" + make_result.stderr)[-3000:]
        return {
            "success": False,
            "message": f"Compilation failed (return code {make_result.returncode}, binary present: {os.path.isfile(binary_path)}).",
            "make_log_tail": tail,
        }

    return {
        "success": True,
        "message": "micrOmegas project compiled successfully.",
        "project_path_in_container": project_path,
        "main_binary": binary_path,
    }


def main():

    global project_name, calchep_input_name, main_source_name

    result_dict = {
        "success": False,
        "message": "micrOmegas compilation did not complete.",
    }

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--calchep_secret", type=str, required=True)
        parser.add_argument("--main_secret", type=str, required=True)
        parser.add_argument("--target_path", type=str, required=True)
        parser.add_argument("--project", type=str, default="")
        parser.add_argument(
            "--micromegas_root",
            type=str,
            default=os.environ.get("MICROMEGAS_ROOT", _DEFAULT_MICROMEGAS_ROOT),
        )
        args = parser.parse_args()

        if args.project.strip():
            project_name = args.project.strip()

        # Download CalcHEP model directory
        magnus.download_file(
            file_secret = args.calchep_secret,
            target_path = calchep_input_name,
        )
        print(f"Downloaded CalcHEP model to {calchep_input_name}/")

        # Download main.c
        magnus.download_file(
            file_secret = args.main_secret,
            target_path = main_source_name,
        )
        print(f"Downloaded main.c to {main_source_name}")
        print("\n================ main.c (user-supplied) ================")
        with open(main_source_name) as file_pointer:
            print(file_pointer.read(), end="")
        print("\n========================================================\n")

        result_dict = _compile(micromegas_root = args.micromegas_root)

        # If successful, upload the compiled project directory
        if result_dict.get("success"):
            project_path = os.path.join(args.micromegas_root, project_name)
            file_secret = magnus.custody_file(project_path)
            result_dict["project_dir"] = args.target_path

            action_path = os.environ.get("MAGNUS_ACTION")
            assert action_path is not None, "Environment variable MAGNUS_ACTION is not set."
            with open(action_path, "w", encoding="utf-8") as file_pointer:
                file_pointer.write(f"magnus receive {file_secret} --output {args.target_path}")

        print("============ micrOmegas Compile Result ============")
        print(json.dumps(result_dict, ensure_ascii=False, indent=4))
        print("===================================================")

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
