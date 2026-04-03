---
name: reproduction-guide-generator
description: >
  Generate a self-contained reproduction guide from a completed analysis pipeline run.
  Triggers when the user asks to "create a reproduction guide", "write a reproduction package",
  "make this reproducible", or "create scripts for reproducing this analysis".
---

# Reproduction Guide Generator

## Overview

After a collider physics analysis pipeline has completed, this skill generates a **self-contained reproduction directory** containing all scripts, model files, and a step-by-step guide that allows another person or AI agent to reproduce the results from scratch.

The reproduction package must support **two execution backends**:

| Backend | Tools | Use case |
|---------|-------|----------|
| **local** | wolframscript + mg5_aMC (installed locally) | User has Mathematica and MadGraph5 on their machine |
| **magnus** | Magnus cloud CLI (`magnus run <blueprint>`) | No local HEP tools needed; computation runs on remote clusters |

## When to Invoke

- After a pipeline run has completed (all steps finished, plots generated)
- When the user asks to create a reproduction guide, reproducibility package, or standalone scripts

## Run Discovery

This skill can be invoked in two ways:

1. **By the orchestrator** at the end of a pipeline run — the conversation already contains context (run label, progress paths, results). Use that context directly.
2. **Standalone** in a new conversation — no prior context is available. In this case:
   - Read `progress/run_manifest.yaml` to discover all completed runs.
   - If the user specified a run label, package that run.
   - If there is only one run, package that run.
   - If there are multiple runs and the user did not specify, package the most recent run (by timestamp).

## Inputs

In orchestrator mode, inputs come from the conversation context. In standalone mode, this skill reads artifacts from the completed run:

1. **Original task file** (e.g., `prompt_*.md`) — the physics specification
2. **Progress files** in `progress/<run_label>/` — step-by-step records of what was done
3. **Generated code files** — `.fr` model files, MadGraph `.dat` scripts, Python analysis scripts
4. **Output results** — scan summary files, plots, cross section tables

## Output Structure

Create a `reproduction/` directory with the following structure. Everything must be self-contained — no file should depend on paths outside this directory at rest (paths are configured at run time).

```
reproduction/
├── README.md                      # Main guide document
├── run_all.sh                     # One-click automation script (--local / --magnus)
├── models/                        # Model files
│   ├── <Model>.fr                 # FeynRules model file (cp from models/)
│   └── <Model>_UFO/              # Pre-built UFO model directory (cp from workdir/models/)
└── scripts/                       # All executable scripts
    ├── generate_ufo.wl            # WolframScript for UFO generation (Write — new file, used only with --from-fr)
    ├── mg5_<label>.mg5            # MadGraph scripts (cp from scripts/)
    ├── ma5_<label>.ma5            # MadAnalysis scripts (cp from scripts/, if used)
    └── plot_<desc>.py             # Python analysis scripts (cp from scripts/)
```

At runtime, `run_all.sh` creates a `workdir/` following the standard pipeline layout:

```
reproduction/workdir/              # created at runtime
├── models/<Model>_UFO/            # UFO model (copied from package, or regenerated with --from-fr)
├── events/<process_label>/        # MadGraph output + events
├── analysis/<label>/              # MadAnalysis output (if used)
└── output/
    ├── figures/                   # plots
    └── data/                      # data tables
```

## Workflow

### Step 1: Inventory the completed run (standalone mode only)

Skip this step if invoked by the orchestrator — the conversation already contains all needed context.

In standalone mode, collect artifacts from the target run identified in Run Discovery:

- Read progress files from `progress/<run_label>/`:
  - Step 1 (Model Building): `step1_feynrules.md`, `.fr` files in `models/`
  - Step 2 (Event Generation): `step2_madgraph.md`, MadGraph scripts, output directories
  - Step 3 (Event Analysis): `step3_madanalysis.md` (may not exist)
  - Step 4 (Post-Processing): `step4_postprocessing.md`, plotting scripts in `scripts/`, event-level analysis scripts in `analysis/`

Also read the original task/prompt file for context.

