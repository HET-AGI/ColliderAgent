# Research Targets: Models for the 95 GeV Diphoton Excess

- **Study label**: `excess_95gev`
- **Date**: 2026-09-20
- **Mode**: B. Model survey
- **Literature access**: partial — INSPIRE, arXiv and HEPData APIs worked; the literature budget of this run was limited to 25 lookups and one paper source (arXiv:2306.03889). Consequences: (i) most papers were read at abstract level only, (ii) Lagrangians below are own mass-basis parameterizations, not copied from source equations, (iii) SM reference branching ratios at 95 GeV could not be retrieved and are tagged `[unverified]`.

<!-- Evidence labels used in this report:
     (untagged)    backed by a reference in Section 7, verified in this session
     [estimate]    own estimate; formula given
     [unverified]  from memory or a source that could not be checked -->

## 1. Problem Statement

### 1.1 User goal (verbatim)

> Find all the models that could explain the 95 GeV diphoton excess reported at the LHC.

### 1.2 Interpretation

- **Physics question**: Which classes of BSM models contain a narrow neutral resonance at $m\simeq95.4$ GeV whose rate $\sigma(pp\to\phi)\times\text{BR}(\phi\to\gamma\gamma)$ reproduces the excess seen by CMS and ATLAS in Run 2, which of them survive the other constraints, and which collider signatures tell them apart?
- **Success criterion**: the model contains a state with $m_\phi = 95.4$ GeV and a diphoton signal strength inside the $1\sigma$ range of the ATLAS+CMS combination, $\mu_{\gamma\gamma}=0.24^{+0.09}_{-0.08}$ [3], i.e. $\sigma\times\text{BR}(\gamma\gamma)\approx 30^{+11}_{-10}$ fb at 13 TeV `[estimate]` ($\mu_{\gamma\gamma}\times0.124$ pb, with the SM-like reference rate taken from the ratio of CMS HEPData tables, Section 1.3), and is not excluded by other data. Secondary (reported, not required): the LEP $b\bar b$ hint $\mu_{bb}=0.117\pm0.057$ and the CMS $\tau\tau$ hint $\mu_{\tau\tau}=1.2\pm0.5$ (both as quoted in [3]).
- **Boundary conditions**: none given by the user. Collider of interest taken to be the LHC (Run 2/3, HL-LHC); $e^+e^-$ Higgs factories are mentioned where they are the decisive test.
- **Assumptions made on the user's behalf**:
  1. "The 95 GeV diphoton excess" = CMS full Run 2 [1] + ATLAS full Run 2 [2], combined by theorists in [3]. There is no official ATLAS+CMS combination.
  2. "Explain" = reproduce $\mu_{\gamma\gamma}$ within $1\sigma$. The LEP $b\bar b$ and CMS $\tau\tau$ hints are optional, because the LEP interpretation is disputed [8] and the $\tau\tau$ rate is hard to fit together with $\gamma\gamma$ in most models.
  3. "All models" = all model **classes**, each with a representative minimal realization and its variants listed by reference. A paper-by-paper bibliography (more than 200 INSPIRE records) is not attempted — see the coverage statement in Section 2.
  4. Scope of this run is `targets`: no research plans are written; Section 5 is a recommendation only.
  5. Report language: English (language of the prompt).

### 1.3 Current status

| Observable | Measurement | SM prediction | Tension | Source | As of |
|---|---|---|---|---|---|
| CMS $pp\to\phi\to\gamma\gamma$, 13 TeV, 36.3+41.5+54.4 fb$^{-1}$ | largest deviation at $m=95.4$ GeV; observed (expected) 95% CL limit on $\sigma\times$BR at 95.4 GeV: 73.4 (27.9) fb; relative to SM-like: 0.593 (0.224) | smooth background | 2.9σ local, 1.3σ global | [1] abstract; HEPData ins2791038, Figures 5a/5b (files in `data/`) | 2024-05 |
| ATLAS $pp\to\phi\to\gamma\gamma$, 13 TeV, 140 fb$^{-1}$ | "no significant excess" in the collaboration's words; limits 19–102 fb (model-dependent), 8–53 fb (fiducial) | smooth background | 1.7σ local at 95.4 GeV (as reported in [3] for the model-dependent analysis) | [2] abstract; [3] abstract | 2024-07 (paper), 2023-06 ([3], based on the preliminary result) |
| $\mu_{\gamma\gamma}$ per experiment (derived in [3], not by the collaborations) | CMS: $0.33^{+0.19}_{-0.12}$; ATLAS: $0.18\pm0.10$ | 0 | — | [3] Sec. 1, Eqs. labelled `muCMS`, `muATLAS` (TeX source) | 2023-06 |
| $\mu_{\gamma\gamma}$ ATLAS+CMS (correlations neglected) | $0.24^{+0.09}_{-0.08}$ at 95.4 GeV | 0 | 3.1σ local | [3] abstract and Eq. `muAC` | 2023-06 |
| LEP $e^+e^-\to Z\phi\to Zb\bar b$ | $\mu_{bb}=0.117\pm0.057$ | 0 | 2.3σ local | [5] (search), number as quoted in [3] Sec. 1, which attributes it to [6] | 2003 / 2016 |
| CMS $gg\to\phi\to\tau\tau$, 138 fb$^{-1}$ | excess "at about three standard deviations" at $m_\phi=0.1$ TeV [7]; at 95 GeV: 2.6σ local, $\mu_{\tau\tau}=1.2\pm0.5$ (as quoted in [3]) | 0 | 2.6–3.1σ local | [7] abstract; [3] Sec. 1 | 2022-08 |

Per-production-mode CMS limits at 95.4 GeV (HEPData ins2791038, Figures 6a–6d, files in `data/`), observed (expected): ggH+ttH 82.0 (31.5) fb; VBF+VH 28.6 (12.4) fb; VBF only 15.3 (7.6) fb; VH only 50.5 (21.1) fb.

Derived reference rate `[estimate]`: dividing CMS Figure 5b (limit in pb) by Figure 5a (limit relative to SM-like) at 95.4 GeV gives the SM-like reference $\sigma\times\text{BR}(\gamma\gamma)=0.0734/0.5931=0.124$ pb. (Ref. [3] writes "126 pb" for this quantity in its introduction; this is read here as a misprint for 0.126 pb, consistent with the HEPData-derived value.) Hence the combined excess corresponds to $\approx30^{+11}_{-10}$ fb, and the CMS-only value to $\approx41$ fb, in line with observed minus expected limit (45 fb).

How solid is it? The global significance in the most sensitive single analysis is 1.3σ [1]; ATLAS itself reports no significant excess [2]; the 3.1σ is a local, unofficial combination [3]. The LEP support is contested: Ref. [8] concludes from the LEP public notes that the LEP data "strongly disfavour" a new 95 GeV scalar. No Run 3 result in the 70–110 GeV diphoton range was found in this session (INSPIRE `(cn CMS or cn ATLAS) and t diphoton and de > 2024`, plus two web searches, 2026-09-20); the newest related experimental inputs are the CMS 10–70 GeV diphoton search, the CMS $X\to YH$ searches [43,44] and the ATLAS $T\bar T\to tS\,tS$, $S\to\gamma\gamma$ search [42]. A Run 3 update of either low-mass diphoton search would change the picture decisively: with doubled luminosity a real signal of 30 fb should exceed 4σ local in one experiment `[estimate: significance ∝ √L]`.

### 1.4 What the data require (EFT-level)

- **Spin**: a resonance decaying to two photons cannot have spin 1 (Landau–Yang); spin 0 (CP-even, CP-odd or mixed) or spin 2.
- **Width**: narrow — all surveyed explanations have widths far below the detector resolution.
- **Master simplified model** (own parameterization, standard coupling-modifier form; mass basis, $v=246$ GeV). For a CP-even state `h95`:

$$\mathcal{L}_{h95} = \tfrac12\partial_\mu h_{95}\partial^\mu h_{95}-\tfrac12 m_{95}^2h_{95}^2 + c_V\,h_{95}\Big(\frac{2m_W^2}{v}W^+_\mu W^{-\mu}+\frac{m_Z^2}{v}Z_\mu Z^\mu\Big) - \sum_{f=t,b,c,\tau}c_f\frac{m_f}{v}\,h_{95}\,\bar f f + c_g^\text{eff}\frac{\alpha_s}{12\pi v}\,h_{95}\,G^a_{\mu\nu}G^{a\mu\nu} + c_\gamma^\text{eff}\frac{\alpha}{8\pi v}\,h_{95}\,F_{\mu\nu}F^{\mu\nu}$$

  and for a CP-odd state `A95`:

$$\mathcal{L}_{A95} = \tfrac12\partial_\mu A_{95}\partial^\mu A_{95}-\tfrac12 m_{95}^2A_{95}^2 - \sum_{f}\tilde c_f\frac{m_f}{v}\,A_{95}\,\bar f\,i\gamma_5 f + \tilde c_g^\text{eff}\frac{\alpha_s}{8\pi v}\,A_{95}\,G^a_{\mu\nu}\tilde G^{a\mu\nu} + \tilde c_\gamma^\text{eff}\frac{\alpha}{8\pi v}\,A_{95}\,F_{\mu\nu}\tilde F^{\mu\nu}$$

  with $\tilde X^{\mu\nu}=\tfrac12\epsilon^{\mu\nu\rho\sigma}X_{\rho\sigma}$; all $c$'s real and dimensionless; every term is hermitian as written (no "+ h.c."); $\bar ff=\bar fP_Lf+\bar fP_Rf$. Widths `[estimate]`: $\Gamma(\phi\to\gamma\gamma)=\alpha^2m^3|c_\gamma^\text{eff}|^2/(256\pi^3v^2)$; $\Gamma(h_{95}\to gg)=\alpha_s^2m^3|c_g^\text{eff}|^2/(72\pi^3v^2)$, $\Gamma(A_{95}\to gg)=\alpha_s^2m^3|\tilde c_g^\text{eff}|^2/(32\pi^3v^2)$ at LO.
