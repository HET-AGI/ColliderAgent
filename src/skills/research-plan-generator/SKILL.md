---
name: research-plan-generator
description: >
  Generate an executable research plan (.md) for a collider phenomenology study.
  Triggers when the user asks to "make a research plan", "design a collider study",
  "plan an analysis for this model", or wants an idea, a research target, or a paper's
  model turned into a concrete task specification — model Lagrangian, collider process,
  simulation settings, parameter scan, event selection, statistical analysis, and figures.
  The plan follows the task-prompt format that the pheno-pipeline-orchestrator executes,
  so it can be run directly with "Execute the analysis following <plan>.md".
  Do NOT trigger when the user already has a complete task prompt and wants it executed.
---

# Research Plan Generator

## Overview

This skill turns a research target (a model plus a physics question) into a **research plan**: a self-contained Markdown specification that the downstream pipeline — model-generator → collider-simulator → event-analyzer → pheno-analyzer, driven by the pheno-pipeline-orchestrator skill — can execute without further physics input.

Inputs, any of:
- a target from `research/<study_label>/targets.md` (research-target-finder skill)
- a model the user specified directly (Lagrangian, well-known model name, or paper)

This is a **pure planning task** — no Magnus blueprints are involved. Web access is used to retrieve experimental inputs (search selections, HEPData tables); see the research-target-finder skill's `references/literature_search.md` for API recipes and the citation verification protocol.

## Output Paths

All paths are **relative to the working directory**.

| Output | Path pattern | Example |
|--------|-------------|---------|
| Research plan | `research/<study_label>/plans/plan_<nn>_<slug>.md` | `research/rd_anomaly_lq/plans/plan_01_u1_monotau_recast.md` |
| Experimental data for the plan | `research/<study_label>/data/<file>` | `research/rd_anomaly_lq/data/ins1649273_table1.csv` |

`<nn>`: two-digit number in recommended execution order. `<slug>`: model + strategy, e.g. `u1_monotau_recast`, `zp_hllhc_projection`.

## Workflow

Work through these steps **one at a time**, starting from a copy of [templates/research_plan.md](templates/research_plan.md). Read [references/pipeline_capabilities.md](references/pipeline_capabilities.md) before Step 2.

### Step 1: Fix the Question and the Deliverable

Plan backwards from the result. State the physics question in one sentence, then the figure or table that answers it (axes, curves, bands). Everything else in the plan exists to produce that deliverable.

**One plan = one pipeline run = one coherent simulation campaign.** If the study needs different processes, colliders, or analyses, write several plans, number them in execution order, and declare dependencies (a later plan can reuse the UFO model of an earlier one and skip model building).

### Step 2: Choose the Strategy

Pick from Section 6 of the capability reference — signal characterization, recast of an existing search, limit reinterpretation, sensitivity projection, collider + dark matter complementarity. For a new model, a cheap characterization plan (cross sections, branching ratios, key distributions) first is usually worth it: it validates the model and informs the scan ranges of the expensive plan.

### Step 3: Write the Model Section

- Take the Lagrangian from the target report. If the user supplied the model, bring it into pipeline-ready form following Section 4 of the research-target-finder skill's `references/model_building_guide.md`
- Define every symbol. The model builder has no other source: if a field's quantum numbers, a coupling's reality, or a chirality is not in the plan, it will be guessed
- Include only what this study needs — couplings irrelevant to the process can be dropped (say so), which makes model validation faster and safer

### Step 4: Define the Process

- Physics notation plus the subtleties the MadGraph process string must capture: heavy flavours in the proton, charge conjugates, resonant vs non-resonant contributions, interference with the SM, on-shell decay chains vs MadSpin
- Check that the process exists at tree level in the model as written. If it is loop-induced, the effective vertex must be in the Lagrangian (Step 3)

### Step 5: Simulation Settings and Parameter Strategy

- Collider and $\sqrt s$, events per point, PDF, shower, detector card, output format — each stated explicitly. Match the level to the analysis: parton level suffices for total cross sections; selections on reconstructed objects need Pythia8 + Delphes (request LHCO output)
- Benchmarks and scans: justify ranges from constraints and estimates (target report Section 3; guide Section 7). Exploit scaling laws — simulate at a reference coupling and rescale analytically where the dependence is a pure power
- Keep the campaign proportionate: (parameter points) × (runs) × (events). State the total in the Appendix

### Step 6: Specify the Analysis