### Step 2: Collect scripts (cp-first strategy)

Every pipeline script should be **copied first**. Pipeline subagents are expected to generate scripts with relative paths, so most files can be copied verbatim. After copying, verify and fix any remaining absolute paths.

**Step 2a: Copy all scripts**

```bash
mkdir -p reproduction/models reproduction/scripts
cp models/<Model>.fr reproduction/models/
cp -r workdir/models/<Model>_UFO reproduction/models/
cp scripts/*.mg5 reproduction/scripts/
cp scripts/*.ma5 reproduction/scripts/ 2>/dev/null || true
cp scripts/*.py reproduction/scripts/
cp analysis/*.py reproduction/scripts/ 2>/dev/null || true
```

The UFO directory (`workdir/models/<Model>_UFO/`) is the version that was generated and validated during the pipeline run. It must be included because agent-generated UFO models may contain fixes applied during the run that are not reproducible from the `.fr` file alone.

**Step 2b: Verify portability — check for absolute paths**

After copying, use `Grep` to check for any remaining absolute paths in the copied scripts:

```
Grep(pattern="/Users/|/home/|/tmp/", path="reproduction/scripts/", output_mode="content")
```

- **If no matches** → all scripts are portable, proceed to Step 3.
- **If matches found** → Grep returns the offending lines with content. Use `Edit` to replace those specific lines with relative-path equivalents (e.g., using `os.path.join(SCRIPT_DIR, ...)`). Do NOT `Read` the full file — the Grep output provides enough context for `Edit`.

**Files to `Write` (new)** — only files that don't exist in the pipeline:

| File | Purpose |
|------|---------|
| `reproduction/scripts/generate_ufo.wl` | WolframScript for local UFO generation |
| `reproduction/run_all.sh` | Dual-backend automation script |
| `reproduction/README.md` | Guide document |

### Step 3: Create the automation script (`run_all.sh`)

Write a bash script that executes the full pipeline end-to-end with **dual-backend support**:

```bash
#!/bin/bash
set -e

# Parse --magnus (default) or --local, and optional --from-fr
BACKEND="magnus"
FROM_FR=false
for arg in "$@"; do
    case $arg in
        --magnus)  BACKEND="magnus" ;;
        --local)   BACKEND="local" ;;
        --from-fr) FROM_FR=true ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORK_DIR="${SCRIPT_DIR}/workdir"
MG5_BIN="${MG5_BIN:-mg5_aMC}"
FR_PATH="${FR_PATH:-${HOME}/Library/Mathematica/Applications/FeynRules}"

mkdir -p "${WORK_DIR}/models" "${WORK_DIR}/events" "${WORK_DIR}/output/figures" "${WORK_DIR}/output/data"
```

Requirements for `run_all.sh`:

- **Dual backend**: each pipeline step has an `if [ "${BACKEND}" = "magnus" ]` branch selecting the correct tool
- **`--from-fr` flag**: when specified, regenerates UFO from the `.fr` file (useful if the user modifies the model). Without this flag, the script uses the pre-built UFO directory shipped in `models/<Model>_UFO/`
- **Configurable via environment variables**: `MG5_BIN`, `FR_PATH` (local mode), plus Magnus credentials via `magnus login` (Magnus mode)
- **Idempotent**: each step checks whether its output already exists and skips if so
- **Self-contained working directory**: all intermediate outputs go into `workdir/`
- **Clear progress output**: print section headers, backend name, and status for each step
- **Error handling**: use `set -e` to stop on first error

#### Backend-specific commands per step:

**Step 1 — UFO Model Setup:**

By default, the script copies the pre-built UFO directory from the reproduction package into `workdir/models/`. This is the recommended approach because the UFO model shipped in the package has been validated during the original pipeline run and may contain fixes that are not reproducible from the `.fr` file alone.

With `--from-fr`, the script regenerates UFO from the `.fr` file instead:

