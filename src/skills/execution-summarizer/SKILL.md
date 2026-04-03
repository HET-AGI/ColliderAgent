---
name: execution-summarizer
description: >
  Summarize the full execution of a collider physics analysis after all tasks are complete.
  Triggers automatically at the end of a pipeline run, or when the user asks to
  "summarize the run", "generate an execution report", or "what did the agent do".
---

# Execution Summarizer

## Overview

This skill produces a structured execution summary after the agent completes a user prompt. The summary covers **what was done, what results were obtained**, and provides a **detailed mapping between the user's physics specification and the generated code/scripts**.

## When to Invoke

Invoke this skill **after the entire user prompt has been fulfilled** — i.e., after all pipeline steps (model building, event generation, analysis, post-processing) or standalone tasks have finished.

## Run Discovery

This skill can be invoked in two ways:

1. **By the orchestrator** at the end of a pipeline run — the conversation already contains context (run label, progress paths, results). Use that context directly.
2. **Standalone** in a new conversation — no prior context is available. In this case:
   - Read `progress/run_manifest.yaml` to discover all completed runs.
   - If the user specified a run label, summarize that run.
   - If there is only one run, summarize that run.
   - If there are multiple runs and the user did not specify, summarize the most recent run (by timestamp).

## Workflow

### Step 1: Collect Execution Artifacts (standalone mode only)

Skip this step if invoked by the orchestrator — the conversation already contains all needed context.

In standalone mode, gather information from the target run identified in Run Discovery:

- The original user prompt / task file (`.md`)
- Progress files from the target run's directory `progress/<run_label>/` (e.g., `step1_feynrules.md`, `step2_madgraph.md`, `step3_madanalysis.md`, `step4_postprocessing.md`)
- Generated code files: `.fr` model files, MadGraph scripts, MadAnalysis scripts, Python analysis scripts
- Output logs and result files: cross sections, event files, plots

### Step 2: Write the Execution Summary

**File naming**:
- For the **initial run** (no `parent` field in manifest): create **`execution_summary.md`** in the working directory.
- For **incremental runs** (has a `parent` field): create **`execution_summary_<run_label>.md`** (e.g., `execution_summary_heavyN_xsec_scan_11TeV.md`). Do NOT overwrite the initial `execution_summary.md` or any previous incremental summary.

The summary must contain the following sections:

---

#### Section 1: Run Info

- **Run label**: the `<run_label>` from the manifest or orchestrator context
- **Timestamp**: when the run was executed

#### Section 2: Task Overview

A brief paragraph describing what the user requested and the overall outcome.

#### Section 3: Execution Steps

A numbered list of every major action the agent performed, including:

- Which skill or subagent was invoked
- Key input parameters
- Key outputs and results (cross sections, file paths, plot locations, etc.)
- Any errors encountered and how they were resolved

Example format:

```
1. **Model Building** (feynrules-model-generator → feynrules-model-validator → ufo-generator)
   - Generated `models/MyModel.fr` with 2 new particles (S1, S2) and 3 couplings
   - Validation: passed (Hermiticity ✓, mass diagonalization ✓)
   - UFO output: `models/MyModel_UFO/`

2. **Event Generation** (madgraph-simulator)
   - Process: `p p > s1 s1~, s1 > t t~`
   - √s = 14 TeV, 50k events
   - Cross section: 12.3 ± 0.2 fb
   - Script: `scripts/mg5_14TeV.mg5`
   - Events: `events/pp_s1s1/Events/run_01/`
   ...
```

#### Section 4: Prompt-to-Code Mapping Tables

This is the **core section**. Build one mapping table per pipeline stage, showing how each element in the user prompt corresponds to the generated code.

**Table A: Lagrangian ↔ FeynRules `.fr` File**

Map each term in the user's LaTeX Lagrangian to the corresponding FeynRules code in the `.fr` file.

| User Prompt (LaTeX) | FeynRules Code (`.fr`) | Notes |
|---|---|---|
| $y_S \bar{Q}_L S t_R$ | `yS * QLbar.S.tR` | Yukawa coupling, left-handed |
| $\|D_\mu S\|^2$ | `DC[Sbar, mu] * DC[S, mu]` | Covariant derivative, kinetic term |
| $M_S$ = 1 TeV | `MS -> {MS, 1000}` in M$Parameters | External mass parameter |
| ... | ... | ... |

**Table B: Physics Process ↔ MadGraph Script**

Map the user-specified collider process and settings to the MadGraph commands.

| User Prompt | MadGraph Command / Parameter | Notes |
|---|---|---|
| $pp \to S \bar{S}$ at 14 TeV | `generate p p > s1 s1~` | Main process |
| $\sqrt{s}$ = 14 TeV | `set ebeam1 7000` / `set ebeam2 7000` | Beam energy |
| 50,000 events | `set nevents 50000` | Event count |
| $M_S$ scan: 500–2000 GeV | `set MS 500`, `set MS 1000`, ... | Parameter scan points |
| ... | ... | ... |

**Table C: Analysis Cuts ↔ MadAnalysis / Analysis Script** (if applicable)

Map the user-specified event selection criteria to the analysis code.

| User Prompt | Analysis Code | Notes |
|---|---|---|
| $p_T(\ell) > 25$ GeV | `select (PT(l) > 25)` | Lepton pT cut |
| $\|\eta(\ell)\| < 2.5$ | `select (ABSETA(l) < 2.5)` | Lepton pseudorapidity |
| $M_{\ell\ell} > 120$ GeV | `select (M(l+ l-) > 120)` | Dilepton invariant mass |
| ... | ... | ... |

**Only include tables that are relevant to the executed steps.** If a step was skipped (e.g., no MadAnalysis was run), omit the corresponding table.

#### Section 5: Output Files

A list of all key output files produced, with their paths and brief descriptions.

```
- execution_summary.md (or execution_summary_<run_label>.md for incremental runs) — this summary
- models/MyModel.fr                 — FeynRules model file
- models/MyModel_UFO/               — UFO model directory
- scripts/mg5_14TeV.mg5             — MadGraph script
- scripts/plot_mll.py               — analysis script
- events/pp_s1s1/Events/run_01/     — generated events (LHE + HepMC)
- output/figures/mll_distribution.pdf — dilepton invariant mass plot
```

---

### Step 3: Report to User

After writing `execution_summary.md`, inform the user that the summary has been generated and print a brief highlight of the key results (cross sections, plot locations, etc.).

## Rules

1. **Be precise** — use actual file names, actual parameter values, and actual code snippets from the generated files. Do not paraphrase or approximate.
2. **Read scripts, not progress files (orchestrator mode)** — in orchestrator mode, obtain run metadata and physics results (cross sections, event counts, run names) from the conversation context — do NOT re-read `progress/<run_label>/step*.md` files, since the orchestrator already has this information from subagent returns. However, always `Read` the actual **code files** (`.fr`, `.mg5`, `.ma5`, `.py`) to extract exact code snippets, line numbers, and parameter values for the mapping tables. In standalone mode, read everything.
3. **Keep it concise** — the summary should be informative but not excessively long. Focus on the mapping tables and key results.
4. **Handle partial pipelines** — if only some steps were executed (e.g., only model building), only include the relevant sections and tables.
5. **Use LaTeX notation** in the "User Prompt" column of the mapping tables for readability.
