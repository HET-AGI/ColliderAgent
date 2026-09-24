# ColliderAgent skills v2 — context-lean skills + cross-run experience loop

Date: 2026-09-16 · Branch: `feat/skill-evolution-v2` · Status: approved by autonomous run (design written for human review; see §8)

## 0. Why now

The 11 skills + 4 subagents on `main` were written in March–April 2026 for Claude Opus 4.6.
Today's runs use Opus 4.8 / Opus 5 / Sonnet 5 / Fable 5.1. Two things changed:

1. **The models.** Current models follow instructions more literally, plan on their own, use
   fewer tools and fewer subagents by default, and lose quality when prompts are over-prescriptive
   (Anthropic migration guides for Opus 4.7/4.8 and Fable 5.1; the `claude-api` skill's
   `shared/prompt-audit.md`). Skills tuned with "CRITICAL / Do NOT / STEP 1..6" scaffolds are now
   a liability, not a safeguard.
2. **The harness.** Claude Code 2.1.x added skill frontmatter (`context: fork`, `effort`,
   `allowed-tools`, `user-invocable`, `disable-model-invocation`) and subagent frontmatter
   (`memory: user|project|local`, `maxTurns`, `effort`). Subagent `memory:` injects the first
   200 lines / 25 KB of a per-agent `MEMORY.md` into the subagent's system prompt on every run and
   gives it Read/Write/Edit on that directory. That is a first-class, harness-supported surface
   for cross-run learning that did not exist when the skills were written.

Measured baseline on `main` (2026-09-16):