```bash
if [ "${FROM_FR}" = true ]; then
    # Regenerate UFO from .fr file
    if [ "${BACKEND}" = "magnus" ]; then
        magnus run validate-feynrules ...
        magnus run generate-ufo ...
    else
        cd workdir && wolframscript ../scripts/generate_ufo.wl
    fi
else
    # Default: use pre-built UFO
    cp -r "${SCRIPT_DIR}/models/<Model>_UFO" "${WORK_DIR}/models/"
fi
```

| Mode | Default (pre-built UFO) | `--from-fr` |
|------|------------------------|-------------|
| **Local** | `cp -r models/<Model>_UFO workdir/models/` | `cd workdir && wolframscript ../scripts/generate_ufo.wl` |
| **Magnus** | `cp -r models/<Model>_UFO workdir/models/` | `magnus run validate-feynrules -- --model <fr> --lagrangian <L>` then `magnus run generate-ufo -- --model <fr> --lagrangian <L> --output workdir/models/<Model>_UFO` |

**Step 2 — Process Compilation + Event Generation:**

| Local | Magnus |
|-------|--------|
| `cd workdir && ${MG5_BIN} ../scripts/mg5_<label>.mg5` (scripts already contain `output` + `launch` with relative paths) | `magnus run madgraph-compile -- --ufo <ufo_dir> --process "..." --output workdir/events/<process>` then `magnus run madgraph-launch -- --process workdir/events/<process> --commands "..." --output workdir/events/<process>` |

Key syntax differences between local and Magnus for parameter setting:

| What | Local mg5_aMC syntax | Magnus --commands syntax |
|------|---------------------|-------------------------|
| Set external parameter | `set <ParamName> <value>` | `set param_card <BLOCK> <CODE> <value>` |
| Set mass | `set <MassName> <value>` | `set param_card MASS <PDG> <value>` |
| Set width | `set <WidthName> Auto` | `set param_card DECAY <PDG> Auto` |
| Mass scan | `set <MassName> scan:[v1,v2,...]` | `set param_card MASS <PDG> scan:[v1,v2,...]` |
| State machine | No explicit `done` needed for no-shower | First `done` (enter param state) + final `done` (start run) |
| Systematics | On by default | Add `set use_syst False` to avoid LHAPDF issues |

These differences are critical — the `run_all.sh` must use the correct syntax for each backend.

**Step 4 — Plotting:**

Always runs locally via Python (same for both backends).

### Step 4: Write the guide document (`README.md`)

The README.md must contain the following sections, written in the language matching the user's conversation (e.g., Chinese if the user speaks Chinese):

---

#### Section 1: Overview
- One paragraph summarizing the physics goal and the pipeline
- **Run label**: the `<run_label>` this reproduction package corresponds to
- A simple ASCII flow diagram showing the pipeline stages
- Table summarizing the two supported backends

#### Section 2: Prerequisites
- **Common dependencies** (Python, numpy, matplotlib) — needed for both backends
- **Local mode dependencies**: MadGraph5 is always required. Mathematica/wolframscript and FeynRules are only required with `--from-fr`; without it, the pre-built UFO is used directly. Include verified versions.
- **Magnus mode dependencies** (`magnus-sdk` via pip, `magnus login` for authentication)
- Notes on installation paths and how to configure them

#### Section 3: File Inventory
- Table listing every file in the reproduction directory
- Include the `models/<Model>_UFO/` directory and note it contains the pre-built UFO model from the original run
- Annotate which files are backend-specific (e.g., `scripts/generate_ufo.wl` = local + `--from-fr` only)

#### Section 4: Automated Run
- **Default mode** (pre-built UFO): `bash run_all.sh --magnus` or `bash run_all.sh --local` — uses the validated UFO model shipped in the package, no Mathematica needed
- **From-FR mode**: `bash run_all.sh --magnus --from-fr` or `bash run_all.sh --local --from-fr` — regenerates UFO from the `.fr` file (requires Mathematica for local, or Magnus for cloud)
- Explain the difference: default is recommended because the shipped UFO has been validated; `--from-fr` is for users who modify the `.fr` model
- Description of what the script does at each stage for each backend
- Where to find the output
- **Disclaimer**: note that `run_all.sh` was auto-generated by ColliderAgent — each individual step has been verified, but the full end-to-end script has not been tested as a whole. Recommend running it inside a coding agent (Claude Code, Cursor, etc.) for convenient debugging.