- **Loop content of the effective coefficients** at $m=95.4$ GeV `[estimate: one-loop functions $A_1$, $A_{1/2}$, $A_0$ evaluated numerically with $m_W=80.37$, $m_t=172.5$ GeV; $b$ loop neglected]`: $c_g^\text{eff}=1.018\,c_t+\delta c_g$; $c_\gamma^\text{eff}=-7.63\,c_V+1.81\,c_t+\delta c_\gamma$ (SM-like value $-5.82$; $W$ and top interfere destructively); $\tilde c_\gamma^\text{eff}=2.74\,\tilde c_t+\delta\tilde c_\gamma$; a charged scalar of mass 100–300 GeV contributes $\delta c_\gamma=\frac{v\,g_{\phi H^+H^-}}{2m_{H^\pm}^2}\times(0.38\text{–}0.34)$; a heavy vector-like fermion of charge $Q$, colour multiplicity $N_c$ and Yukawa $y_F$ contributes $\delta c_\gamma=\tfrac43N_cQ^2\,y_Fv/M_F$ and (if coloured) $\delta c_g=y_Fv/M_F$. $\delta c$ denote new-physics loops.
- **Quantitative requirement**: $\mu_{\gamma\gamma}=\dfrac{\sigma(pp\to\phi)}{\sigma_\text{SM-like}}\cdot\dfrac{\text{BR}(\phi\to\gamma\gamma)}{\text{BR}_\text{SM-like}}=0.24^{+0.09}_{-0.08}$. Three generic ways to obtain it, which organize the landscape of Section 2:
  1. *reduced production, enhanced BR($\gamma\gamma$)*: $c_t^2\sim0.1$ with the $b\bar b$ width suppressed ($c_b<c_t$) — singlet-like states in 2HDM+singlet and SUSY-singlet models;
  2. *electroweak production, fermiophobic decays*: small $c_f$, $c_V\sim0.3$, BR($\gamma\gamma$) of order 1–2% — type-I 2HDM, triplets;
  3. *new loops*: $\delta c_\gamma$ and/or $\delta c_g$ from charged scalars, doubly-charged scalars, $W_R$, or vector-like fermions — Georgi–Machacek, left-right, dilaton/radion, singlet + vector-like matter; also the CP-odd option, where the missing $W$ loop removes the destructive interference.

## 2. Model Landscape

All 95 GeV candidates are colour-singlet, electrically neutral spin-0 states; the column "Mediator" gives the gauge representation the 95 GeV state (mostly) lives in, plus the companions that matter. "Tree / loop" refers to the origin of the $\phi gg$ and $\phi\gamma\gamma$ couplings beyond SM-particle loops.

| Class | Mediator(s): spin, $(SU(3),SU(2),Y)$ | Tree / loop | Addresses goal via | Status | Characteristic collider signature | Key refs |
|---|---|---|---|---|---|---|
| **A1** SM + real singlet, pure mixing | scalar $(1,1,0)$ | SM loops $\times\sin\theta$ | $\mu_{\gamma\gamma}=\mu_{bb}=\sin^2\theta$ | excluded / strongly disfavoured `[estimate]` (T7) | SM-like pattern in all channels, rate $\times\sin^2\theta$ | none found as a standalone explanation; [19] argues singlets need extra vector-like matter |
| **A2** 2HDM + singlet: N2HDM (real), S2HDM / 2HDMS (complex), 2HDM+s, Yukawa types II and IV(flipped) | singlet-dominated scalar $(1,1,0)$ mixing with two doublets $(1,2,\tfrac12)$ | SM loops with $c_t\neq c_b$ | way 1: suppressed $c_b$ enhances BR($\gamma\gamma$); fits $\gamma\gamma$ + LEP $b\bar b$; $\tau\tau$ only partly (type IV, ≈1σ) | viable (T1) | ggF-dominated $\gamma\gamma$; $Zh_{95}$ at $e^+e^-$; heavy $H/A\to Z h_{95}$, $H\to h_{125}h_{95}$ cascades | [9], [4], [3], [12], [14]; variants V1–V6 |
| **A3** SUSY singlet: NMSSM family and gauge-extended SUSY | singlet-like CP-even Higgs of the superfield $\hat S$ | as A2 (+ light chargino/higgsino loops) | as A2; $\gamma\gamma$ + $b\bar b$ within 1–2σ | viable (collider phenomenology of $h_{95}$ as T1) | as A2, plus light higgsinos / singlino LSP, $H\to h h_s$ cascades | [6], [15], [16], [17]; variants V7–V17 |
| **A4** Singlet + vector-like matter / conformal-sector scalars: minimal dilaton, radion, scalar with effective $\phi GG$, $\phi\gamma\gamma$ operators, $U(1)$-breaking scalars with anomalons, stealth boson | scalar $(1,1,0)$ + vector-like quarks/leptons, e.g. $T\,(3,1,\tfrac23)$ | new loops (way 3) | $\delta c_g$, $\delta c_\gamma$ from heavy fermions or the trace anomaly, with small Higgs mixing | viable, weakly predictive (T6) | $t\bar t$-associated $\gamma\gamma$; VLQ pair production $T\bar T\to tS\,tS$, $S\to\gamma\gamma$; multiphoton cascades | [19], [36], [37], [38], [39], [40], [41], [42]; variants V18–V20 |
| **A5** Singlet from a neutrino-mass / dark-matter / extended gauge sector | scalar $(1,1,0)$ or $SU(2)_R$-breaking scalar; companions: inert doublets, $W_R$, $Z'$ | mixing + new charged loops | scotogenic variant: $\gamma\gamma$ (+LEP); minimal LRSM: seesaw scalar, $\gamma\gamma$ from Higgs mixing and heavy charged bosons | viable | as A2 with smaller rates in non-$\gamma\gamma$ channels; correlated DM / $W_R$ / Higgs-mixing signals at HL-LHC and Higgs factories | [34], [35]; variants V21–V27 |
| **B1** Type-I 2HDM, (moderately) fermiophobic CP-even state, 125 GeV state is the heavier one | second doublet $(1,2,\tfrac12)$ | SM $W$ loop with small $c_f$ (way 2) | VBF+VH production, BR($\gamma\gamma$) ~ 1–2%; also cascades $t\to bH^+\to bW^*H$, $pp\to W^*\to H^\pm H$; $\gamma\gamma$ + LEP, $\tau\tau$ with $h$+$A$ superposition | viable, needs light $H^\pm$ (T2) | $\gamma\gamma$ + forward jets / leptons / $b$-jets; light $H^\pm$ (140–160 GeV in [19]) | [19], [20], [21]; variant V28 |
| **B2** CP-odd state: 2HDM pseudoscalar, 2HDM + pseudoscalar singlet (2HD+a), CP-violating aligned 2HDM | CP-odd component of $(1,2,\tfrac12)$ or pseudoscalar $(1,1,0)$ | top loop only (no $W$ loop); $H^\pm$ loop if CP is violated | fits $\gamma\gamma$ + $\tau\tau$; cannot give the LEP $Zb\bar b$ signal (no $AVV$ coupling) unless CP-mixed | constrained: flavour ($b\to s\gamma$) tension in the plain 2HDM [22]; EDM-correlated in [24] (T3) | ggF only — no VBF/VH component, no $e^+e^-\to ZA$; $t\bar tA$; CP-sensitive $\tau\tau$ observables [28] | [22], [12], [23], [24], [25], [28] |
| **B3** General (type-III) 2HDM | second doublet with general Yukawa textures | SM loops with free $c_t,c_b,c_\tau$ | all three hints at ≈1.3σ [26]; CP-even + CP-odd superposition at 1σ [27] | viable, flavour-model dependent | as B1/B2; predicts enhanced $t\bar th_{125}$ (up to 12% in the top Yukawa) [26] | [26], [27]; variants V29–V30 |
| **C1** Real triplet $Y=0$ (ΔSM) | scalar $(1,3,0)$: $\Delta^0,\Delta^\pm$ quasi-degenerate | tree-level Drell–Yan production $pp\to W^*\to\Delta^0\Delta^\pm$; decay via $W$ loop | sizable BR($\gamma\gamma$) at small mixing; no ggF needed | **excluded in minimal form** (T5): $m_{\Delta^\pm}<110$ GeV excluded by stau-search reinterpretation [30] | $\gamma\gamma$ + $\tau$/jets, associated-production $p_T$ spectrum; $pp\to\tau\tau\nu\nu$ | [29], [30], [47] |
| **C2** Georgi–Machacek (custodial triplets) | real $(1,3,0)$ + complex $(1,3,1)$; 95 GeV state = custodial singlet; companions $H_5^{\pm\pm},H_5^\pm,H_3^\pm$ | SM loops + $H^{\pm\pm}$, $H^\pm$ loops (way 3) | $\gamma\gamma$ well described; $\gamma\gamma$+$b\bar b$ by one state; $\tau\tau$ only ≈0.5 or with a CP-odd twin | viable in a narrow region [33] (T4) | light doubly-charged Higgs, 100–200 GeV [31]; shifts of $\kappa_V$ | [31], [32], [33]; variants V31–V33 |
| **C3** 2HDM + type-II-seesaw triplet, SUSY triplet / SUSY-GM | doublets + $(1,3,1)$ | as C2 | unified $\gamma\gamma$/$b\bar b$/$\tau\tau$ claimed (title level) | not assessed (title-only) | $H^{\pm\pm}$ | variants V34–V36 |
| **D** Generic ALP with $aG\tilde G$, $aF\tilde F$ couplings | pseudoscalar $(1,1,0)$ | effective operators | bottom-up possibility (way 3, CP-odd) | no dedicated paper found (query 12 in the search log); model-independent CP-odd case covered by [28] and B2 | ggF $\gamma\gamma$, dijet; no VBF/VH | — |
| **E** Spin-2 resonance | massive graviton-like state | effective operators | bottom-up possibility allowed by Landau–Yang | no prior work found (query 12); universal couplings would face dilepton resonance limits `[unverified]` | $\gamma\gamma$ with spin-2 angular distribution, $\ell\ell$ | — |
| **F** No new physics | — | — | statistical fluctuation and/or residual $Z\to e^+e^-$ mis-identification background near $m_Z$ (the background the refined analyses target [31]) | open — the null hypothesis; global significance 1.3σ [1] | disappears with Run 3 data | [1], [2], [8] |

