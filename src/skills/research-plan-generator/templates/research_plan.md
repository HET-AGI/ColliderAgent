<!-- RESEARCH PLAN TEMPLATE
     - Fill every <...> placeholder; delete guidance comments and sections marked optional if unused,
       then renumber the remaining sections consecutively.
     - Sections 1–4 follow the task-prompt format consumed by the pheno-pipeline-orchestrator skill.
     - The sub-structure is a starting point: add sub-sections and steps (several processes, calibration,
       interpolation, ...) where the study needs them. Do not squeeze a study into the skeleton.
     - Be explicit: no "suitable cuts", "appropriate range", "standard settings".
     - Labels: [estimate] own estimate, [assumed] analysis choice not fixed by a source, [unverified] unchecked fact. -->

> **Research plan** `<plan_nn_slug>` — study `<study_label>`, target `<T-id: model name>` — generated <YYYY-MM-DD> by the principal-investigator agent.
> User goal: "<one-line paraphrase of the user's prompt>".
> Depends on: <none | plan_xx (reuses `models/<Model>_UFO`, skip model building)>.
> Caveats: <study-level caveats a reader of the results must know — e.g. "the scanned coupling regime is in tension with flavour bounds in generic UV completions", "LO + fast simulation" | none>.

# 1. Target

<Two to four sentences: the physics question, the model, and the concrete deliverable — e.g. "Considering the $U_1$ leptoquark model described in this document, plot the 2σ exclusion contour in the $(M_{U_1}, \sqrt{|g_cg_b|})$ plane from LHC $pp\to\tau\nu$ data, together with the band preferred by $R_{D^{(*)}}$.">

Deliverables (with output file names):
- <Figure 1 (`output/figures/<name>.pdf`): ...>
- <Table / data file (`output/data/<name>.csv`): ...>

---

# 2. Model

<One paragraph introducing the model.>

<!-- If the model already exists from an earlier plan, replace 2.1–2.2 by:
     "Reuse the UFO model `models/<Model>_UFO` (FeynRules file `models/<Model>.fr`) built by plan_xx. Skip model building."
     and still list the particles and parameters that Section 3 refers to. -->

## 2.1 Lagrangian

$$\mathcal{L}_\text{BSM} = \ldots$$

Here,
- <$X$> is a <real/complex scalar | Dirac/Majorana fermion | real/complex vector> beyond the SM: colour <singlet/triplet/...>, $SU(2)_L$ <singlet/...>, hypercharge $Y=$ <...> ($Q=T_3+Y$), electric charge $Q=$ <...>. It is <not> self-conjugate. Suggested name: `<Xx>`.
- $D_\mu$ is the covariant derivative containing the SM gauge fields <under which $X$ is charged>.
- $P_{L,R}=\frac12(1\mp\gamma^5)$ are the chirality projectors.
- <every SM field symbol used: e.g. $\tau$ is the tau lepton, $\nu_\tau$ the tau neutrino, $b$ the bottom quark>
- <every coupling: symbol, real or complex, dimensionless or GeV>

<!-- Only the BSM part. "+ h.c." explicit where needed. Loop-induced couplings as effective operators with explicit coefficients. Mark Z2-odd fields for dark matter models. -->

## 2.2 Parameters

The free (external) parameters are:
- <$M_X$>: mass of $X$. <Benchmark / scan: see Section 3.3.>
- <$g_1$, ...>: <definition>. Real.

<Derived (internal) parameters, if any — given as formulas of the free ones, with every numerical constant and its source: e.g. $c_{c\nu}=V_{cs}\beta_{23}+V_{cb}$ with $V_{cs}=\ldots$ (PDG ...).>

- Width of $X$: computed automatically by MadGraph at each parameter point. <Cross-check value [estimate]: $\Gamma/M\simeq\ldots$> <or: fixed to ... GeV because ...>

<SM-side settings that differ from the pipeline defaults (diagonal CKM, massless light fermions, massive $b$): e.g. "set $m_b=0$: $b$ quarks appear in the initial state". Otherwise: "SM parameters at their defaults.">

<Model outputs required: UFO (default) <and CalcHEP, for the Dark Matter section>.>

---

# 3. Collider Simulation

## 3.1 Process

$$<pp \to \ldots>$$

<!-- Several processes are fine: label them P1, P2, ... and say whether they are generated together or separately. -->

<State what the process string must capture:
- which diagrams matter (e.g. "mediated by $t$-channel $U_1$ exchange; include SM–BSM interference" or "BSM-only contribution")
- initial-state flavours (e.g. "include $b$ and $c$ quarks in the proton")
- charge-conjugate processes to add
- decay chains, and whether decays are done in the matrix element or with MadSpin>

## 3.2 Collider simulation settings

There are <n> runs. For each run:
- collider: <13 TeV LHC ($pp$) | 3 TeV $\mu^+\mu^-$ | ...>
- event number: <...> per parameter point
- PDF: <MG5 default | LHAPDF set name and ID>
- parton shower: <none | Pythia8> <!-- "none" is fine: a parton-level cross-section campaign is a legitimate plan -->
- detector simulation: <none | Delphes ATLAS card | Delphes CMS card | Delphes default card>
- output format for reconstructed events: <LHCO — required if Section 4 reads reconstructed events>
- generator-level cuts: <none beyond MG5 defaults | e.g. $m_{\ell\ell}>120$ GeV>

<Run 1: ... / Run 2: ... — what differs between runs.>

## 3.3 Parameter settings for each run

- <$g_1 = 1$> <(reference coupling; the signal scales as $g^4$, see Section 4.2)>
- <$M_X$ = 750, 1000, 1250, 1500, 2000, 2500, 3000 GeV>
- all other parameters at their defaults

