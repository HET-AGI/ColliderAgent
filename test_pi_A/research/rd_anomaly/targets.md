# Research Targets: New physics for the $R_D$ / $R_{D^*}$ anomalies and its test with LHC data

- **Study label**: `rd_anomaly`
- **Date**: 2026-09-20
- **Mode**: A. Model building (with a brief landscape map to position the construction)
- **Literature access**: full (INSPIRE, arXiv, HEPData, HFLAV and PDG all reachable; 25 references verified)

<!-- Evidence labels used in this report:
     (untagged)    backed by a reference in Section 7, verified in this session
     [estimate]    own estimate; formula given
     [unverified]  from memory or a source that could not be checked -->

## 1. Problem Statement

### 1.1 User goal (verbatim)

> Build a new physics model that can explain the R_D and R_D* anomalies in B decays, and design a study of how LHC data can test it.

### 1.2 Interpretation

- **Physics question**: Which minimal extension of the SM enhances $b\to c\tau\nu$ by the amount the $R_{D^{(*)}}$ data ask for, and which part of its anomaly-preferred parameter space is excluded (or will be probed) by high-$p_T$ LHC data?
- **Success criterion**: a model counts as a target if it (i) moves both $R_D$ and $R_{D^*}$ to within $2\sigma$ of the HFLAV CKM-2025 average, (ii) has a mediator heavy enough to evade LQ pair-production limits ($M\gtrsim1.5$ TeV) with perturbative couplings and $\Gamma/M<0.3$, and (iii) produces an LHC signature for which published data exist that the pipeline can recast.
- **Boundary conditions**: collider = LHC (user's wording); no constraint on minimality or UV completeness was given. The orchestrator asked for exactly one research plan, for the top-ranked target.
- **Assumptions made on the user's behalf**:
  1. "New physics model" is read as "a model of new physics (BSM)", not as "a model never published before". The $b\to c\tau\nu$ mediator landscape is exhaustively mapped in the literature (Section 2); a claim of novelty for any single tree-level mediator would not be honest. Origins are labelled explicitly per target.
  2. "The anomalies" = the HFLAV world average prepared for CKM 2025 (last update 28.09.2025) [1]. This is the latest average found; it is also the one quoted by the most recent ATLAS search [3].
  3. "LHC data" = high-$p_T$ ATLAS/CMS data (published Run-2 results that can be recast, plus a luminosity projection). LHCb/Belle II flavour measurements are treated as inputs defining the anomaly, not as the test.
  4. Simplified-model level: one mediator, tree level, mass-basis couplings. No UV completion is built; its implications are stated where they matter.
  5. Only $R_{D^{(*)}}$ is addressed. No attempt is made to explain or fit any other flavour observable.

### 1.3 Current status

| Observable | Measurement | SM prediction | Tension | Source | As of |
|---|---|---|---|---|---|
| $R_D$ | $0.358 \pm 0.024$ (stat+syst combined) | $0.298 \pm 0.004$ (HFLAV arithmetic average of predictions) | $2.5\sigma$ | [1] | 28.09.2025 |
| $R_{D^*}$ | $0.281 \pm 0.011$ | $0.254 \pm 0.005$ | $2.3\sigma$ | [1] | 28.09.2025 |
| $R_D$–$R_{D^*}$ combined | correlation $-0.374$ | — | $\chi^2=17.63$ for 2 dof, $p=1.48\times10^{-4}$, "about $3.8\sigma$" | [1] | 28.09.2025 |
| (previous average, for comparison) | $R_D=0.342\pm0.026$, $R_{D^*}=0.287\pm0.012$ | — | $4.4\sigma$ with the form-factor treatment of [2] | [2] abstract | Spring 2024 |

The average in [1] combines nine inputs (BaBar 2012/13; Belle 2015, 2017/18, 2020; LHCb 2023 muonic, 2023 hadronic, 2025 muonic; Belle II 2025 semileptonic tag; Belle II hadronic tag presented at CKM 2025), with an internal consistency of $\chi^2/\text{dof}=16.7/14$. The anomaly is a persistent $\sim3$–$4\sigma$ effect, but its significance depends on the SM prediction used for $R_{D^*}$: [1] lists compatibilities between $2.3\sigma$ and $4.1\sigma$ for different form-factor inputs (lattice-only $R_{D^*}$ predictions are higher, e.g. $0.265\pm0.013$ FNAL/MILC, $0.279\pm0.013$ HPQCD as listed in [1]). Further Belle II and LHCb Run-3 measurements and the resolution of the $B\to D^*$ form-factor differences could move it in either direction.

### 1.4 What the data require (EFT-level)

Effective Hamiltonian at $\mu_b$ ([2], Eq. (2.1) there):

$$\mathcal{H}_\text{eff}=2\sqrt2\,G_FV_{cb}\left[(1+C_{V_L})O_{V_L}+C_{V_R}O_{V_R}+C_{S_L}O_{S_L}+C_{S_R}O_{S_R}+C_TO_T\right],\qquad O_{V_L}=(\bar c\gamma^\mu P_Lb)(\bar\tau\gamma_\mu P_L\nu_\tau).$$

Single-operator fits of [2] (Table 2 there; Spring-2024 data; real coefficients; "Pull" $=\sqrt{\chi^2_\text{SM}-\chi^2_\text{best}}$):

| Scenario | Fitted value at $\mu_b$ | Pull | Remarks from [2] |
|---|---|---|---|
| $C_{V_L}$ | $+0.079(16)$ | 4.8 | "well explains the present data"; current LHC bound $\lvert C_{V_L}\rvert<0.32$ (EFT), 0.42 (2 TeV LQ) |
| $C_{V_R}$ | $-0.070(26)$ | 2.6 | lower pull |
| $C_{S_L}$ (real) | $+0.165(48)$ | 3.1 | "not likely to explain the present data within $2\sigma$" |
| $C_{S_R}$ | (viable within 95% CL) | — | type-II 2HDM gives the wrong sign; generic 2HDM "difficult" ($\Delta M_s$, LHC) |
| $C_{S_L}=4C_T$ complex ($R_2$-like, $C_{V_R}=0$) | $C_{S_L}=8.4\,C_T=-0.09\pm0.56i$ | 4.4 | needs a large imaginary part |
| $C_{S_L}=-4C_T$ ($S_1$-like, $C_{V_L}=0$) | $C_{S_L}=-8.9\,C_T=0.18$ | 4.1 | |

Own update with the CKM-2025 average [estimate]: for a pure $C_{V_L}$, $R_{D^{(*)}}/R^\text{SM}_{D^{(*)}}=|1+C_{V_L}|^2$ for both ratios. A one-parameter $\chi^2$ fit to the two HFLAV numbers of Section 1.3 (correlation $-0.374$, SM uncertainties added in quadrature) gives

$$C_{V_L}\equiv\epsilon_L=0.066\pm0.016\;(1\sigma),\qquad [0.033,\,0.099]\;(2\sigma),\qquad \chi^2_\text{min}=0.8\ \text{vs}\ \chi^2_\text{SM}=16.7 .$$

(script: `research/rd_anomaly/tools/fit_cvl.py`; [2] found $0.079(16)$ with the Spring-2024 data, consistent within uncertainties. The $\chi^2_\text{SM}$ here differs slightly from HFLAV's 17.63 because SM uncertainties are included.)

**Sign and structure**: constructive interference with the SM, left-handed vector current, third-generation leptons only. **Scale** [estimate]: $\epsilon_L\cdot 2V_{cb}/v^2 = 0.066\times2\times0.0418/(0.246\ \text{TeV})^2\simeq0.09\ \text{TeV}^{-2}$, i.e. $M/\sqrt{g_1g_2}\simeq3.3$ TeV for tree-level exchange — a TeV-scale mediator with $O(1)$ couplings to $b\tau$ and $c\nu$, hence large $pp\to\tau\nu$, $\tau\tau$ rates initiated by heavy-flavour partons. A loop-level origin would need $g^4/(16\pi^2M^2)\sim0.09\ \text{TeV}^{-2}$, i.e. $M\simeq0.27$ TeV for $g=1$, or couplings at the perturbativity limit $g\to\sqrt{4\pi}$ for $M\simeq3$ TeV [estimate], which is why only tree-level mediators are pursued.

## 2. Model Landscape

Bottom-up enumeration: open $(\bar c\,\Gamma b)(\bar\tau\,\Gamma\nu)$ into two vertices. Pairing quark–quark/lepton–lepton gives colour-singlet charged mediators ($W'$, $H^\pm$); pairing quark–lepton gives leptoquarks. Top-down cross-check against [2] (four LQ candidates: $U_1$, $S_1$, $R_2$, $V_2$) and [13] (vector triplet, 2HDM, scalar LQ, vector LQ).

| Class | Mediator(s): spin, $(SU(3),SU(2),Y)$ | Tree / loop | Addresses goal via | Status | Characteristic collider signature | Key refs |
|---|---|---|---|---|---|---|
| Vector LQ $U_1$ | spin 1, $(3,1,\tfrac23)$ | tree | $C_{V_L}$ (and $C_{S_R}$ if right-handed couplings) | **viable** | $pp\to\tau\nu(+b)$, $pp\to\tau\tau(+b)$ non-resonant; single/pair production $\to b\tau,\ t\nu$ | [2,3,5,6,10] |
| Scalar LQ $S_1$ | spin 0, $(\bar3,1,\tfrac13)$ | tree | $C_{V_L}$ and/or $C_{S_L}=-4C_T$ | constrained ($B\to K^*\nu\bar\nu$, $\Delta M_s$ rule out part of the space; avoided for $y_L^{b\tau}\gg y_L^{s\tau}$ [2]) | pair production $\to t\tau,\ b\nu,\ c\tau$; $t$-channel $\tau\nu(+b)$ | [2,23] |
| Scalar LQ $R_2$ | spin 0, $(3,2,\tfrac76)$ | tree | $C_{S_L}=4C_T$, complex (plus $C_{V_R}$ with doublet mixing) | constrained (general best fit conflicts with the LHC $\tau\nu$ bound [2]; pure tensor-type solutions "challenged" by mono-$\tau$ [12]) | $\tau\nu(+b)$ tails — most sensitive class; pair production $\to b\tau,\ c\nu$ | [2,12] |
| Vector LQ $V_2$ | spin 1, $(\bar3,2,\tfrac56)$ | tree | $C_{S_R}$ | viable since the 2023 data [2] | $\tau\tau$ final state is "the key probe" [2] | [2,19] |
| Colour-singlet vector triplet $W'$ | spin 1, $(1,3,0)$ | tree | $C_{V_L}$ | strongly constrained: $\tau^+\tau^-$ searches "pose a serious challenge", "stringent limits" [13] | $Z'\to\tau\tau$, $W'\to\tau\nu$ | [13] |
| $W'_R$ + light $\nu_R$ | spin 1, $(1,1,1)$ | tree | right-handed current | "challenged" by mono-$\tau$ data [12] | $W'\to\tau\nu$ resonance | [12] |
| Charged Higgs (2HDM) | spin 0, $(1,2,\tfrac12)$ | tree | $C_{S_L}$, $C_{S_R}$ | disfavoured: real $C_{S_L}$ not within $2\sigma$; type-II sign wrong; generic 2HDM difficult [2] | $H^\pm\to\tau\nu$, $pp\to\tau\tau$ | [2,13] |
| Triplet LQs $S_3$, $U_3$ | $(\bar3,3,\tfrac13)$, $(3,3,\tfrac23)$ | tree | $C_{V_L}$ | [unverified] commonly stated not to accommodate $R_{D^{(*)}}$ alone ($b\to s\nu\bar\nu$; sign) — not checked in this session | — | — |
| Loop-level models | — | loop | — | not pursued: required scale too low (Section 1.4) [estimate] | — | — |

**Coverage statement**: the table covers all single-mediator tree-level completions of the dimension-six $b\to c\tau\nu_\tau$ operators with SM neutrinos (plus the $W'_R$+$\nu_R$ case), cross-checked against the LQ classification used in [2] (after [20]) and the simplified models of [13]; the tree-level dictionary [21] was used as the enumeration guide. Left out: UV-complete constructions (e.g. gauge-LQ models of the type in [24], which add a $Z'$ and a coloron), $R$-parity-violating SUSY (maps onto the $S_1$ row), two-mediator models, and models explaining several anomalies at once [5]. These do not change the single-mediator collider signatures targeted here.

## 3. Candidate Targets

### T1: Left-handed $U_1$ vector leptoquark (three-parameter benchmark: $M_{U_1}$, $g_U$, $\beta_L^{23}$)

- **Origin**: literature — Lagrangian of [8] as written in the ATLAS search [3] (its Section 3), flavour ansatz of [9,10]. What is done here is parameter fixing with the 2025 data and the reduction to the mass-basis terms the collider study needs; no novelty is claimed for the model.
- **Status**: viable (constrained at large $\beta_L^{23}$ by loop-level flavour observables in a UV-model-dependent way, see Constraints)
- **One-line idea**: a TeV-scale colour-triplet vector couples $b_L\tau_L$ and $c_L\nu_{\tau L}$; its exchange generates $C_{V_L}>0$, the structure the data prefer.

#### Field content

| Field | Spin / type | $SU(3)_C$ | $SU(2)_L$ | $Y$ | $Q$ | Self-conj. | Mass | Decays? | $Z_2$ |
|---|---|---|---|---|---|---|---|---|---|
| `U1` ($U_{1\mu}$) | complex vector | 3 | 1 | 2/3 | +2/3 | no | $M_{U_1}$ | yes (auto width): $b\tau^+$, $s\tau^+$, $c\bar\nu_\tau$, $t\bar\nu_\tau$ | — |

#### Lagrangian (BSM part, pipeline-ready)

Gauge-invariant form ([3], Section 3, quoting [8]; $\kappa=\tilde\kappa=0$, "Yang–Mills" case; $\beta_R=0$):

$$\mathcal{L}_{U_1}=-\tfrac12U^\dagger_{1\mu\nu}U_1^{\mu\nu}+M_{U_1}^2U^\dagger_{1\mu}U_1^\mu-ig_sU^\dagger_{1\mu}T^aU_{1\nu}G^{a\mu\nu}-ig_Y\tfrac23U^\dagger_{1\mu}U_{1\nu}B^{\mu\nu}+\frac{g_U}{\sqrt2}\left[U_1^\mu\,\beta_L^{ij}\,\bar q_L^i\gamma_\mu\ell_L^j+\text{h.c.}\right]$$

with $U_{1\mu\nu}=D_\mu U_{1\nu}-D_\nu U_{1\mu}$, $q_L^i=(V^*_{ji}u_L^j,\;d_L^i)^T$ (down-aligned basis), $\beta_L^{33}=1$, $\beta_L^{23}$ free, $\beta_L^{13}=(V_{td}^*/V_{ts}^*)\beta_L^{23}$, all other entries zero.

Mass-basis component form (own expansion of the above; real couplings; first-generation down-type coupling dropped, see below):

$$\mathcal{L}_\text{int}=\frac{g_U}{\sqrt2}\,U_1^\mu\Big[\bar b\gamma_\mu P_L\tau+\beta_L^{23}\,\bar s\gamma_\mu P_L\tau+(V_{cs}\beta_L^{23}+V_{cb})\,\bar c\gamma_\mu P_L\nu_\tau+(V_{tb}+V_{ts}\beta_L^{23})\,\bar t\gamma_\mu P_L\nu_\tau+\kappa_u\,\bar u\gamma_\mu P_L\nu_\tau\Big]+\text{h.c.}$$

where
- $U_1^\mu$: complex vector, colour triplet, $Q=+2/3$; $P_L=\tfrac12(1-\gamma^5)$; $D_\mu$ contains the gluon and hypercharge fields ($Y=2/3$).
- $\kappa_u=|V_{ub}|\,(1+\beta_L^{23}|V_{tb}/V_{ts}|)$ [estimate — own derivation: $\sum_iV_{ui}\beta_L^{i3}$ with the $\beta_L^{13}$ ansatz and CKM unitarity gives $V_{ub}(1-\beta_L^{23}V_{tb}^*/V_{ts}^*)$; the phase is irrelevant for the BSM-only rate]. The ansatz suppresses the valence-$u$ coupling from the naive $V_{us}\beta_L^{23}$ to this value.
- Dropped: $\beta_L^{13}\,\bar d\gamma_\mu P_L\tau$ ($|\beta_L^{13}|\simeq0.21\beta_L^{23}$; changes the width by $\sim$2% [estimate]); the small $V_{cd}\beta_L^{13}$ piece of the $c\nu_\tau$ coupling ($\simeq+4\%$ of that coupling [estimate]); the hypercharge non-minimal term is kept in the gauge-invariant form but is irrelevant for QCD-driven production.
- CKM inputs (PDG 2025 global fit [25], Eq. (12.27)): $|V_{cs}|=0.97349$, $|V_{cb}|=0.04183$, $|V_{tb}|=0.999118$, $|V_{ts}|=0.04111$ (sign $V_{ts}<0$ in the standard parametrization), $|V_{ub}|=0.003732$.
- Source: [3] Section 3 (unnumbered equation + Eq. (1)); convention changes: none for the gauge-invariant form; the covariant-derivative sign convention is not stated in [3] and is taken as $D_\mu=\partial_\mu-ig_sT^aG^a_\mu-i\tfrac23g_YB_\mu$ [unverified against [8]].

#### Parameters

| Parameter | Meaning | Type | Benchmark | Allowed / interesting range | Basis for the range |
|---|---|---|---|---|---|
| $M_{U_1}$ | mass | real, GeV | 2000 | 1500–3000 (contact-interaction regime above) | pair-production limits $\sim1.6$ TeV [3,14]; ATLAS grid [3] |
| $g_U$ | overall coupling | real, dimensionless | 1.0 | 0.3–3.0 | $R_{D^{(*)}}$ band below; perturbativity; $\Gamma/M<0.3$ |
| $\beta_L^{23}$ | relative $s\tau$ coupling | real, dimensionless | 1.0 | 0.1–2.2 | 0.06–0.16 preferred under general UV assumptions [10, as quoted in 3]; up to 2.2 explored by ATLAS [3] |

Width [estimate, formula $\Gamma=g^2M/(24\pi)$ per channel, colour factor 1 for LQ $\to q\ell$, massless fermions]: $\Gamma/M\simeq0.0262\,g_U^2$ ($\beta_L^{23}=1$), $0.0761\,g_U^2$ ($\beta_L^{23}=2.2$); cross-check: $g_U=2$, $\beta_L^{23}=0.6$, $M=1.5$ TeV gives 7.3%, [3] quotes "about 7%". BR$(U_1\to b\tau)\simeq25\%$ (9%) for $\beta_L^{23}=1$ (2.2).

#### How it addresses the goal

Tree-level matching (derived here by integrating out $U_1$ and Fierzing; agrees with Eq. (1) of [3] and with Eq. (A.2) of [2]):

$$C_{V_L}(M_{U_1})=\frac{g_U^2v^2}{4M_{U_1}^2}\left(1+\frac{V_{cs}}{V_{cb}}\beta_L^{23}\right),\qquad C_{V_L}(\mu_b)\simeq1.12\,C_{V_L}(M_{U_1})\ \text{(QCD one-loop matching factor of [2], Section 3)},$$

$R_{D^{(*)}}/R^\text{SM}_{D^{(*)}}=|1+C_{V_L}|^2$. Couplings needed for the $2\sigma$ range $C_{V_L}(\mu_b)\in[0.033,0.099]$ (best 0.066) [estimate]:

| $\beta_L^{23}$ | $M_{U_1}=1.5$ TeV | 2.0 TeV | 2.5 TeV | 3.0 TeV |
|---|---|---|---|---|
| 0.2 | $g_U=1.24\;[0.88,1.52]$ | $1.66\;[1.17,2.03]$ | $2.07\;[1.47,2.54]$ | $2.49\;[1.76,3.04]$ |
| 1.0 | $0.60\;[0.43,0.74]$ | $0.80\;[0.57,0.98]$ | $1.00\;[0.71,1.22]$ | $1.20\;[0.85,1.47]$ |
| 2.2 | $0.41\;[0.29,0.50]$ | $0.55\;[0.39,0.67]$ | $0.68\;[0.48,0.84]$ | $0.82\;[0.58,1.00]$ |

#### Constraints

| Constraint | Bound / impact | Source | Verdict |
|---|---|---|---|
| LQ pair production ($b\tau$ channel) | "LQ masses below approximately 1.6 TeV were excluded"; vector (Yang–Mills) LQ below 1.58 TeV for coupling 1.0 | [3] intro; [14] abstract | ok for $M\ge1.5$–1.6 TeV; bounds weaken for BR$(b\tau)<1$ [estimate] |
| Non-resonant $pp\to\tau\tau$ | $\lambda_{b\tau}/M\gtrsim1\ \text{TeV}^{-1}$ excluded; $g_U>2.1,\,2.8,\,3.5$ excluded at 1.5, 2.0, 2.5 TeV for $\beta_L^{23}\sim O(0.1)$ | [15] as quoted in [3] | ok: $R_{D^{(*)}}$ band at $\beta_L^{23}=0.2$ is $g_U\simeq1.2$–2.1 there (not yet excluded, close) |
| CMS $\tau\tau(+b)$ | excess up to $2.8\sigma$ local for $M=2$ TeV, coupling 2.5; weaker observed limit | [16] abstract; [3] intro | no exclusion of the band; worth watching |
| $pp\to\tau\nu(+b)$, ATLAS 140 fb$^{-1}$ | $g_U<1.13$ (0.52) at $\beta_L^{23}=1.0$ (2.2), $M=1.5$ TeV; $g_U<2.30$ (1.22) at 2.5 TeV | [3] | ok: the band (table above) lies below these limits everywhere except the upper $2\sigma$ edge at $M=1.5$ TeV, $\beta_L^{23}=2.2$ |
| $pp\to\tau\nu$ inclusive (CMS 138 fb$^{-1}$, ATLAS 139 fb$^{-1}$) | first $t$-channel LQ limits (CMS, no $b$-jet requirement); EFT-level $\lvert C_{V_L}\rvert<0.32$–0.42 | [17], [4]; [2] Table 1 (from [18]) | ok ($0.066\ll0.32$) |
| Flavour at one loop ($B_s$ mixing, LFU in $\tau$ decays) | prefers $\beta_L^{23}\in[0.06,0.16]$ under general UV-completion assumptions; "model dependent and may be affected by additional states in the UV theory" | [10] as quoted in [3] | excludes part: $\beta_L^{23}\gtrsim0.2$ requires UV-model-dependent cancellations. This is the main caveat of the large-$\beta_L^{23}$ regime |
| Theory | massive vector needs a UV origin (gauge LQ: extra $Z'$ and coloron, typically more constrained [24]); $g_U\le3.0<\sqrt{4\pi}$; $\Gamma/M<0.3$ for $g_U<3.4$ (2.0) at $\beta_L^{23}=1$ (2.2) [estimate] | — | ok as a simplified model |

#### Collider signatures

| Process | Collider | Final state | Rate driver | Existing search (HEPData?) | Untested region |
|---|---|---|---|---|---|
| $gc\to b\,\tau^+\nu_\tau$ (resonant $U_1\to b\tau$ + $t$-channel) | LHC 13 TeV | $\tau_h+E_T^\text{miss}+b$ | $(g_{b\tau}g_{c\nu})^2$ — same combination as $R_{D^{(*)}}$; $c$ PDF | [3] (ins3164547: SR distributions, cut-flows, $A\times\epsilon$ maps, signal cross sections, limits) | $R_{D^{(*)}}$ band itself; $M>3$ TeV |
| $gs,\,gb\to c\,\tau^-\bar\nu_\tau$ | LHC 13 TeV | $\tau_h+E_T^\text{miss}+$jet (mistagged $c$) | $g_{s\tau}g_{c\nu}$, $s$ PDF | [3] SR0b regions; [17] | — |
| $b\bar b,\,b\bar s,\,s\bar s\to\tau^+\tau^-$ ($t$-channel) | LHC 13 TeV | $\tau\tau(+b)$ | $g_{b\tau}^4$, $b$ PDF | [15], [16], [22] (HEPData not checked in this session) | $g_U\lesssim2$ at 1.5 TeV |
| $gg,q\bar q\to U_1\bar U_1$ | LHC 13 TeV | $b\tau b\tau$, $b\tau t\nu$, … | QCD, $\kappa$ | [14], [16] | $M\gtrsim1.6$–2 TeV |

#### Pipeline feasibility

- Tree-level UFO possible: yes (one complex vector colour triplet; Yang–Mills gluon coupling written explicitly).
- Special requirements: five-flavour scheme with massless $b$ and $c$ in the matrix element; heavy-flavour initial states; BSM-only diagrams (no $W$); Pythia8 + Delphes (ATLAS card) with ROOT output (truth jet flavour needed for a parametrized $b$-tag at the ATLAS working point) in addition to LHCO.
- Not executable with the current pipeline: CKKW-L merged $\tau\nu$+0,1,2-jet signal as generated by ATLAS (replaced by fixed-order $2\to3$ with a generator-level jet $p_T$ cut); NLO; SM–BSM interference in the SR0b regions (therefore SR0b is not recast).

#### Open issues

- Viability of $\beta_L^{23}=O(1)$ against loop-level flavour constraints needs a UV completion; not settled here.
- For large $\beta_L^{23}$ the $s$-initiated $\tau\tau$ production strengthens the $\tau\tau$ limits quoted for $\beta_L^{23}\sim0.1$; not quantified here.

### T2: $S_1$ scalar leptoquark with $y_L^{b\tau}$ and $y_R^{c\tau}$ ($C_{S_L}=-4C_T$)

- **Origin**: literature [23]; couplings and matching from [2] (Eq. (A.3)–(A.4)).
- **Status**: constrained
- **One-line idea**: a renormalizable scalar LQ (no UV completion needed) generating a scalar–tensor combination; choosing $y_L^{s\tau}\simeq0$ avoids tree-level $b\to s\nu\bar\nu$.

#### Field content

| Field | Spin / type | $SU(3)_C$ | $SU(2)_L$ | $Y$ | $Q$ | Self-conj. | Mass | Decays? | $Z_2$ |
|---|---|---|---|---|---|---|---|---|---|
| `S1` | complex scalar | $\bar3$ | 1 | 1/3 | +1/3 | no | $M_{S_1}$ | yes (auto width): $\bar t\tau^+$… (see note) | — |

#### Lagrangian (BSM part, pipeline-ready)

$$\mathcal{L}_{S_1}=(D_\mu S_1)^\dagger(D^\mu S_1)-M_{S_1}^2S_1^\dagger S_1+\Big[y_{Lb}\big(V_{tb}^*\,\overline{t^C}P_L\tau-\overline{b^C}P_L\nu_\tau\big)S_1+y_{Rc}\,\overline{c^C}P_R\tau\,S_1+\text{h.c.}\Big]$$

where
- $\psi^C$ is the charge-conjugate spinor; $y_{Lb}\equiv y_L^{b\tau}$ real, $y_{Rc}\equiv y_R^{c\tau}$ complex in general (real suffices for the $C_{S_L}=-4C_T$ solution of [2]); CKM-suppressed terms $V_{cb}^*\overline{c^C}P_L\tau$, $V_{ub}^*\overline{u^C}P_L\tau$ dropped (they generate $C_{V_L}=v^2|y_{Lb}|^2/4M^2\simeq0.004$ for $y_{Lb}=1$, $M=2$ TeV [estimate]).
- Diquark couplings of $S_1$ (proton decay) must be forbidden by baryon-number conservation (imposed).
- Source: [2], Eq. (A.3), restricted to two couplings; convention changes: none.

#### Parameters

| Parameter | Meaning | Type | Benchmark | Allowed / interesting range | Basis for the range |
|---|---|---|---|---|---|
| $M_{S_1}$ | mass | real, GeV | 2000 | 1500–4000 | scalar-LQ pair limits 1.28–1.53 TeV [14] (for the charge-4/3 benchmark there) |
| $y_{Lb}\,y_{Rc}$ | coupling product | real | $-1.0$ at 2 TeV | $\sqrt{\lvert y_{Lb}y_{Rc}\rvert}\simeq0.50\,(M/\text{TeV})$ | fit of [2] + running, below |

#### How it addresses the goal

$C_{S_L}(M)=-4C_T(M)=-\dfrac{v^2}{4V_{cb}}\dfrac{y_{Lb}\,y_{Rc}^*}{M_{S_1}^2}$ ([2], Eq. (A.4)); running/matching matrix of [2] gives $C_{S_L}(\mu_b)\simeq2.0\,C_{S_L}(M)$ for $C_T=-C_{S_L}/4$ [estimate from the matrix in [2]]. The fit value $C_{S_L}(\mu_b)=0.18$ [2] then needs $\lvert y_{Lb}y_{Rc}\rvert/M^2\simeq0.25\ \text{TeV}^{-2}$ with $y_{Lb}y_{Rc}<0$ [estimate].

#### Constraints

| Constraint | Bound / impact | Source | Verdict |
|---|---|---|---|
| $B\to K^*\nu\bar\nu$, $\Delta M_s$ | rule out part of the general $S_1$ space; avoided for $y_L^{b\tau}\gg y_L^{s\tau}$ | [2] | ok in the restricted scenario chosen here |
| LHC $\tau\nu$ | $\lvert C_{S_L}(\mu_b)\rvert<0.80$ (2 TeV LQ); HL-LHC $\tau\nu b$ prospect 0.22 | [2] Table 1 (from [18], [11]) | ok now ($0.18$); **at the edge of / below the projected HL-LHC reach** |
| $B_c\to\tau\nu$ | $C_{S_L}\in[-0.94,1.4]$ allowed | [2] Table 2 | ok |

#### Collider signatures

| Process | Collider | Final state | Rate driver | Existing search (HEPData?) | Untested region |
|---|---|---|---|---|---|
| $gc\to b\,\tau\nu$ via $S_1$ | LHC 13 TeV | $\tau_h+E_T^\text{miss}+b$ | $(y_{Lb}y_{Rc})^2$ | [3] — interpreted by ATLAS for $U_1$ only; an $S_1$ reinterpretation was not found (query: `refersto:recid:3164547`, 4 hits, all ATLAS summary notes) | everything |
| $S_1\bar S_1$ pair | LHC 13 TeV | $t\tau$, $b\nu$, $c\tau$ mixtures | QCD | [14] (other charge) | — |

#### Pipeline feasibility

- Tree-level UFO possible: yes. Special requirements: charge-conjugated fermion bilinears (fermion-number-violating vertices) — supported by FeynRules/MadGraph but more error-prone in model validation than T1.
- Not executable: same limitations as T1.

#### Open issues

- Scalar and tensor operators have harder $\tau\nu$ tails than $V_L$; acceptance differs from the $U_1$ benchmark, so ATLAS's published $U_1$ limits cannot simply be rescaled.

### T3: $R_2$ scalar leptoquark ($C_{S_L}=4C_T$, complex)

- **Origin**: literature; couplings and matching from [2] (Eq. (A.5)–(A.6)).
- **Status**: constrained (the most collider-exposed of the three scalar/vector LQ solutions)
- **One-line idea**: the charge-2/3 component of a weak-doublet scalar LQ couples $\bar b_L\tau_R$ and $\bar c_R\nu_{\tau L}$; a large imaginary part is needed.

#### Field content

| Field | Spin / type | $SU(3)_C$ | $SU(2)_L$ | $Y$ | $Q$ | Self-conj. | Mass | Decays? | $Z_2$ |
|---|---|---|---|---|---|---|---|---|---|
| `R2a` ($R_2^{(2/3)}$) | complex scalar | 3 | 2 (lower comp.) | 7/6 | +2/3 | no | $M_{R_2}$ | yes | — |
| `R2b` ($R_2^{(5/3)}$) | complex scalar | 3 | 2 (upper comp.) | 7/6 | +5/3 | no | $M_{R_2}$ (degenerate) | yes | — |

#### Lagrangian (BSM part, pipeline-ready)

$$\mathcal{L}_{R_2}\supset y_R^{b\tau}\,\bar bP_R\tau\,R_2^{(2/3)}+y_L^{c\tau}\,\bar cP_L\nu_\tau\,R_2^{(2/3)}+\text{h.c.}\qquad\text{(plus kinetic and mass terms)}$$

where
- both couplings complex; source: [2], Eq. (A.5). The couplings of the $Q=5/3$ component (fixed by $SU(2)_L$) are **not** given in [2]; they must be taken from the original reference ([7]) before a plan is written for this target — not pipeline-ready yet for processes involving $R_2^{(5/3)}$.

#### Parameters

| Parameter | Meaning | Type | Benchmark | Allowed / interesting range | Basis for the range |
|---|---|---|---|---|---|
| $M_{R_2}$ | mass | real, GeV | 2000 | 1500–4000 | pair limits [14] |
| $y_L^{c\tau}(y_R^{b\tau})^*$ | coupling product | complex | $\lvert\cdot\rvert\simeq3.4$ at 2 TeV | $\sqrt{\lvert\cdot\rvert}\simeq0.93\,(M/\text{TeV})$ [estimate] | fit of [2]: $C_{S_L}(\mu_b)=-0.09\pm0.56i$; $C_{S_L}(\mu_b)\simeq1.82\,C_{S_L}(M)$ for $C_T=+C_{S_L}/4$ |

#### How it addresses the goal

$C_{S_L}(M)=4C_T(M)=\dfrac{v^2}{4V_{cb}}\dfrac{y_L^{c\tau}(y_R^{b\tau})^*}{M_{R_2}^2}$ ([2], Eq. (A.6)).

#### Constraints

| Constraint | Bound / impact | Source | Verdict |
|---|---|---|---|
| LHC $\tau\nu$ | $\lvert C_{S_L}\rvert<0.80$ (2 TeV LQ) vs required 0.57; HL-LHC prospect 0.22 | [2] | ok now, within reach of HL-LHC |
| General $R_2$ best fit with $C_{V_R}$ | "not consistent with the LHC bound" | [2] | that sub-scenario excluded |
| Perturbativity | couplings $\sim1.9$ at 2 TeV, growing $\propto M$ [estimate] | — | limits $M\lesssim3.5$ TeV |

#### Collider signatures

| Process | Collider | Final state | Rate driver | Existing search (HEPData?) | Untested region |
|---|---|---|---|---|---|
| $gc\to b\tau\nu$ via $R_2^{(2/3)}$ | LHC 13 TeV | $\tau_h+E_T^\text{miss}+b$ | $\lvert y_Ly_R\rvert^2$ | [3] ($U_1$ interpretation only) | everything |

#### Pipeline feasibility

- Tree-level UFO possible: yes once the full doublet Lagrangian is fixed from the source. Not executable: same as T1.

#### Open issues

- Needs the complete $SU(2)_L$ doublet Lagrangian from the source; complex couplings imply EDM-type constraints not assessed here.

### T4 (documented dead ends): colour-singlet $W'$ triplet and charged Higgs

- **Origin**: literature [13], [2]. **Status**: $W'$ — strongly constrained ($\tau\tau$ searches, "stringent limits" already with 8 and 13 TeV data [13]); charged Higgs — disfavoured by the fit itself (real $C_{S_L}$ outside $2\sigma$; type-II sign wrong; generic 2HDM "difficult" [2]). Not developed further: field tables and Lagrangians not applicable (no plan will be written for them).

## 4. Comparison and Ranking

| Rank | Target | Addresses goal | Viability | Collider testability | Minimality | Pipeline feasibility | Novelty |
|---|---|---|---|---|---|---|---|
| 1 | T1 $U_1$ | best single-operator fit ($C_{V_L}$, pull 4.8 [2]) | viable; large-$\beta_L^{23}$ regime UV-dependent | excellent: dedicated ATLAS search with complete HEPData [3] | 1 field, 3 parameters; needs UV completion | good (validated benchmark exists) | low for the model; **medium for the study** (no reinterpretation of [3] exists yet) |
| 2 | T2 $S_1$ | good (pull 4.1 [2]) | constrained but open | good; never confronted with [3] | 1 field, renormalizable | moderate (charge-conjugate vertices; no experimental benchmark to validate against) | higher |
| 3 | T3 $R_2$ | good with complex couplings (pull 4.4 [2]) | constrained; large couplings | very good (hard tails) | 2 components | moderate; Lagrangian incomplete in this report | higher |
| — | T4 $W'$, $H^\pm$ | partial | strongly constrained / disfavoured | — | — | — | — |

T1 is ranked first because it addresses the goal best, is viable, and — decisive for a first plan — is the only target for which the experiment provides its own benchmark yields, efficiencies and limits, so the whole recast chain can be validated before any new statement is made. T2 and T3 are the natural follow-ups: once the chain is validated on $U_1$, recasting the same SR1b regions for scalar LQs is new physics output.

## 5. Recommended Research Program

| Plan | Target | Physics question | Deliverable (figure/table) | Strategy | Depends on |
|---|---|---|---|---|---|
| `plans/plan_01_u1_taunub_recast.md` (written) | T1 | How much of the $U_1$ parameter space preferred by the CKM-2025 $R_{D^{(*)}}$ average is excluded by the ATLAS 140 fb$^{-1}$ $\tau\nu+b$ search, and would 3 ab$^{-1}$ close the gap? | 95% CL exclusion in $(M_{U_1},g_U)$ at $\beta_L^{23}=1.0,\,2.2$: recast (validated against ATLAS), $R_{D^{(*)}}$ $1\sigma/2\sigma$ band, 3 ab$^{-1}$ projection | recast of an existing search + luminosity-scaled projection | — |
| plan_02 (not written — one-plan limit) | T1 | Same question in the UV-motivated regime $\beta_L^{23}\simeq0.1$–0.2, where $pp\to\tau\tau$ dominates | exclusion in $(M_{U_1},g_U)$ from high-mass $\tau\tau$ data [15] | recast; reuse the UFO of plan_01 | plan_01 (model); HEPData availability for [15] to be checked |
| plan_03 (not written) | T2 (then T3) | Does the $\tau\nu+b$ search [3] exclude the scalar-LQ solutions? | exclusion in $(M_{S_1},\sqrt{\lvert y_{Lb}y_{Rc}\rvert})$ with the $C_{S_L}=-4C_T$ band | recast with the validated analysis of plan_01 | plan_01 (analysis code, calibration) |

## 6. Decisions for the User

1. **Meaning of "new"** — options: (a) a well-motivated known mediator confronted with the newest data (done here), (b) a genuinely new construction (e.g. a two-mediator or UV-complete model). Recommendation: (a) first; the single-mediator space is fully mapped, and the newest ATLAS search has not been reinterpreted by anyone yet, so the *study* is new even though the *model* is not.
2. **Which flavour regime of $U_1$ to test** — large $\beta_L^{23}$ ($\tau\nu+b$, plan_01: directly tied to $R_{D^{(*)}}$, complete HEPData, but in tension with loop-level flavour bounds in generic UV completions) or small $\beta_L^{23}$ ($\tau\tau$, plan_02). Recommendation: run plan_01 first (validation benchmark), then plan_02.
3. **Scalar leptoquark follow-up (plan_03)** — this is where genuinely new exclusion statements are expected. Recommendation: yes, after plan_01 validates.
4. **Campaign size of plan_01** — 48 runs × 10k events (Pythia8+Delphes). A reduced version ($\beta_L^{23}=1.0$ only, 24 runs) is possible at the cost of the panel where the data are closest to the band.

## 7. References

<!-- Every entry verified via INSPIRE/arXiv in this session (exists + title/first author match). "read:" states what was actually read and therefore what the entry is cited for. -->

[1] HFLAV, "Average of R(D) and R(D*) for CKM 2025", https://hflav-eos.web.cern.ch/hflav-eos/semi/ckm25/html/RDsDsstar/RDRDs.html (last update 28.09.2025) — read: full page — used for: world averages, correlation, SM predictions, tension.
[2] Iguro, Kitahara, Watanabe, "Global fit to $b\to c\tau\nu$ anomalies as of Spring 2024", arXiv:2405.06062 — read: abstract + TeX source (Sections 2–3, Tables 1–2, Appendix A) — used for: EFT basis, single-operator and LQ fits, LHC bounds on Wilson coefficients, LQ Lagrangians and matching, running/matching factors.
[3] ATLAS, "Search for a leptoquark in events with a hadronically decaying $\tau$-lepton and missing transverse momentum using $pp$ collisions at $\sqrt s=13$ TeV with the ATLAS detector", arXiv:2606.02067 (HEPData ins3164547) — read: abstract + TeX source (Sections 1, 3, 4, 5, 6, 8) — used for: $U_1$ Lagrangian and flavour ansatz, Eq. (1), selection, observed/expected yields, limits, quoted limits of other searches.
[4] ATLAS, "Search for high-mass resonances in final states with a $\tau$-lepton and missing transverse momentum with the ATLAS detector", arXiv:2402.16576 (HEPData ins2762382) — read: abstract, HEPData table list — used for: existence of the inclusive $\tau\nu$ search and its data.
[5] Buttazzo, Greljo, Isidori, Marzocca, "B-physics anomalies: a guide to combined explanations", arXiv:1706.07808 — read: abstract — used for: $U_1$ as the successful simplified model; $U(2)$ flavour structure.
[6] Angelescu, Bečirević, Faroughy, Sumensari, "Closing the window on single leptoquark solutions to the $B$-physics anomalies", arXiv:1808.08179 — read: abstract — used for: $U_1$ with left-handed couplings as the viable single-LQ scenario.
[7] Doršner, Fajfer, Greljo, Kamenik, Košnik, "Physics of leptoquarks in precision experiments and at particle colliders", arXiv:1603.04993 — verified title/authors only — used for: LQ nomenclature; pointer for the full $R_2$ Lagrangian.
[8] Baker, Fuentes-Martín, Isidori, König, "High-$p_T$ signatures in vector–leptoquark models", arXiv:1901.10480 — verified title/authors only — used for: origin of the $U_1$ Lagrangian as quoted in [3].
[9] Cornella, Faroughy, Fuentes-Martín, Isidori, Neubert, "Reading the footprints of the B-meson flavor anomalies", arXiv:2103.16558 — verified title/authors only — used for: flavour ansatz, as cited in [3].
[10] Aebischer, Isidori, Pesut, Stefanek, Wilsch, "Confronting the vector leptoquark hypothesis with new low- and high-energy data", arXiv:2210.13422 — read: abstract; $\beta_L^{23}$ range as quoted in [3] — used for: compatibility of $U_1$ with $\tau\tau$ data, HL-LHC coverage statement, preferred $\beta_L^{23}$.
[11] Endo, Iguro, Kitahara, Takeuchi, Watanabe, "Non-resonant new physics search at the LHC for the $b\to c\tau\nu$ anomalies", arXiv:2111.04748 — read: abstract — used for: $\tau_h+b+E_T^\text{miss}$ strategy, $\approx40\%$ sensitivity gain, LQ-mass dependence.
[12] Greljo, Martin Camalich, Ruiz-Álvarez, "The Mono-Tau Menace: From $B$ Decays to High-$p_T$ Tails" (journal title: "Mono-$\tau$ Signatures at the LHC Constrain Explanations of $B$-decay Anomalies"), arXiv:1811.07920 — read: abstract — used for: crossing relation $b\to c\tau\nu\leftrightarrow b\bar c\to\tau\nu$; tensor and right-handed solutions challenged.
[13] Faroughy, Greljo, Kamenik, "Confronting lepton flavor universality violation in B decays with high-$p_T$ tau lepton searches at LHC", arXiv:1609.07138 — read: abstract — used for: $\tau\tau$ constraints on $W'$, 2HDM, LQ simplified models.
[14] ATLAS, "Search for leptoquarks decaying into the $b\tau$ final state in $pp$ collisions at $\sqrt s=13$ TeV with the ATLAS detector", arXiv:2305.15962 — read: abstract — used for: pair/single-production mass limits.
[15] ATLAS, "A measurement of the high-mass $\tau\bar\tau$ production cross-section at $\sqrt s=13$ TeV with the ATLAS detector and constraints on new particles and couplings", arXiv:2503.19836 — read: abstract; limits as quoted in [3] — used for: non-resonant $\tau\tau$ limits on $U_1$.
[16] CMS, "Search for a third-generation leptoquark coupled to a $\tau$ lepton and a b quark through single, pair, and nonresonant production in proton-proton collisions at $\sqrt s=13$ TeV", arXiv:2308.07826 — read: abstract — used for: CMS limits and the $2.8\sigma$ local excess.
[17] CMS, "Search for new physics in the $\tau$ lepton plus missing transverse momentum final state in proton-proton collisions at $\sqrt s=13$ TeV", arXiv:2212.12604 — read: abstract — used for: first $t$-channel LQ limits in $\tau\nu$.
[18] Iguro, Takeuchi, Watanabe, "Testing leptoquark/EFT in $\bar B\to D^{(*)}l\bar\nu$ at the LHC", arXiv:2011.02486 — verified title/authors only — used for: origin of the LHC bounds tabulated in [2].
[19] Iguro, Omura, "A closer look at isodoublet vector leptoquark solution to the $R_{D^{(*)}}$ anomaly", arXiv:2306.00052 — verified title/authors only — used for: $V_2$ scenario (via [2]).
[20] Sakaki, Tanaka, Tayduganov, Watanabe, "Testing leptoquark models in $\bar B\to D^{(*)}\tau\bar\nu$", arXiv:1309.0301 — verified title/authors only — used for: LQ classification (via [2]).
[21] de Blas, Criado, Pérez-Victoria, Santiago, "Effective description of general extensions of the Standard Model: the complete tree-level dictionary", arXiv:1711.10391 — verified title/authors only — used for: enumeration guide.
[22] CMS, "Searches for additional Higgs bosons and for vector leptoquarks in $\tau\tau$ final states in proton-proton collisions at $\sqrt s=13$ TeV", arXiv:2208.02717 — verified title only — used for: existence of a CMS $\tau\tau$ vector-LQ interpretation.
[23] Bauer, Neubert, "Minimal Leptoquark Explanation for the $R_{D^{(*)}}$, $R_K$, and $(g-2)_\mu$ Anomalies", arXiv:1511.01900 — verified title/authors only — used for: origin of the $S_1$ explanation.
[24] Di Luzio, Greljo, Nardecchia, "Gauge leptoquark as the origin of B-physics anomalies", arXiv:1708.08450 — verified title/authors only — used for: gauge-LQ UV completion pointer.
[25] Particle Data Group, "CKM Quark-Mixing Matrix" review, 2025 edition (pdg.lbl.gov/2025/reviews/rpp2025-rev-ckm-matrix.pdf), Eq. (12.27) — read: the equation — used for: CKM magnitudes.

## Appendix: Search Log

| # | Service | Query | Yield |
|---|---|---|---|
| 1 | WebSearch | `HFLAV R(D) R(D*) world average 2026 tension with Standard Model sigma` | pointer to the HFLAV CKM-2025 page [1] |
| 2 | INSPIRE | `leptoquark B anomalies` (mostcited) | 395 hits; [5], [6], [23], [24] and the classic LQ papers |
| 3 | HFLAV web (WebFetch + curl, 3 requests) | CKM-2025 $R(D^{(*)})$ page | averages, inputs, SM predictions, tension statement |
| 4 | INSPIRE | `global fit b -> c tau nu anomalies and de > 2023` (mostrecent) | 7 hits; [2]; also arXiv:2505.05552 (tauphilic LQs, not used) |
| 5 | arXiv (WebFetch) | abs/2405.06062 | abstract of [2] |
| 6 | INSPIRE | `cn ATLAS and t tau and t neutrino and de > 2022`; `cn CMS and t leptoquark and t tau and de > 2022` | 0 hits each (title words fail when the title contains `$\tau$`/MathML) |
| 7 | INSPIRE | `cn ATLAS and t leptoquark and de > 2023`; `cn ATLAS and t tau and de > 2023`; free text `ATLAS search high-mass resonances tau neutrino final state 139 fb` | found [3] (June 2026) and [4] |
| 8 | arXiv API | `id_list=2606.02067,2402.16576` | abstracts of [3], [4] |
| 9 | HEPData | records `ins2762382`, `ins3164547` | table lists; 34 tables of ins3164547 downloaded to `data/` |
| 10 | arXiv e-print | 2606.02067 | TeX source of [3] |
| 11 | arXiv e-print | 2405.06062 | TeX source of [2] |
| 12 | INSPIRE | batch `arxiv:<id>` for 16 IDs | [7]–[22] verified |
| 13 | PDG (WebFetch → saved PDF, read locally) | CKM review 2025 | Eq. (12.27) |
| 14 | INSPIRE | `refersto:recid:3164547` | 4 hits, all ATLAS summary-plot notes → no reinterpretation of [3] exists yet |
| 15 | INSPIRE | `cn CMS and t leptoquark and de > 2024` | 2 hits; no CMS $\tau\nu+b$ LQ search found |
| 16 | INSPIRE | `vector leptoquark U1 R(D) LHC tau neutrino b-jet and de > 2025` | 0 hits (query too strict) |
| 17 | arXiv API | `id_list=` 10 IDs | abstracts of [5], [6], [10]–[17] |
