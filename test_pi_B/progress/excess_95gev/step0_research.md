# Step 0 — Research (principal-investigator): `excess_95gev`

Date: 2026-09-20 · Scope: `targets` (no research plans written) · Status: success

## 1. Request classification and interpreted goal

- **Mode**: B. Model survey.
- **User prompt (verbatim)**: "Find all the models that could explain the 95 GeV diphoton excess reported at the LHC."
- **Interpreted goal**: catalogue all classes of BSM models containing a narrow neutral resonance at 95.4 GeV with $\sigma\times\text{BR}(\gamma\gamma)$ matching the CMS+ATLAS Run 2 excess ($\mu_{\gamma\gamma}=0.24^{+0.09}_{-0.08}$, i.e. ≈ 30 fb at 13 TeV), assess their viability, and identify the collider signatures that separate them.

## 2. Assumptions made on behalf of the user

1. The excess = CMS full Run 2 (2.9σ local / 1.3σ global at 95.4 GeV, arXiv:2405.18149) + ATLAS full Run 2 (1.7σ local, arXiv:2407.07546), combined unofficially in arXiv:2306.03889 (3.1σ local).
2. "Explain" = reproduce $\mu_{\gamma\gamma}$ within 1σ; LEP $b\bar b$ ($0.117\pm0.057$) and CMS $\tau\tau$ ($1.2\pm0.5$) hints are secondary, not required (LEP interpretation disputed by arXiv:2407.10948).
3. "All models" = all model classes with representative realizations; variants listed by reference; no paper-by-paper bibliography.
4. Collider of interest: LHC (Run 2/3, HL-LHC); $e^+e^-$ Higgs factory where decisive.
5. Report in English.

## 3. Research targets

| ID | Model | Origin | Rank | One-line rationale | Status |
|---|---|---|---|---|---|
| T1 | Singlet-like scalar of 2HDM + singlet (N2HDM / S2HDM, Yukawa type II/IV); stands in for the SUSY-singlet class (NMSSM family) | literature; simplified Lagrangian own parameterization | 1 | best-established; suppressed $c_b$ lifts BR($\gamma\gamma$); fits $\gamma\gamma$ + LEP; ggF-dominated | viable |
| T2 | Type-I 2HDM, fermiophobic-leaning light CP-even Higgs + light $H^\pm$ | literature; own parameterization | 2 | VBF/VH + $H^\pm$ cascades; testable against CMS per-production-mode limits | viable ($H^\pm$ limits to be updated) |
| T4 | Georgi–Machacek custodial singlet with light $H_5^{\pm\pm}$ (100–200 GeV) | literature; own parameterization | 3 | charged-scalar loops; striking companion signature | viable in a narrow region |
| T3 | CP-odd 95 GeV state (2HDM $A$, 2HD+a, CP-violating aligned 2HDM) | literature; own parameterization | 4 | fits $\gamma\gamma$ + $\tau\tau$; no VBF/VH, no LEP signal | constrained (flavour, EDM) |
| T6 | Singlet + vector-like matter / dilaton / radion (effective $SGG$, $S\gamma\gamma$) | literature; own parameterization | 5 | can always fit; interest lies in VLQ and $t\bar t\gamma\gamma$ channels | viable, weakly predictive |
| T5 | Real $Y=0$ triplet (ΔSM), Drell–Yan production | literature | 6 | needs $m_{\Delta^\pm}\approx95$ GeV, but $m_{\Delta^\pm}<110$ GeV is excluded (arXiv:2411.18618) | excluded (documented dead end) |
| T7 | SM + real singlet, pure mixing | bottom-up enumeration | 7 | needs $\sin^2\theta=0.24$: conflicts with LEP and 125 GeV Higgs rates | excluded `[estimate]` |

Landscape classes without a target block: A5 (scotogenic, minimal LRSM, $U(1)$ extensions, DM-motivated singlets), B3 (type-III 2HDM), C3 (2HDM + type-II seesaw, SUSY triplets), D (generic ALP — no dedicated paper found), E (spin-2 — no prior work found), F (no new physics).

## 4. Research plans

None written (scope `targets`). Recommended program (Section 5 of `targets.md`):

