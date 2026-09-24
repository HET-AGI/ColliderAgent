---
name: execution-summarizer
description: Write the execution summary of a completed collider-analysis run — what was done, the results, and prompt-to-code mapping tables (Lagrangian ↔ .fr, process ↔ MadGraph commands, cuts ↔ analysis code). Use at the end of a pipeline run or when the user asks to summarize a run or asks what the agent did.
context: fork
background: false
---

# Execution Summarizer

Produces `execution_summary.md` (or `execution_summary_<run_label>.md` for an incremental run, so earlier summaries survive) in the working directory. The summary's value is the mapping between the user's physics specification and the generated code: someone reading it should be able to check every parameter without opening the scripts.

## Which run

Read `progress/run_manifest.yaml`. Summarize the run the user named; with one run, that run; with several and no name, the most recent. Then read that run's `progress/<run_label>/stepN_*.json` sidecars (paths, tables, job IDs) and `stepN_*.md` files, the original task file, and the scripts they name (`models/*.fr`, `scripts/*.mg5`, `scripts/*.ma5`, `scripts/*.py`, `analysis/*.py`). Take numbers (cross sections, event counts, fit results) from the sidecars and the scripts' outputs, not from memory.

## Content

1. **Run info** — label, timestamp, parent (incremental runs), Magnus job IDs per stage.
2. **Task overview** — one paragraph: what was requested, what came out.
3. **Execution steps** — numbered, per stage: skill or subagent, key inputs, key outputs with paths and numbers, errors and how they were resolved.
4. **Prompt-to-code mapping tables** — one per executed stage, only for stages that ran:
   - Lagrangian ↔ `.fr`: each LaTeX term or parameter → the FeynRules line (`| $y_S \bar Q_L S t_R$ | \`yS * QLbar.S.tR\` | Yukawa, left-handed |`);
   - Process ↔ MadGraph: process, energy, statistics, scan points, PDF, shower/detector → the `generate`/`set` lines;
   - Cuts ↔ analysis code: each selection, binning, and statistical choice → the MA5 line or Python snippet.
   Use LaTeX in the prompt column and verbatim code in the code column.
5. **Output files** — every key artifact with path and one-line description.
6. **Lessons** — the run's `lessons.yaml` entries, if any, in one line each.

Include only stages that ran; a partial pipeline gets a partial summary. When done, tell the user where the file is and give the two or three headline numbers.
