# Step 0 — Research targets and plan: `rd_anomaly`

Date: 2026-09-20. Agent: principal-investigator. Scope: `targets+plan` (exactly one plan requested). Status: **success**.

## 1. Request classification and interpreted goal

- **Mode**: A (model building), with a brief landscape map (Mode-B style) to position the model.
- **Interpreted goal**: identify the minimal BSM mediator that enhances $b\to c\tau\nu$ by the amount required by the current $R_D$/$R_{D^*}$ world average, fix its anomaly-preferred parameter region, and design a pipeline-executable recast that shows how much of that region LHC high-$p_T$ data exclude now and could probe with 3 ab$^{-1}$.
- **Key facts established** (all sourced in `research/rd_anomaly/targets.md`):
  - HFLAV CKM-2025 average (28.09.2025): $R_D=0.358\pm0.024$, $R_{D^*}=0.281\pm0.011$, correlation $-0.374$; SM $0.298\pm0.004$, $0.254\pm0.005$; combined tension about $3.8\sigma$.
  - EFT requirement: left-handed vector operator, $C_{V_L}=0.066\pm0.016$ [own one-parameter fit to the CKM-2025 numbers]; literature fit with Spring-2024 data: $0.079(16)$, pull 4.8 (arXiv:2405.06062).
  - ATLAS published in June 2026 the first dedicated $U_1$ search in $\tau_\text{had}+E_T^\text{miss}(+b)$ (arXiv:2606.02067, 140 fb$^{-1}$) with a complete HEPData record (ins3164547). An INSPIRE citation search found no reinterpretation of it yet.

## 2. Assumptions made on behalf of the user

1. "New physics model" = a BSM model, not necessarily an unpublished one; the tree-level mediator space for $b\to c\tau\nu$ is fully mapped in the literature, so the top target is a literature model and is labelled as such.
2. "The anomalies" = HFLAV CKM-2025 world average.
3. "LHC data" = published ATLAS/CMS Run-2 high-$p_T$ results (recast) plus a luminosity-scaled 3 ab$^{-1}$ projection; flavour measurements define the anomaly, they are not the test.
4. Simplified-model level (one mediator, tree level, mass basis); no UV completion is built.
5. Only $R_{D^{(*)}}$ is addressed; no other flavour observable is fitted.
6. For the collider study the large-$\beta_L^{23}$ regime of the $U_1$ model is targeted (where $\tau\nu+b$ is sensitive); this regime is in tension with loop-level flavour bounds in generic UV completions — stated in the report and the plan.

## 3. Research targets

| ID | Model | Origin | Rank | One-line rationale | Status |
|---|---|---|---|---|---|
| T1 | Left-handed $U_1$ vector leptoquark $(3,1,2/3)$; parameters $M_{U_1}$, $g_U$, $\beta_L^{23}$ | literature (arXiv:1901.10480 as used in ATLAS arXiv:2606.02067) | 1 | generates $C_{V_L}>0$, the best single-operator fit; only target with an experimental benchmark (yields, efficiencies, limits) to validate the recast | viable (large $\beta_L^{23}$: UV-dependent flavour constraints) |
| T2 | $S_1$ scalar leptoquark $(\bar3,1,1/3)$ with $y_L^{b\tau}$, $y_R^{c\tau}$ ($C_{S_L}=-4C_T$) | literature (arXiv:1511.01900; couplings from arXiv:2405.06062) | 2 | renormalizable; never confronted with the new ATLAS $\tau\nu+b$ data; projected HL-LHC reach marginal | constrained |
| T3 | $R_2$ scalar leptoquark $(3,2,7/6)$ ($C_{S_L}=4C_T$, complex) | literature (couplings from arXiv:2405.06062) | 3 | hardest $\tau\nu$ tails, within HL-LHC reach; Lagrangian of the $Q=5/3$ component still to be taken from the source | constrained |
| T4 | colour-singlet $W'$ triplet; charged Higgs (2HDM) | literature (arXiv:1609.07138, arXiv:2405.06062) | — | documented dead ends ($\tau\tau$ limits; fit quality / sign) | strongly constrained / disfavoured |

## 4. Research plans

