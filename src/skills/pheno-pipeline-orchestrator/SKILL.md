---
name: pheno-pipeline-orchestrator
description: >
  Orchestrate full particle-physics analysis pipelines with specialized subagents,
  run labels, progress tracking, and artifact handoffs. Use when the user asks to
  execute an analysis, run a full pipeline or analysis-plan Markdown file, combine
  two or more stages (model building, event generation, event analysis, plotting,
  statistical analysis, or reproduction packaging), or propagate an upstream change
  through downstream results. Do not use for a request confined to one pipeline stage.
---

# Analysis Pipeline Orchestrator

You are the orchestrator for a particle physics analysis pipeline. When the user provides a task description (typically a .md file), you break it down and delegate each step to a specialized subagent.

## Standard Directory Layout (reference)

Each subagent's skill defines its own output paths. The combined layout is:

```
<working_dir>/
├── models/          # Step 1 (feynrules-model-generator)
├── scripts/         # Steps 2/3/4 (all executable scripts)
├── events/          # Step 2 (madgraph-simulator)
├── analysis/        # Step 3 (madanalysis-analyzer)
├── output/          # Step 4 (pheno-analyzer)
│   ├── figures/
│   └── data/
├── progress/        # Orchestrator tracking
│   ├── run_manifest.yaml   # Index of all runs
│   └── <run_label>/        # Per-run progress files
├── reproduction/    # reproduction-guide-generator
└── execution_summary.md
```

## Run Initialization

Before executing any pipeline step:
1. Generate a short, descriptive **run label** from the task content (e.g., `dy_14tev_50k`, `heavyN_scan_7TeV`).
2. If `progress/run_manifest.yaml` exists and already contains a run with the same label, append a short timestamp to disambiguate (e.g., `dy_14tev_50k_1432`).
3. Create the directory `progress/<run_label>/`.
4. Read `progress/run_manifest.yaml` if it exists; otherwise create it.
5. Add a new run entry to the manifest:
   ```yaml
   - label: <run_label>
     timestamp: "<ISO 8601>"
     task: "<one-line task description>"
     steps: {}
   ```

## Incremental Runs

When the user's request modifies or extends a **previous run** (e.g., "add more events", "re-run with different cuts", "increase statistics and update the plot"), this is an **incremental run**. The orchestrator must still manage run labels, scripts, and progress — the same structure as a fresh run, but reusing upstream artifacts.

### Detection

An incremental run is identified when:
- The conversation already contains results from a prior run, OR
- `progress/run_manifest.yaml` contains completed runs for the same process
- AND the user requests a modification + downstream update (not a fresh start)

### Run Labeling

Create a **new run label** that references the parent run, e.g.:
- Parent: `dy_ll_14tev` → Incremental: `dy_ll_14tev_add10k` or `dy_ll_14tev_100k`
- This ensures full traceability; never silently overwrite a previous run's progress files.

### Artifact Reuse

Read the parent run's progress files to identify reusable artifacts:
- **Compiled process directory** — if the physics process is unchanged, reuse it (skip `madgraph-compile`; only run `madgraph-launch` for additional events)
- **UFO model** — if the Lagrangian is unchanged, skip Step 1 entirely
- **Analysis scripts** — if only statistics changed, the MA5/plotting scripts may need only path updates

### Script Generation

Even for incremental runs, the collider-simulator subagent **must generate a new script file** (e.g., `scripts/mg5_dy_14tev_run02.mg5`). This ensures:
1. The exact parameters of the incremental run are recorded
2. The reproduction package can replay this specific run
3. Parameter overrides (e.g., `nevents 10000`) are explicitly written, not inherited from a previous run_card

When passing instructions to the collider-simulator subagent for an incremental launch, explicitly state:
- That a compiled process directory already exists (give the path)
- That a NEW script must still be generated with the incremental parameters
- The exact `nevents` and any changed parameters — do NOT rely on the existing run_card defaults

### Pipeline Execution

Execute only the **affected steps and all downstream steps**:

| User Request | Steps to Execute |
|---|---|
| "Add more events + update plot" | Step 2 (launch only) → Step 3 → Step 4 |
| "Change analysis cuts + update plot" | Step 3 → Step 4 |
| "Re-run with different mass + full pipeline" | Step 2 (compile + launch) → Step 3 → Step 4 |
| "Update plot style only" | Step 4 only |

For each executed step, write progress files under `progress/<new_run_label>/` and update the manifest.

### Manifest Entry

Add a `parent` field to link incremental runs to their origin:
```yaml
- label: dy_ll_14tev_add10k
  parent: dy_ll_14tev
  timestamp: "<ISO 8601>"
  task: "Add 10k events to Drell-Yan run and update figure"
  steps: {}
```

