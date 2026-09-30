# Step 0 — Research (principal-investigator), study `lz_excess`

Date: 2026-09-21. Scope: `targets+plan`. Status: **success**, with open issues listed below.

## Request classification and interpreted goal

- **Mode**: A (model building — new constructions explicitly requested by the user), with a short landscape map of the existing explanations to position them.
- **Interpreted goal**: build at least two models that have not yet been proposed for the single 248 keV nuclear-recoil event reported by LZ (arXiv:2609.02823, posted 2026-09-02; 2.84 t yr; maximum local significance 3.4σ, global 2.6σ), vet them honestly, and write one pipeline-ready plan for the best one.

## Assumptions made on behalf of the user

1. "The LZ excess" is the 248 keV event of arXiv:2609.02823, not the low-mass result arXiv:2512.08065 (which reports no dark-matter excess).
2. "Never been considered to explain the LZ excess" = not proposed as an interpretation of this event in any paper found by the logged searches (as of 2026-09-21; newest arXiv entry visible was dated 2026-09-16). It does not mean that every ingredient is new: both constructions are variants of the known $t$-channel simplified models.
3. Models with an LHC-accessible mediator are preferred, because the pipeline is a collider pipeline.
4. Dark matter makes up the full local density; Standard Halo Model.

## Research targets

| ID | Model | Origin | Rank | One-line rationale | Status |
|---|---|---|---|---|---|
| T1 | Quark-portal pseudo-Dirac dark matter: singlet fermion $\chi$ (split by δ ≈ 230–340 keV) + coloured scalar $\varphi(3,1,\tfrac23)$ coupled to $u_R$ | new construction for the event; variant of `S3D_uR` (arXiv:2307.10367), cf. pseudo-Dirac bino | 1 | the Fierzed vector current is purely off-diagonal → endothermic scattering; the freeze-out coupling (λ ≈ 0.9–2.5) puts $\sigma_{\rm eff} = 5\times10^{-43}$–$1.3\times10^{-41}$ cm² inside LZ's band with no free normalisation; today's annihilation is $p$-wave into light quarks; LHC jets + $E_T^{\rm miss}$ status unknown in the literature | viable (halo-tail sensitive like all endothermic models; solar capture not computed) |
| T2 | Quark-portal split-scalar dark matter: complex singlet $S\to S_{1,2}$ + vector-like quark $\psi(3,1,\tfrac23)$ coupled to $u_R$ | new construction for the event; variant of `F3C_uR`; nearest prior work arXiv:2609.09120 (elastic, $Z_3$) | 2 | $S_2$ cannot decay radiatively (0→0) and conversions decouple at $T\gg\delta$, so half the dark matter is the excited state: the model is automatically exothermic, with $y\sim0.05$–0.3 and $\sigma_{\rm eff}\sim(0.3$–$1.4)\times10^{-44}$ cm² | constrained: the $t$-channel thermal-relic version is excluded by LZ's own window; needs the coannihilation strip; $S_2\to S_1\gamma\gamma$ bound borderline |
| T3 | Majorana singlet + $d_R$-philic coloured scalar: elastic spin-dependent, neutron-dominated | new for the event; standard Majorana $t$-channel model otherwise | 3 | $\mathcal O_4$ without halo-tail tuning | constrained — marginal: any elastic-SD explanation needs $\sigma^n_{\rm SD}\approx(3$–$7)\times10^{-42}$ cm² at 500 GeV against LZ's own limit of $2.6\times10^{-42}$ cm²; not assessed quantitatively |

Existing explanations (≥ 83 papers, 10 classes, plus the no-new-physics hypothesis) are catalogued in Section 2 of `targets.md`.

## Research plans

