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

## Inputs

This skill reads artifacts from the completed run:

1. **Original task file** (e.g., `prompt_*.md`) — the physics specification
2. **Progress files** in `progress/` — step-by-step records of what was done
3. **Generated code files** — `.fr` model files, MadGraph `.dat` scripts, Python analysis scripts
4. **Output results** — scan summary files, plots, cross section tables

## Output Structure

Create a `reproduction/` directory with the following structure. Everything must be self-contained — no file should depend on paths outside this directory at rest (paths are configured at run time).

```
reproduction/
├── README.md                      # Main guide document
├── run_all.sh                     # One-click automation script (--local / --magnus)
├── models/                        # Model files
│   └── <Model>.fr                 # FeynRules model file (cp from models/)
└── scripts/                       # All executable scripts
    ├── generate_ufo.wl            # WolframScript for UFO generation (Write — new file)
    ├── mg5_<label>.mg5            # MadGraph scripts (cp from scripts/)
    ├── ma5_<label>.ma5            # MadAnalysis scripts (cp from scripts/, if used)
    └── plot_<desc>.py             # Python analysis scripts (cp from scripts/)
```

At runtime, `run_all.sh` creates a `workdir/` following the standard pipeline layout:

```
reproduction/workdir/              # created at runtime
├── models/<Model>_UFO/            # generated UFO model
├── events/<process_label>/        # MadGraph output + events
├── analysis/<label>/              # MadAnalysis output (if used)
└── output/
    ├── figures/                   # plots
    └── data/                      # data tables
```

## Workflow

### Step 1: Inventory the completed run

Read all progress files and identify which pipeline steps were executed:

Read `progress/run_manifest.yaml` to identify the relevant run(s) and their progress file locations. Each run's files are in `progress/<run_label>/`:
- Step 1 (Model Building): `step1_feynrules.md`, `.fr` files in `models/`
- Step 2 (Event Generation): `step2_madgraph.md`, MadGraph scripts, output directories
- Step 3 (Event Analysis): `step3_madanalysis.md` (may not exist)
- Step 4 (Post-Processing): `step4_postprocessing.md`, plotting scripts in `scripts/`, event-level analysis scripts in `analysis/`

Also read the original task/prompt file for context.

### Step 2: Collect scripts (cp-first strategy)

Because all pipeline scripts already use **relative paths**, most files can be copied verbatim. Only 3 files need to be created from scratch.

**Files to `cp` (via Bash)** — do NOT rewrite with Write tool:

| Source | Destination | Notes |
|--------|-------------|-------|
| `models/<Model>.fr` | `reproduction/models/<Model>.fr` | Model file, verbatim |
| `scripts/mg5_*.mg5` | `reproduction/scripts/` | MadGraph scripts, already use relative paths |
| `scripts/ma5_*.ma5` | `reproduction/scripts/` | MadAnalysis scripts (if used) |
| `scripts/plot_*.py` | `reproduction/scripts/` | Plotting scripts, already use relative paths |
| `analysis/*.py` | `reproduction/scripts/` | Event-level analysis scripts (if any) |

```bash
mkdir -p reproduction/models reproduction/scripts
cp models/<Model>.fr reproduction/models/
cp scripts/*.mg5 reproduction/scripts/
cp scripts/*.py reproduction/scripts/
cp analysis/*.py reproduction/scripts/ 2>/dev/null || true   # if event-level analysis was used
# cp scripts/*.ma5 reproduction/scripts/   # if MA5 was used
```

**Files to Write (new)** — these don't exist in the pipeline:

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

# Parse --magnus (default) or --local
BACKEND="magnus"
for arg in "$@"; do
    case $arg in
        --magnus) BACKEND="magnus" ;;
        --local)  BACKEND="local" ;;
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
- **Configurable via environment variables**: `MG5_BIN`, `FR_PATH` (local mode), plus Magnus credentials via `magnus login` (Magnus mode)
- **Idempotent**: each step checks whether its output already exists and skips if so
- **Self-contained working directory**: all intermediate outputs go into `workdir/`
- **Clear progress output**: print section headers, backend name, and status for each step
- **Error handling**: use `set -e` to stop on first error

#### Backend-specific commands per step:

**Step 1 — UFO Generation:**

| Local | Magnus |
|-------|--------|
| `cd workdir && wolframscript ../scripts/generate_ufo.wl` | `magnus run validate-feynrules -- --model <fr> --lagrangian <L>` then `magnus run generate-ufo -- --model <fr> --lagrangian <L> --output workdir/models/<Model>_UFO` |

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
- A simple ASCII flow diagram showing the pipeline stages
- Table summarizing the two supported backends

#### Section 2: Prerequisites
- **Common dependencies** (Python, numpy, matplotlib) — needed for both backends
- **Local mode dependencies** (Mathematica/wolframscript, FeynRules, MadGraph5) with verified versions
- **Magnus mode dependencies** (`magnus-sdk` via pip, `magnus login` for authentication)
- Notes on installation paths and how to configure them

#### Section 3: File Inventory
- Table listing every file in the reproduction directory
- Annotate which files are backend-specific (e.g., `scripts/generate_ufo.wl` = local only)

#### Section 4: Quick Start (one-click)
- **Local mode** example with environment variables
- **Magnus mode** example with `magnus login` prerequisite
- Description of what the script does at each stage for each backend
- Where to find the output

#### Section 5: Step-by-Step Instructions
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

2. **cp-first strategy** — pipeline scripts already use relative paths. Copy them with `cp` via Bash. Only `generate_ufo.wl`, `run_all.sh`, and `README.md` need to be created with Write.

3. **Path portability** — `run_all.sh` executes MG5 scripts via `cd workdir && ${MG5_BIN} ../scripts/mg5_<label>.mg5`. The scripts' relative paths (`events/...`, `models/...`) resolve correctly relative to `workdir/`. No hardcoded absolute paths in any file.

4. **Correct Magnus syntax** — Magnus `madgraph-launch` uses `set param_card BLOCK CODE VALUE` syntax (not `set ParamName value`). It requires explicit `done` commands for the state machine. Include `set use_syst False` to avoid LHAPDF issues on cloud. See the `madgraph-simulator` skill for the complete state machine specification.

5. **Language matching** — write the README in the same language the user has been using in the conversation. Code comments stay in English.

6. **Include actual results** — the README should contain numerical results from the original run as a verification reference.

7. **Organized directory** — `reproduction/` contains `models/`, `scripts/`, plus `README.md` and `run_all.sh` at the top level. `workdir/` is created at runtime following the standard pipeline layout.

8. **Idempotent automation** — `run_all.sh` must be safe to run multiple times. Each step checks for existing output.

9. **Minimal dependencies** — do not add dependencies beyond what the original pipeline used.

10. **Read, don't recall** — always read the actual files from the completed run. Do not rely on conversation memory.