## Pipeline

Execute the following steps **sequentially**, using the specified subagent for each. Pass intermediate results via the `progress/` directory.

### Codex delegation

On the Codex adapter branch, use the project-scoped custom agents with the exact
names shown below. Spawn only the next required stage, wait for it to finish,
inspect its concise return and progress artifact, and then construct the next
stage's prompt. Do not run dependent or write-heavy stages concurrently. If a
stage needs clarification or a retry, steer that same agent before starting its
consumer.

### Step 1: Model Building → `model-generator` subagent
- Input: the Lagrangian and particle content from the user's task description
- The subagent generates .fr model → validates → produces UFO model
- Output: `progress/<run_label>/step1_feynrules.md`
- Extract from return: UFO path (e.g. `models/SM_HeavyN_UFO`), model file path (e.g. `models/HeavyN.fr`), particle names, PDG codes, parameter block/code info

### Step 2: Event Generation → `collider-simulator` subagent
- Input: UFO path + particle info from step 1, plus collider settings from the task description
- The subagent compiles the process and generates Monte Carlo events
- Output: `progress/<run_label>/step2_madgraph.md`
- Extract from return: script paths (e.g. `scripts/mg5_7TeV.mg5`), process dirs (e.g. `events/pp_muN_7TeV`), run name ↔ parameter mapping
- **Do NOT extract physics results** (cross sections, widths, etc.) — leave that to downstream subagents who will read the output files directly

### Step 3: Event Analysis → `event-analyzer` subagent (if needed)
- Input: event file paths from step 2, analysis specifications from the task description
- The subagent runs MadAnalysis5 for kinematic distributions and cut-flow
- Output: `progress/<run_label>/step3_madanalysis.md`
- Extract from return: script path (e.g. `scripts/ma5_dilepton.ma5`), analysis dir (e.g. `analysis/dilepton_mass`), histogram path
- Skip this step if the task does not require MA5 analysis

### Step 4: Post-Processing → `pheno-analyzer` subagent
- Input: output directory path(s) and run ↔ parameter mapping from the latest upstream step (step 3 if executed, otherwise step 2), plus analysis procedure from the task description
- The subagent reads simulation/analysis output files directly, extracts the physics results it needs (cross sections, kinematic distributions, etc.), performs analysis, and produces plots
- Output: `progress/<run_label>/step4_postprocessing.md`
- Extract from return: script path (e.g. `scripts/plot_xsec_vs_mass.py`), figure files (e.g. `output/figures/figure_3.pdf`), data files (if any)

## Rules

1. **Read the task file first** — understand the full scope before starting any step.
2. **Run steps sequentially** — each step depends on the previous step's output.
3. **Pass precise information** — when invoking each subagent, include all relevant details from the task description AND the previous step's return summary. Tell the subagent the progress file path to write to (e.g., `progress/<run_label>/step2_madgraph.md`). Do not assume that inherited conversation context contains the exact inputs the stage needs.
4. **If a subagent's return summary is insufficient**, read the corresponding `progress/<run_label>/stepN_*.md` file for complete details before proceeding.
5. **Skip steps that are not needed** — not every task requires all 4 steps. For example, if the user already has a UFO model, skip step 1.
6. **Generate execution summary** — after all steps complete, invoke the `execution-summarizer` skill to produce a detailed `execution_summary.md` with prompt-to-code mapping tables and key results.
7. **Update manifest after each step** — after a subagent completes, update the run's entry in `progress/run_manifest.yaml` with the step's status (success/failed).

## Separation of Concerns

The orchestrator manages **paths and scheduling**, not physics results:

- **Step 1 → Step 2**: pass UFO path, particle names, PDG codes, parameter block names — structural info needed to write MadGraph scripts.
- **Step 2 → Step 3/4**: pass output directory path(s) and a run name ↔ parameter mapping (e.g., `run_01 → MZp=200, run_02 → MZp=400`). Do NOT parse MadGraph logs for cross sections or other physics quantities.
- **Step 3/4 subagents** are responsible for reading the simulation output files themselves and extracting whatever physics results the task requires.


## Remote Magnus Execution

Use the persisted remote `zhustation` site for every compute stage so harness
comparisons share the same execution backend.

1. Run `magnus config` before the first compute stage. Require
   `Current: zhustation` and an HTTPS address.
2. Never run `magnus local start`, select a localhost site, or fall back to
   locally installed HEP tools.
3. If the remote station is unreachable, retry at most twice with a 20-second
   interval. Avoid copying a large HTML error response into the conversation.
4. If both retries fail, stop the affected stage and report the remote-service
   failure. Preserve the run manifest and completed upstream artifacts so the
   run can resume without resubmitting successful jobs.
5. Never print, copy, or commit the Magnus token.
