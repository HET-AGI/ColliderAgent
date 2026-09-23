---
name: research-target-finder
description: >
  Find research targets for a BSM collider study from a high-level physics goal.
  Triggers when the user wants to build a new model that explains an experimental anomaly
  or realizes a given purpose (e.g. "build a model that explains the muon g-2",
  "construct a minimal dark matter model testable at the LHC"), or wants a survey of the
  models relevant to a purpose (e.g. "which models can explain this excess",
  "find all leptoquark models for R_D"). Produces a research-target report with
  literature-verified status, vetted candidate models, and pipeline-ready Lagrangians.
  Do NOT trigger when the user already supplies a complete Lagrangian together with the
  process and analysis specification.
---

# Research Target Finder

## Overview

This skill turns a high-level goal ("explain anomaly X", "which models do Y") into a ranked list of **research targets**: concrete BSM models, each with a pipeline-ready Lagrangian, a constraint assessment, and its collider signatures. The report feeds the research-plan-generator skill, which turns selected targets into executable research plans.

Two modes, which can be combined:

| Mode | Goal | Core activity |
|------|------|---------------|
| **A. Model building** | Construct model(s) that address an anomaly or a purpose | Anomaly → effective operator → mediator → consistent Lagrangian |
| **B. Model survey** | Find the models relevant to a purpose | Systematic enumeration + literature search → classification → comparison |

This is a **literature and reasoning task** — no Magnus blueprints are involved. It needs web access (`WebSearch`/`WebFetch`, or `curl` to the INSPIRE/arXiv/HEPData APIs). See [references/literature_search.md](references/literature_search.md) for tested API recipes and the offline fallback.

## Output Paths

All paths are **relative to the working directory**.

| Output | Path |
|--------|------|
| Research-target report | `research/<study_label>/targets.md` |
| Downloaded experimental data (if any) | `research/<study_label>/data/` |
| Downloaded paper sources (if any) | `research/<study_label>/sources/<arXiv-id>/` |
| Helper scripts for lookups and estimates (if any) | `research/<study_label>/tools/` |

Helper scripts are for your own estimates. If a research plan is to use one as an analysis input (e.g. a rate code for an overlay), the script must state its assumptions in its header, and the plan must contain its validation (what published result it reproduces, and how well) — an unvalidated script may only be used for shapes and scalings, and the plan must say so.

`<study_label>`: short descriptive tag, e.g. `rd_anomaly_lq`, `dm_higgs_portal`, `excess_95gev`. When invoked by the orchestrator, use the label it provides.

## Workflow

### Step 1: Write the Problem Statement

Skim the research-plan-generator skill's `references/pipeline_capabilities.md` first — what the pipeline can simulate decides which papers and models are worth your reading time.

Before searching, pin down what is being asked:
- **Goal**: the anomaly/observable to explain, or the purpose to realize (neutrino mass, dark matter, a collider signature, ...)
- **Success criterion**: what must a model achieve to count as a target? (e.g. "shifts $R_D$ by +10% while $M > 1$ TeV", "gives $\Omega h^2 = 0.12$ and is within HL-LHC reach")
- **Boundary conditions** from the user: colliders of interest, minimality, UV-completeness, particle types to include/exclude
- **Assumptions**: every interpretation choice you made for an ambiguous prompt

### Step 2: Literature Reconnaissance

Follow [references/literature_search.md](references/literature_search.md). Collect in this order:

