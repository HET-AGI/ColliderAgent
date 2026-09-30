> **Research plan** `plan_01_u1_taunub_recast` — study `rd_anomaly`, target `T1: left-handed U1 vector leptoquark` — generated 2026-09-20 by the principal-investigator agent.
> User goal: "Build a new-physics model that explains the R_D and R_D* anomalies and design a study of how LHC data can test it."
> Depends on: none.

# 1. Target

Considering the $U_1$ vector-leptoquark model described in this document, determine which part of the parameter region that explains the $R_D$ and $R_{D^*}$ anomalies (HFLAV CKM-2025 average) is excluded by the ATLAS 140 fb$^{-1}$ search for leptoquarks in the $\tau_\text{had}+E_T^\text{miss}(+b)$ final state (arXiv:2606.02067), by recasting its two $b$-tagged signal regions, and estimate how far 3 ab$^{-1}$ would reach. The recast is validated against the signal yields and limits that ATLAS published for the same benchmark model.

Deliverables:
- **Figure 1** (`output/figures/u1_taunub_exclusion.pdf`): two panels ($\beta_L^{23}=1.0$ and $2.2$) showing, in the $(M_{U_1}, g_U)$ plane, the recast observed and expected 95% CL limits, the published ATLAS limits, the $1\sigma/2\sigma$ band preferred by $R_{D^{(*)}}$, and the 3 ab$^{-1}$ projections.
- **Figure 2** (`output/figures/u1_taunub_validation.pdf`): ratio of pipeline to ATLAS expected signal yields per signal region and parameter point.
- **Table** (`output/data/u1_taunub_results.csv`): per parameter point — cross sections, selection efficiencies, signal yields per region (P1, P2, total), calibration constants, ATLAS reference yields, ratios; per $(M_{U_1},\beta_L^{23})$ — observed/expected/projected limits on $g_U$ and the band edges.

---

# 2. Model

The SM is extended by one vector leptoquark $U_1$, a colour triplet and weak singlet with hypercharge $2/3$, coupled to left-handed quarks and leptons of the second and third generation. It is the benchmark model of the ATLAS search (Section 3 of arXiv:2606.02067, after arXiv:1901.10480), written here in the mass basis after electroweak symmetry breaking and reduced to the terms this study needs.

## 2.1 Lagrangian

$$
\begin{aligned}
\mathcal{L}_\text{BSM} ={}& -\frac12\,U^\dagger_{1\mu\nu}U_1^{\mu\nu} + M_{U_1}^2\,U^\dagger_{1\mu}U_1^{\mu} - i g_s\,U^\dagger_{1\mu}\,T^a\,U_{1\nu}\,G^{a\mu\nu} \\
&+ \frac{g_U}{\sqrt2}\Big[\,U_1^{\mu}\Big(\bar b\gamma_\mu P_L\tau + \beta_{23}\,\bar s\gamma_\mu P_L\tau + c_{c\nu}\,\bar c\gamma_\mu P_L\nu_\tau + c_{t\nu}\,\bar t\gamma_\mu P_L\nu_\tau + c_{u\nu}\,\bar u\gamma_\mu P_L\nu_\tau\Big) + \text{h.c.}\Big]
\end{aligned}
$$

with the internal (derived, not free) coefficients

$$c_{c\nu}=V_{cs}\beta_{23}+V_{cb},\qquad c_{t\nu}=V_{tb}+V_{ts}\beta_{23},\qquad c_{u\nu}=|V_{ub}|\Big(1+\beta_{23}\frac{|V_{tb}|}{|V_{ts}|}\Big),$$

and fixed numerical constants $V_{cs}=0.97349$, $V_{cb}=0.04183$, $V_{tb}=0.999118$, $V_{ts}=-0.04111$, $|V_{ub}|=0.003732$ (PDG 2025 CKM review, Eq. (12.27); the sign of $V_{ts}$ is that of the standard parametrization).