- **Experimental data**: locate the search paper and its HEPData record; download the needed tables to `research/<study_label>/data/` and reference the file path in the plan; note luminosity and $\sqrt s$. Tell the analyst how to read each file (block and column names — HEPData CSVs are multi-block), which published regions are used, and which are left out and why. If no HEPData record exists, transcribe the numbers from the paper's table into the plan and cite the table
- **Selection**: copy object definitions and cuts from the experimental paper (cite section/table), including the exact definition of derived variables
- **Signal prediction**: the normalization formula, where the cross section comes from, K-factors with source
- **Statistics**: a complete prescription — likelihood or test statistic, nuisance treatment, combination, and the numerical criterion that defines the result
- **Backgrounds** (projections only): each process, its generation settings, and K-factor

### Step 7: Specify the Figures

Every element (curve, band, shaded region) with its origin and style; axes with labels, units, ranges, scales. Analytic overlays need closed-form expressions and input values with sources — the pipeline does not compute flavour or precision observables.

### Step 8: Add Validation

For recasts and reinterpretations, include a validation target the experiment itself provides (benchmark-signal yields, efficiencies, or a published limit to reproduce). Validate at the level of signal-region yields, not generator-level quantities. State the tolerance, and that a failed validation is reported rather than tuned away. A calibration constant (e.g. for a tagging rate the paper does not quote) is allowed only if the plan declares it up front, fixes it on a stated subset of the validation points, and tests it on the rest.

Where possible, test the plan's statistical prescription **now**: feed it the experiment's own published signal yields and check that it reproduces the published limit. This costs minutes, needs no simulation, and catches a wrong likelihood before an expensive campaign. Quote the result in the Appendix.

### Step 9: Self-Review

Run the checklist below. Then re-read the plan as each downstream subagent in turn, asking: "could I do my step with only this document?"

### Step 10: Save

Write the plan to its output path. Fill the Appendix (rationale, approximations, expected outcome, verified references).

## Self-Review Checklist

**Completeness**
- [ ] Deliverable stated concretely (which figure, which axes)
- [ ] Every new field: spin/type, colour, $SU(2)_L$, $Y$, $Q$, self-conjugate or not, name ≥ 2 characters
- [ ] Every coupling: real/complex, dimension, value; "+ h.c." explicit; chirality explicit; free (external) vs derived (internal) parameters distinguished, derived ones with formulas and sourced constants
- [ ] Deviations from the pipeline's SM defaults (diagonal CKM, massless light fermions, massive $b$) stated, or "defaults" stated
- [ ] Process, collider, $\sqrt s$, events, PDF, shower, detector, output format, scan points — all explicit
- [ ] Width treatment stated for every unstable BSM particle
- [ ] Selection, binning, luminosity, normalization formula, statistical criterion — all explicit
- [ ] Experimental numbers present in the plan or in a referenced file that exists
- [ ] Figure elements, axes, ranges, scales specified

**Correctness**
- [ ] Each Lagrangian term is a Lorentz scalar, colour singlet, electrically neutral, with consistent mass dimension — do the charge and colour bookkeeping term by term (field vs conjugate-field slips are the classic error)
- [ ] $SU(2)_L$-partner and CKM-induced couplings included, or dropped explicitly with an estimate of the effect
- [ ] The process is allowed at tree level by the Lagrangian as written
- [ ] Benchmark points are not already excluded (or that is the point of the study — say so); couplings perturbative; $\Gamma/M$ consistent with the treatment used
- [ ] Scaling laws used for rescaling are exact for the process (no interference term neglected silently)
- [ ] Units everywhere (GeV, fb, fb$^{-1}$)

**Feasibility**
- [ ] Nothing outside `references/pipeline_capabilities.md`; approximations (LO, fast simulation, K-factors) stated in the Appendix
- [ ] Event numbers sufficient after selection; campaign size proportionate

**Integrity**
- [ ] Every reference verified in this session; every experimental number has a source
- [ ] Own estimates marked `[estimate]`, analysis choices not fixed by a source marked `[assumed]`, unverifiable facts marked `[unverified]`
- [ ] Every `[estimate]` recomputed once before saving

## Key Conventions

- **Self-contained**: downstream subagents have no access to the target report, the literature, or the conversation. Refer to files only by paths that exist in the working directory
- **Explicit over elegant**: never write "suitable cuts", "standard settings", "an appropriate range". Write the numbers
- **Format**: keep the section structure of the template (`1. Target`, `2. Model`, `3. Collider Simulation`, `4. Numerical Analysis`) — it is the format of the task prompts the orchestrator is built around. LaTeX for all formulae
- **English**: plans are written in English regardless of the user's language
- **Honest scope**: if the ideal study is not executable with the pipeline, plan the best executable version and state the gap in the Appendix — do not plan steps the pipeline cannot run
- **No execution**: this skill ends when the plan is saved. Running it is the orchestrator's job ("Execute the analysis following `<plan path>`")