1. **Experimental status** — latest measurement(s), SM prediction (and the spread between competing SM predictions, if any), tension, and date. Anomalies evolve, so always retrieve the current status instead of recalling it. (Examples as of 2026-09: the $R_{K^{(*)}}$ deficit disappeared with LHCb's December 2022 update, arXiv:2212.09152; the size of the $(g-2)_\mu$ tension depends on which SM prediction is used, arXiv:2006.04822 vs arXiv:2505.21476.)
2. **Reviews and most-cited explanations** — the established model landscape
3. **Recent papers (last ~2 years)** — new ideas and updated constraints
4. **Collider searches** — existing ATLAS/CMS/LHCb/Belle II limits on the candidate mediators, and whether HEPData records exist (needed later for recasts)

Record each source as you go (arXiv ID + what you took from it). Apply the verification protocol of the reference doc to every citation.

### Step 3A: Model Building (Mode A)

Follow [references/model_building_guide.md](references/model_building_guide.md):

1. **Anomaly → operator**: identify the effective operator(s) and the Wilson coefficient size/sign/chirality the data require
2. **Operator → mediator**: enumerate the tree-level mediators (by spin and SM quantum numbers); consider loop-level realizations if tree-level options are excluded
3. **Mediator → Lagrangian**: write the minimal consistent Lagrangian, in pipeline-ready form (Section 4 of the guide)
4. **Compare with the literature**: state honestly whether the construction is new, a variant of a known model (cite it), or a known model rediscovered. For a well-studied anomaly every minimal mediator is already in the literature — then the target **is** a literature model: say so, and put the novelty where it can honestly be (newest data, an untested search, an unexplored parameter region). Do not invent a variant for novelty's sake. A genuinely new construction is warranted when the user explicitly asks for one, or when the known models are excluded and a modification evades the constraint (the modification must then be motivated by that constraint)
5. **When the user asks for new models — find the gap systematically.** Enumerate bottom-up every way of generating what the data require (each operator class × each tree-level mediator topology × spin assignments; then loop-level), mark each entry with the papers that cover it (novelty check: `references/literature_search.md`, Section 5a), and build in the empty cells. Prefer a gap that exists for a physics reason you can state (e.g. "this class was considered excluded — but the exclusion disappears once ...") over one that is merely unoccupied. "New" has two axes — the *structure* (field content and couplings) and the *application* (proposed for this goal before?); a known simplified model never applied to this anomaly is "known structure, new application": deliver it under that label, and record how you read the user's request as an assumption. If a construction turns out to exist, say so and build another
6. Build **more than one** candidate when the data allow it — alternatives with different collider signatures are what make the collider study informative. Several requested constructions should differ in mechanism or in signature, not by relabelling; siblings of one class (e.g. exchanged spins) qualify only if their phenomenology really differs — show that it does
7. **This is a collider pipeline**: among otherwise comparable explanations prefer those with a collider handle (a producible mediator or partner). If the best explanations of the anomaly have none, say so plainly in the report instead of forcing one

### Step 3B: Model Survey (Mode B)

1. **Define inclusion criteria** from the problem statement (what counts as "relevant")
2. **Enumerate bottom-up**: operator → all mediators that generate it (tree level, then loop level). This guards against the literature's popularity bias
3. **Enumerate top-down**: literature search — reviews first, then most cited, then most recent
4. **Merge and classify**: by mediator spin / gauge representation / tree vs loop / mass scale / characteristic collider signature
5. **Completeness check**: cross-check the catalogue against at least one review article (or, if none exists, the reference list of a recent comprehensive paper). "All models" is an aspiration — state explicitly what the survey covers, what it leaves out, and why
6. **Include the null hypothesis** when surveying explanations of an anomaly: statistical fluctuation, underestimated SM uncertainty, or an experimental effect — with what would settle it
7. **Catalogue vs targets**: every class gets a row in the landscape table (Section 2 of the report), with its variants listed by reference. Only classes that could be recommended become **targets** with a full block (typically 3–6); excluded or unassessed classes get the short form of the block (origin, status, the reason, references)
8. **Shared simplified models**: when several classes differ only in the values of a common set of couplings (e.g. coupling modifiers of a new scalar), define one master simplified model and express each target as a region of its parameter space. Say so explicitly — one UFO model then serves several targets

### Step 4: Vet Each Candidate

Apply the checklists in [references/model_building_guide.md](references/model_building_guide.md) (Sections 5–6):

- **Theory**: gauge and Lorentz invariance, hermiticity, anomaly cancellation, perturbativity, stability of the DM candidate or proton where relevant
- **Experiment**: direct searches, flavour, electroweak precision, Higgs data, cosmology/astro where relevant. Give each bound with its source and mark the candidate `viable` / `constrained` (viable in part of parameter space — say which) / `excluded`
- **Collider testability**: production and decay channels, final states, which existing search constrains it, what is untested
- **Pipeline feasibility**: can the downstream pipeline simulate it? (tree-level UFO, effective vertices for loop-induced couplings, prompt decays, ...) See the research-plan-generator skill's `references/pipeline_capabilities.md`

Keep excluded candidates in the report with the reason — a documented dead end is a result.

### Step 5: Rank and Recommend

Rank by: (1) how well the goal is addressed, (2) viability after constraints, (3) distinctiveness and reach of the collider signature, (4) minimality, (5) pipeline feasibility, (6) novelty (is there something new to learn?). Give a short justification per candidate, then propose the research program: which targets to study, with which deliverable, in which order.

### Step 6: Write the Report

Copy [templates/targets_report.md](templates/targets_report.md) to `research/<study_label>/targets.md` and fill it section by section. Do not drop numbered sections; write "not applicable" with a reason instead. Recommendable targets get the full block, excluded or unassessed ones the short form. Fill Section 5 (Recommended Research Program) even when no plans will be written in this session — it then lists *proposed* plans. Finish by renumbering the references.

## Key Conventions

- **No fabrication**: every reference is verified by an INSPIRE or arXiv lookup in the current session (title and first author must match what you cite it for), and carries its reading depth (`source` / `abstract` / `title` — see the verification protocol). Every number carries source and date.
- **Evidence labels**: facts you could not verify are tagged `[unverified]`; your own estimates are tagged `[estimate]` with the formula used; choices you made where no source fixes the value (an efficiency, a systematic uncertainty, a working point) are tagged `[assumed]`. Untagged statements must be backed by a listed reference. Collect inputs shared by many estimates (e.g. reference cross sections) in one place in the report, with their source or tag. Before finishing, **recompute every `[estimate]`** once — slips in quick estimates are the most common error in these reports.
- **Lagrangian provenance** — each Lagrangian in the report is labelled as one of:
  - `from source`: taken from a paper you read (prefer the TeX source); give the equation number and any change of convention
  - `new construction`: terms inherited from a parent model are `from source` (cite it); your additions are labelled "own addition"; every relation you derive (matching coefficients, cross sections, lifetimes) is labelled `[own derivation]` and recomputed once, and cross-checked against a published special case wherever one exists
  - `own parameterization`: a mass-basis simplified model you wrote to capture the model's collider phenomenology (the normal case in a survey, where full models are defined by scalar potentials or gauge structures the pipeline does not need). State what it does *not* capture (parameter correlations of the full model)
  - never an unlabelled reconstruction from memory. Individual couplings you could not check are tagged `[unverified]`
  A target that is selected for a research plan must have its Lagrangian and benchmark values checked against a source before the plan is written; if the lookup budget does not allow it, return this as an open decision. Candidates that are not selected may carry an incomplete Lagrangian (e.g. only some multiplet components) — mark it "not pipeline-ready: requires reading [n]".
- **Pipeline-ready Lagrangian**: BSM part only, LaTeX, every field's spin and $(SU(3)_C, SU(2)_L, U(1)_Y)$ representation and electric charge stated, couplings declared real or complex, chirality projectors and "+ h.c." explicit. See the guide, Section 4.
- **Hypercharge convention**: $Q = T_3 + Y$ throughout. Convert when a source uses $Q = T_3 + Y/2$.
- **New vs known**: always state the origin of a target — `literature` (cite), `variant` (cite + what changed), or `new construction`. Claim novelty only after searching for prior work, and phrase it as "no prior work found with queries ...".