<!-- A non-rectangular scan is given as a table: one row per (run group, mass) with its list of coupling values.
     If no exact scaling law exists (e.g. the width enters through a resonant contribution), scan the coupling
     explicitly and describe the interpolation in Section 4.2. State the total number of runs and events. -->

<!-- Sensitivity projections: add "## 3.4 Background processes" — one entry per background with process,
     model (`sm`), event number, generator-level cuts, and the K-factor (with source) to apply in Section 4. -->

---

# 4. Numerical Analysis

## 4.1 Experimental data

<!-- For recasts / comparisons with data. Otherwise delete. -->

**<Experiment, search name>** (arXiv:<id>, HEPData ins<id>, <Table n>):
- stored as `<research/<study_label>/data/...csv>` <or given inline:>
- luminosity: <...> fb$^{-1}$ at $\sqrt s=$ <...> TeV
- observable and binning: <$m_T$, n bins from ... to ... GeV>
- columns: observed events $n_i$, SM background $b_i$, background uncertainty $\delta b_i$

| <bin / signal region> | $n_\text{obs}$ | $b_\text{SM}$ | $\delta b$ |
|---|---|---|---|

<!-- For a limit reinterpretation the data are instead a grid of published upper limits: give the file, its
     columns (e.g. mediator mass, invisible-particle mass, 95% CL upper limit on the cross section in fb),
     how to interpolate between grid points, and the assumption that makes the published limit applicable
     to this model (same final state and kinematics; any acceptance ratio with its [assumed] inputs). -->

<How to read the data file: HEPData CSV files hold several blocks separated by blank lines, each with `#:` header lines and its own column line — name the block and columns to use.>

<Published regions/bins that are **not** used, and why (e.g. "the $b$-veto regions are dropped: the paper reports large SM–BSM interference there, which this signal model does not include").>

## 4.2 Simulated signal events

<!-- Add steps as needed, e.g. "object definitions", "calibration", "interpolation in the coupling". -->

### Step 1: event selection

Read the <reconstructed (LHCO) | reconstructed (Delphes ROOT — needed for truth jet flavour) | parton-level (LHE)> events of each run and apply:
- <object definitions: e.g. hadronic tau with $p_T>80$ GeV, $|\eta|<2.3$>
- <vetoes>
- <event-level cuts, with the exact definition of every derived variable, e.g. $m_T=\sqrt{2p_T^\tau E_T^\text{miss}(1-\cos\Delta\phi)}$>

### Step 2: signal prediction

<How selected events become a prediction: e.g.
$$s_i = \frac{N_i^\text{pass}}{N_\text{gen}}\times\sigma\times\mathcal{L}\;(\times K)$$
with the cross section read from the MadGraph output of each run; coupling rescaling rule if a reference coupling is used; K-factor value and source if applied.>

## 4.3 Statistical analysis

<Exact prescription: test statistic, treatment of background uncertainty (nuisance parameters), combination across bins/experiments, and the criterion defining the result — e.g. "$-2\Delta\ln L = 4.0$ defines the 2σ exclusion", or "$Z=\sqrt{2[(s+b)\ln(1+s/b)-s]}\ge 2$ defines the expected 95% CL reach".>

<Systematic variations to show as bands or alternative curves: e.g. K-factor range, scale choice, each [assumed] input varied over a stated range.>

## 4.4 Figure

The figure contains:
1. **<element>** — <what it is, how obtained (section reference), line/fill style>
2. **<analytic overlay, e.g. anomaly-preferred band>** — <closed-form expression, input values with uncertainties, source>

Plot styles:
- aspect ratio: <...>
- x-axis: <label [unit]>, range <[a, b]>, <linear | log>
- y-axis: <label [unit]>, range <[a, b]>, <linear | log>
- legend / annotations: <...>

---

<!-- OPTIONAL -->
# 5. Dark Matter Observables

Computed with micrOmegas from the CalcHEP output of the same model (not part of the collider pipeline).
- $Z_2$-odd particles: <...> (dark matter candidate: <...>)
- observables: <relic density $\Omega h^2$ | SI/SD direct-detection cross sections | ...>
- parameter points: <...>
- use in figures: <e.g. overlay the $\Omega h^2=0.12$ contour in Figure 1>
- interpretation notes: <e.g. "the model is inelastic: micrOmegas' elastic $\sigma^\text{SI}_p$ (splitting switched off) is the $\sigma_p$ entering the inelastic rate — compare it with the closed-form value of Section 2, do not compare it with elastic limits">
- analytic or scripted overlays not computed by micrOmegas (e.g. the direct-detection event rate): <formula or script path, its inputs, and its validation against a published result>

---

<!-- RECOMMENDED for recasts -->
# 6. Validation

Before interpreting the results, validate the analysis chain:
- <e.g. reproduce the experiment's expected signal yield for its own benchmark ($W'_\text{SSM}$ at 3 TeV: n events in bin k, HEPData Table m) within 30%>
- <e.g. compare the LO cross section at a benchmark point with the value quoted in arXiv:<id>, Table n>
- <calibration, if any: the constant, the subset of validation points it is fixed on, and the remaining points it is tested on — declared here, before running>

If validation fails, report the discrepancy with the results instead of tuning the analysis to match.

---

# Appendix: Rationale and References

<!-- For human readers; downstream subagents do not need this section. -->

- **Why this study**: <link to target report `research/<study_label>/targets.md`, target <T-id>>
- **Design choices**: <why this process / collider / benchmark / statistics; approximations made and their expected impact (LO, fast detector simulation, K-factors, narrow width, ...)>
- **Expected outcome** [estimate]: <rough expectation and the estimate behind it — so that surprising results get noticed>
- **References** (all verified):
  - [1] <First-author> et al., "<Title>", arXiv:<id> — used for: <...>