**Coverage statement**: The catalogue is complete at the level of model *classes* to the extent that (a) the bottom-up enumeration of Section 1.4 (spin; production by ggF / electroweak / associated Drell–Yan / cascades; decay through $W$, top, charged-scalar, vector-like-fermion loops) has every branch populated or explicitly marked empty (D, E), and (b) every one of the 59 INSPIRE records with "95 GeV" in the title since 2023, the 15 records with "96 GeV" in the title, and the 45 most recent of the 75 papers citing the CMS publication [1] falls into one of the classes above (checked by title; about 45 papers by abstract; one by TeX source). It was cross-checked against the list of 19 interpretation papers in the introduction of [3] (all map onto classes A2, A3, A4, B1, B2) and the anomalies review [45] (abstract only — a dedicated review article of 95 GeV models was **not** found). Left out: a paper-by-paper list of the ≈200 free-text INSPIRE hits; papers that use a 95 GeV scalar only as an ingredient for other anomalies (650 GeV, 152 GeV, multi-lepton, $W$ mass, $(g-2)_\mu$) unless they define a new class; three-Higgs-doublet constructions (seen only in connection with the 650 GeV hint); future-collider studies (listed as V37–V40 for the research program). Title-only variants (V-list in Section 7) are classified by their titles and were not vetted.

## 3. Candidate Targets

Common to all targets: the 95 GeV state is produced and decays promptly (total width of order 0.1–1 MeV `[estimate]`), and the pipeline needs the loop-induced $gg$ and $\gamma\gamma$ couplings as the effective operators of Section 1.4. Benchmark numbers marked `[estimate]` were obtained by rescaling SM-like partial widths and production fractions with the coupling modifiers, using **`[unverified]` memory values** for a 95 GeV SM-like Higgs (BR: $b\bar b$ 0.80, $\tau\tau$ 0.083, $gg$ 0.065, $c\bar c$ 0.037, $VV^*$ 0.0054, $\gamma\gamma$ 0.0014; production shares at 13 TeV: ggF 0.87, VBF+VH 0.125, $t\bar tH$ 0.005). They are meant to fix scan ranges, not to replace the fits in the cited papers.

### T1: Singlet-like scalar of a 2HDM + singlet (N2HDM / S2HDM, Yukawa type II or IV)

- **Origin**: literature [9], [4], [3]; the simplified Lagrangian below is an own mass-basis parameterization (variant: full scalar potential replaced by coupling modifiers). The SUSY realizations of class A3 [15–17] map onto the same parameterization for the 95 GeV state.
- **Status**: viable
- **One-line idea**: a mostly-singlet CP-even scalar inherits couplings from both doublets; in types II/IV the couplings to $t$ and $b$ are independent, so $c_b<c_t$ suppresses the $b\bar b$ width and lifts BR($\gamma\gamma$) while ggF production stays sizeable ([3], Sec. 2 of the TeX source).

#### Field content

| Field | Spin / type | $SU(3)_C$ | $SU(2)_L$ | $Y$ | $Q$ | Self-conj. | Mass | Decays? | $Z_2$ |
|---|---|---|---|---|---|---|---|---|---|
| `h95` | real scalar (mass eigenstate, singlet-dominated) | 1 | mixture of 1 and 2 | — (mass basis) | 0 | yes | 95.4 GeV | yes (auto width) | — |

Heavier states of the full model ($H$, $A$, $H^\pm$; in the S2HDM also a pseudo-Nambu-Goldstone DM state [3]) are omitted: they are not needed to describe the 95 GeV signal.

#### Lagrangian (BSM part, pipeline-ready)

$$\mathcal{L}_\text{BSM}=\mathcal{L}_{h95}\ \text{of Section 1.4, with}\ \delta c_g=\delta c_\gamma=0 .$$

where
- $c_V,c_t,c_b,c_c,c_\tau$: real, dimensionless; $c_c=c_t$; $c_\tau=c_b$ (type II) or $c_\tau=c_t$ (type IV), following the statement in [3] that $c_{h_{95}\tau\tau}=c_{h_{95}bb}$ in type II and $=c_{h_{95}tt}$ in type IV.
- $c_g^\text{eff}=1.018\,c_t$, $c_\gamma^\text{eff}=-7.63\,c_V+1.81\,c_t$ `[estimate]` (Section 1.4).
- Source: own construction (coupling-modifier form). The S2HDM source [3] describes the model in words and does not print the scalar potential; no equation was copied. Convention changes: none.

#### Parameters

| Parameter | Meaning | Type | Benchmark | Allowed / interesting range | Basis for the range |
|---|---|---|---|---|---|
| $m_{95}$ | mass | real, GeV | 95.4 | fixed | [1], [3] |
| $c_V$ | $h_{95}VV$ coupling / SM | real | 0.35 | 0.2–0.45 | LEP $\mu_{bb}$ [3]; unitarity sum rule $c_V^2\le1-\kappa_V^2(h_{125})$ `[estimate]` |
| $c_t$ | top Yukawa / SM | real | 0.35 | 0.2–0.5 | $\mu_{\gamma\gamma}$ `[estimate]` |
| $c_b$ | bottom Yukawa / SM | real | 0.25 | 0–0.4 | needs $c_b<c_t$ [3] |
| $c_\tau$ | tau Yukawa / SM | real | 0.25 (II) / 0.35 (IV) | tied to $c_b$ or $c_t$ | Yukawa type [3], [46] |

Benchmark check `[estimate]`: type II → $\mu_{\gamma\gamma}=0.22$, $\mu_{bb}^\text{LEP}=0.11$, $\mu_{\tau\tau}=0.11$; type IV → $0.20$, $0.10$, $0.20$; BR($\gamma\gamma$) ≈ 0.24%.

#### How it addresses the goal

$\mu_{\gamma\gamma}=\big[0.87\,(c_g^\text{eff})^2+0.125\,c_V^2+0.005\,c_t^2\big]\times\dfrac{(c_\gamma^\text{eff}/5.82)^2}{\sum_X\text{BR}^\text{SM}_X\,c_X^2}$ `[estimate]`; $\mu_{bb}^\text{LEP}=c_V^2\,\text{BR}(b\bar b)/\text{BR}^\text{SM}(b\bar b)$ (the approximation $\sigma/\sigma_\text{SM}=c_{h_{95}VV}^2$ is the one used in [3]). Literature result: N2HDM types II and IV fit the CMS and LEP excesses simultaneously [9]; S2HDM types II and IV describe the combined $\mu_{\gamma\gamma}$, with the $\tau\tau$ hint reachable only at the 1σ level in type IV [4], [3].

#### Constraints

| Constraint | Bound / impact | Source | Verdict |
|---|---|---|---|
| 125 GeV Higgs rates, LEP/Tevatron/LHC Higgs searches | fits found in agreement with all of them | [9], [3] abstracts | ok |
| LEP $Zb\bar b$ | supports $c_V^2\,\text{BR}\approx0.1$ if taken as signal; disfavoured as a signal by [8] | [3], [8] | ok either way ($c_V$ can be lowered) |
| Direct and indirect limits on the type-II 2HDM+S scalar sector | large exclusions, exotic channels $A/H\to Zh_S$ most sensitive at $1<\tan\beta<7$ | [14] abstract | constrains the heavy states, not $h_{95}$ itself |
| $b\to s\gamma$ on $m_{H^\pm}$ in types II/IV | heavy $H^\pm$ required `[unverified]` | — | ok (decouples from $h_{95}$) |
| Resonant $X\to h_{125}Y$, $Y\to\gamma\gamma$ / $\tau\tau$ | 0.05–2.69 fb ($b\bar b\gamma\gamma$), 0.69–15 fb ($\gamma\gamma$ leg of $\gamma\gamma\tau\tau$) | [43], [44] abstracts | constrains cascades of the heavy scalar |

#### Collider signatures

| Process | Collider | Final state | Rate driver | Existing search (HEPData?) | Untested region |
|---|---|---|---|---|---|
| $gg\to h_{95}\to\gamma\gamma$ | LHC 13/13.6 TeV | $\gamma\gamma$ | $c_t^2$, BR($\gamma\gamma$) | [1] (ins2791038: Figures 5a,b, 6a–d); [2] (no HEPData record: HTTP 404) | the signal itself; Run 3 |
| VBF / $Vh_{95}$, $h_{95}\to\gamma\gamma$ | LHC | $\gamma\gamma jj$, $\gamma\gamma\ell$ | $c_V^2$ | [1] Figure 6b–d | sub-dominant (≈10% of the rate) |
| $gg\to h_{95}\to\tau\tau$ | LHC | $\tau\tau$ | $c_t^2c_\tau^2$ | [7] | type IV vs II discriminator |
| $e^+e^-\to Zh_{95}$ | 240–250 GeV | recoil mass | $c_V^2$ | LEP [5] | decisive test; studies V37–V39 |

#### Pipeline feasibility

- Tree-level UFO possible: yes with effective vertices $h_{95}GG$ and $h_{95}FF$ (coefficients above).
- Special requirements: ggF normalization must come from the SM-like reference rate (0.124 pb × rescaling) or a literature K-factor, since LO effective-vertex ggF underestimates the rate; the FeynRules SM must keep $m_c\neq0$ if $c\bar c$ is to enter the automatic width, otherwise give the total width as an external parameter.
- Not executable with the current pipeline: full N2HDM/S2HDM/NMSSM parameter scans with Higgs-data fits (HiggsTools-type global fits are outside the pipeline); $p_T(\gamma\gamma)$ modelling of ggF beyond parton-shower accuracy (no jet merging).

#### Open issues

- Whether the $\tau\tau$ hint belongs to the same state; whether LEP is a signal at all [8].
- The simplified model hides correlations imposed by the scalar potential (e.g. between $c_V$ of $h_{95}$ and $\kappa_V$ of $h_{125}$).

### T2: Type-I 2HDM with a fermiophobic-leaning light CP-even Higgs and a light $H^\pm$

- **Origin**: literature [19], [20], [21]; simplified Lagrangian is an own parameterization.
- **Status**: viable ([20] states that all direct and indirect constraints were satisfied at the time, 2017; [21] provides 2024 benchmark points; current light-$H^\pm$ limits were not re-checked in this run)
- **One-line idea**: with small universal fermion couplings the $W$ loop is unscreened and the $b\bar b$ width collapses, so BR($\gamma\gamma$) reaches the per-cent level and VBF+VH (plus $H^\pm$-mediated cascades) supply the rate [19], [20].

