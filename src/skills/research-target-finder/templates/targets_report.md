# Research Targets: <TITLE>

- **Study label**: `<study_label>`
- **Date**: <YYYY-MM-DD>
- **Mode**: <A. Model building | B. Model survey | A+B>
- **Literature access**: <full | partial | none — if not full, all affected items are tagged [unverified]>

<!-- Evidence labels used in this report:
     (untagged)    backed by a reference in Section 7, verified in this session
     [estimate]    own estimate; formula given
     [assumed]     a choice made where no source fixes the value
     [unverified]  a fact from memory or from a source that could not be checked -->

## 1. Problem Statement

### 1.1 User goal (verbatim)

> <paste the user's prompt>

### 1.2 Interpretation

- **Physics question**: <one or two sentences>
- **Success criterion**: <what a model must achieve to count as a target>
- **Boundary conditions**: <colliders, minimality, exclusions requested by the user>
- **Assumptions made on the user's behalf**:
  1. <assumption — why this choice>

### 1.3 Current status

<!-- Use the table that fits; delete the other. -->

Measured observable deviating from the SM:

| Observable | Measurement | SM prediction | Tension | Source | As of |
|---|---|---|---|---|---|
| <e.g. $R_D$> | <value ± stat ± syst> | <value; give the spread if competing SM predictions exist> | <n σ> | [n] | <date> |
| <combination of correlated observables, e.g. $R_D$–$R_{D^*}$> | <correlation $\rho$ = ...> | | <combined n σ> | [n] | <date> |

Excess in a search (bump, tail, or event count):

| Search (experiment, channel, $\sqrt s$, luminosity) | Location (mass / bin) | Local (global) significance | Observed (expected) limit or fitted signal rate | Source (paper, HEPData) | As of |
|---|---|---|---|---|---|
| | | <n σ (m σ)> | | [n], ins<id> | <date> |

<Short paragraph: how solid is the anomaly/motivation? Is any combination official or made by theorists? Upcoming measurements that could change it? If no newer result was found, give the query and date.>

### 1.4 What the data require

<Model-independent requirements, before any model is chosen:
- indirect anomaly → effective operator(s), required Wilson coefficient size/sign/chirality, implied scale $\Lambda/g$
- resonance-type excess → allowed spin/CP, width, required $\sigma\times\text{BR}$, a master simplified model with generic couplings, and the distinct generic ways of obtaining the rate
- direct-detection (recoil) signal → kinematics ($q$, $v_\text{min}$, mass range), what the spectrum excludes (form factor, low-energy recoils), the generic mechanisms and which of them the experiment itself tested, the required cross-section band versus the mechanism's parameter, halo assumptions, target dependence
- purpose that is not an anomaly (e.g. dark matter) → the quantitative requirement, e.g. $\Omega h^2 = 0.12$>

**Shared inputs for estimates**: <reference cross sections, branching ratios, loop-function values, luminosities used by the `[estimate]`s below — each with source or `[unverified]` tag>

## 2. Model Landscape

<Mode B: the full classified catalogue. Mode A: a brief map of existing explanations, to position the new construction.>

| Class | New state(s): spin, $(SU(3),SU(2),Y)$ | Mechanism (tree / loop / mixing) | Addresses goal via | Status | Characteristic collider signature | Key refs | Variants (by reference) |
|---|---|---|---|---|---|---|---|
| <class name> | | | | viable / constrained / excluded / not assessed | | [n] | [n], [n] |
| No new physics | — | — | <fluctuation, SM uncertainty, experimental effect> | open | <what would settle it> | [n] | |

<!-- "New state(s)": for an indirect anomaly this is the mediator; for a resonance it is the resonance itself plus the companions that matter. -->

**Coverage statement**: <what this survey covers; what it leaves out and why; which review(s) or reference lists it was cross-checked against; how deeply the entries were read (source / abstract / title)>

## 3. Candidate Targets

<!-- Full block for every target that could be recommended: T1, T2, ...
     Short form for excluded or unassessed candidates: keep only Origin / Status / One-line idea,
     plus one paragraph "Why excluded (or not assessed)" with references.
     If several targets share one master simplified model, give its Lagrangian once (Section 1.4 or the
     first target) and let each target state its region of that parameter space. -->

### T1: <model name>

- **Origin** — structure: <literature [n] | variant of [n]: what changed | new>; application to this goal: <proposed before [n] | new — no prior work found as of <date>; basis: <n citing papers at abstract level, full-text probes, arXiv listing up to <date>>, queries: Appendix #...>
- **Status**: <viable | constrained | excluded>
- **One-line idea**: <...>

#### Field content