| Surface | Size | Notes |
|---|---|---|
| 11 × SKILL.md | 94.6 k chars (~24 k tokens) | preloaded whole into each subagent via `skills:` |
| references/ + templates/ | 72.4 k chars | loaded on demand (fine) |
| 4 × agents/*.md | 12.8 k chars | duplicates the skill bodies they preload |
| Pressure language | 5 × `CRITICAL`, prohibition clusters in 8 files | prompt-audit group 1a/1c |
| Duplicated boilerplate | FileSecret note ×7, `--output` overwrite warning ×5, "see magnus skill" ×6, "Return ONLY a concise summary" ×4 | one owner each is enough |
| Fossils | "Reproducibility note (pre-2026-04)", "Current repo limitation" ×2, MG5 "3-done" history | prompt-audit group 1d |
| Doc drift found by smoke test | `madanalysis-analyzer` documents `<output>/analysis_output/Output/HTML/...`; the blueprint actually returns `<output>/Output/{HTML,PDF,Histos,SAF}` | fix |
| Install drift | `~/.claude/skills` copies were 5 months behind `main` (still had the wrong MG5 3-state machine) | nothing checks it |

Verification of the Magnus side (same day, zhustation): all 8 blueprints present, schemas match
the skills, and compile → launch (parton) → MadAnalysis, validate-feynrules, and launch
(Pythia8+Delphes) all succeeded. So the *contracts* in the skills are right; the *prose* is dated.

## 1. Goals / non-goals

Goals
- G1 Cut per-run context cost and remove dated scaffolding while keeping every tool contract
  (parameters, result fields, paths, failure modes, retry bounds).
- G2 A bounded, evidence-grounded **experience loop**: each run can leave lessons that the next
  run sees, and recurring lessons can be promoted into skill text through a human-gated path.
- G3 A **benchmark harness** that runs a paper-reproduction prompt in a clean sandbox with a chosen
  model, and emits the numbers the paper's Tables S3/S4/S5 need. It is also the regression gate
  for G2's promotions.

Non-goals
- Changing blueprints or the Magnus side.
- Auto-merging any skill change without a human.
- Storing task physics (Lagrangians, cuts) in memory — only pipeline/tool lessons.

## 2. Design 1 — context-lean skills (G1)

### 2.1 Ownership rules (one owner per fact)
| Fact | Owner | Everyone else |
|---|---|---|
| Magnus mechanics: FileSecret upload, `--output` is replaced on download, `magnus job result/logs/status`, reconnect-don't-resubmit, retry policy, zhustation pin, token hygiene | `magnus/SKILL.md` | one line: "Execution and download mechanics: see the magnus skill." |
| Workspace layout, run labels, `progress/` protocol, handoff sidecars, parallelism guidance | `pheno-pipeline-orchestrator/SKILL.md` | each stage skill lists only its own output paths |
| Tool contract of a blueprint (params, result JSON, output tree) | that stage's skill | agents do not restate it |
| Agent role, inputs it needs, what it returns, when to delegate/parallelise | `agents/*.md` (thin) | — |

### 2.2 SKILL.md shape
- Frontmatter `description`: intent categories, not synonym lists (routing text may keep mild urgency).
- Body order: **Contract** (params/results/paths) → **Workflow goal + the few fragile rules with
  their reasons** → **Pointers** ("read `references/x.md` when …"). Examples move to
  `references/examples.md`. Target ≤ 5 k tokens per SKILL.md (Claude Code re-attaches only the
  last 5 k tokens of a skill after auto-compaction; keep the whole skill inside that window).
- Prompt-audit edits: drop `CRITICAL`/`MUST`/`NEVER` shouting; keep each real constraint once,
  stated plainly with its reason (two `done` lines; no `submit`; no `define` keyword; relative
  paths; `~`-prefixed odd particles). Delete fossils/migration-relative phrasing ("pre-2026-04",
  "current repo limitation", "no longer"). Keep contract detail (FeynRules 2.3.49 UFO bug list,
  MG5 3.7.0 `delphes_card` behaviour) — that is context only the author knows.
- Re-baseline for current models (additions, not deletions): explicit delegation guidance
  ("dispatch independent mass points / detector cards as parallel subagents"), evidence-grounded
  progress claims, the lesson-recording contract (§3), "state boundaries" (don't tidy, don't
  refactor the user's files).
- Frontmatter: `execution-summarizer` and `reproduction-guide-generator` get `context: fork`
  + `background: false` (they read many files; their reads should not land in the orchestrator's
  context). New `skill-evolve` gets `disable-model-invocation: true`.

### 2.3 Handoff sidecars
Each stage subagent writes `progress/<run_label>/stepN_<stage>.md` (as today) **and**
`progress/<run_label>/stepN_<stage>.json` with only the fields the next stage consumes:
```yaml
# step1_feynrules.json
{ "status": "success", "fr": "models/X.fr", "ufo": "models/X_UFO", "lagrangian": "LX",
  "particles": [{"name":"zp","pdg":9000001}], "params": [{"name":"gzp","block":"NPINPUTS","code":1}],
  "jobs": ["d04d9e353d1e59ff"], "lessons": [ ...see §3.2... ] }
# step2_madgraph.json
{ "status": "success", "process_dir": "events/pp_zp_13TeV",
  "runs": [{"run":"run_01","params":{"MZp":1000},"xsec_pb":"0.12 +- 0.001","nevents":10000,
            "files":{"lhe":"...","hepmc":"...","root":"...","lhco":"..."}}],
  "scripts": ["scripts/mg5_13TeV.mg5"], "jobs": ["..."], "lessons": [] }
```
The orchestrator passes **paths** to the next subagent; it never parses physics. The `.md`
remains the human-readable record. `jobs` and `lessons` feed §3 and §4.

### 2.4 Install / sync check
`scripts/install.sh [--check]` copies `src/skills` and `src/agents` into `~/.claude` (or
`$CLAUDE_CONFIG_DIR`) and `--check` diffs them, exiting non-zero on drift. README points to it.

## 3. Design 2 — experience loop (G2)

### 3.1 Storage: harness-native subagent memory
All four subagents get `memory: user` → `~/.claude/agent-memory/<agent>/` (or the
`$CLAUDE_CONFIG_DIR` equivalent). Claude Code injects `MEMORY.md` (≤200 lines / 25 KB) into the
subagent's system prompt at start and grants Read/Write/Edit on the directory. No retrieval code
is needed on the read side; the write side is a contract in each agent file plus a deterministic
maintainer script.

Layout (per agent):
```
MEMORY.md                       # index: one line per lesson: "- [stage] symptom → fix (support N, last YYYY-MM-DD) [file]"
lessons/<stage>-<slug>.md       # one lesson per file (frontmatter below + ≤ 15 lines body)
```
Lesson frontmatter (the schema `scripts/memory/schema.json` validates):
```yaml
stage: madgraph        # feynrules | ufo | calchep | madgraph | madanalysis | micromegas | pheno | orchestrator
blueprint: madgraph-launch   # or "none"
symptom: "job success=true but nevents=10000 instead of requested"
root_cause: "set lines placed after the second done"
fix: "keep every set/decay line above the final done"
evidence: ["job:ca68f501890c2786", "progress/dy_14tev/step2_madgraph.md"]
generalizable: true    # false = specific to one model/paper; never promoted
support: 1             # number of distinct runs that confirmed it
first_seen: 2026-09-16
last_confirmed: 2026-09-16
```

### 3.2 Write side (in each agent's contract)
At the end of its stage the subagent records a lesson only when (a) a tool result in this run
showed a failure/retry/silent-default that it had to work around, or (b) a non-obvious approach
was confirmed by a tool result. It updates an existing lesson (support+1, last_confirmed) instead
of adding a near-duplicate, and it never stores the task's physics, file contents, or tokens. The
same lesson list goes into `stepN.json.lessons` so the run record is self-contained.

### 3.3 Maintain (deterministic, no LLM): `scripts/memory/distill.py`
- Validates every lesson file against the schema; rebuilds `MEMORY.md` from the lesson files
  (sorted by support desc, last_confirmed desc), truncating to the 200-line cap.
- Merges near-duplicates (same stage + normalised symptom) → support summed, evidence unioned.
- Decays: a lesson not confirmed for `--stale-runs N` (default 10 runs, counted from a run log)
  moves to `archive/`.
- `--propose`: lists lessons with `generalizable: true` and `support ≥ 3` as promotion candidates,
  with the target skill file.
- `--import <sandbox_config_dir>`: merges memory harvested from a benchmark sandbox into the
  central store (used by the harness).

### 3.4 Promote (human-gated): `skill-evolve` skill (`/skill-evolve`)
User-invoked only. Runs `distill.py --propose`, then for each candidate: drafts the smallest
SKILL.md edit that states the rule with its reason (prompt-audit style), runs
`scripts/bench/smoke.sh`, and leaves a commit on a `skill-evolve/<date>` branch with a PR-style
summary (candidate, evidence, diff, smoke result). A human merges. This closes the loop that the
git history shows was previously done by hand (e.g. the MG5 state-machine fix in April 2026).

### 3.5 Guardrails
Evidence required · generalizable flag · bounded size (200-line index, archive on decay) ·
recency-trap check in `skill-evolve` ("would this have helped most recent runs, or one run?") ·
no secrets / no task physics · promotions never bypass the smoke gate or the human.

## 4. Design 3 — benchmark harness (G3): `scripts/bench/`
- `run_benchmark.sh <arxiv-id> <figure> <model> [--effort E] [--memory cold|warm] [--label L]`
  - sandbox `bench_runs/<label>/` with `prompt.md` (copied from `paper-reproduction/`),
    a private `CLAUDE_CONFIG_DIR` (skills + agents from this checkout, credentials + settings
    copied from `~/.claude`, agent-memory empty for `cold` or copied from the central store for
    `warm`), and `hepdata/` inputs if the prompt needs them.
  - runs `claude -p "$(cat prompt.md)" --model <id> --effort <E> --output-format json
    --dangerously-skip-permissions` with `nohup`, records wall-clock, saves `result.json`.
  - post-run: `collect_metrics.py`, and copies the session transcript next to the sandbox.
- `collect_metrics.py <sandbox>` → `metrics.json` + one Markdown row:
  wall-clock, sub-agent calls (`Agent` tool_use count), Magnus jobs (`Bash` inputs matching
  `magnus (run|launch|blueprint run)`), files written (distinct Write/Edit paths), tokens in
  (input + cache_creation + cache_read), tokens out, cost. Reads `result.json` (public API) first;
  transcript parsing is best-effort and version-tolerant.
- `judge.sh <sandbox> <reference.png>` → `verdict.yaml` (`success`, `failure_mode` ∈ {model,
  generation, analysis, infrastructure}, notes) via a `claude -p` vision comparison; marked
  *assistive* — a human confirms before the number goes into a table.
- `aggregate.py bench_runs/` → Tables S3/S4/S5 in Markdown.
- `smoke.sh` → the 5-blueprint smoke (compile, launch, ma5, validate, pythia+delphes) with the
  same inputs used on 2026-09-16; exit non-zero on any `success: false`.

## 5. Data flow
```
prompt.md ─► claude -p (orchestrator skill) ─► subagents (skills preloaded, MEMORY.md injected)
      │                                            │  writes stepN.md + stepN.json (+ lessons)
      │                                            └► memory/lessons/*.md (per agent, user scope)
      └► result.json ─► collect_metrics.py ─► metrics.json ─┐
                                                  distill.py ◄┘ (rebuild index, merge, decay, --propose)
                                                  /skill-evolve ─► branch + smoke.sh ─► human merge
```

## 6. Error handling
- Memory write failures never fail a run (advisory surface).
- `distill.py` refuses to rebuild if any lesson fails schema validation; it prints the file.
- Harness: a sandbox never touches `~/.claude` except to *read* credentials/settings; `warm`
  imports are explicit (`distill.py --import`).
- Smoke gate failure blocks `skill-evolve` from committing.

## 7. Testing
- Unit (pytest, `scripts/tests/`): schema validation; index rebuild + 200-line cap; duplicate
  merge; decay; `--propose` threshold; `collect_metrics.py` on a fixture transcript + result.json;
  `aggregate.py` on fixture sandboxes.
- Integration: `scripts/install.sh --check`; `smoke.sh` against zhustation; one quickstart
  prompt (SM dilepton m_ll) through the orchestrator with Sonnet 5 in a harness sandbox.
- Benchmark: `1701.05379` Fig. 8 (ALP EFT, parton-level E_T^miss) with Opus 5, Opus 4.8,
  Sonnet 5 (cold memory), which fills one row of Tables S3/S4/S5.

## 8. Decisions taken without the user (flag for review)
- `memory: user` scope by default (persists across the fresh working dirs users are told to use);
  the harness isolates memory per sandbox via `CLAUDE_CONFIG_DIR` instead of a project scope.
- Lesson store is Markdown+frontmatter (what the harness injects verbatim) rather than JSON.
- Benchmark for the first cross-model row: 1701.05379 Fig. 8 (cheapest full-pipeline case).
- No changes to blueprints or the Python ADK agent.