| File | Target | Deliverable | Colliders / processes | Depends on |
|---|---|---|---|---|
| `research/lz_excess/plans/plan_01_t1_quarkportal_lhc_reinterpretation.md` (**written**) | T1 | ATLAS-excluded region, relic line, required splitting δ and HL-LHC event counts in the $(M_\varphi,\lambda)$ plane ($m_\chi$ = 1 TeV and 0.5 TeV) and in the $(M_\varphi,m_\chi)$ plane on the relic line; table of cross-section coefficients in powers of λ | $pp$ 13 TeV and 14 TeV, parton level: $pp\to\varphi\varphi^*$ (QCD + $t$-channel χ), $pp\to\varphi\chi$; 310 runs, 3.2M events; micrOMEGAs at 8 points | — |
| `plan_02_t1_hllhc_projection` (proposed) | T1 | HL-LHC reach with backgrounds | 14 TeV, jets + $E_T^{\rm miss}$, mono-jet | plan_01 |
| `plan_03_t2_compressed_vlq` (proposed) | T2 | coannihilation strip vs mono-jet limits | 13/14 TeV, $pp\to\psi\bar\psi$ compressed | — |
| `plan_04_t3_samesign_mediators` (proposed) | T3 | same-sign $dd\to\varphi\varphi$ limits vs the $\sigma^n_{\rm SD}$ band | 13 TeV | plan_01 (method) |

The statistical prescription of plan_01 was tested in this session against the experiment's own result: crossing at 1232 GeV vs ATLAS's published single-squark limit of 1220 GeV.

## Open decisions for the user

1. Is "new as an interpretation of the event" the intended meaning of "never been considered"? (Recommended: yes.)
2. A deeper pass is needed before publication-level claims: solar capture for T1; the $S_2\to S_1\gamma\gamma$ lifetime and X-ray limits for T2; LZ's data release (not resolvable on 2026-09-21) to replace the by-eye band; a re-run of the arXiv listing search (the literature grows by ~4 papers per day).
3. $u_R$ (plan as written) or $d_R$ version of T1?
4. Run the cheap plan_01 now and decide on the expensive plan_02 after LZ's next exposure update? (Recommended.)

## Verification statistics

- Lookups: 34 logged (13 INSPIRE, 7 arXiv API, 9 HEPData, 1 WebSearch, 1 web page fetched twice, 3 source downloads). Budget was 35–45 and 3 downloads.
- References verified (exist + match): 42 numbered entries + 51 LZ-event papers cited by ID. Reading depth: **source** 3 (arXiv:2609.02823, 2307.10367, 2609.08993) + 1 raw web page; **abstract (incl. HEPData tables where used)** 31 numbered + 49 by-ID; **title** 4 numbered (hep-ph/0101138, 2105.00599, Lewin–Smith, and the operator-basis papers are not cited) + 2 by-ID.
- `[unverified]` items remaining: Standard Halo Model parameter values and Helm form-factor parameters used in `tools/idm_rate.py`; nucleon spin fractions; the numerical value $2.2\times10^{-26}$ cm³/s (abstract only partially printed); the mass at which LZ's Fig. S7 is drawn (taken as 1 TeV, [assumed]); the upper mass end and width of T2's coannihilation strip; X-ray limits on $S_2\to S_1\gamma\gamma$; fermion-vs-scalar pair-production rate ratio; one-loop elastic SI for T1 in the compressed region.
- HEPData record of the LZ paper: announced (doi:10.17182/hepdata.182472.v1) but not resolvable — all LZ intervals are read off figures by eye (±30%).

## Files written

- `research/lz_excess/targets.md`
- `research/lz_excess/plans/plan_01_t1_quarkportal_lhc_reinterpretation.md`
- `research/lz_excess/data/`: `ins1827025_xsec_ul_1.csv`, `ins1827025_obs_contour_2.csv`, `ins2841863_SI_cross_section.csv`, `ins2841863_SDn_cross_section.csv`, `stop_xsec_13TeV_nnll.csv`, `susyxsec_stop13TeV.html`
- `research/lz_excess/sources/`: `2609.02823/`, `2307.10367/`, `2609.08993/`
- `research/lz_excess/tools/`: `inspire.py`, `idm_rate.py` (imported by plan_01), `exo_rate.py`, `tchannel_estimates.py`, `search_log.tsv`, `citing_titles.txt`, `citing_abstracts.txt`, `citing_abstracts.xml`, `prior_art_abstracts.txt`, `arxiv_newest_q1.txt`, `arxiv_newest_q2.txt`
- `progress/lz_excess/step0_research.md` (this file)