Here,
- $U_{1\mu}$ is a **complex vector** field beyond the SM: colour **triplet**, $SU(2)_L$ **singlet**, hypercharge $Y=2/3$ ($Q=T_3+Y$), electric charge $Q=+2/3$. It is **not** self-conjugate. Suggested name: `U1` (antiparticle `U1~`); if this clashes with a gauge-group symbol in the FeynRules SM file use `ULQ`.
- $U_{1\mu\nu}=D_\mu U_{1\nu}-D_\nu U_{1\mu}$, where $D_\mu=\partial_\mu-ig_sT^aG^a_\mu-i\frac23g_YB_\mu$ is the covariant derivative containing the gluon field $G^a_\mu$ and the hypercharge field $B_\mu$ (sign convention of the FeynRules SM). $T^a=\lambda^a/2$ are the $SU(3)_C$ generators in the fundamental representation, $g_s$ the strong coupling, $G^{a\mu\nu}$ the gluon field-strength tensor.
- The first three terms (kinetic, mass, non-minimal gluon coupling) are hermitian by themselves and must **not** get an additional "h.c.". The coefficient of the non-minimal gluon term is exactly $-ig_s$ ("Yang–Mills" case, $\kappa=0$ in the convention $-ig_s(1-\kappa)$ of the ATLAS paper): the gluon couplings of $U_1$ are those of a gauge boson. The analogous non-minimal hypercharge term is omitted; it is irrelevant for the QCD-induced processes of this study.
- "+ h.c." applies to the fermion interaction bracket only. Colour indices of the quark and of $U_1$ are contracted with $\delta_{ij}$ (e.g. $\bar b^{\,i}\gamma_\mu P_L\tau\,U^\mu_{1\,i}$). Every term is electrically neutral: e.g. $\bar b\,\tau\,U_1$ has charge $+\tfrac13-1+\tfrac23=0$, $\bar c\,\nu_\tau U_1$ has $-\tfrac23+0+\tfrac23=0$.
- $P_{L}=\frac12(1-\gamma^5)$ is the left-handed chirality projector.
- $b$, $s$, $c$, $t$, $u$ are the bottom, strange, charm, top and up quarks; $\tau$ is the tau lepton and $\nu_\tau$ the tau neutrino (SM mass eigenstates).
- $g_U$ and $\beta_{23}$ ($\equiv\beta_L^{23}$ of the ATLAS paper) are **real, dimensionless** free parameters. $c_{c\nu}$, $c_{t\nu}$, $c_{u\nu}$ are real internal parameters computed from $\beta_{23}$ with the formulas above.
- Gauge-invariant origin (for information; do not implement): $\frac{g_U}{\sqrt2}U_1^\mu\beta_L^{ij}\bar q_L^i\gamma_\mu\ell_L^j$ in the down-aligned basis with $\beta_L^{33}=1$, $\beta_L^{23}=\beta_{23}$, $\beta_L^{13}=(V_{td}^*/V_{ts}^*)\beta_{23}$. Dropped on purpose: the $\bar d\gamma_\mu P_L\tau$ coupling ($\simeq0.21\beta_{23}$ relative to $\bar b\tau$; $\sim$2% effect on the width) and the $V_{cd}\beta_L^{13}$ piece of $c_{c\nu}$ ($\simeq+4\%$).

## 2.2 Parameters

The free parameters are:
- $M_{U_1}$: mass of $U_1$ (external, GeV). Scan: Section 3.3.
- $g_U$: overall leptoquark coupling (external). Real. Scan: Section 3.3.
- $\beta_{23}$: relative coupling to $s\tau$ (external). Real. Two values: 1.0 and 2.2.
- Width of $U_1$: computed automatically by MadGraph at each parameter point (decay channels $b\tau^+$, $s\tau^+$, $c\bar\nu_\tau$, $t\bar\nu_\tau$, $u\bar\nu_\tau$). Cross-check value: $\Gamma/M\simeq0.0262\,g_U^2$ for $\beta_{23}=1.0$ and $0.0761\,g_U^2$ for $\beta_{23}=2.2$ (massless-fermion estimate $\Gamma=g^2M/24\pi$ per channel, colour factor 1).

Five-flavour scheme: the $c$ and $b$ quarks must be **massless in the matrix element** (set $m_c=m_b=0$ and the corresponding Yukawa couplings to zero through the parameter card or a model restriction), because they appear in the initial state. The $\tau$ keeps its mass.

Model outputs required: UFO (default).

---

# 3. Collider Simulation

## 3.1 Process

Two signal processes, generated **separately** (so that each has adequate statistics):

$$\textbf{P1:}\quad pp\to\tau^+\nu_\tau\,b\quad\text{and}\quad pp\to\tau^-\bar\nu_\tau\,\bar b$$
$$\textbf{P2:}\quad pp\to\tau^-\bar\nu_\tau\,c\quad\text{and}\quad pp\to\tau^+\nu_\tau\,\bar c$$

What the process strings must capture:
- The proton (and the initial-state multiparticle) contains $g,u,d,s,c,b$ and their antiquarks (five-flavour scheme).
- **BSM-only**: keep only diagrams with exactly two $U_1$–fermion vertices; exclude every diagram containing a $W^\pm$ propagator (there is then no SM contribution and no SM–BSM interference). All remaining topologies must be kept together: resonant single production ($gc\to\nu_\tau U_1$, $U_1\to b\tau^+$; $gs\to\tau^-U_1$ and $gb\to\tau^-U_1$, $U_1\to c\bar\nu_\tau$; $gu\to\nu_\tau U_1$) and non-resonant $t$-channel $U_1$ exchange, including their interference. Do **not** use an on-shell decay-chain syntax for $U_1$ and do not use MadSpin: $U_1$ appears as an internal propagator with its automatically computed width.
- The final-state $b$ (P1) or $c$ (P2) quark is generated at matrix-element level with a transverse-momentum cut (Section 3.2). The $2\to2$ processes $b\bar c\to\tau\nu$ etc. are **not** generated (they would double count the $g\to b\bar b$ splitting already contained in P1).
- Both charge-conjugate final states are added in each process.
- The $\tau$ is stable at matrix-element level and decayed by Pythia8.

