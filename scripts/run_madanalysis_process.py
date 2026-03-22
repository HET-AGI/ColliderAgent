# scripts/run_madanalysis_process.py
# Executed by Magnus blueprint `madanalysis-process`.
# THIS IS NOT DEAD CODE.
import os
import re
import json
import magnus
import argparse
import subprocess
import traceback
from typing import Any, Dict


ma5_executable = "/opt/madanalysis5/bin/ma5"
events_dir_name = "events_input"
output_dir_name = "analysis_output"


def _process(
    events_dir: str,
    script: str,
    level: str,
)-> Dict[str, Any]:

    # Map level to command-line flag
    level_flags = {
        "parton": "-P",
        "hadron": "-H",
        "reco": "-R",
    }
    level_flag = level_flags.get(level.lower())
    if not level_flag:
        return {
            "success": False,
            "message": f"Invalid level '{level}'. Use 'parton', 'hadron', or 'reco'.",
        }

    # Replace {EVENTS_DIR} placeholder with actual download path
    script = script.replace("{EVENTS_DIR}", events_dir)

    # Strip any user-written submit lines — we always append our own
    script = re.sub(r'(?mi)^\s*submit\b.*$', '', script)
    script += f"\nsubmit {output_dir_name}\n"

    # Write script to file
    script_filename = "analysis.ma5"
    with open(script_filename, "w") as file_pointer:
        file_pointer.write(script)

    print("================ MA5 Analysis Script ================")
    print(script, end="")
    print("======================================================")

    process_result = subprocess.run(
        [ma5_executable, level_flag, "-s", script_filename],
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

    # Check for errors: returncode or stderr errors
    has_stderr_error = bool(re.search(r"(?i)^error\b", stderr_content, re.MULTILINE))

    if process_result.returncode != 0 or has_stderr_error:
        reason = []
        if process_result.returncode != 0:
            reason.append(f"return code {process_result.returncode}")
        if has_stderr_error:
            reason.append("errors detected in stderr")

        # Strip ANSI escape codes for clean agent output
        clean = re.sub(r"\x1b\[[0-9;]*m", "", stdout_content + "\n" + stderr_content)

        result_dict = {
            "success": False,
            "message": f"MadAnalysis5 failed ({', '.join(reason)}).",
            "stdout": clean[-3000:],
        }
    else:
        result_dict = {
            "success": True,
            "message": "MadAnalysis5 analysis completed successfully.",
        }

        # Warn if output directory was not created
        if not os.path.isdir(output_dir_name):
            result_dict["warning"] = f"Output directory '{output_dir_name}' not found. Analysis may not have produced output."
            result_dict["stdout"] = stdout_content[-2000:]

    return result_dict


def main():

    result_dict = {
        "success": False,
        "message": "MadAnalysis5 analysis did not complete.",
    }

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--events_secret", type=str, required=True)
        parser.add_argument("--script", type=str, required=True)
        parser.add_argument("--level", type=str, default="parton")
        parser.add_argument("--target_path", type=str, required=True)
        args = parser.parse_args()

        # Download events directory
        magnus.download_file(
            file_secret = args.events_secret,
            target_path = events_dir_name,
        )
        print(f"Downloaded events directory to {events_dir_name}/")

        print("\n\n\n")

        # Run analysis
        result_dict = _process(
            events_dir = events_dir_name,
            script = args.script,
            level = args.level,
        )

        # If successful, upload the output directory
        if result_dict.get("success") and os.path.isdir(output_dir_name):
            file_secret = magnus.custody_file(output_dir_name)
            download_target = args.target_path
            result_dict["output_dir"] = download_target

            action_path = os.environ.get("MAGNUS_ACTION")
            assert action_path is not None, "Environment variable MAGNUS_ACTION is not set."
            with open(action_path, "w", encoding="utf-8") as file_pointer:
                file_pointer.write(f"magnus receive {file_secret} --output {download_target}")

        print("============ MA5 Analysis Result ============")
        print(json.dumps(result_dict, ensure_ascii=False, indent=4))
        print("==============================================")

    except Exception as e:
        traceback.print_exc()
        result_dict = {
            "success": False,
            "message": f"MadAnalysis5 crashed: {e}",
            "traceback": traceback.format_exc(),
        }

    # Write result — always reached
    result_path = os.environ.get("MAGNUS_RESULT")
    assert result_path is not None, "Environment variable MAGNUS_RESULT is not set."
    with open(result_path, "w", encoding="utf-8") as file_pointer:
        json.dump(result_dict, file_pointer, ensure_ascii=False, indent=4)


if __name__ == "__main__":

    main()