#### Field content

| Field | Spin / type | $SU(3)_C$ | $SU(2)_L$ | $Y$ | $Q$ | Self-conj. | Mass | Decays? | $Z_2$ |
|---|---|---|---|---|---|---|---|---|---|
| `h95` | real scalar | 1 | doublet admixture | — | 0 | yes | 95.4 GeV | yes (auto) | — |
| `Hp` ($H^\pm$) | complex scalar | 1 | component of $(1,2,\tfrac12)$ | $\tfrac12$ | $\pm1$ | no | $m_{H^\pm}$ | yes (auto) | — |

#### Lagrangian (BSM part, pipeline-ready)

$$\mathcal{L}_\text{BSM}=\mathcal{L}_{h95}\big|_{c_f\equiv c_F}+D_\mu H^+D^\mu H^- - m_{H^\pm}^2H^+H^- +\frac{g}{2}\,s_{HW}\Big[\,i\,W^+_\mu\big(H^-\partial^\mu h_{95}-h_{95}\,\partial^\mu H^-\big)+\text{h.c.}\Big]+\mathcal{L}_{H^\pm ff'}$$

$$\mathcal{L}_{H^\pm ff'}=-\frac{\sqrt2}{v}\,\xi\,H^+\Big[V_{tb}\,\bar t\,(m_tP_L-m_bP_R)\,b-m_\tau\,\bar\nu_\tau P_R\,\tau\Big]+\text{h.c.}$$

where
- $D_\mu H^\pm$ contains the photon and $Z$ couplings of a $Q=\pm1$, $T_3=\pm\tfrac12$, $Y=\tfrac12$ state (drives $pp\to H^+H^-$).
- $c_F$ (universal fermion coupling of `h95`), $c_V$, $s_{HW}$, $\xi=\cot\beta$: real, dimensionless. In the 2HDM $s_{HW}^2=1-c_V^2$. The overall phase of the $W^\pm H^\mp h_{95}$ term is convention dependent; only $|g\,s_{HW}/2|$ matters for the processes below.
- $\delta c_\gamma$ from the $H^\pm$ loop: $\tfrac{v\,g_{hH^+H^-}}{2m_{H^\pm}^2}\times0.35$ `[estimate]`, potential dependent; set to 0 in the benchmark.
- Source: own construction; the type-I charged-Higgs Yukawa structure is the standard one of [46] written from memory `[unverified against the source equation — signs to be checked before a plan is executed]`.

#### Parameters

| Parameter | Meaning | Type | Benchmark | Allowed / interesting range | Basis for the range |
|---|---|---|---|---|---|
| $c_V$ | $h_{95}VV$ / SM | real | 0.30 | 0.2–0.35 | [19] quotes $\sin^2\delta\sim0.1$; LEP [3] |
| $c_F$ | universal Yukawa / SM | real | 0.10 | 0.03–0.2 | "moderate-to-strong fermiophobia" [19], [20] |
| $m_{H^\pm}$ | charged Higgs mass | real, GeV | 150 | 100–170 | [19]: 140–160 GeV, $\tan\beta\sim5$; spectra 80–350 GeV in [20] |
| $\xi=\cot\beta$ | $H^\pm$ Yukawa | real | 0.2 | 0.1–0.5 | [19] |

Benchmark check `[estimate]`: $\mu_{\gamma\gamma}=0.25$ (SM-like normalization), BR($\gamma\gamma$) = 1.8%, VBF+VH share of the rate 56%, $\mu_{bb}^\text{LEP}=0.085$, $\mu_{\tau\tau}=0.02$.

#### How it addresses the goal

Same formula as T1 with $c_t=c_b=c_\tau=c_F$; production through VBF+VH $\propto c_V^2$ plus $pp\to W^*\to H^\pm h_{95}$ and $t\to bH^+\to bW^*h_{95}$ [19], [20]. Note that the CMS limit for pure VBF+VH production at 95.4 GeV is 28.6 fb observed vs 12.4 fb expected (HEPData Figure 6b), i.e. an excess of roughly 16 fb in that hypothesis `[estimate: observed − expected]`, so a smaller rate than in T1 is needed.

#### Constraints

| Constraint | Bound / impact | Source | Verdict |
|---|---|---|---|
| CMS VBF+VH, VBF-only, VH-only $\gamma\gamma$ limits at 95.4 GeV | 28.6, 15.3, 50.5 fb | HEPData ins2791038 Figures 6b–d | defines the allowed rate |
| Light charged Higgs: $t\to bH^+$, LEP | model point dependent; LEP lower bound ≈ 80 GeV `[unverified]` | [20] abstract: constraints satisfied (2017) | to be re-checked with current $t\to bH^+$ limits — not done in this run |
| $\tau\tau$ hint | not reproduced by $h$ alone; needs the $h$+$A$ superposition of [21] | [21] | partial |

#### Collider signatures

| Process | Collider | Final state | Rate driver | Existing search (HEPData?) | Untested region |
|---|---|---|---|---|---|
| VBF, $Wh_{95}$, $Zh_{95}$; $h_{95}\to\gamma\gamma$ | LHC | $\gamma\gamma$ + forward jets / leptons | $c_V^2$ | [1] Figure 6b–d | category-level comparison with the excess |
| $pp\to W^*\to H^\pm h_{95}$ | LHC | $\gamma\gamma+\tau\nu$ or $\gamma\gamma+W^*h_{95}$ | gauge coupling, $s_{HW}$ | none dedicated found | yes |
| $t\bar t$, $t\to bH^+\to bW^*h_{95}$ | LHC | $t\bar t$-like + $\gamma\gamma$ | $\xi^2$ | $t\bar t$-associated $\gamma\gamma$ projections V40, [38] | yes |

#### Pipeline feasibility

- Tree-level UFO possible: yes; VBF, $Vh_{95}$, $H^\pm h_{95}$ and top-decay cascades are tree-level; $h_{95}\to\gamma\gamma$ through the effective vertex.
- Special requirements: MadSpin or decay chains for $t\to bH^+$; $b$ quarks in the proton are not needed.
- Not executable: nothing essential.

#### Open issues

- Present-day limits on a 100–170 GeV $H^\pm$ with $H^\pm\to W^*h_{95}$ decays were not collected in this run.

### T3: CP-odd 95 GeV state (2HDM pseudoscalar, 2HD+a, CP-violating aligned 2HDM)

- **Origin**: literature [22], [12], [23], [24], [25]; simplified Lagrangian own parameterization.
- **Status**: constrained — in the CP-conserving 2HDM the region fitting $\gamma\gamma$+$\tau\tau$ is "in tension with current constraints from the flavour sector", notably $b\to s\gamma$ [22]; the 2HD+a version is reported to pass all constraints [23].
- **One-line idea**: without an $AVV$ coupling there is no destructive $W$ loop; ggF is enhanced relative to a scalar with the same Yukawa, and the state decays to $\tau\tau$ at a rate that can match the CMS hint [22].

#### Field content

| Field | Spin / type | $SU(3)_C$ | $SU(2)_L$ | $Y$ | $Q$ | Self-conj. | Mass | Decays? | $Z_2$ |
|---|---|---|---|---|---|---|---|---|---|
| `A95` | real pseudoscalar | 1 | doublet or singlet–doublet admixture | — | 0 | yes | 95.4 GeV | yes (auto) | — |

#### Lagrangian (BSM part, pipeline-ready)

$$\mathcal{L}_\text{BSM}=\mathcal{L}_{A95}\ \text{of Section 1.4},\quad \tilde c_g^\text{eff}=1.03\,\tilde c_t,\quad \tilde c_\gamma^\text{eff}=2.74\,\tilde c_t+\delta\tilde c_\gamma\ \texttt{[estimate]}$$

- $\tilde c_f$ real; type-I-like pattern $\tilde c_t=\tilde c_b=\tilde c_\tau=\cot\beta$ up to signs (signs do not enter the rates used here). Source: own construction.
- In the CP-violating aligned 2HDM an $H^+H^-A$ coupling adds a charged-Higgs loop to $A\to\gamma\gamma$, correlated with electron/neutron/proton EDMs [24].

#### Parameters

| Parameter | Meaning | Type | Benchmark | Allowed / interesting range | Basis for the range |
|---|---|---|---|---|---|
| $\tilde c_t=\tilde c_b=\tilde c_\tau$ | Yukawa / SM ($\cot\beta$, type I) | real | 0.76 | 0.6–0.9 | $\mu_{\gamma\gamma}$ 1σ `[estimate]` |

Benchmark check `[estimate]` ($\sigma(gg\to A)/\sigma(gg\to h_\text{SM})=2.29\,\tilde c_t^2$ at LO): $\mu_{\gamma\gamma}=0.24$ and $\mu_{\tau\tau}=1.07$ at $\tilde c=0.76$; BR($\gamma\gamma$) = $2.9\times10^{-4}$; $\mu_{bb}^\text{LEP}=0$.

#### How it addresses the goal

$\mu_{\gamma\gamma}\simeq0.87\times2.29\,\tilde c^2\times\dfrac{(2.74\,\tilde c/5.82)^2}{\tilde c^2\,[\text{BR}_{bb}+\text{BR}_{\tau\tau}+\text{BR}_{cc}+2.29\,\text{BR}_{gg}]}$ `[estimate]`. Literature: $\gamma\gamma$ + $\tau\tau$ by a pseudoscalar, all three hints only with a CP-mixed state [22]; type-I pseudoscalar interpretation compatible with a first-order electroweak phase transition but $v_c/T_c\lesssim1$ [25].

#### Constraints

| Constraint | Bound / impact | Source | Verdict |
|---|---|---|---|
| Flavour ($b\to s\gamma$) with $\tan\beta\sim1$ and light spectrum | tension | [22] abstract | excludes part: plain CP-conserving 2HDM |
| EDMs (CP-violating version) | correlated with BR($A\to\gamma\gamma$) | [24] abstract | constrains |
| LEP $b\bar b$ hint | cannot be produced | [22] | irrelevant if [8] is right |

#### Collider signatures

| Process | Collider | Final state | Rate driver | Existing search (HEPData?) | Untested region |
|---|---|---|---|---|---|
| $gg\to A_{95}\to\gamma\gamma,\ \tau\tau$ | LHC | $\gamma\gamma$; $\tau\tau$ | $\tilde c_t^2$ | [1] Figure 6a (ggH+ttH: 82.0 fb obs., 31.5 exp.); [7] | absence in VBF/VH categories is the discriminator against T1/T2 |
| $t\bar tA_{95}$ | LHC / HL-LHC | $t\bar t\gamma\gamma$, $t\bar t\tau\tau$ | $\tilde c_t^2$ | — | yes |
| CP analysis in $\tau\tau$ | HL-LHC | $\tau\tau$ decay planes | — | projection: mixing angle to ±(0.27–0.47) rad at 90% CL [28] | — |

#### Pipeline feasibility

- Tree-level UFO possible: yes with effective $A G\tilde G$, $AF\tilde F$ vertices.
- Not executable: $\tau$-polarization CP observables beyond what Pythia8/Delphes provide were not checked against the capability list — treat as not supported.

#### Open issues

- Flavour viability must be taken from the literature per realization; the pipeline does not compute it.

### T4: Georgi–Machacek custodial-singlet scalar with a light doubly-charged Higgs

- **Origin**: literature [31], [32], [33]; simplified Lagrangian own parameterization.
- **Status**: viable in a "narrow but viable parameter region" after vacuum-stability, unitarity, electroweak-precision, $B$-physics and Higgs constraints [33].
- **One-line idea**: doubly- and singly-charged scalars of the triplets add to the $\gamma\gamma$ loop of a light custodial-singlet Higgs while $\rho=1$ at tree level [31].

#### Field content

| Field | Spin / type | $SU(3)_C$ | $SU(2)_L$ | $Y$ | $Q$ | Self-conj. | Mass | Decays? | $Z_2$ |
|---|---|---|---|---|---|---|---|---|---|
| `h95` | real scalar (custodial singlet, doublet–triplet mixture) | 1 | mixture | — | 0 | yes | 95.4 GeV | yes (auto) | — |
| `H5pp` ($H_5^{\pm\pm}$) | complex scalar | 1 | component of $(1,3,1)$ | 1 | $\pm2$ | no | $m_5$ | yes (auto) | — |

($H_5^\pm$, $H_5^0$, $H_3^\pm$, $H_3^0$ exist in the full model and are omitted in the minimal collider parameterization.)

#### Lagrangian (BSM part, pipeline-ready)

$$\mathcal{L}_\text{BSM}=\mathcal{L}_{h95}+D_\mu H_5^{++}D^\mu H_5^{--}-m_5^2H_5^{++}H_5^{--}+\frac{g^2v\,s_H}{2}\Big(H_5^{++}W^-_\mu W^{-\mu}+\text{h.c.}\Big)$$

- $D_\mu$ for $Q=2$, $T_3=1$; $s_H$ real, dimensionless (triplet share of the electroweak vev). The $H_5^{\pm\pm}W^\mp W^\mp$ normalization is written from memory `[unverified]`.
- $\delta c_\gamma=\sum_{i}\tfrac{v\,g_{h_{95}S_iS_i^*}Q_i^2}{2m_{S_i}^2}A_0(\tau_i)$ with $A_0\approx0.34$–$0.38$ `[estimate]`; trilinear couplings are potential parameters.

#### Parameters

| Parameter | Meaning | Type | Benchmark | Allowed / interesting range | Basis for the range |
|---|---|---|---|---|---|
| $m_5$ | $H_5^{\pm\pm}$ mass | real, GeV | 150 | 100–200 | [31] abstract |
| $s_H$ | triplet vev fraction | real | 0.1 `[estimate]` | not extracted | [33] (values not in abstract) |
| $c_V,c_t,c_b,\delta c_\gamma$ | as Section 1.4 | real | not extracted | — | would require reading [31], [33] |

#### How it addresses the goal

$\gamma\gamma$ rate "well described" [31]; $\gamma\gamma$+$b\bar b$ by a single state, $\tau\tau$ only with a CP-odd twin [32]; with renormalization-group-improved stability conditions $\mu_{\gamma\gamma}$ reaches the central value while $\mu_{\tau\tau}\approx0.5$ [33].

#### Constraints

| Constraint | Bound / impact | Source | Verdict |
|---|---|---|---|
| Vacuum stability (positive definiteness), unitarity, EWPT, $B$ physics, Higgs data | narrow surviving region | [33] | excludes most of the space |
| Searches for light $H^{\pm\pm}$ (100–200 GeV) decaying to $W^\pm W^{\pm(*)}$ | "motivates dedicated searches" | [31] | open — the key test |

#### Collider signatures

| Process | Collider | Final state | Rate driver | Existing search (HEPData?) | Untested region |
|---|---|---|---|---|---|
| $pp\to\gamma^*/Z\to H_5^{++}H_5^{--}$, $H_5^{\pm\pm}\to W^\pm W^{\pm(*)}$ | LHC | same-sign dileptons + jets/$E_T^\text{miss}$ | gauge couplings only | not collected in this run | 100–200 GeV window per [31] |
| $h_{95}\to\gamma\gamma$ (ggF + VBF/VH) | LHC | $\gamma\gamma$ | $c_t,c_V,\delta c_\gamma$ | [1] | — |
| $\kappa_V$ of $h_{125}$ | HL-LHC, $e^+e^-$ | — | $s_H$ | — | [33] |

#### Pipeline feasibility

- Tree-level UFO possible: yes for the two-field parameterization; the full GM model in $SU(2)_L$-covariant form is error-prone (capability reference, Section 2) and a public UFO would not be fetched automatically.
- Not executable: the vacuum-stability / unitarity / global-fit part.

#### Open issues

- Benchmark couplings must be read from [31] or [33] before a plan can be written.

### T5: Real $Y=0$ triplet (ΔSM) with Drell–Yan production — documented dead end

- **Origin**: literature [29]
- **Status**: **excluded** in its minimal form. The model needs $m_{\Delta^\pm}\approx95\pm5$ GeV [29]; the same group later found that reinterpreted ATLAS and CMS stau searches exclude $m_{\Delta^\pm}<110$ GeV at 95% CL, with $\Delta^0$ and $\Delta^\pm$ quasi-degenerate [30]. (Inference from the two abstracts; [30] was read at abstract level only.)
- **One-line idea**: at small Higgs mixing $\Delta^0$ has a naturally large BR($\gamma\gamma$), so electroweak pair production $pp\to W^*\to\Delta^0\Delta^\pm$ alone gives the signal [29].

#### Field content

| Field | Spin / type | $SU(3)_C$ | $SU(2)_L$ | $Y$ | $Q$ | Self-conj. | Mass | Decays? | $Z_2$ |
|---|---|---|---|---|---|---|---|---|---|
| `D0` ($\Delta^0$) | real scalar | 1 | 3 | 0 | 0 | yes | 95.4 GeV | yes | — |
| `Dp` ($\Delta^\pm$) | complex scalar | 1 | 3 | 0 | $\pm1$ | no | $\approx m_{\Delta^0}$ (quasi-degenerate [30]) | yes | — |

#### Lagrangian (BSM part, pipeline-ready)

$$\mathcal{L}_\text{BSM}\supset D_\mu\Delta^+D^\mu\Delta^-+\tfrac12\partial_\mu\Delta^0\partial^\mu\Delta^0-m_\Delta^2\big(\Delta^+\Delta^-+\tfrac12\Delta^{0\,2}\big)+g\Big[\,i\,W^+_\mu\big(\Delta^-\partial^\mu\Delta^0-\Delta^0\partial^\mu\Delta^-\big)+\text{h.c.}\Big]+c_\gamma^\text{eff}\frac{\alpha}{8\pi v}\Delta^0F_{\mu\nu}F^{\mu\nu}$$

- Source: own component form of the triplet gauge-kinetic term (coupling strength $g$ for the $T_3=0\leftrightarrow\pm1$ transition; phase convention dependent). Not copied from [29].

#### Parameters, goal, constraints, signatures

- Predictions of [29]: associated-production $p_T$ spectrum of the $\gamma\gamma$ system, photons accompanied by $\tau$ leptons and jets but not VBF-like, $\sigma(pp\to\tau\tau\nu\nu)\approx0.4$ pb, positive shift of $m_W$.
- Fatal constraint: $m_{\Delta^\pm}<110$ GeV excluded [30].
- The triplet remains a target for the separate ≈152 GeV hints [47] — outside this study.

#### Pipeline feasibility

- Would be fully executable (tree-level Drell–Yan production). Not recommended because excluded. A non-minimal variant with a split multiplet would need a new construction — not pursued.

#### Open issues

- Whether any extension splits $\Delta^\pm$ from $\Delta^0$ by more than 15 GeV without violating electroweak precision data — no prior work searched for.

### T6: Singlet with vector-like matter / dilaton-like couplings

- **Origin**: literature [19], [36], [37], [38], [39]; related search [42]; simplified Lagrangian own parameterization.
- **Status**: viable, weakly predictive (couplings are free effective coefficients).
- **One-line idea**: heavy vector-like fermions (or the trace anomaly of a conformal sector) generate $SGG$ and $S\gamma\gamma$ directly; Higgs mixing can be small, so 125 GeV data are untouched [36], [37].

#### Field content

| Field | Spin / type | $SU(3)_C$ | $SU(2)_L$ | $Y$ | $Q$ | Self-conj. | Mass | Decays? | $Z_2$ |
|---|---|---|---|---|---|---|---|---|---|
| `S95` | real scalar | 1 | 1 | 0 | 0 | yes | 95.4 GeV | yes (auto) | — |
| `TP` ($T$) | Dirac fermion, vector-like | 3 | 1 | 2/3 | +2/3 | no | $M_T$ | yes (auto) | — |

#### Lagrangian (BSM part, pipeline-ready)

$$\mathcal{L}_\text{BSM}=\tfrac12\partial_\mu S\partial^\mu S-\tfrac12m_S^2S^2+\bar T(i\gamma^\mu D_\mu-M_T)T-y_T\,S\,\bar TT-\big(\kappa_T\,S\,\bar T P_L\,t+\text{h.c.}\big)+c_g\frac{\alpha_s}{12\pi v}S\,G^a_{\mu\nu}G^{a\mu\nu}+c_\gamma\frac{\alpha}{8\pi v}S\,F_{\mu\nu}F^{\mu\nu}$$

- $y_T$ real; $\kappa_T$ complex in general (take real); $D_\mu$ contains gluon, photon and $Z$ (hypercharge) couplings of a colour-triplet, $Q=2/3$ singlet. Heavy-fermion limit `[estimate]`: $c_g=N_T\,y_Tv/M_T$, $c_\gamma=\tfrac43N_cQ_T^2\,c_g=\tfrac{16}{9}c_g$. The effective operators replace the $T$ loop and must not be double counted: they are valid for $m_S\ll2M_T$.
- Source: own construction following the idea of [36] ("ultraviolet complete model with vectorial quarks, or ... gluon-scalar and photon-scalar effective operators").

#### Parameters

| Parameter | Meaning | Type | Benchmark | Allowed / interesting range | Basis for the range |
|---|---|---|---|---|---|
| $c_g$ | effective gluon coupling | real | 0.32 | 0.25–0.4 | $\mu_{\gamma\gamma}$ with BR($\gamma\gamma$) = 0.39% for $gg$+$\gamma\gamma$ decays only `[estimate]` |
| $c_\gamma$ | effective photon coupling | real | 0.57 | $\tfrac{16}{9}c_g$ for $Q=2/3$; larger for $Q=5/3$ (then BR ≈ 13%, $c_g\approx0.05$) | `[estimate]` |
| $M_T$ | VLQ mass | real, GeV | 1500 | above current VLQ limits `[unverified]` | [42] gives limits vs ($M_T$, $m_S$) — numbers not in abstract |
| $y_T$ | Yukawa | real | 2.0 (for $N_T=1$) | $<\sqrt{4\pi}$ | $c_g=y_Tv/M_T$ `[estimate]` |

#### How it addresses the goal

$\sigma\times\text{BR}=c_g^2\,\sigma^\text{SM-like}_\text{ggF}\times\dfrac{\Gamma_{\gamma\gamma}}{\Gamma_{\gamma\gamma}+\Gamma_{gg}}$ with $\Gamma_{\gamma\gamma}/\Gamma_{gg}=\tfrac{9}{32}(\alpha/\alpha_s)^2(c_\gamma/c_g)^2$ `[estimate]`. Minimal dilaton model: the large-diphoton scenario has $|\sin\theta_S|\lesssim0.2$ and $0.5\lesssim v/f\lesssim1$ [37]; HL-LHC covers $|\sin\theta_S|>0.2$ at 3σ in $t\bar t(s\to\gamma\gamma)$ [38]. Radion–Higgs mixing gives a diphoton excess consistent with observations and a fit to 125 GeV data better than the SM (2019 data) [39].

#### Constraints

| Constraint | Bound / impact | Source | Verdict |
|---|---|---|---|
| VLQ pair production with $T\to tS$, $S\to\gamma\gamma$ | first search in this final state, no excess; limits on fiducial $\sigma\times$BR vs $(M_T,m_S)$ | [42] abstract | constrains light $T$ with large BR($T\to tS$) |
| Dijet resonance at 95 GeV | not constraining at this mass `[unverified]` | — | ok |
| No LEP signal (no $SZZ$ coupling without mixing) | — | — | fine if [8] is right |

#### Collider signatures

| Process | Collider | Final state | Rate driver | Existing search (HEPData?) | Untested region |
|---|---|---|---|---|---|
| $gg\to S\to\gamma\gamma$ | LHC | $\gamma\gamma$ | $c_g^2$ | [1] Figure 6a | — |
| $pp\to T\bar T\to tS\,\bar tS$ | LHC | $t\bar t$ + $\gamma\gamma$ (+$gg$) | QCD, BR($T\to tS$) | [42] (HEPData not checked) | high $M_T$ |
| $pp\to t\bar tS$ (through mixing) | HL-LHC | $t\bar t\gamma\gamma$ | $\sin\theta_S$ | projection [38] | yes |

#### Pipeline feasibility

- Tree-level UFO possible: yes with effective vertices; VLQ pair production is tree-level QCD.
- Not executable: nothing essential.

#### Open issues

- The class is under-constrained: any $\mu_{\gamma\gamma}$ can be dialled. Its value as a target lies in the associated VLQ signatures.

### T7: SM + real singlet with pure Higgs mixing — documented dead end

- **Origin**: bottom-up enumeration (class A1); no paper was found proposing it as a standalone explanation.
- **Status**: excluded / strongly disfavoured `[estimate]`
- **One-line idea**: $c_V=c_f=\sin\theta$ for all couplings, SM-like branching ratios, so $\mu_{\gamma\gamma}=\mu_{bb}=\mu_{\tau\tau}=\sin^2\theta$.
- **Field content**: `S95`, real scalar $(1,1,0)$, $Q=0$, self-conjugate, 95.4 GeV.
- **Lagrangian**: $\mathcal{L}_{h95}$ of Section 1.4 with $c_V=c_t=c_b=c_c=c_\tau=\sin\theta$, $\delta c=0$ (own construction).
- **Why it fails**: $\mu_{\gamma\gamma}=0.24$ requires $\sin^2\theta=0.24$. This (i) over-predicts the LEP rate, $0.24$ vs $0.117\pm0.057$ [3] (2.2σ above a measurement that is itself an excess, i.e. in conflict with the LEP limit), and (ii) reduces all 125 GeV Higgs rates by 24%, far outside the precision of the combined Run 2 coupling measurements `[unverified number; percent-level precision]`. This is why the literature adds a second doublet or vector-like matter ([19] makes the same point for singlet models).
- **Pipeline feasibility**: trivially executable; not recommended.
- Remaining template items (parameters, signatures, open issues): not applicable — excluded candidate.

## 4. Comparison and Ranking

| Rank | Target | Addresses goal | Viability | Collider testability | Minimality | Pipeline feasibility | Novelty |
|---|---|---|---|---|---|---|---|
| 1 | T1 (2HDM+singlet, types II/IV; covers SUSY-singlet class) | $\gamma\gamma$ + $b\bar b$; $\tau\tau$ partly (IV) | viable | high: ggF $\gamma\gamma$ now, $Zh_{95}$ at $e^+e^-$ | medium (many potential parameters; 4 effective ones) | good (effective vertices) | low |
| 2 | T2 (type-I 2HDM, fermiophobic-leaning, light $H^\pm$) | $\gamma\gamma$ + $b\bar b$ | viable, $H^\pm$ limits to be updated | high and distinctive: VBF/VH categories, $H^\pm$ cascades | high (plain 2HDM) | good (mostly tree level) | medium: category-level confrontation with CMS Figure 6 data |
| 3 | T4 (Georgi–Machacek) | $\gamma\gamma$ (+$b\bar b$) | narrow region | striking: $H^{\pm\pm}$ at 100–200 GeV | low | medium | medium |
| 4 | T3 (CP-odd) | $\gamma\gamma$ + $\tau\tau$, no LEP | constrained (flavour, EDM) | distinctive by absence of VBF/VH and $ZA$ | high | good | medium |
| 5 | T6 (singlet + vector-like matter / dilaton) | $\gamma\gamma$ only | viable | VLQ and $t\bar t\gamma\gamma$ channels | medium | good | low–medium |
| 6 | T5 (real triplet) | $\gamma\gamma$ | excluded | — | high | good | — |
| 7 | T7 (pure singlet mixing) | — | excluded | — | highest | good | — |

T1 ranks first because it is the best-established explanation (independent groups, non-SUSY and SUSY versions, [3], [9], [15], [17]) and defines the reference ggF-dominated signal. T2 ranks second because its production pattern is qualitatively different and CMS has published per-production-mode limits that show how the excess is distributed (82.0/31.5 fb for ggH+ttH vs 28.6/12.4 fb for VBF+VH, observed/expected) — confronting T1 and T2 with these tables is the most informative study the pipeline can do with existing data. T4 is the most predictive model beyond the 95 GeV state itself, but needs source-level reading before it can be specified. T3 is kept because it is the only class that naturally fits the $\tau\tau$ hint and because its "null" predictions are sharp. T6 can always fit and therefore teaches least. T5 and T7 are documented dead ends.

## 5. Recommended Research Program

No plans were written in this run (scope `targets`). Recommended, in execution order:

| Plan | Target | Physics question | Deliverable (figure/table) | Strategy | Depends on |
|---|---|---|---|---|---|
| `plans/plan_01_h95_production_modes.md` | T1, T2, T3 (master simplified model of Sec. 1.4: `h95` and `A95`) | For coupling patterns that give $\mu_{\gamma\gamma}=0.24$, how is the $\gamma\gamma$ rate shared between ggF, VBF, $Wh$, $Zh$, $t\bar th$ at 13 and 13.6 TeV, and how do $p_T^{\gamma\gamma}$, $N_\text{jet}$, $m_{jj}$ differ? | table of $\sigma\times$BR($\gamma\gamma$) per production mode and benchmark; normalized $p_T^{\gamma\gamma}$, $N_\text{jet}$, $m_{jj}$ distributions | signal characterization | — |
| `plans/plan_02_h95_cms_modes_reinterpretation.md` | T1 vs T2 vs T3 | Which region of the $(c_t,c_V)$ plane reproduces the excess without exceeding the CMS per-mode limits and the LEP rate? | contours in $(c_t,c_V)$ for fixed $c_b/c_t$: $\mu_{\gamma\gamma}$ 1σ/2σ band, LEP $\mu_{bb}$ band, CMS ggH+ttH / VBF+VH / VBF / VH limits (`data/ins2791038_figure6a–6d.csv`) | limit reinterpretation (valid because CMS limits are given per SM-like production mode — state the acceptance assumption) | plan 01 (UFO, cross sections) |
| `plans/plan_03_h95_ee_recoil_projection.md` | T1, T2, T4 (any $c_V\neq0$); T3/T6 as null cases | What $c_V^2$ can a 240 GeV $e^+e^-$ collider discover through $e^+e^-\to Z(\mu^+\mu^-)h_{95}$ recoil? | expected significance vs $c_V^2$ for 5 ab$^{-1}$ `[estimate of a typical luminosity]`; recoil-mass spectrum with $\mu\mu b\bar b$, $\mu\mu jj$ backgrounds | sensitivity projection | plan 01 (UFO) |

Optional extensions (beyond the default three plans): `plan_04_t2_hpm_associated` — $pp\to W^*\to H^\pm h_{95}$ and $t\to bH^+$ cascades for T2 (characterization, then Run 3/HL-LHC yield estimate); `plan_05_gm_h5pp_pairs` — Drell–Yan $H_5^{++}H_5^{--}$ with same-sign dileptons for T4 (requires benchmark couplings from [31], [33]).

## 6. Decisions for the User

1. **Which hints must be explained?** Options: $\gamma\gamma$ only (assumed) / $\gamma\gamma$ + LEP $b\bar b$ / all three. Recommendation: keep $\gamma\gamma$ as the requirement and report the others, since [8] disputes the LEP signal and the $\tau\tau$ rate selects only the CP-odd or two-state solutions.
2. **Breadth vs depth of the survey.** This report is complete at class level but abstract-level in depth (25 lookups, one source). Option: a deeper pass reading the sources of [9], [21], [31], [33] to extract benchmark points and source-exact Lagrangians (needed before plans for T4 and the optional T2 plan).
3. **Which targets to plan.** Recommendation: the common simplified model covering T1/T2/T3 (plans 01–03). Alternative: a model-specific study of T4 or T6.
4. **Treatment of SUSY models (class A3).** The full NMSSM-type models are not executable with the pipeline; recommendation: represent them by the T1 simplified model. Confirm this is acceptable.
5. **Future-collider detector card** for plan 03: the pipeline uses the Delphes `default` card unless a card path is provided. Provide an $e^+e^-$ detector card or accept `default`.
6. **Reference inputs.** SM-like branching ratios and production shares at 95 GeV are `[unverified]` memory values; before executing plans they should be replaced by the LHC Higgs Working Group numbers (the public BR page reachable in this session tabulates only 120–130 GeV).

## 7. References

<!-- Every entry verified via INSPIRE/arXiv in this session (existence + title + first author). "abs" = abstract read; "src" = TeX source read; "title" = only title/author verified, cited only for the existence of the model named in the title. -->

[1] CMS Collaboration, "Search for a standard model-like Higgs boson in the mass range between 70 and 110 GeV in the diphoton final state in proton-proton collisions at √s = 13 TeV", arXiv:2405.18149 (INSPIRE 2791038; HEPData ins2791038) — abs + HEPData; used for: significance, luminosities, limits.
[2] ATLAS Collaboration, "Search for diphoton resonances in the 66 to 110 GeV mass range using pp collisions at √s = 13 TeV with the ATLAS detector", arXiv:2407.07546 (INSPIRE 2806613; no HEPData record) — abs; used for: ATLAS limits and wording.
[3] Biekötter, Heinemeyer, Weiglein, "The 95.4 GeV di-photon excess at ATLAS and CMS", arXiv:2306.03889 — abs + src; used for: all signal strengths, S2HDM interpretation, type II/IV statements.
[4] Biekötter, Heinemeyer, Weiglein, "The CMS di-photon excess at 95 GeV in view of the LHC Run 2 results", arXiv:2303.12018 — abs; used for: S2HDM, $\tau\tau$ at 1σ in type IV.
[5] LEP Working Group for Higgs boson searches (Barate et al.), "Search for the standard model Higgs boson at LEP", arXiv:hep-ex/0306033 — title; used for: origin of the LEP excess (numbers via [3]).
[6] Cao, Guo, et al., "Diphoton signal of the light Higgs boson in natural NMSSM", arXiv:1612.08522 — title; used for: NMSSM class; source of $\mu_{bb}$ according to [3].
[7] CMS Collaboration, "Searches for additional Higgs bosons and for vector leptoquarks in ττ final states in proton-proton collisions at √s = 13 TeV", arXiv:2208.02717 — abs; used for: $\tau\tau$ excess.
[8] Janot, "The infamous 95 GeV bb̄ excess at LEP: two b or not two b?", arXiv:2407.10948 — abs; used for: criticism of the LEP interpretation.
[9] Biekötter, Chakraborti, Heinemeyer, "A 96 GeV Higgs boson in the N2HDM", arXiv:1903.11661 — abs.
[12] Arcadi, Busoni, Cabo-Almeida, et al., "Is there a (Pseudo)Scalar at 95 GeV?", arXiv:2311.14486 — abs.
[14] Li, Li, Su, et al., "The neutral scalars of type-II 2HDM+S under the LHC", arXiv:2605.00098 — abs.
[15] Cao, Jia, Lian, et al., "95 GeV diphoton and bb̄ excesses in the general next-to-minimal supersymmetric standard model", arXiv:2310.08436 — abs.
[16] Ellwanger, Hugonie, King, et al., "NMSSM explanation for excesses in the search for neutralinos and charginos and a 95 GeV Higgs boson", arXiv:2404.19338 — abs.
[17] Lian, "Interpreting light scalar excesses and heavy scalar cascades in the μ-term extended NMSSM", arXiv:2606.02069 — abs.
[19] Fox, Weiner, "Light Signals from a Lighter Higgs", arXiv:1710.07649 — abs.
[20] Haisch, Malinauskas, "Let there be light from a second light Higgs doublet", arXiv:1712.06599 — abs.
[21] Khanna, Moretti, Sarkar, "Explaining 95 GeV anomalies in the 2-Higgs doublet model type-I", arXiv:2409.02587 — abs.
[22] Azevedo, Biekötter, Ferreira, "2HDM interpretations of the CMS diphoton excess at 95 GeV", arXiv:2305.19716 — abs.
[23] Arcadi, Djouadi, "Interpreting the current Higgs excesses at the LHC in the 2HD+a framework", arXiv:2512.08807 — abs.
[24] Banik, Coloretti, Crivellin, et al., "Correlating A → γγ with electric dipole moments in the two Higgs doublet model in light of the diphoton excesses at 95 GeV and 152 GeV", arXiv:2412.00523 — abs.
[25] Bhatnagar, Croon, Schicho, "Interpreting the 95 GeV resonance in the Two Higgs Doublet Model: implications for the electroweak phase transition", arXiv:2506.20716 — abs.
[26] Belyaev, Benbrik, Boukidi, et al., "Explanation of the hints for a 95 GeV Higgs boson within a 2-Higgs Doublet Model", arXiv:2306.09029 — abs.
[27] Benbrik, Boukidi, Moretti, et al., "Superposition of CP-even and CP-odd Higgs resonances: explaining the 95 GeV excesses within a Two-Higgs Doublet Model", arXiv:2405.02899 — abs.
[28] Mondal, Moretti, Sanyal, "On the CP nature of the '95 GeV' anomalies", arXiv:2412.00474 — abs.
[29] Ashanujjaman, Banik, Coloretti, et al., "SU(2)_L triplet scalar as the origin of the 95 GeV excess?", arXiv:2306.15722 — abs.
[30] Ashanujjaman, Banik, Coloretti, et al., "Anatomy of the real Higgs triplet model", arXiv:2411.18618 — abs; used for: $m_{\Delta^\pm}<110$ GeV exclusion.
[31] Chen, Chiang, Heinemeyer, et al., "A 95 GeV Higgs boson in the Georgi-Machacek model", arXiv:2312.13239 — abs.
[32] Ahriche, "The 95 GeV excess in the Georgi-Machacek model: single or twin peak resonance", arXiv:2312.10484 — abs.
[33] Chang, Du, Zhu, et al., "Interpreting the 95 GeV di-photon and di-tau excesses in the Georgi-Machacek model", arXiv:2509.26155 — abs.
[34] Escribano, Martin Lozano, Vicente, "A Scotogenic explanation for the 95 GeV excesses", arXiv:2306.03735 — abs.
[35] Dev, Mohapatra, Zhang, "Explanation of the 95 GeV γγ and bb̄ excesses in the minimal left-right symmetric model", arXiv:2312.17733 — abs.
[36] Kundu, Maharana, Mondal, "A 96 GeV scalar tagged to dark matter models", arXiv:1907.12808 — abs.
[37] Liu, Qiao, Wang, et al., "A light scalar in the minimal dilaton model in light of LHC constraints", arXiv:1812.00107 — abs.
[38] Wang, Zhu, "95 GeV light Higgs in the top-pair-associated diphoton channel at the LHC in the minimal dilaton model", arXiv:2402.11232 — abs.
[39] Sachdeva, Sadhukhan, "Discussing 125 GeV and 95 GeV excess in light radion model", arXiv:1908.01668 — abs.
[40] Armbruster, Dobrescu, Yu, "Quark-universal U(1) breaking scalar at the LHC", arXiv:2506.06068 — abs; used for: $U(1)$-breaking scalar with anomalon-induced diphoton decays (the abstract does not claim to explain the 95 GeV excess).
[41] Aguilar-Saavedra, Joaquim, "Multiphoton signals of a (96 GeV?) stealth boson", arXiv:2002.07697 — abs.
[42] ATLAS Collaboration, "Search for pair-production of vector-like T quarks decaying into a top quark and a spin-0 particle in the diphoton final state in proton proton collisions at √s = 13 TeV with the ATLAS detector", arXiv:2607.28381 — abs.
[43] CMS Collaboration, "Search for a new scalar resonance decaying to a Higgs boson and another new scalar particle in the final state with two bottom quarks and two photons in proton-proton collisions at √s = 13 TeV", arXiv:2508.11494 — abs.
[44] CMS Collaboration, "Search for the nonresonant and resonant production of a Higgs boson in association with an additional scalar boson in the γγττ final state in proton-proton collisions at √s = 13 TeV", arXiv:2506.23012 — abs.
[45] Crivellin, "Anomalies in Particle Physics", arXiv:2304.01694 — abs; used for: completeness cross-check (review of hints incl. ≈95 GeV).
[46] Branco, Ferreira, et al., "Theory and phenomenology of two-Higgs-doublet models", arXiv:1106.0034 — title; used for: Yukawa types (cited for this purpose in [3]).
[47] Crivellin, Ashanujjaman, Banik, et al., "Growing evidence for a Higgs triplet", arXiv:2404.14492 — abs; used for: triplet at ≈152 GeV (context only).

(Numbers [10], [11], [13], [18] are not used; the corresponding papers appear in the V-list.)

**Variants — title and first author verified through the INSPIRE listings of this session; content not read (classification by title only):**
V1 Heinemeyer, Li, et al., "Phenomenology of a 96 GeV Higgs boson in the 2HDM with an additional singlet", arXiv:2112.11958 · V2 Dutta, Lahiri, et al., "Dark matter phenomenology in 2HDMS in light of the 95 GeV excess", arXiv:2308.05653 · V3 Aguilar-Saavedra et al., "Confronting the 95 GeV excesses within the U(1)'-extended next-to-minimal 2HDM", arXiv:2307.03768 · V4 Benbrik et al., "Interpreting the 650 GeV and 95 GeV Higgs anomalies in the next-to-two-Higgs-doublet model", arXiv:2510.19605 · V5 Xu et al., "95 GeV Higgs boson and nano-Hertz gravitational waves from domain walls in the next-to-two-Higgs-doublet model", arXiv:2505.03592 · V6 Biekötter, Chakraborti, et al., "The '96 GeV excess' at the LHC", arXiv:2003.05422 · V7 Cao et al., "96 GeV diphoton excess in seesaw extensions of the natural NMSSM", arXiv:1908.07206 · V8 Ellwanger et al., "NMSSM with correct relic density and an additional 95 GeV Higgs boson", arXiv:2403.16884 · V9 Lian et al., "95 GeV excesses in the Z3-symmetric next-to-minimal supersymmetric standard model", arXiv:2406.10969 · V10 Kalinowski et al., "Interpreting 95 GeV di-photon/bb̄ excesses as a lightest Higgs boson of the MRSSM", arXiv:2403.08720 · V11 Liu et al., "95 GeV excess in a CP-violating μ…SSM" (title truncated in the lookup), arXiv:2402.00727 · V12 Diaz et al., "Bayesian active search on parameter space: a 95 GeV spin-0 resonance in the (B−L)SSM", arXiv:2404.18653 · V13 Yang et al., "Explaining the possible 95 GeV excesses in the B−L symmetric SSM", arXiv:2406.01926 · V14 Gao et al., "A 95 GeV Higgs boson in the U(1)XSSM", arXiv:2411.13261 · V15 Wang et al., "95 and 125 GeV Higgs boson excesses in the left-right supersymmetric standard model", arXiv:2602.13976 · V16 Cao et al., "Unified interpretation of the muon g−2 anomaly, the 95 GeV diph…" (title truncated), arXiv:2402.15847 · V17 Hammad et al., "Explaining data excesses over the NMSSM parameter space with Deep Learning techniques", arXiv:2508.13912 · V18 Richard, "Search for a light radion at HL-LHC and ILC250", arXiv:1712.06410 · V19 Sun, Zhao, "Higgs bosons at 95 and 125 GeV in the U(1)X VLFM", arXiv:2604.06781 · V20 Ge et al., "The origin of the 95 GeV excess in the flavor-dependent U(1)X model", arXiv:2405.07243 · V21 Borah et al., "Scotogenic U(1)… " (title truncated), arXiv:2310.11953 · V22 Ahriche et al., "Scale invariant scotogenic model: CDF-II W-boson mass and the 95 GeV excesses", arXiv:2311.08297 · V23 Li et al., "Light dark matter confronted with the 95 GeV diphoton excess", arXiv:2312.17599 · V24 Yaser Ayazi et al., "Vector dark matter and LHC constraints, including a 95 GeV light Higgs boson", arXiv:2405.01132 · V25 Baek et al., "96 GeV scalar boson in the 2HDM with U(1)H gauge symmetry", arXiv:2412.02178 · V26 Arhrib et al., "When the Standard Model Higgs meets its lighter 95 GeV twin", arXiv:2405.03127 (class not identifiable from the title) · V27 Cárcamo Hernández et al., "Strongly coupled inert scalar sector with radiative neutrino masses", arXiv:2504.07193 · V28 Hmissou et al., "Investigating the 95 GeV Higgs boson excesses within the type-I (…)" (title truncated), arXiv:2502.03631 · V29 Benbrik et al., "Explaining the 96 GeV di-photon anomaly in a generic 2HDM Type-III", arXiv:2204.07470 · V30 Benbrik et al., "Exploring potential Higgs resonances at 650 GeV and 95 GeV in the 2HDM Type III", arXiv:2505.07811 · V31 Du et al., "Interpretation of 95 GeV excess within the Georgi-Machacek model in light of positive definiteness constraints", arXiv:2502.06444 · V32 Mondal et al., "Light scalars in the extended Georgi-Machacek model", arXiv:2506.06427 · V33 Xu, "Global fits and the 95 GeV diphoton excesses in the supersymmetric Georgi-Machacek model", arXiv:2506.13623 · V34 Ait-Ouazghour et al., "Unified interpretation of 95 GeV excesses in the two Higgs doublet type II seesaw model", arXiv:2410.11140 · V35 Li, Liu, et al., "Interplay of 95 GeV diphoton excess and dark matter in supersymmetric triplet model", arXiv:2504.21273 · V36 Gao et al., "95 GeV Higgs boson and spontaneous CP-violation at the fini…" (title truncated), arXiv:2408.03705 · V37 Biekötter et al., "The '96 GeV excess' at the ILC", arXiv:2002.06904 · V38 Dong et al., "Testing a 95 GeV scalar at the CEPC with machine learning", arXiv:2506.21454 · V39 Dong et al., "Prospects for a 95 GeV Higgs boson at future Higgs factories with transformer networks", arXiv:2510.24662 · V40 Dong, Wang, et al., "Probing a type I 2HDM light Higgs boson in the top-pair-associated diphoton channel", arXiv:2410.13636.

**`[unverified]` — taken from the bibliography of [3] (TeX source), not looked up in this session**: Liu, Liu, Wagner, Wang, "A Light Higgs at the LHC and the B-Anomalies"; Cline, Toma, "Pseudo-Goldstone dark matter confronts cosmic ray and collider anomalies"; Iguro, Kitahara, Omura, "Scrutinizing the 95–100 GeV di-tau excess in the top associated process"; Biekötter, Heinemeyer, Muñoz, "Precise prediction for the Higgs-boson masses in the μνSSM"; Domingo, Heinemeyer, Paßehr, Weiglein, "Decays of the neutral Higgs bosons into SM fermions and gauge bosons in the CP-violating NMSSM"; Biekötter, Heinemeyer, Weiglein, "Mounting evidence for a 95 GeV Higgs boson"; Biekötter, Heinemeyer, Weiglein, "Excesses in the low-mass Higgs-boson search and the W-boson mass measurement"; Biekötter, Grohsjean, Heinemeyer, Schwanenberger, Weiglein, "Possible indications for new Higgs bosons in the reach of the LHC: N2HDM and NMSSM …"; Biekötter, Olea-Romacho, "Reconciling Higgs physics and pseudo-Nambu-Goldstone dark matter in the S2HDM using a genetic algorithm".

## Appendix: Search Log

| # | Service | Query | Yield |
|---|---|---|---|
| 1 | WebSearch | `95 GeV diphoton excess CMS ATLAS latest status 2026` | orientation; pointed to [3], [22]; no Run 3 news |
| 2 | INSPIRE | free text `95 GeV diphoton excess`, mostcited, size 25 | 213 hits, dominated by 125 GeV discovery and 750 GeV-era papers; only [9] useful — free text is a poor entry point for this topic |
| 3 | INSPIRE | `t "95 GeV" and de > 2022`, mostcited, size 40 | 59 hits; backbone of the landscape (classes A2, A3, A5, B, C) |
| 4 | INSPIRE | `(cn CMS or cn ATLAS) and t diphoton and (t "low-mass" or ...) and de > 2022` | 5 hits: [1], [2], the two preliminary notes, CMS very-low-mass search |
| 5 | arXiv API | `id_list` of 4 IDs | abstracts of [1], [2], [3], [4] |
| 6 | INSPIRE | `refersto:recid:2791038`, mostrecent, size 45 | 75 hits (= citation count): 2025–2026 developments, [14], [17], [23], [33], [43], [44], V15 |
| 7 | WebSearch | `CMS OR ATLAS Run 3 low-mass diphoton search 70-110 GeV 95 GeV excess update 2025 2026 result` | no Run 3 result found |
| 8 | arXiv API | `id_list` of 14 IDs | abstracts of [7], [8], [9], [12], [15], [21], [22], [23], [28], [29], [31], [34], [35], [38] |
| 9 | INSPIRE | `(cn CMS or cn ATLAS) and t diphoton and de > 2024`, mostrecent | 8 hits; no 70–110 GeV update; found [42] |
| 10 | INSPIRE | `t "96 GeV"`, mostcited | 15 hits; pre-2023 landscape (V1, V6, V7, V29, [36], [41]) |
| 11 | HEPData | record `ins2791038` (CMS) and `ins2806613` (ATLAS) | CMS: 6 tables; ATLAS: HTTP 404, no record; HEPData free-text search returned unrelated records |
| 12 | INSPIRE | `"95 GeV" and (vector-like or axion-like or radion or dilaton or "spin-2" or graviton or composite) and de > 2016` | 16 hits: [37], [38], [39], [45], V18, V19; nothing dedicated for ALP or spin-2 |
| 13 | arXiv e-print | `2306.03889` TeX source | signal strengths, LEP and ττ numbers, type II/IV logic, interpretation list |
| 14 | INSPIRE | batch `arxiv:... or arxiv:...` (10 IDs) | verified [5], [6], [19], [20], [36], [46], V1, V2, V6 and the tree-level dictionary of the skill's guide |
| 15 | arXiv API | `id_list` of 14 IDs | abstracts of [16], [19], [20], [24], [25], [36], [37], [39], [40], [41], [42], [43], [44], [45] |
| 16 | INSPIRE | `refersto:recid:2672557 and (t triplet or t "charged Higgs" or t "Drell-Yan" or t associated)` | 8 hits; found [30], [47], V35, V40 |
| 17 | HEPData | download Figures 5a, 5b, 6a–6d of ins2791038 | limits at 95.4 GeV; SM-like reference rate 0.124 pb |
| 18 | arXiv API | `id_list` of 8 IDs | abstracts of [14], [17], [26], [27], [30], [32], [33], [47] |
| 19 | WebFetch | LHC Higgs WG branching-ratio page (twiki.cern.ch … CERNYellowReportPageBR) | page tabulates only 120–130 GeV; no 95 GeV numbers → inputs stay `[unverified]` |