## 3.2 Collider simulation settings

There are 4 run groups (A–D), 12 parameter points each, 48 runs in total. For each run:
- collider: 13 TeV LHC ($pp$), 6500 GeV per beam
- event number: 10,000 per parameter point
- PDF: LHAPDF set `NNPDF31_nlo_as_0118` (ID 303400)
- factorization/renormalization scales: MadGraph default dynamical scale
- parton shower: Pythia8 (including $\tau$ decays)
- detector simulation: Delphes ATLAS card
- output format for reconstructed events: keep the **Delphes ROOT file** (the analysis needs the truth jet flavour `Jet.Flavor`) and also write LHCO
- generator-level cuts: $p_T>40$ GeV for the final-state $b$/$c$ quark (it is part of the jet definition in the five-flavour scheme, so this is the jet-$p_T$ cut `ptj = 40`); $p_T(\tau)>150$ GeV (charged-lepton cut `ptl = 150`; if the installed version does not apply `ptl` to the $\tau$, use `pt_min_pdg = {15: 150}`); **no** cut on missing transverse energy; all other cuts at MadGraph defaults

Run group A: P1 with $\beta_{23}=1.0$. Run group B: P2 with $\beta_{23}=1.0$. Run group C: P1 with $\beta_{23}=2.2$. Run group D: P2 with $\beta_{23}=2.2$.

## 3.3 Parameter settings for each run

Each $(M_{U_1}, g_U)$ point below is simulated for P1 and for P2. All points coincide with points of the ATLAS signal grid, so that every point has a reference yield (Section 4.1).

| $\beta_{23}$ | $M_{U_1}$ [GeV] | $g_U$ values |
|---|---|---|
| 1.0 (groups A, B) | 1500 | 0.5, 1.0, 2.0 |
| 1.0 | 2000 | 1.0, 2.0, 3.0 |
| 1.0 | 2500 | 1.5, 2.0, 3.0 |
| 1.0 | 3000 | 2.0, 2.5, 3.0 |
| 2.2 (groups C, D) | 1500 | 0.5, 0.75, 1.5 |
| 2.2 | 2000 | 0.5, 1.0, 1.5 |
| 2.2 | 2500 | 1.0, 1.5, 2.0 |
| 2.2 | 3000 | 1.0, 1.5, 2.0 |

- width of $U_1$: Auto at every point (largest value: $\Gamma/M\simeq0.30$ at $\beta_{23}=2.2$, $g_U=2.0$; $0.24$ at $\beta_{23}=1.0$, $g_U=3.0$)
- the largest single vertex coupling in the scan is the $\bar s\tau$ coupling $g_U\beta_{23}/\sqrt2=3.1$ ($\beta_{23}=2.2$, $g_U=2.0$), below $\sqrt{4\pi}$
- several scan points lie above the published ATLAS limit on purpose: the scan has to bracket the exclusion boundary, and these points serve as validation references
- all SM parameters at their defaults, except $m_c=m_b=0$ (Section 2.2)

There is no exact coupling scaling law for this process (the amplitude is $\propto g_U^2$, but the resonant part depends on the width, which is $\propto g_U^2$); therefore $g_U$ is scanned explicitly and interpolated as described in Section 4.2, Step 4.

---

# 4. Numerical Analysis

The whole analysis is done in Python on the Delphes ROOT files (pheno-analyzer step); the optional MadAnalysis5 step is not needed.

## 4.1 Experimental data

**ATLAS, search for a leptoquark in $\tau_\text{had}+E_T^\text{miss}$ events** (arXiv:2606.02067, HEPData ins3164547):
- luminosity: 140 fb$^{-1}$ (140.07 fb$^{-1}$ in the HEPData cut-flow headers) at $\sqrt s=13$ TeV
- observable: event counts in two single-bin signal regions with exactly one $b$-jet (Section 8 of the paper; background after the background-only fit to the control regions):

| Region | $n_\text{obs}$ | $b_\text{SM}$ | $\delta b$ |
|---|---|---|---|
| SR1b-Res | 3 | 2.69 | 0.83 |
| SR1b-NonRes | 2 | 1.88 | 0.71 |

