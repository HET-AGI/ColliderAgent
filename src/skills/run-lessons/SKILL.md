---
name: run-lessons
description: Contract for the per-agent memory that ColliderAgent pipeline subagents keep across runs — when to consult it, when to write a lesson, and the lesson file format. Preloaded by the pipeline subagents; not meant to be invoked on its own.
user-invocable: false
---

# Run lessons (cross-run memory)

Your memory directory is injected into your prompt as `MEMORY.md`: one line per lesson learned in earlier runs of your stage, each linking to a lesson file. It exists because the same pipeline mistakes (a silently ignored `set` line, a card name that is swallowed, a naming convention micrOmegas needs) recur across runs and are cheap to avoid once known.

## Reading

Before you build commands or scripts, scan `MEMORY.md` for entries whose stage or blueprint matches what you are about to do, and open the linked file when the symptom could apply. Lessons are advisory and symptom-keyed: apply one only when its symptom matches what you observe, and verify the outcome against the tool result as you would any other change. When a lesson contradicts the current tool contract or the task, the contract and the task win. If you tried a lesson's fix and it did not help, add `contradictions: 1` (or increment it) to that lesson file instead of deleting it; the maintainer script demotes lessons whose contradictions reach their support, which is how a stale pattern leaves the store without anyone editing it by hand.

## Writing

Record a lesson at the end of the stage only when this run's tool results show one of:

- a job failure or retry you had to work around;
- a job reporting `success: true` while a parameter was silently ignored or an expected file was missing;
- a non-obvious approach that a tool result confirmed works.

One lesson per file at `lessons/<stage>-<short-slug>.md` in your memory directory. If `MEMORY.md` already lists the same symptom, update that file (increment `support`, set `last_confirmed`, add evidence) instead of adding a near-duplicate. Never store the task's physics content, file contents, credentials, or anything a reader could not act on in a different run. Copy the same entries into the `lessons` array of your stage's `stepN_<stage>.json` sidecar so the run record is self-contained.

Format (the frontmatter is validated by `scripts/memory/distill.py`; keep the body under 15 lines):

```
---
stage: madgraph              # feynrules | ufo | calchep | madgraph | madanalysis | micromegas | pheno | orchestrator
blueprint: madgraph-launch   # or none
symptom: "success=true but nevents=10000 instead of the requested 50000"   # at most 200 characters
root_cause: "set lines were placed after the second done"
fix: "keep every set/decay/card line above the final done; compare result nevents with the request"
evidence: ["job:ca68f501890c2786", "progress/dy_14tev/step2_madgraph.md"]
generalizable: true          # false when it only applies to one model or paper
support: 1
contradictions: 0          # optional; runs in which the fix did not help
first_seen: 2026-09-16
last_confirmed: 2026-09-16
---
Optional short note: what you tried first and how you noticed.
```

Add the index line to `MEMORY.md` yourself as `- [<stage>] <symptom> → <fix> (support <N>, last <date>) [lessons/<file>]`; the maintainer script rebuilds and prunes the index later, so an approximate line is fine.