| File | Target | Deliverable | Colliders / processes | Depends on |
|---|---|---|---|---|
| `research/rd_anomaly/plans/plan_01_u1_taunub_recast.md` | T1 | 95% CL exclusion in $(M_{U_1},g_U)$ at $\beta_L^{23}=1.0$ and $2.2$ from a recast of the SR1b regions of ATLAS arXiv:2606.02067, overlaid with the published ATLAS limits (validation), the $R_{D^{(*)}}$ $1\sigma/2\sigma$ band (CKM-2025) and 3 ab$^{-1}$ projections; validation figure; results table | LHC 13 TeV; BSM-only $pp\to\tau\nu b$ (P1) and $pp\to\tau\nu c$ (P2), five-flavour scheme, Pythia8 + Delphes (ATLAS card), 48 runs × 10k events | none |

Recommended but not written (one-plan limit): plan_02 — $pp\to\tau\tau$ recast for the small-$\beta_L^{23}$ regime (reuses the UFO of plan_01; HEPData for arXiv:2503.19836 still to be checked); plan_03 — recast of the same ATLAS regions for T2 (then T3), reusing the validated analysis of plan_01.

Pre-checks done in this session (estimates, not pipeline runs): the two-bin CL$_s$ prescription of the plan, fed with ATLAS's own signal yields, reproduces the published $g_U$ limits within 7% (except $M=1.5$ TeV, $\beta_L^{23}=2.2$: 0.66 vs 0.52, where ATLAS gains from its $b$-veto regions). Naive 3 ab$^{-1}$ scaling reaches the central $R_{D^{(*)}}$ line only for $M_{U_1}\lesssim1.5$–2 TeV with reduced systematics.

## 5. Open decisions for the user

1. Is a literature model confronted with the newest data what was meant by "new physics model", or is a genuinely new construction (two-mediator / UV-complete) wanted? Recommendation: the former first.
2. Flavour regime of $U_1$: large $\beta_L^{23}$ ($\tau\nu+b$, plan_01) vs UV-motivated small $\beta_L^{23}$ ($\tau\tau$, plan_02). Recommendation: plan_01 first (it validates the chain), then plan_02.
3. Scalar-leptoquark follow-up (plan_03) — this is where new exclusion statements are expected. Recommendation: yes, after plan_01 validates.
4. Campaign size of plan_01: 480k events; reduced option 240k ($\beta_L^{23}=1.0$ only).

## 6. Verification status

- References verified in this session: **25** (23 via INSPIRE/arXiv with title and first-author match, plus the HFLAV CKM-2025 web page and the PDG 2025 CKM review). For 15 of them the abstract, page, equation and/or TeX source was read; the other 10 are verified at the title/author level only and are used only as pointers (marked as such in the reference list).
- Paper sources downloaded: 2 (arXiv:2606.02067, arXiv:2405.06062).
- Network lookups: about 22.
- `[unverified]` items remaining: **2**, both in `targets.md` — (i) the statement that the triplet leptoquarks $S_3$/$U_3$ cannot accommodate $R_{D^{(*)}}$ (landscape table; not used further); (ii) the sign convention of the covariant derivative in the $U_1$ kinetic term, which the ATLAS paper does not state (taken as the FeynRules SM convention; relevant for the relative sign of the non-minimal gluon coupling). Assumed numerical inputs in the plan that are not from a source are marked "assumed": light-jet mistag probability 0.01, fallback charm mistag 0.30, 20% signal uncertainty.

## 7. Files written

- `research/rd_anomaly/targets.md`
- `research/rd_anomaly/plans/plan_01_u1_taunub_recast.md`
- `research/rd_anomaly/data/` — 34 HEPData tables of ins3164547 (`ins3164547_*.csv`) and the derived `atlas_sr1b_expected_yields.csv`
- `research/rd_anomaly/tools/insp.py` (INSPIRE lookup helper), `tools/fit_cvl.py` ($C_{V_L}$ fit and band), `tools/estimate_limits.py` (reference implementation of the plan's statistical procedure)
- `research/rd_anomaly/sources/2606.02067/`, `research/rd_anomaly/sources/2405.06062/` (TeX sources, 10 MB)
- `progress/rd_anomaly/step0_research.md` (this file)