(The two $b$-veto regions SR0b-Res/NonRes — 33 observed vs $36.4\pm7.3$, 45 vs $38.3\pm9.9$ — are **not** used: their signal has a 20–40% destructive SM interference according to the paper, which this BSM-only simulation cannot reproduce. ATLAS states that the sensitivity is driven by the SR1b regions.)

Reference files (all exist in the working directory):
- `research/rd_anomaly/data/atlas_sr1b_expected_yields.csv` — derived from HEPData: ATLAS expected **BSM-only** signal yields $N=\mathcal{L}\,\sigma\,(A\times\epsilon)$ in SR1b-Res and SR1b-NonRes for every ATLAS grid point; columns `mU1_GeV,gU,betaL23,sigma_BSMonly_pb,AxE_SR1bRes,AxE_SR1bNonRes,N_SR1bRes,N_SR1bNonRes`; lines starting with `#` are comments. Values at the 24 simulated points:

| $\beta_{23}$ | $M_{U_1}$ | $g_U$ | $N^\text{ATLAS}_\text{Res}$ | $N^\text{ATLAS}_\text{NonRes}$ | | $\beta_{23}$ | $M_{U_1}$ | $g_U$ | $N^\text{ATLAS}_\text{Res}$ | $N^\text{ATLAS}_\text{NonRes}$ |
|---|---|---|---|---|---|---|---|---|---|---|
| 1.0 | 1500 | 0.5 | 2.08 | 0.138 | | 2.2 | 1500 | 0.5 | 3.57 | 0.724 |
| 1.0 | 1500 | 1.0 | 4.03 | 0.938 | | 2.2 | 1500 | 0.75 | 6.55 | 2.85 |
| 1.0 | 1500 | 2.0 | 51.9 | 17.9 | | 2.2 | 1500 | 1.5 | 119 | 49.7 |
| 1.0 | 2000 | 1.0 | 0.626 | 0.386 | | 2.2 | 2000 | 0.5 | 0.564 | 0.268 |
| 1.0 | 2000 | 2.0 | 8.30 | 7.12 | | 2.2 | 2000 | 1.0 | 3.26 | 3.03 |
| 1.0 | 2000 | 3.0 | 34.6 | 33.6 | | 2.2 | 2000 | 1.5 | 30.8 | 20.5 |
| 1.0 | 2500 | 1.5 | 0.416 | 0.777 | | 2.2 | 2500 | 1.0 | 0.852 | 1.42 |
| 1.0 | 2500 | 2.0 | 2.36 | 2.91 | | 2.2 | 2500 | 1.5 | 8.93 | 9.91 |
| 1.0 | 2500 | 3.0 | 13.4 | 16.6 | | 2.2 | 2500 | 2.0 | 36.1 | 38.1 |
| 1.0 | 3000 | 2.0 | 0.910 | 1.55 | | 2.2 | 3000 | 1.0 | 0.357 | 0.958 |
| 1.0 | 3000 | 2.5 | 1.98 | 3.81 | | 2.2 | 3000 | 1.5 | 3.30 | 4.79 |
| 1.0 | 3000 | 3.0 | 5.12 | 8.46 | | 2.2 | 3000 | 2.0 | 15.8 | 18.6 |

- `research/rd_anomaly/data/ins3164547_Observed_limit_beta_L_23_1_0.csv`, `..._Observed_limit_beta_L_23_2_2.csv`, `..._Expected_limit_beta_L_23_1_0.csv`, `..._Expected_limit_beta_L_23_2_2.csv` — published 95% CL upper limits on $g_U$ vs $m_{U_1}$ (HEPData CSV: comment lines start with `#:`, several sub-tables separated by blank lines, first column $m_{U_1}$ [GeV], second column $g_U$). Observed values at the four masses: $\beta_{23}=1.0$: 1.13, 1.81, 2.30, 2.69; $\beta_{23}=2.2$: 0.52, 0.99, 1.22, 1.42 (for 1500, 2000, 2500, 3000 GeV).
- `research/rd_anomaly/data/ins3164547_Signal_cutflow_SR1b_Res.csv`, `..._Signal_cutflow_SR1b_NonRes.csv` — ATLAS cut-flows for $(1500, 1.5, 0.6)$ and $(3000, 2.5, 1.0)$, for orientation when debugging the selection.

## 4.2 Simulated signal events

### Step 1: object definitions (from Section 5 of the ATLAS paper, adapted to Delphes)

