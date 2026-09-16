---
name: skill-evolve
description: Promote recurring cross-run lessons into skill text. Reads the per-agent lesson store, proposes the smallest SKILL.md edits that would prevent the recurring failures, runs the blueprint smoke test, and leaves the change on a review branch for a human to merge. Invoke as /skill-evolve after a batch of runs.
disable-model-invocation: true
argument-hint: "[--min-support N] [--dry-run]"
---

# Skill evolve

The pipeline subagents record lessons in their memory directories (run-lessons skill). This skill closes the loop: a lesson that keeps recurring becomes part of the skill that should have prevented it. A human merges the result; nothing here changes `main` on its own.

## Procedure

1. **Collect candidates.** From the repository root run
   `python3 scripts/memory/distill.py rebuild` and then
   `python3 scripts/memory/distill.py propose --min-support ${MIN_SUPPORT:-3}`.
   The proposal lists lessons with `generalizable: true` and enough independent runs behind them, each with a guessed `target_skill`. Open every lesson file and its evidence (job IDs, progress files) before trusting it.
2. **Apply the recency test.** Keep a candidate only if it would have helped most recent runs, not just the runs that wrote it, and only if the current skill text does not already state the rule. A lesson caused by a since-fixed blueprint or a one-off environment problem is archived, not promoted (`distill.py decay` handles ageing; move it by hand when the cause is known).
3. **Draft the edit.** On a branch `skill-evolve/<YYYY-MM-DD>`, make the smallest change to the target `SKILL.md` (or its `references/`) that states the rule and its reason where the reader needs it — a row in a parameter table, one sentence in the relevant section. No shouting, no history narrative, no incident IDs in the skill text: the lesson file keeps the provenance.
4. **Gate.** Run `scripts/install.sh --check` after `scripts/install.sh`, then `scripts/bench/smoke.sh --quick` (full `smoke.sh` when the edit touches launch or analysis text). A failing gate blocks the commit.
5. **Commit and hand over.** One commit per promoted lesson, message `skill(<skill>): <rule> (lesson <file>, support N)`. Write `docs/skill-evolve/<date>.md` with, per candidate: the lesson, the evidence, the diff, the smoke result, and the promote/archive decision. Report the branch name; do not merge.

With `--dry-run`, stop after step 3 and print the diffs.

## Boundaries

Promote pipeline and tool lessons only; never task physics. Never weaken a tool contract because a lesson contradicts it — check the blueprint (`magnus blueprint schema <id>`) and fix whichever side is wrong. Never touch `paper-reproduction/` prompts: they are the benchmark.
