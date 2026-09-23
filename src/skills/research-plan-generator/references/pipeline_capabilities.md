# Pipeline Capabilities Reference

What the downstream ColliderAgent pipeline can execute, and what each stage needs from a research plan. A plan that asks for something outside this document will fail or be silently approximated — design within it, and state openly in the plan when the physics would call for more.

This document summarizes the skills `feynrules-model-generator`, `feynrules-model-validator`, `ufo-generator`, `calchep-generator`, `madgraph-simulator`, `madanalysis-analyzer`, `micromegas-calculator`, and the agents that use them. When in doubt, read those skills — they are the source of truth.

## 1. Stage Overview

| Step | Subagent | Tools | Consumes from the plan | Produces |
|------|----------|-------|------------------------|----------|
| 1 | model-generator | FeynRules (Mathematica) → UFO / CalcHEP | Section 2 (Model) | `models/<Model>.fr`, `models/<Model>_UFO/` |
| 2 | collider-simulator | MadGraph5_aMC, Pythia8, Delphes, MadSpin | Section 3 (Collider Simulation) | `events/<process_label>/Events/run_XX/` |
| 3 | event-analyzer (optional) | MadAnalysis5, normal mode | Section 4 (distributions, simple cut-flows) | `analysis/<label>/` |
| 4 | pheno-analyzer | Python: numpy, scipy, matplotlib, uproot | Section 4 (data, selections, statistics, figures) | `scripts/*.py`, `output/figures/`, `output/data/` |
| — | (main agent, outside the 4-step pipeline) | micrOmegas via `micromegas-calculator` skill | Section 5 (Dark Matter Observables), if present | `dm/<project_label>/<run_label>/results.json` |

The orchestrator passes information between stages; **subagents see only what is in the plan** plus the previous stage's summary. They do not see the target report, the literature, or the user's original prompt.

## 2. Model Building (Step 1)

Supported:
- BSM extension of the SM from a LaTeX Lagrangian: new scalars, fermions (Dirac/Majorana), vectors, spin-2; new couplings; mixing matrices
- Automatic validation: hermiticity, diagonal quadratic and mass terms, kinetic-term normalisation
- Output as UFO (MadGraph5) and/or CalcHEP (micrOmegas) — request CalcHEP explicitly in the plan if Section 5 is used
- Widths: external parameter or computed automatically by MadGraph (`Auto`)

Requirements on the plan: see Section 4 of the research-target-finder skill's `references/model_building_guide.md` (field table, mass basis, explicit chirality and h.c., real/complex couplings, names ≥ 2 characters).

