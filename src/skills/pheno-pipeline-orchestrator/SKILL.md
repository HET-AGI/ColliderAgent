---
name: pheno-pipeline-orchestrator
description: >
  Orchestrate the full particle physics analysis pipeline using subagents.
  Triggers when the user asks to "execute an analysis", "run the full pipeline",
  "execute <filename>.md", or references an analysis prompt/plan .md file to
  execute end-to-end.
---

# Analysis Pipeline Orchestrator

You are the orchestrator for a particle physics analysis pipeline. When the user provides a task description (typically a .md file), you break it down and delegate each step to a specialized subagent.

## Pipeline

Execute the following steps **sequentially**, using the specified subagent for each. Pass intermediate results via the `progress/` directory.

### Step 1: Model Building → `model-generator` subagent
- Input: the Lagrangian and particle content from the user's task description
- The subagent generates .fr model → validates → produces UFO model
- Output: `progress/step1_feynrules.md`
- Extract from return: UFO path, particle names, PDG codes, parameter block/code info

### Step 2: Event Generation → `collider-simulator` subagent
- Input: UFO path + particle info from step 1, plus collider settings from the task description
- The subagent compiles the process and generates Monte Carlo events
- Output: `progress/step2_madgraph.md`
- Extract from return: output directory, cross sections, event file paths

### Step 3: Event Analysis → `event-analyzer` subagent (if needed)
- Input: event file paths from step 2, analysis specifications from the task description
- The subagent runs MadAnalysis5 for kinematic distributions and cut-flow
- Output: `progress/step3_madanalysis.md`
- Skip this step if the task does not require MA5 analysis

### Step 4: Post-Processing → `pheno-analyzer` subagent
- Input: event files from step 2, experimental data and analysis procedure from the task description
- The subagent performs event selection, statistical analysis, and plotting
- Output: `progress/step4_postprocessing.md`
- Extract from return: physics results, plot file paths

## Rules

1. **Read the task file first** — understand the full scope before starting any step.
2. **Run steps sequentially** — each step depends on the previous step's output.
3. **Pass precise information** — when invoking each subagent, include all relevant details from the task description AND the previous step's return summary. The subagent has no access to the task file or conversation history.
4. **If a subagent's return summary is insufficient**, read the corresponding `progress/stepN_*.md` file for complete details before proceeding.
5. **Skip steps that are not needed** — not every task requires all 4 steps. For example, if the user already has a UFO model, skip step 1.
6. **Report final results** — after all steps complete, summarize the key physics results and plot locations to the user.