| Field | Spin / type | $SU(3)_C$ | $SU(2)_L$ | $Y$ | $Q$ | Self-conj. | Mass | Decays? | $Z_2$ |
|---|---|---|---|---|---|---|---|---|---|
| <`U1`> | complex vector | 3 | 1 | 2/3 | +2/3 | no | $M_{U_1}$ | yes (auto width) | — |

<!-- One row per component of an SU(2)_L multiplet (e.g. R2: `R2u` with Q=+5/3 and `R2d` with Q=+2/3,
     both "2" in the SU(2)_L column), since each component becomes its own field downstream.
     For a mass eigenstate that mixes gauge representations, write "mass basis" in the SU(2)_L and Y
     columns and add a line below the table: "gauge origin: <e.g. singlet (1,1,0) mixing with the
     doublets (1,2,1/2), mixing angle alpha>". -->

#### Lagrangian (BSM part, pipeline-ready)

$$\mathcal{L}_\text{BSM} = \ldots$$

where
- <symbol>: <definition — field/coupling, real or complex, chirality projector conventions>
- Provenance: <from source [n], Eq. (x); convention changes: none | ... — or — own parameterization; does not capture: ...>

#### Parameters

| Parameter | Meaning | Type | Benchmark | Allowed / interesting range | Basis for the range |
|---|---|---|---|---|---|
| $M_{U_1}$ | mass | real, GeV | 2000 | 1000–5000 | direct searches [n]; anomaly fit |

<!-- A benchmark you could not extract is written "not extracted — requires reading [n]", never guessed.
     A parameter that is dropped from the pipeline model (e.g. a keV splitting that only enters an analytic
     overlay) is marked "not a UFO parameter" in the Type column. -->

#### How it addresses the goal

<Matching relation between model parameters and the observable, with source or derivation. Parameter region that satisfies the success criterion.>

#### Constraints

| Constraint | Bound / impact | Source | Verdict |
|---|---|---|---|
| <e.g. LQ pair production, $b\tau$ channel> | <$M >$ ... GeV at 95% CL> | [n] | <ok / excludes part: ... / fatal> |

#### Collider signatures

| Process | Collider | Final state | Rate driver | Existing search (HEPData?) | Untested region |
|---|---|---|---|---|---|
| <$pp\to\tau\nu$ via $t$-channel $U_1$> | LHC 13 TeV | $\tau_h + E_T^\text{miss}$ | $g_bg_c$, $b/c$ PDFs | [n] (ins<id>, tables ...) | |

#### Non-collider predictions and tests

<!-- Delete if not applicable. For dark-matter and low-energy anomalies these are often the decisive tests. -->
- <e.g. signal in other targets, annual modulation, companion elastic spin-dependent signal, neutrino-telescope signal, flavour observables, EDMs — each with the size of the effect and the experiment that can see it>

#### Pipeline feasibility

- Tree-level UFO possible: <yes / yes with effective vertices: ... / no: ...>
- Special requirements: <heavy-flavour initial states, LHCO output, LUXlep PDF, CalcHEP + micrOmegas for DM, ...>
- Not executable with the current pipeline: <none | e.g. displaced vertices, NLO, expert-mode recast>

#### Open issues

- <theory or phenomenology questions this study will not settle>

## 4. Comparison and Ranking

| Rank | Target | Addresses goal | Viability | Collider testability | Minimality | Pipeline feasibility | Novelty |
|---|---|---|---|---|---|---|---|
| 1 | T1 | | | | | | |

<Justification of the ranking in a few sentences per target.>

## 5. Recommended Research Program

| Plan | Status | Target(s) | Physics question | Deliverable (figure/table) | Strategy | Depends on |
|---|---|---|---|---|---|---|
| `plans/plan_01_<slug>.md` | <written / proposed> | T1 <(or T1–T3 via a shared simplified model)> | <e.g. which part of the anomaly-preferred region is excluded by LHC mono-τ data?> | <exclusion contour in (M, g) with anomaly band> | <recast / projection / characterization / DM complementarity> | — |

## 6. Decisions for the User

1. <Open decision — options — your recommendation and why>

## 7. References

<!-- Every entry verified via INSPIRE/arXiv in this session (exists + title/author match).
     depth = how far it was read: source | abstract | title. Number the list once, at the end, without gaps. -->

[1] <First-author> et al., "<Title>", arXiv:<id> (depth: <source|abstract|title>) — used for: <what>
[2] <Data source: HEPData ins<id>, table "<name>" | web page <URL>, accessed <date>> (depth: data) — used for: <what>
[3] Grouped entry — <topic>, <n> papers verified in one batch lookup (depth: <abstract|title>): arXiv:<id>, <id>, ...

## Appendix: Search Log

| # | Service | Query | Yield |
|---|---|---|---|
| 1 | INSPIRE | `<query>` | <n hits; what was taken from it> |
