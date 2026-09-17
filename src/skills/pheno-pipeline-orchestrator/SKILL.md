---
name: pheno-pipeline-orchestrator
description: Orchestrate a multi-stage collider-phenomenology analysis (model building, event generation, event analysis, statistics and plotting, reproduction packaging) with specialized subagents, run labels, and progress records. Use when a request spans two or more stages, asks to execute an analysis plan (.md) end to end, or changes an upstream stage and needs the downstream results refreshed. Not for a request confined to one stage.
---

# Pipeline Orchestrator

You coordinate the pipeline; the subagents do the physics. You own run labels, the `progress/` record, what each subagent is told, and the final summary. You do not parse MadGraph logs, open event files, or extract physics numbers yourself: the stage that needs a number reads it from the files, and the sidecars below carry it forward.

## Workspace layout

```
<working_dir>/
├── models/          # Step 1: .fr and UFO / CalcHEP directories
├── scripts/         # every executable script the stages generate (mg5, ma5, python)
├── events/          # Step 2: compiled processes + Events/run_XX
├── analysis/        # Step 3 output and Step 4 event-level scripts
├── output/figures/  # Step 4 plots        output/data/  # tables
├── progress/
│   ├── run_manifest.yaml        # index of all runs
│   └── <run_label>/             # stepN_<stage>.md + stepN_<stage>.json + lessons.yaml
├── reproduction/    # reproduction-guide-generator (on request)
└── execution_summary.md
```

Scripts use paths relative to the working directory so they can be copied into a reproduction package unchanged.

## Run initialization

1. Derive a short run label from the task (`dy_14tev_50k`, `heavyN_scan_7TeV`). If `progress/run_manifest.yaml` already has that label, append `_HHMM`.
2. Create `progress/<run_label>/` and add the manifest entry:
   ```yaml
   - label: <run_label>
     timestamp: "<ISO 8601>"
     task: "<one line>"
     parent: <parent label>      # incremental runs only
     steps: {}                   # step name -> success | failed, updated after each stage
   ```

A request that modifies an earlier run (more events, different cuts, another mass) is an **incremental run**: give it a new label that references the parent (`dy_ll_14tev` → `dy_ll_14tev_100k`), reuse the parent's artifacts where the physics is unchanged (compiled process directory → launch only; unchanged Lagrangian → skip Step 1), and execute only the changed stage plus everything downstream. The stage subagent still writes a new script with the incremental parameters spelled out (`set nevents 100000`, not inherited from a run card), so the record and the reproduction package stay exact. Never overwrite a previous run's progress files.

## Stages and subagents

| Step | Subagent | Needs | Produces |
|---|---|---|---|
| 1 Model | `model-generator` | Lagrangian and particle content from the task | `models/…`, `step1_feynrules.{md,json}` |
| 2 Events | `collider-simulator` | UFO path + particle/parameter tables (step 1 sidecar), collider settings, scan points, shower/detector/format requests | `scripts/mg5_*.mg5`, `events/…`, `step2_madgraph.{md,json}` |
| 3 MA5 analysis (optional) | `event-analyzer` | event paths + run↔parameter map (step 2 sidecar), distributions and cuts | `scripts/ma5_*.ma5`, `analysis/…`, `step3_madanalysis.{md,json}` |
| 4 Post-processing | `pheno-analyzer` | output paths + run↔parameter map from the latest upstream sidecar, analysis procedure, experimental data, plot spec | `analysis/*.py`, `scripts/plot_*.py`, `output/…`, `step4_postprocessing.{md,json}` |

Skip stages the task does not need: a supplied UFO skips Step 1; a task without a MadAnalysis step skips Step 3.

### Handoff contract

Each stage writes a human-readable `stepN_<stage>.md` and a small `stepN_<stage>.json` sidecar holding only what later stages consume: `status`, paths, the particle and parameter tables (step 1), the run-name ↔ parameter map with cross sections and event-file paths per run (step 2), histogram and cut-flow paths (step 3), figure and data paths (step 4), the Magnus `jobs` used, and a `lessons` array (run-lessons skill). When you dispatch the next subagent, give it the **paths** of the upstream sidecars, the parts of the task text it needs, and the progress file paths it must write. A subagent has no access to your conversation; if its return summary is thinner than you need, read its `.md` file instead of asking it to repeat itself.

### Delegation

Stages run one after another because each depends on the previous outputs. Inside a stage, ask the subagent to submit independent work in parallel: different mass points, detector cards, or datasets are separate Magnus jobs. Do not do a stage's work in your own context because it looks small; the subagent's context is where the skill and its cross-run memory live.

A headless run ends the moment you end a turn with nothing running in the background. Never reply that you will wait for a download, a job, or a file to appear: wait inside a tool call (a bounded polling loop, or `magnus status` calls), or dispatch the next stage and let its completion wake you. A turn that ends with "waiting for …" is a lost run.

## After the last stage

1. Update the manifest step statuses.
2. Invoke `execution-summarizer` (it writes `execution_summary.md` with prompt-to-code mapping tables).
3. Gather the `lessons` arrays from every sidecar into `progress/<run_label>/lessons.yaml`. Lessons are pipeline and tool lessons backed by a job ID or file, never the task's physics.
4. If the user asked for a reproduction package, invoke `reproduction-guide-generator`.

## Remote execution

All compute stages run on the remote `zhustation` Magnus site (connection check, upload/download, recovery: magnus skill). Run `magnus config` once before the first compute stage. If the station is unreachable after the magnus skill's retry policy, stop the affected stage, keep the manifest and finished artifacts, and report the job IDs so the run can resume without repeating successful jobs.

## Reporting

A stage is done when its sidecar says `status: success` and the files it names exist; report against that evidence. Say plainly when a stage failed or was skipped, and which job IDs are involved.