#### Section 5: Step-by-Step Instructions
The following guide is for running the reproduction scripts step by step. You can also pass this guide to a coding agent (Claude Code, Cursor, etc.) to run it automatically.

For each pipeline step, provide **both local and Magnus commands** clearly separated:

- **What it does**: brief physics description
- **Input files**: which files from this directory are used
- **Local mode**: exact commands
- **Magnus mode**: exact `magnus run` commands
- **Key settings**: table of physics parameters and their values
- **Syntax differences**: highlight local vs Magnus parameter-setting differences (especially for MadGraph launch)
- **Validation**: how to check the step succeeded
- **Expected output**: file names and formats

#### Section 6: Expected Results
- Summary table of key numerical results from the original run
- Note on expected MC statistical uncertainty

#### Section 7: Notes and Caveats
- PDF set details and alternatives (including `--pdf` flag for Magnus)
- Magnus state machine explanation (number of `done` commands)
- Runtime estimates for both backends
- Physics-specific notes (e.g., Majorana warnings)

---

### Step 5: Final verification

After creating all files:

1. List the `reproduction/` directory to confirm all files are present
2. Verify no absolute paths remain in the portable scripts
3. Report the file listing to the user

## Rules

1. **Preserve physics exactly** — never modify Lagrangian terms, coupling values, process definitions, parameter scan ranges, plot styles, or any physics content.

2. **cp-first strategy** — `cp` all existing pipeline scripts and the UFO directory first. Then use `Grep` to check for absolute paths; if any are found, use `Edit` to fix only the matching lines. Only use `Write` for files that don't exist in the pipeline (`generate_ufo.wl`, `run_all.sh`, `README.md`). Never use `Write` to recreate an existing file.

3. **Path portability** — `run_all.sh` executes MG5 scripts via `cd workdir && ${MG5_BIN} ../scripts/mg5_<label>.mg5`. The scripts' relative paths (`events/...`, `models/...`) resolve correctly relative to `workdir/`. No hardcoded absolute paths in any file.

4. **Correct Magnus syntax** — Magnus `madgraph-launch` uses `set param_card BLOCK CODE VALUE` syntax (not `set ParamName value`). It requires explicit `done` commands for the state machine. Include `set use_syst False` to avoid LHAPDF issues on cloud. See the `madgraph-simulator` skill for the complete state machine specification.

5. **Language matching** — write the README in the same language the user has been using in the conversation. Code comments stay in English.

6. **Include actual results** — the README should contain numerical results from the original run as a verification reference.

7. **Organized directory** — `reproduction/` contains `models/`, `scripts/`, plus `README.md` and `run_all.sh` at the top level. `workdir/` is created at runtime following the standard pipeline layout.

8. **Idempotent automation** — `run_all.sh` must be safe to run multiple times. Each step checks for existing output.

9. **Minimal dependencies** — do not add dependencies beyond what the original pipeline used.

10. **Ship the validated UFO** — always include the UFO directory (`workdir/models/<Model>_UFO/`) that was generated and validated during the pipeline run. The default execution path in `run_all.sh` must use this pre-built UFO. UFO models generated by FeynRules can sometimes fail MadGraph import; the agent-generated version has already been fixed during the run, so it is the reliable default. The `--from-fr` flag provides an opt-in path to regenerate from the `.fr` file for users who modify the model.

11. **Read scripts, not progress files (orchestrator mode)** — in orchestrator mode, obtain run metadata and physics results (cross sections, paths, run names) from the conversation context — do NOT re-read `progress/<run_label>/step*.md` files, since the orchestrator already has this information from subagent returns. However, always `Read` the actual **script files** (`.mg5`, `.ma5`, `.py`, `.fr`) when you need to inspect or modify their content (e.g., for path portability checks). In standalone mode, read everything.