Read the Delphes ROOT file of each run (tree `Delphes`; branches `Jet.PT, Jet.Eta, Jet.Phi, Jet.Mass, Jet.Flavor, Jet.TauTag, Electron.PT, Electron.Eta, Muon.PT, Muon.Eta, MissingET.MET, MissingET.Phi`).
- $\tau_\text{had}$ candidates: jets with `TauTag == 1`, $p_T>20$ GeV, $|\eta|<2.5$, excluding $1.37<|\eta|<1.52$.
- analysis jets: all other jets (`TauTag == 0`) with $p_T>20$ GeV, $|\eta|<2.5$.
- light leptons: electrons with $p_T>10$ GeV, $|\eta|<2.47$ (excluding $1.37<|\eta|<1.52$); muons with $p_T>10$ GeV, $|\eta|<2.5$.
- $E_T^\text{miss}$ and its azimuth from `MissingET`.
- $b$-tagging is **not** taken from the Delphes flag. Each analysis jet $j$ gets a tag probability from its truth flavour: $\varepsilon_j=0.85$ if `Flavor == 5` (the 85% working point used by ATLAS), $\varepsilon_j=\varepsilon_c$ if `Flavor == 4` ($\varepsilon_c$ is determined in Step 3), $\varepsilon_j=0.01$ otherwise (assumed; negligible impact).
- derived variables: $m_T=\sqrt{2\,p_T^{\tau}E_T^\text{miss}\,(1-\cos\Delta\phi(\tau,E_T^\text{miss}))}$; $m_{b\tau}$ = invariant mass of the $b$-tagged jet and the $\tau_\text{had}$ candidate (visible four-momenta).

### Step 2: event selection (Table 2 and Section 5 of the ATLAS paper)

Preselection and common cuts:
1. exactly one $\tau_\text{had}$ candidate, and it has $p_T>200$ GeV;
2. no light lepton;
3. at least one analysis jet;
4. multijet cleaning: reject the event if $\min_j\Delta\phi(j,E_T^\text{miss})<0.4$ **and** $E_T^\text{miss}/p_T(j_\text{min})<6$, where $j_\text{min}$ is the analysis jet with the smallest $\Delta\phi$;
5. trigger: assumed fully efficient for $E_T^\text{miss}>200$ GeV.

Region-specific cuts (the "$b$-jet" is the one tagged jet; exactly one tagged jet is required):

| | SR1b-Res | SR1b-NonRes |
|---|---|---|
| $E_T^\text{miss}$ | $>200$ GeV | $>400$ GeV |
| $m_T$ | $>200$ GeV | $>600$ GeV |
| $b$-jet $p_T$ | $>250$ GeV | $50$–$250$ GeV |
| $m_{b\tau}$ | $>800$ GeV | — |
| $\Delta\phi(\tau,E_T^\text{miss})$ | — | $>1.2$ |
| number of analysis jets | $\le4$ | $\le2$ |

Because tagging is probabilistic, every event passing the $b$-independent cuts gets a **weight** per region instead of a pass/fail decision:

$$w_R=\sum_{j\,\in\,\text{analysis jets}}\Theta_R(j)\;\varepsilon_j\prod_{k\neq j}(1-\varepsilon_k),$$

where $\Theta_R(j)=1$ if jet $j$, taken as the $b$-jet, satisfies the $b$-jet $p_T$ (and, for SR1b-Res, $m_{b\tau}$) requirement of region $R$, else 0.

### Step 3: signal prediction and calibration

For run $r$ (process P1 or P2 at a given parameter point) and region $R$:

$$s_R^{(r)}(\varepsilon_c)=\sigma_r\times\mathcal{L}\times\frac{\sum_\text{events}w_R}{N_\text{gen}},\qquad \mathcal{L}=140.07\ \text{fb}^{-1},$$

with $\sigma_r$ the MadGraph cross section of the run after generator cuts (MadGraph reports pb; convert to fb, $1\ \text{pb}=1000\ \text{fb}$) and $N_\text{gen}=10{,}000$. No K-factor (ATLAS also used LO signal cross sections). The prediction at a parameter point is $s_R=k\,[s_R^{(P1)}+s_R^{(P2)}]$.

Two calibration constants are fixed **once**, using only the six $M_{U_1}=2000$ GeV points (12 numbers): scan $\varepsilon_c\in\{0.05,0.10,\dots,0.60\}$ and $k\in[0.3,3]$ (for each $\varepsilon_c$ the best $k$ is analytic: $\ln k=-\langle\ln(s_R/N_R^\text{ATLAS})\rangle$) and minimize $\sum[\ln(s_R/N^\text{ATLAS}_R)]^2$. $k$ absorbs overall differences ($\tau$ identification, trigger, scale factors, fixed-order vs merged generation); $\varepsilon_c$ is the charm mistag rate of the ATLAS tagger at this working point, which is not quoted in the paper. Report both values. If the fit prefers $\varepsilon_c$ outside $[0.10,0.50]$ or $k$ outside $[0.5,2]$, flag it as a validation failure (Section 6) and continue with $\varepsilon_c=0.30$, $k=1$.