| Proposed file | Target | Deliverable | Colliders / processes | Depends on |
|---|---|---|---|---|
| `research/excess_95gev/plans/plan_01_h95_production_modes.md` | T1, T2, T3 (master simplified model `h95` / `A95`) | $\sigma\times$BR($\gamma\gamma$) per production mode and benchmark; $p_T^{\gamma\gamma}$, $N_\text{jet}$, $m_{jj}$ shapes | $pp$ 13 and 13.6 TeV: ggF (effective vertex), VBF, $Wh$, $Zh$, $t\bar th$ | — |
| `research/excess_95gev/plans/plan_02_h95_cms_modes_reinterpretation.md` | T1 vs T2 vs T3 | $(c_t,c_V)$ plane: $\mu_{\gamma\gamma}$ band, LEP band, CMS per-mode limits | $pp$ 13 TeV; uses `data/ins2791038_figure6a–6d.csv` | plan 01 |
| `research/excess_95gev/plans/plan_03_h95_ee_recoil_projection.md` | T1, T2, T4 (T3/T6 null) | expected significance vs $c_V^2$; recoil-mass spectrum | $e^+e^-\to Z(\mu\mu)h_{95}$ at 240 GeV + SM backgrounds | plan 01 |
| optional: `plan_04_t2_hpm_associated`, `plan_05_gm_h5pp_pairs` | T2; T4 | $H^\pm h_{95}$ / top-cascade rates; $H_5^{++}H_5^{--}$ same-sign dilepton rates | $pp$ 13.6 / 14 TeV | plan 01; source-level reading of arXiv:2312.13239, 2509.26155 |

## 5. Open decisions for the user

1. Which hints must be explained: $\gamma\gamma$ only (assumed) / + LEP $b\bar b$ / + CMS $\tau\tau$.
2. Deeper literature pass (source-level reading of N2HDM, type-I, GM papers for benchmark points and source-exact Lagrangians) before plans for T2-$H^\pm$ and T4.
3. Which targets to plan: recommended common simplified model (T1/T2/T3, plans 01–03) vs a model-specific study (T4 or T6).
4. Accept representing the SUSY models (NMSSM family) by the T1 simplified model — full SUSY spectra are not pipeline-executable.
5. Detector card for the $e^+e^-$ projection (Delphes `default` unless a card path is provided).
6. SM-like reference BRs and production shares at 95 GeV are `[unverified]` memory values and must be replaced by LHC Higgs WG numbers before plans are executed.

## 6. Verification bookkeeping

- Lookups: 25 network lookups in total (2 WebSearch, 1 WebFetch, 8 INSPIRE, 4 arXiv API batches, 1 arXiv e-print source, HEPData record/search/table downloads). One paper source downloaded (arXiv:2306.03889).
- **References verified: 83** — 43 in the main list (1 by TeX source + abstract, 38 by abstract, 4 by title/first author only) and 40 "variant" entries verified by title and first author only (used solely for the existence of the model named in the title; 6 of these titles were truncated in the lookup output).
- **`[unverified]` items remaining**:
  1. SM-like Higgs branching ratios and production shares at 95 GeV (inputs to every benchmark `[estimate]`).
  2. $b\to s\gamma$ bound on $m_{H^\pm}$ in type II/IV; LEP lower bound on $m_{H^\pm}$.
  3. Sign conventions of the type-I $H^\pm$ Yukawa Lagrangian (T2) and normalization of the $H_5^{\pm\pm}W^\mp W^\mp$ vertex (T4) — written from memory.
  4. Precision of the 125 GeV coupling measurements used in the T7 argument; VLQ mass limits and dijet limits at 95 GeV (T6); dilepton limits on a spin-2 state (class E).
  5. Nine entries taken from the bibliography of arXiv:2306.03889 but not looked up (listed at the end of Section 7 of `targets.md`).
- Notable finding during verification: the real-triplet explanation (arXiv:2306.15722) is excluded by its authors' later reinterpretation of stau searches (arXiv:2411.18618). ATLAS has no HEPData record for arXiv:2407.07546 (HTTP 404); CMS has six tables.

## 7. Files written

- `research/excess_95gev/targets.md`
- `research/excess_95gev/data/ins2791038_figure5a.csv` (limit relative to SM-like), `..._figure5b.csv` (limit in pb), `..._figure6a.csv` (ggH+ttH), `..._figure6b.csv` (VBF+VH), `..._figure6c.csv` (VBF), `..._figure6d.csv` (VH)
- `research/excess_95gev/sources/2306.03889/` (TeX source, unpacked)
- `progress/excess_95gev/step0_research.md` (this file)
