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

Create a **single directory** (default: `reproduction/`) containing all files needed to reproduce the analysis. Everything must be self-contained — no file should depend on paths outside this directory at rest (paths are configured at run time).

```
reproduction/
├── README.md                  # Main guide document (see Section 4)
├── run_all.sh                 # One-click automation script (supports --local and --magnus)
├── <model>.fr                 # FeynRules model file
├── generate_ufo.wl            # WolframScript for UFO generation (local mode only)
├── mg5_compile.dat            # MadGraph process compilation script (local step-by-step only)
├── mg5_launch_<label>.dat     # MadGraph launch scripts (local step-by-step only)
├── <analysis>.py              # Python analysis/plotting script(s)
└── ...                        # Any other scripts used in the pipeline
```

## Workflow

### Step 1: Inventory the completed run

Read all progress files and identify which pipeline steps were executed:

- Step 1 (Model Building): look for `progress/step1_feynrules.md`, `.fr` files in `models/`
- Step 2 (Event Generation): look for `progress/step2_madgraph.md`, MadGraph `.dat` scripts, output directories
- Step 3 (Event Analysis): look for `progress/step3_madanalysis.md` (may not exist)
- Step 4 (Post-Processing): look for `progress/step4_postprocessing.md`, Python scripts in `analysis/`

Also read the original task/prompt file for context.

### Step 2: Collect and adapt scripts

For each pipeline step that was executed:

1. **Read the original script/file** from its current location
2. **Create a portable copy** in `reproduction/` with the following adaptations:
   - **`.fr` model files**: use `cp` via Bash to copy verbatim — do NOT use Write to rewrite identical content (saves tokens)
   - For all other files that need path changes, replace all **hardcoded absolute paths** with either:
     - Placeholder tokens (e.g., `<UFO_PATH>`, `<OUTPUT_PATH>`) for MadGraph `.dat` scripts
     - Command-line arguments or environment variables for shell/Python scripts
     - Relative paths where appropriate
   - Keep all physics content (Lagrangian terms, parameters, process definitions, cuts, plot styles) **exactly as-is** — do not modify any physics
   - Preserve comments that explain the physics

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
| `wolframscript -code '...'` (inline FeynRules script) | `magnus run validate-feynrules -- --model <fr> --lagrangian <L>` then `magnus run generate-ufo -- --model <fr> --lagrangian <L> --output <ufo_dir>` |

**Step 2 — Process Compilation:**

| Local | Magnus |
|-------|--------|
| Write a `.dat` script, then `mg5_aMC script.dat` | `magnus run madgraph-compile -- --ufo <ufo_dir> --process "..." --output <mg5_dir>` |

**Step 3 — Event Generation (launch):**

| Local | Magnus |
|-------|--------|
| Write a `.dat` launch script with `set <param> <value>` syntax, then `mg5_aMC script.dat` | `magnus run madgraph-launch -- --process <mg5_dir> --commands "done\nset ...\ndone" --output <mg5_dir>` |

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
- Annotate which files are backend-specific (e.g., `generate_ufo.wl` = local only, `mg5_compile.dat` = local step-by-step only)

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

2. **Path portability** — no hardcoded absolute paths in any script except `run_all.sh` (which constructs them from `SCRIPT_DIR` and environment variables). MadGraph `.dat` files use `<PLACEHOLDER>` tokens.

3. **Dual backend** — `run_all.sh` must support both `--local` and `--magnus` via a `BACKEND` variable. Every compute step branches on this variable. The README must document both paths with exact commands.

4. **Correct Magnus syntax** — Magnus `madgraph-launch` uses `set param_card BLOCK CODE VALUE` syntax (not `set ParamName value`). It requires explicit `done` commands for the state machine. Include `set use_syst False` to avoid LHAPDF issues on cloud. See the `madgraph-simulator` skill for the complete state machine specification.

5. **Language matching** — write the README in the same language the user has been using in the conversation. Code comments stay in English.

6. **Include actual results** — the README should contain numerical results from the original run as a verification reference.

7. **Single directory** — everything goes in one flat directory. Only `workdir/` is created at runtime.

8. **Idempotent automation** — `run_all.sh` must be safe to run multiple times. Each step checks for existing output.

9. **Minimal dependencies** — do not add dependencies beyond what the original pipeline used.

10. **Read, don't recall** — always read the actual files from the completed run. Do not rely on conversation memory.