### Step 4: interpolation in $g_U$

For each $(M_{U_1},\beta_{23})$ and region, fit $s_R(g_U)=A_R\,g_U^2+B_R\,g_U^4$ with $A_R,B_R\ge0$ to the three simulated $g_U$ points (least squares on relative residuals); report the residuals. This function is used to evaluate the signal at any $g_U$ in $[0.1,\,g_U^\text{max}]$ with $g_U^\text{max}=3.4$ ($\beta_{23}=1.0$) and $2.0$ ($\beta_{23}=2.2$), the values where $\Gamma/M=0.3$.

## 4.3 Statistical analysis

Two-bin counting experiment, CL$_s$ with pseudo-experiments (hybrid treatment of nuisances). For a signal hypothesis $s=(s_\text{Res},s_\text{NonRes})$:
- test statistic $Q(n)=2\sum_R\left[s_R-n_R\ln(1+s_R/b_R)\right]$ with the nominal $b_R$ of Section 4.1;
- generate $N_\text{toy}=40{,}000$ pseudo-experiments for each hypothesis: $b'_R=\max(b_R+\delta b_R\,\theta_R,\,10^{-3})$ with independent $\theta_R\sim N(0,1)$; a common signal scale $f_s=\max(1+0.2\,\theta_s,\,0.05)$, $\theta_s\sim N(0,1)$ (20% signal uncertainty, correlated between regions); $n_R\sim\text{Pois}(b'_R+f_ss_R)$ for the $s{+}b$ hypothesis and $n_R\sim\text{Pois}(b'_R)$ for $b$-only;
- $\text{CL}_{s+b}=P(Q\ge Q_\text{obs}\,|\,s{+}b)$, $\text{CL}_b=P(Q\ge Q_\text{obs}\,|\,b)$, $\text{CL}_s=\text{CL}_{s+b}/\text{CL}_b$; a point is **excluded at 95% CL if $\text{CL}_s<0.05$**;
- observed limit: $Q_\text{obs}$ from $n_\text{obs}$; expected limit: $Q_\text{obs}\to$ median of $Q$ under $b$-only; $\pm1\sigma$ band: 16% and 84% quantiles;
- for each $(M_{U_1},\beta_{23})$ find the $g_U$ with $\text{CL}_s=0.05$ by bisection on $[0.1,g_U^\text{max}]$ (22 iterations); if $\text{CL}_s>0.05$ at $g_U^\text{max}$ report "no exclusion".

3 ab$^{-1}$ projection (luminosity scaling at 13 TeV; no new simulation): multiply $s_R$ and $b_R$ by $f=3000/140.07=21.42$ and compute the **expected** limit with the same procedure for two background-uncertainty scenarios: (A) unchanged relative uncertainty, $\delta b_R\to f\,\delta b_R$; (B) $\delta b_R=0.10\,f\,b_R$.

A reference implementation of exactly this procedure exists at `research/rd_anomaly/tools/estimate_limits.py` (it runs on the ATLAS yields instead of simulated ones).

## 4.4 Figure

**Figure 1** — two panels side by side, left $\beta_{23}=1.0$, right $\beta_{23}=2.2$. Each panel contains:
1. **Recast observed limit** — $g_U^{95}$ vs $M_{U_1}$ from Section 4.3 at the four masses, linearly interpolated; solid red line, region above lightly hatched in red.
2. **Recast expected limit** — dashed black line with a green $\pm1\sigma$ band.
3. **ATLAS published limits** — observed (solid blue with circle markers) and expected (dashed blue) from the HEPData files of Section 4.1.
4. **3 ab$^{-1}$ projections** — scenario A (purple dash-dotted) and scenario B (purple dotted).
5. **$R_{D^{(*)}}$-preferred band** — analytic:
$$g_U(M_{U_1})=\frac{2M_{U_1}}{v}\sqrt{\frac{C_{V_L}}{\eta_\text{QCD}\,\big(1+\frac{V_{cs}}{V_{cb}}\beta_{23}\big)}}$$
with $v=246.22$ GeV, $V_{cs}/V_{cb}=0.97349/0.04183$, $\eta_\text{QCD}=1.12$ (matching/running factor $C_{V_L}(\mu_b)\simeq1.12\,C_{V_L}(M_{U_1})$ from arXiv:2405.06062), and $C_{V_L}=0.0659$ (central, solid brown line), $[0.0495,0.0824]$ ($1\sigma$, gold fill), $[0.0330,0.0988]$ ($2\sigma$, light-yellow fill). These values come from a one-parameter fit of $R_{D^{(*)}}/R^\text{SM}_{D^{(*)}}=|1+C_{V_L}|^2$ to the HFLAV CKM-2025 average ($R_D=0.358\pm0.024$, $R_{D^*}=0.281\pm0.011$, correlation $-0.374$; SM $0.298\pm0.004$, $0.254\pm0.005$); script `research/rd_anomaly/tools/fit_cvl.py`. Check values: at $M_{U_1}=2000$ GeV the central line is at $g_U=0.80$ ($\beta_{23}=1.0$) and $0.55$ ($\beta_{23}=2.2$).
6. **Band centre for $\eta_\text{QCD}=1$** (tree-level relation as used by ATLAS) — thin dotted brown line.
7. **$\Gamma/M>0.3$** — grey shaded region $g_U>3.38$ (left) and $g_U>1.99$ (right).

Plot styles:
- aspect ratio: each panel 1:1, figure 12 in × 5.5 in
- x-axis: $M_{U_1}$ [GeV], range [1500, 3000], linear
- y-axis: $g_U$, range [0, 3.5] (left) and [0, 2.1] (right), linear
- legend in the upper left of each panel; panel titles "$\beta_L^{23}=1.0$" / "$\beta_L^{23}=2.2$"; annotation "ATLAS 140 fb$^{-1}$, $\tau_\text{had}+E_T^\text{miss}+b$ (SR1b regions), recast"

**Figure 2** — validation: x-axis = index of the 24 parameter points (labelled "$M/g_U$", grouped by $\beta_{23}$), y-axis = $s_R/N_R^\text{ATLAS}$, log scale, range [0.2, 5]; filled circles SR1b-Res, open squares SR1b-NonRes; calibration points ($M_{U_1}=2000$ GeV) in grey, validation points in colour; horizontal lines at 1, 0.5 and 2.

---

# 6. Validation

Before interpreting the results, validate the analysis chain:
1. **Statistics implementation** — run the procedure of Section 4.3 on the ATLAS yields (`atlas_sr1b_expected_yields.csv`, all available $g_U$ points per $(M_{U_1},\beta_{23})$, interpolation as in Step 4). Expected observed limits on $g_U$ (obtained in the planning session with `tools/estimate_limits.py`): $\beta_{23}=1.0$: 1.10, 1.71, 2.20, 2.57; $\beta_{23}=2.2$: 0.66, 0.98, 1.25, 1.46 (for 1500, 2000, 2500, 3000 GeV). Tolerance $\pm5\%$ (toy fluctuations). These are within 7% of the published ATLAS limits except at (1500 GeV, 2.2), where ATLAS gains from the SR0b regions (0.52 published).
2. **Signal yields** — for the 18 points with $M_{U_1}\neq2000$ GeV (not used in the calibration): $0.5<s_R/N_R^\text{ATLAS}<2$ for every point and region, and the median ratio within $[0.7,1.4]$.
3. **Limits** — recast observed $g_U^{95}$ within 25% of the published ATLAS value at the seven $(M_{U_1},\beta_{23})$ points other than (1500 GeV, 2.2).
4. **Width** — MadGraph's automatic $\Gamma/M$ within 10% of $0.0262\,g_U^2$ ($\beta_{23}=1.0$) and $0.0761\,g_U^2$ ($\beta_{23}=2.2$) (the top-quark mass reduces the $t\nu$ channel slightly).

If validation fails, report the discrepancy with the results instead of tuning the analysis to match. In particular do not introduce further calibration constants beyond $k$ and $\varepsilon_c$.

---

# Appendix: Rationale and References

- **Why this study**: target T1 of `research/rd_anomaly/targets.md`. The $\tau\nu+b$ final state probes the product of the $b\tau$ and $c\nu$ couplings — the same combination that enters $R_{D^{(*)}}$. ATLAS published a dedicated search in June 2026 with complete HEPData material; an INSPIRE citation search (`refersto:recid:3164547`, 20.09.2026) found only ATLAS summary notes, i.e. no reinterpretation yet. ATLAS overlaid an anomaly band taken from a 2022 analysis; here the band is updated to the CKM-2025 average, includes the QCD matching factor, and a 3 ab$^{-1}$ projection is added.
- **Design choices and approximations**:
  - Fixed-order $2\to3$ signal with a 40 GeV parton cut instead of ATLAS's CKKW-L merged $\tau\nu$+0,1,2 jets (merging is outside the pipeline); absorbed in $k$.
  - BSM-only: ATLAS's cut-flows show interference of $-23\%$ (SR1b-NonRes) and $-3\%$ (SR1b-Res) relative to BSM-only at $(1500,1.5,0.6)$, and $-22\%$/$-24\%$ at $(3000,2.5,1.0)$. Since the calibration targets are ATLAS **BSM-only** yields, the recast limits correspond to BSM-only signal and are therefore too strong by up to $\simeq6\%$ in $g_U$ ($\propto$ yield$^{1/4}$).
  - P2 (charm final state) is included because for $\beta_{23}\gtrsim1$ mistagged charm jets are a large part of the "1 $b$-tag" signal ($\sigma_\text{P2}/\sigma_\text{P1}\sim2$–8 before tagging [estimate]).
  - The final state $\tau^-\bar\nu_\tau t$ (from $gb\to\tau^-U_1$, $U_1\to t\bar\nu_\tau$), which also yields a $b$-jet, is not generated: ATLAS's signal sample ("$\tau$, $\nu$ and up to two partons") does not contain it either, so omitting it keeps the validation like-for-like; the limits are conservative in this respect.
  - SR0b regions not used (interference). Consequence: at (1500 GeV, $\beta_{23}=2.2$) the recast is weaker than ATLAS by $\simeq25\%$ in $g_U$.
  - Calibrating $(k,\varepsilon_c)$ on one mass and validating on the others is a declared part of the method, not a fix applied after a failed validation.
  - Projection by luminosity scaling at 13 TeV with the Run-2 cut-and-count regions: conservative (no $\sqrt s=14$ TeV gain, no re-optimization, no shape information).
  - LO cross sections, Delphes fast simulation, $\tau$ polarization effects left to Pythia8.
  - Large $\beta_{23}$ is in tension with loop-level flavour constraints in generic UV completions ($\beta_L^{23}\in[0.06,0.16]$ preferred according to arXiv:2210.13422 as quoted by ATLAS); the regime $\beta_{23}\simeq0.1$–0.2 is better tested by $pp\to\tau\tau$ (follow-up plan).
- **Campaign size**: 48 runs × 10,000 events = 480,000 events with Pythia8 + Delphes. Reduced option: groups A and B only ($\beta_{23}=1.0$), 240,000 events.
- **Expected outcome** [estimate]: recast limits close to ATLAS's ($g_U<1.1$–2.7 for $\beta_{23}=1.0$; $<0.5$–1.4 for $\beta_{23}=2.2$). The $R_{D^{(*)}}$ band ($g_U\simeq0.60$–1.20 and $0.41$–0.82 along the central line) lies below the Run-2 exclusion by a factor 1.3–2.2 in $g_U$ everywhere except at its upper $2\sigma$ edge for $M_{U_1}=1.5$ TeV, $\beta_{23}=2.2$. With ATLAS's own yields the naive 3 ab$^{-1}$ scaling gives expected limits of 0.72/1.31/1.69/1.96 (scenario A) and 0.54/1.09/1.41/1.64 (B) for $\beta_{23}=1.0$, and 0.44/0.73/0.96/1.12 (A), 0.33/0.59/0.81/0.93 (B) for $\beta_{23}=2.2$: the central line is reached only for $M_{U_1}\lesssim1.5$–2 TeV with reduced systematics, the upper part of the $2\sigma$ band for all masses in scenario B. A result in which the Run-2 recast already excludes the central line would be a red flag for the signal normalization.
- **References** (all verified on INSPIRE/arXiv on 2026-09-20):
  - [1] ATLAS Collaboration, "Search for a leptoquark in events with a hadronically decaying $\tau$-lepton and missing transverse momentum using $pp$ collisions at $\sqrt s=13$ TeV with the ATLAS detector", arXiv:2606.02067, HEPData ins3164547 — used for: model, selection, data, reference yields and limits.
  - [2] HFLAV, "Average of R(D) and R(D*) for CKM 2025", https://hflav-eos.web.cern.ch/hflav-eos/semi/ckm25/html/RDsDsstar/RDRDs.html (28.09.2025) — used for: $R_{D^{(*)}}$ averages and SM predictions.
  - [3] Iguro, Kitahara, Watanabe, "Global fit to $b\to c\tau\nu$ anomalies as of Spring 2024", arXiv:2405.06062 — used for: $C_{V_L}$ matching, QCD factor 1.12, HL-LHC prospects.
  - [4] Baker, Fuentes-Martín, Isidori, König, "High-$p_T$ signatures in vector–leptoquark models", arXiv:1901.10480 — used for: origin of the Lagrangian (as quoted in [1]).
  - [5] Aebischer, Isidori, Pesut, Stefanek, Wilsch, "Confronting the vector leptoquark hypothesis with new low- and high-energy data", arXiv:2210.13422 — used for: preferred $\beta_L^{23}$ range (as quoted in [1]).
  - [6] Endo, Iguro, Kitahara, Takeuchi, Watanabe, "Non-resonant new physics search at the LHC for the $b\to c\tau\nu$ anomalies", arXiv:2111.04748 — used for: the $\tau_h+b+E_T^\text{miss}$ strategy.
  - [7] Particle Data Group, CKM quark-mixing matrix review (2025 edition), Eq. (12.27) — used for: CKM inputs.