Defaults of the SM part (BSM extensions are built on FeynRules' `SM.fr` with the restrictions `Massless.rst` and `DiagonalCKM.rst` loaded automatically):
- **CKM matrix = identity.** No CKM-suppressed SM vertices exist in the model; CKM factors needed in BSM couplings must be written into them as numerical constants
- **Light fermions massless** ($e,\mu,u,d,s,c$ in the standard `Massless.rst`; the generated `param_card` is the authority); $b$, $t$, $\tau$ keep their masses. If the study needs something else (e.g. a massless $b$ for a consistent five-flavour scheme, or a charm Yukawa), say so explicitly in the Model section — it is set through the parameter card or a custom restriction file
- **New couplings carry the interaction order `NP`** (SM couplings: `QCD`, `QED`). This allows diagram selection in the process definition — see Section 3

Not supported → how to plan around it:
| Limitation | Workaround |
|---|---|
| Tree-level models only (no NLO counterterms, no loop-induced vertices) | Write loop-induced couplings ($gg\to S$, $S\to\gamma\gamma$, ...) as effective operators with explicit coefficients; apply higher-order K-factors from the literature in Step 4 (cite the source) |
| The SM part is fixed (FeynRules built-in SM) | Modify SM couplings through added BSM operators, not by editing the SM |
| Full $SU(2)_L$-covariant model building is error-prone | Give the mass-basis component Lagrangian |
| Existing public UFO models are not fetched automatically | If a standard model should be used as-is, say so and give its location; otherwise write the Lagrangian. MG5 built-in models (e.g. `sm`, `mssm`) can be used by name, skipping Step 1 |

## 3. Event Generation (Step 2)

Supported:
- LO matrix elements for $2\to n$ processes with decay chains; multi-particle labels; several processes added together
- Colliders: $pp$ at any energy (set beam energies), and lepton colliders ($e^+e^-$, $\mu^+\mu^-$) via beam-type settings; lepton-in-proton initial states with the LUXlep PDF set
- PDFs: MG5 default (`nn23lo1`), or any LHAPDF set by name + ID (e.g. `NNPDF31_lo_as_0118` = 315000, `NNPDF31_nlo_as_0118` = 303400, `CT18NLO` = 14400, `LUXlep-NNPDF31_nlo_as_0118_luxqed` = 82400)
- Parton shower and hadronization: Pythia8
- Fast detector simulation: Delphes with the `cms`, `atlas`, or `default` card. The Delphes **ROOT file** is always kept; **LHCO output** is optional and must be requested. LHCO is the simplest format for Step 4 (one line per reconstructed object, with the card's own $b$-tag and $\tau$-tag decisions) but has no truth information — an analysis that needs truth jet flavour (custom $b$-/$c$-tag working points, mistag studies) must read the ROOT file with `uproot`
- Heavy-flavour initial states: $b$ (and $c$) quarks are included by stating it in the plan — the proton and jet definitions are then extended (`define p = g u c d s u~ c~ d~ s~ b b~`)
- Diagram selection by coupling order: state in words what is wanted (SM only, BSM only, interference) and, where helpful, in MadGraph syntax — amplitude-level `NP=2`, squared-level `NP^2==4` (pure BSM for a two-vertex exchange) or `NP^2==2` (SM–BSM interference); excluding particles with `/ w+ w-`
- MadSpin for spin-correlated decays of heavy SM or BSM particles
- Parameter scans over masses/couplings with `scan:[...]`; automatic widths per scan point
- Generator-level cuts through run-card parameters (`ptj`, `ptl`, `etal`, `drll`, `mmll`, ...). To cut on one specific particle (e.g. the $\tau$), use the per-PDG-code form, which is unambiguous: `pt_min_pdg = {15: 150}`, `mxx_min_pdg = {...}`
- SM background samples with the built-in `sm` model

Not supported / not documented → how to plan around it:
| Limitation | Workaround |
|---|---|
| NLO QCD event generation for BSM models | LO + K-factor from the literature (cite); state the resulting uncertainty |
| Jet matching/merging (MLM, CKKW-L) is not part of the documented workflow | Avoid analyses whose signal definition depends on extra hard jets; for mono-jet–type signatures generate the hard jet at matrix-element level with a generator-level $p_T$ cut, and state the approximation |
| Loop-induced processes | Effective vertices (Section 2). For $gg\to S$ the LO effective-vertex rate is too low by a factor of roughly 2–3: normalize to reference cross sections (LHC Higgs Working Group, arXiv:1610.07922) or to the experiment's reference rate, never to the LO number. The resonance has no $p_T$ at matrix-element level — avoid observables that depend on it |
| Automatic widths are LO and include only channels present in the model | For narrow states whose branching ratios matter (e.g. light scalars), build $\sigma\times\text{BR}$ in Step 4 from reference branching ratios rescaled by the model's couplings, and say so in the plan; or fix the width explicitly |
| Long-lived particles / displaced vertices | Delphes cards used here have no displaced-object reconstruction. Restrict to prompt decays, or plan a parton-level study of decay lengths with a stated efficiency assumption |
| Custom Delphes cards (e.g. future-collider detectors) | Only if the user provides the card file path; otherwise use `default` and state it |
| Pile-up, full detector effects, data-driven backgrounds | Out of scope — use published background estimates for recasts |

Information the plan must give: process in physics notation **and** any subtlety the process string must capture (heavy flavours in the proton, charge-conjugate processes, which resonances are on-shell, interference wanted or not); collider and $\sqrt s$; number of events; PDF; shower / detector / output format; parameter values per run; scan points; width treatment.

Statistics guidance: shipped examples use 10k–50k events per parameter point and ~10 scan points per run. High-mass tail analyses with tight cuts need enough events **after** selection — if the selection efficiency is expected to be below 1%, raise statistics or add a generator-level cut (and correct the cross section consistently).

## 4. Analysis (Steps 3–4)

**MadAnalysis5 (Step 3, optional)** — normal mode only: histograms of standard observables ($p_T$, $\eta$, $M$, $\Delta R$, $E_T^\text{miss}$, $H_T$, ...) and sequential cuts at parton (LHE), hadron (HepMC), or reco (LHCO/ROOT) level. Use it for kinematic distributions and simple cut-flows. **Expert mode and the Public Analysis Database (automated recasts) are not supported.**

**Python post-processing (Step 4)** — reads LHCO / Delphes ROOT (via `uproot`) / LHE event by event; arbitrary selections and derived variables ($m_T$, $m_{T2}$, angular variables, ...); binned signal templates; statistical inference (counting significance, $\chi^2$, profile likelihood with nuisance parameters, combination of experiments, exclusion contours); publication-quality figures. Analytic curves given in the plan (e.g. an anomaly-preferred band) can be overlaid.

Consequence for recasts: an experimental search is reinterpreted by **re-implementing its selection in Step 4** and comparing with the published binned data. The plan must therefore contain the full selection, bin edges, observed counts, background and its uncertainty (or the HEPData file path), luminosity, and the statistical prescription.

What a recast here cannot match, and how to handle it:
- The experiment's signal sample is usually an inclusive, jet-merged, higher-order-normalized sample; the pipeline generates a fixed-order LO process. Do not try to match generator-level quantities — **validate at the level of signal-region yields** against numbers the experiment published for its own benchmark (HEPData yields, acceptance × efficiency tables)
- Detector performance the paper does not quote (a mistag rate, a trigger efficiency) has to be `[assumed]`. A **calibration constant** is legitimate only if it is declared in the plan before running, fixed on a stated subset of the validation points, and tested on the remaining ones
- Use only the signal regions whose signal model the pipeline can reproduce, and state in the plan which published regions are left out and why

Not computed by the pipeline: flavour observables, electroweak precision fits, Higgs signal-strength fits, loop-level matching. If a figure needs them (as bands or constraints), give closed-form expressions with sources in the plan, or quote the literature result to overlay.

## 5. Dark Matter Observables (outside the 4-step pipeline)

The `micromegas-calculator` skill computes relic density, spin-independent/dependent direct-detection cross sections, and indirect-detection quantities from a CalcHEP model. It is not an orchestrator step: the main agent runs it after Step 1. A plan that needs it must (a) request CalcHEP output in the Model section, (b) mark all $Z_2$-odd fields, (c) list the observables and scan points in a dedicated section. Relic-density scans cost minutes per point for models with many co-annihilation channels — keep scans coarse.

Limits to plan around:
- micrOmegas returns **elastic** DM–nucleon cross sections only — no inelastic (endothermic/exothermic) rates and no recoil spectra. For an inelastic model, its elastic cross section computed with the splitting switched off is exactly the $\sigma_p$ that enters the inelastic rate: use it as a cross-check of the closed-form value, and say in the plan how the number is to be interpreted. The event rate itself (velocity integral, form factor, detector efficiency) must be supplied by the plan as a closed-form or scripted calculation for Step 4, validated against the experiment's published band
- Solar capture, indirect-detection limits beyond $\langle\sigma v\rangle$, and late-decay constraints are not computed — quote the literature or list them as open issues
- When collider scan points depend on the relic density (e.g. "scan along the relic line"), break the circularity in the plan: give an analytic relic line (with source) to define the points, and use micrOmegas at a few points to verify it

Campaign size: parton-level cross-section campaigns are cheap — a plan may contain a few hundred such points if it says why (a pure cross-section campaign without shower and detector is a perfectly good plan). Showered + Delphes runs are the expensive ones; the shipped examples use of order 10–50 of them.

## 6. Study Strategies That Fit the Pipeline

| Strategy | Deliverable | Needs | Notes |
|---|---|---|---|
| **Signal characterization** | cross section vs mass/coupling; kinematic distributions; branching ratios | Steps 1–2 (+3 or 4) | Cheapest; good first plan for a new model |
| **Recast of an existing search** | exclusion contour in a parameter plane | Steps 1–2, 4; published binned data (HEPData) | Validate first on a benchmark the experiment itself provides (e.g. its $W'$/$Z'$ signal) |
| **Limit reinterpretation** | excluded mass/coupling range | Steps 1–2, 4; published $\sigma\times\text{BR}$ limits | Valid only if the signal kinematics/acceptance match the experiment's benchmark — state the assumption |
| **Sensitivity projection** (HL-LHC, future colliders) | expected significance / reach | Steps 1–2, 4; signal **and** background samples | Backgrounds with the `sm` model; list each background process; LO + K-factors |
| **Collider + dark matter complementarity** | collider limits overlaid with relic/direct-detection contours | Steps 1–2, 4 + micrOmegas | Two model outputs (UFO + CalcHEP) from one `.fr` |
