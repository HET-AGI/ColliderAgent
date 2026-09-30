> **Research plan** `plan_01_t1_quarkportal_lhc_reinterpretation` — study `lz_excess`, target `T1: quark-portal pseudo-Dirac dark matter (coloured scalar mediator, u_R-philic)` — generated 2026-09-21 by the principal-investigator agent.
> User goal: "construct new models, never considered before, that explain the LZ 248 keV nuclear-recoil event" — this plan tests the top-ranked new model at the LHC.
> Depends on: none.
> Caveats: (1) the LZ signal is a single event, 2.6σ global, from a non-blind analysis; (2) LO cross sections with reference K-factors, no detector simulation — the exclusion is a reinterpretation of published cross-section limits, valid only if the signal acceptance equals that of QCD squark-pair production (checked at parton level in Section 4.2, Step 4); (3) the LZ band is read off a published figure by eye (±30%) because LZ's data release was not accessible on 2026-09-21; (4) direct-detection rates use the Standard Halo Model and are exponentially sensitive to its high-speed tail.

# 1. Target

The LZ experiment observed one nuclear-recoil event at 248 keV. In the quark-portal model defined below, a TeV-scale singlet fermion $\chi$ couples to right-handed up quarks through a coloured scalar $\varphi$; a tiny Majorana splitting $\delta\approx 230$–340 keV of $\chi$ (irrelevant for colliders, not part of the model file) makes its scattering on nuclei inelastic and can produce the event. The coupling $\lambda$ required by thermal freeze-out is of order one, so $pp\to\varphi\varphi^*$ receives a large $\lambda^4$ contribution from $t$-channel $\chi$ exchange between valence quarks. **Question: which part of the $(M_\varphi,\lambda)$ and $(M_\varphi,m_\chi)$ parameter space that gives the LZ event and the observed relic density is excluded at 95% CL by the ATLAS 139 fb$^{-1}$ squark search, and how many signal events does the open region give at the HL-LHC?**

Deliverables (with output file names):
- Figure 1 (`output/figures/t1_mphi_lambda.pdf`, two panels: $m_\chi$ = 1000 GeV and $m_\chi$ = 500 GeV): $(M_\varphi,\lambda)$ plane with the ATLAS-excluded region, the relic-density line, the splitting $\delta$ that LZ's event requires, HL-LHC event-count contours, and the large-width region.
- Figure 2 (`output/figures/t1_mphi_mchi_relic.pdf`): $(M_\varphi,m_\chi)$ plane on the relic-density line: signal strength $\mu=\sigma_{\rm pred}/\sigma_{\rm UL}$, its $\mu=1$ contour, and contours of the required $\delta$.
- Table (`output/data/t1_xsec_coefficients.csv`): per mass point and $\sqrt s$, the coefficients $A$, $B$, $C$, $D$ defined in Section 4.2 with their Monte Carlo errors.
- Table (`output/data/t1_benchmarks.csv`): for the micrOMEGAs points of Section 5: $\Omega h^2$, elastic cross sections, analytic counterparts, and $\mu$.

---

# 2. Model

The Standard Model is extended by two fields that are odd under a $Z_2$ symmetry (all SM fields are even): a Dirac fermion $\chi$, singlet under the SM gauge group, which is the dark matter, and a complex scalar $\varphi$ with the gauge quantum numbers of a right-handed up squark. This is the structure of the simplified model `S3D_uR` of arXiv:2307.10367.

## 2.1 Lagrangian

$$\mathcal{L}_\text{BSM} = \bar\chi\,(i\slashed\partial - m_\chi)\,\chi + (D_\mu\varphi)^\dagger(D^\mu\varphi) - M_\varphi^2\,\varphi^\dagger\varphi + \big[\lambda\,\bar\chi\,P_R\,u\,\varphi^\dagger + \text{h.c.}\big]$$

Here,
- $\chi$ is a Dirac fermion beyond the SM: colour singlet, $SU(2)_L$ singlet, hypercharge $Y=0$ ($Q=T_3+Y$), electric charge $Q=0$. It is not self-conjugate. It has no gauge interactions. It is $Z_2$-odd and stable. Suggested name: `chiD`.
- $\varphi$ is a complex scalar beyond the SM: colour triplet, $SU(2)_L$ singlet, hypercharge $Y=+2/3$, electric charge $Q=+2/3$. It is not self-conjugate. It is $Z_2$-odd. Suggested name: `phiU`.
- $D_\mu\varphi = (\partial_\mu - i g_s T^a G^a_\mu - i g' Y B_\mu)\,\varphi$ with $Y=2/3$ is the covariant derivative containing the gluon field and the hypercharge field (i.e. photon and $Z$ after electroweak symmetry breaking); $T^a$ are the $SU(3)_C$ generators in the fundamental representation.
- $P_{R}=\frac12(1+\gamma^5)$ is the right-handed chirality projector; $u$ is the up quark (first generation only; no coupling to $c$, $t$ or to down-type quarks).
- $\lambda$ is a real, dimensionless coupling. The hermitian conjugate of the interaction term is $\lambda\,\varphi\,\bar u\,P_L\,\chi$.
- Check of the interaction term: $\bar\chi$ (colour 1, $Q=0$) × $u$ (colour 3, $Q=+\tfrac23$) × $\varphi^\dagger$ (colour $\bar3$, $Q=-\tfrac23$) is a colour singlet, electrically neutral, hypercharge $0+\tfrac23-\tfrac23=0$, mass dimension 4. The vertex describes $u\to\chi\,\varphi$ and, from the h.c., $\varphi\to u\,\bar\chi$.
- No other new interactions: the quartic couplings $\varphi^\dagger\varphi H^\dagger H$ and $(\varphi^\dagger\varphi)^2$ are set to zero (they do not affect any observable of this plan).

Both new fields are $Z_2$-odd: `chiD` and `phiU` (and their antiparticles). The CalcHEP output must mark them as the dark sector (names with the `~` prefix).

## 2.2 Parameters

The free (external) parameters are:
- $m_\chi$: mass of $\chi$. Benchmark 1000 GeV; scan values in Section 3.3.
- $M_\varphi$: mass of $\varphi$, always $M_\varphi > m_\chi$. Benchmark 2000 GeV; scan values in Section 3.3.
- $\lambda$: the Yukawa coupling. Real. Benchmark 1.33; simulated at the reference values 1 and 2 (Section 3.3).

There are no derived (internal) parameters.

- Width of $\varphi$: computed automatically by MadGraph at each parameter point (only needed for the runs of group C, where $\varphi$ decays). Cross-check value [estimate]: $\Gamma_\varphi = \dfrac{\lambda^2 M_\varphi}{16\pi}\Big(1-\dfrac{m_\chi^2}{M_\varphi^2}\Big)^2 = 39.6$ GeV at the benchmark ($\Gamma/M = 2.0\%$); 50.4 GeV for ($M_\varphi$, $m_\chi$, $\lambda$) = (2000, 1000, 1.5).
- $\chi$ is stable (width zero).

SM parameters at their defaults (diagonal CKM, massless $u,d,s,c$ quarks, massive $b$).

Model outputs required: UFO **and** CalcHEP (for Section 5).

---

# 3. Collider Simulation

## 3.1 Process

Three processes, generated separately. Define the multiparticle label `dm = chiD chiD~` so that the process strings do not depend on which of the two carries the conserved dark number.

**P1 — mediator pair production (stable final state, $2\to2$):**
$$pp \to \varphi\,\varphi^*$$
Diagrams: QCD production ($gg\to\varphi\varphi^*$ and $q\bar q\to g^*\to\varphi\varphi^*$, order $g_s^2$ in the amplitude) **and** $t$-channel $\chi$ exchange ($u\bar u\to\varphi\varphi^*$, order $\lambda^2$, `NP=2`), including their interference. Exclude electroweak production (`QED=0`). Two versions are generated: P1-QCD with `NP=0` (pure QCD), and P1-full with both contributions allowed.

**P2 — associated production ($2\to2$):**
$$pp \to \varphi\,\chi\text{-type} \quad\text{and}\quad pp\to\varphi^*\,\chi\text{-type}$$
i.e. `p p > phiU dm` added to `p p > phiU~ dm` ($ug\to\varphi\chi$ and $\bar ug\to\varphi^*\bar\chi$; amplitude of order $g_s\lambda$). Charge-conjugate processes must both be included.

**P3 — decayed pair production, for the acceptance check only:**
$$pp\to\varphi\,\varphi^*,\quad \varphi\to u + \text{dm},\quad \varphi^*\to\bar u + \text{dm}$$
with the decays in the matrix element as an on-shell decay chain (`p p > phiU phiU~, phiU > u dm, phiU~ > u~ dm`). Two versions: P3-QCD (`NP=0` in the production part; the decay vertex necessarily carries `NP=1` each) and P3-full.

Initial-state flavours: default four/five-flavour proton; no heavy-flavour initial states are needed. Same-sign production $pp\to\varphi\varphi$ does not exist for a Dirac $\chi$ and must not be generated.

## 3.2 Collider simulation settings

All runs are parton level:
- PDF: `NNPDF31_lo_as_0118` (LHAPDF ID 315000)
- parton shower: none
- detector simulation: none
- output: LHE (event files are needed only for group C; for groups A and B only the cross section and its Monte Carlo error are used)
- generator-level cuts: none beyond MG5 defaults for groups A and B (the final-state particles are massive); for group C set the jet cuts to zero (`ptj = 0`, `drjj = 0`, `etaj = -1`) so that the decay quarks are not cut at generation
- renormalisation/factorisation scales: MG5 default dynamical scale

Run groups:
- **Group A**: 13 TeV LHC ($pp$), 10,000 events per parameter point. P1-QCD, P1-full, P2.
- **Group B**: 14 TeV LHC ($pp$), 10,000 events per parameter point. P1-QCD, P1-full, P2.
- **Group C**: 13 TeV LHC ($pp$), 20,000 events per parameter point. P3-QCD and P3-full.

## 3.3 Parameter settings for each run

Exact scaling laws (LO, $2\to2$ with stable final state, so no width enters):
$\sigma_{\rm P1}(\lambda) = A + B\lambda^2 + C\lambda^4$ and $\sigma_{\rm P2}(\lambda) = D\lambda^2$. $A$ depends on $M_\varphi$ only; $B$, $C$, $D$ depend on $(M_\varphi, m_\chi)$. Therefore $\lambda$ is simulated only at reference values.

**Group A (13 TeV)** — mass grid: $M_\varphi\in\{600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400\}$ GeV; $m_\chi\in\{100, 300, 500, 700, 900, 1000, 1100\}$ GeV; keep only points with $M_\varphi\ge m_\chi+100$ GeV (61 mass points: 10, 10, 10, 9, 8, 7, 7 per $m_\chi$ value).
- A0: P1-QCD at the 10 values of $M_\varphi$ ($m_\chi$ = 100 GeV, $\lambda$ = 1; neither enters) — 10 runs
- A1: P1-full, $\lambda=1$, 61 mass points — 61 runs
- A2: P1-full, $\lambda=2$, 61 mass points — 61 runs
- A3: P2, $\lambda=1$, 61 mass points — 61 runs

**Group B (14 TeV)** — mass grid: $M_\varphi\in\{1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3500, 4000\}$ GeV; $m_\chi\in\{500, 1000, 1500\}$ GeV; keep only $M_\varphi\ge m_\chi+200$ GeV (33 mass points: 12, 12, 9).
- B0: P1-QCD at the 12 values of $M_\varphi$ — 12 runs
- B1, B2: P1-full at $\lambda$ = 1 and 2 — 66 runs
- B3: P2 at $\lambda=1$ — 33 runs

**Group C (13 TeV)** — $(M_\varphi, m_\chi)$ = (1400, 700), (2000, 1000), (1200, 1000) GeV; for each: P3-QCD with $\lambda=1.5$ (it only sets the width) and P3-full with $\lambda=1.5$ — 6 runs.

All other parameters at their defaults. Total: 310 runs, 3.16 million parton-level events.

---

# 4. Numerical Analysis

## 4.1 Experimental data

**ATLAS, search for squarks and gluinos in jets + missing transverse momentum** (arXiv:2010.14293, HEPData ins1827025), 139 fb$^{-1}$ at $\sqrt s=13$ TeV:
- Cross-section upper limits for squark-pair production with direct decays $\tilde q\to q\tilde\chi^0_1$ (the topology of P1 with $\varphi\to u\chi$): stored as `research/lz_excess/data/ins1827025_xsec_ul_1.csv` (HEPData table "X-section U.L. 1"). The CSV has **two blocks** separated by a blank line, each with its own column line. Use the first block, columns `M(Squark) [GeV]`, `M(LSP) [GeV]`, `OBSERVED CROSS SECTION UPPER LIMIT 95% CL (FB)`: 108 points, $400\le M\le2400$ GeV, $0\le m_{\rm LSP}\le1100$ GeV. Ignore the second block (`Best SR`, text labels). Lines starting with `#:` are header comments. Examples: $(2000, 1000)\to0.57$ fb; $(1200, 0)\to1.69$ fb; $(1500, 1100)\to10.84$ fb.
- Observed exclusion contour for a single non-degenerate light-flavour squark: `research/lz_excess/data/ins1827025_obs_contour_2.csv` (HEPData table "Obs.Contour 2"; one block, columns `M(Squark) [GeV]`, `M(LSP) [GeV]`, 97 points; the contour reaches $M = 1220$ GeV at $m_{\rm LSP}=0$). Used for validation and as a reference line in Figure 2.
- Not used: all gluino and one-step-decay results of the same record (different topologies).

**Reference cross sections** for a single colour-triplet scalar pair at 13 TeV, NNLO$_{\rm approx}$+NNLL (LHC SUSY Cross Section Working Group, stop/sbottom table, retrieved 2026-09-21), stored as `research/lz_excess/data/stop_xsec_13TeV_nnll.csv` (columns `M_GeV`, `sigma_fb`, `unc_percent`; first line is a `#` comment):

| $M$ [GeV] | 600 | 800 | 1000 | 1200 | 1400 | 1600 | 1800 | 2000 | 2200 | 2400 |
|---|---|---|---|---|---|---|---|---|---|---|
| $\sigma$ [fb] | 217.8 | 34.82 | 7.395 | 1.876 | 0.5371 | 0.1678 | 0.05585 | 0.01956 | 0.007098 | 0.002646 |
| unc. [%] | 6.0 | 7.3 | 9.1 | 11.4 | 14.7 | 19.5 | 26.3 | 35.4 | 47.9 | 64.3 |

**LZ** (arXiv:2609.02823): two-sided 90% CL interval on the isoscalar DM–nucleon cross section for inelastic spin-independent scattering, $m_\chi$ = 1 TeV, as a function of the splitting $\delta$ — read off Fig. S7 **by eye (±30%)**; no data file exists:

| $\delta$ [keV] | 150 | 200 | 250 | 300 | 350 |
|---|---|---|---|---|---|
| lower [cm²] | 1.3e-45 | 1.2e-44 | 8e-44 | 3.5e-43 | 4e-41 |
| upper [cm²] | 2.0e-44 | 1.7e-43 | 1.1e-42 | 7.5e-42 | 6.5e-40 |
| central $\sigma_c=\sqrt{\text{lower}\times\text{upper}}$ [cm²] | 5.1e-45 | 4.5e-44 | 3.0e-43 | 1.6e-42 | 1.6e-40 |

Exposure 2.84 t yr; nuclear-recoil efficiency above 50% for 5.4–269.9 keV.

**LZ 4.2 t yr limits** (arXiv:2410.17036, HEPData ins2841863): `research/lz_excess/data/ins2841863_SDn_cross_section.csv` and `..._SI_cross_section.csv` (multi-block; first block, columns `mass`, `limit`, in GeV and cm²). At 1000 GeV (log-log interpolation): $\sigma_{\rm SD}^n<5.0\times10^{-42}$ cm².

## 4.2 Simulated signal events

### Step 1: cross-section coefficients

For each mass point and each $\sqrt s$, read the cross section $\sigma$ and its Monte Carlo error from the MadGraph output of each run and compute
$$A=\sigma_{\text{P1-QCD}},\quad C=\frac{\sigma_{\text{P1-full}}(\lambda{=}2)-4\,\sigma_{\text{P1-full}}(\lambda{=}1)+3A}{12},\quad B=\sigma_{\text{P1-full}}(\lambda{=}1)-A-C,\quad D=\sigma_{\rm P2}(\lambda{=}1).$$
$B$ may be negative (interference). Propagate the Monte Carlo errors linearly. Write everything to `output/data/t1_xsec_coefficients.csv` (columns: `sqrts_TeV, Mphi, mchi, A, dA, B, dB, C, dC, D, dD`, in fb).

### Step 2: signal prediction

$$\sigma_{\rm P1}(M_\varphi,m_\chi,\lambda) = K_{\rm QCD}\,A + \sqrt{K_{\rm QCD}K_t}\;B\,\lambda^2 + K_t\,C\,\lambda^4,\qquad \text{BR}(\varphi\to u\chi)=1 .$$
- $K_{\rm QCD}(M_\varphi)=\sigma_{\rm NNLL}(M_\varphi)/A(M_\varphi)$ from the reference table (13 TeV). At 14 TeV use the 13 TeV value at the same mass, and for $M_\varphi>2400$ GeV the value at 2400 GeV [assumed].
- $K_t=1$ [assumed] (no higher-order calculation for the $\chi$-exchange contribution is used). As a systematic variation, repeat with $K_t=K_{\rm QCD}$.
- The geometric mean for the interference term is the prescription of arXiv:2307.10367 (Sec. II B 5).
- $\sigma_{\rm P2}=D\lambda^2$, no K-factor. P2 is **not** added to the signal that is compared with the ATLAS limit (different topology: one hard jet); it enters only the HL-LHC event counts.

Interpolation in $M_\varphi$ at fixed $m_\chi$ (needed for Figure 1): cubic spline of $\ln A$, $\ln C$, $\ln D$ and of the ratio $B/\sqrt{AC}$ as functions of $\ln M_\varphi$.

### Step 3: reinterpretation of the ATLAS limit

Interpolate $\log_{10}\sigma_{\rm UL}$ linearly in the $(M, m_{\rm LSP})$ plane (`scipy.interpolate.LinearNDInterpolator` on the 108 points), with $M\to M_\varphi$, $m_{\rm LSP}\to m_\chi$. Outside the convex hull of the points there is no limit. Define
$$\mu(M_\varphi,m_\chi,\lambda)=\frac{\sigma_{\rm P1}(M_\varphi,m_\chi,\lambda)}{\sigma_{\rm UL}(M_\varphi,m_\chi)} .$$

### Step 4: acceptance check (group C)

The limit of Step 3 is valid only if signal events from $\chi$ exchange pass the ATLAS selection as often as QCD-produced squark pairs do. Test this at parton level with proxy cuts [assumed — they mimic the two-jet, high-$m_{\rm eff}$ regions of the search but are **not** the ATLAS selection and are used only for a ratio]:
- jets = the two decay quarks with $p_T>50$ GeV and $|\eta|<2.8$; require both;
- $p_T(j_1)>250$ GeV; $|\eta(j_{1,2})|<2.0$;
- $E_T^{\rm miss}$ = magnitude of the vector sum of the transverse momenta of the two dark-matter particles, $>300$ GeV;
- $\Delta\phi(j_{1,2},\vec p_T^{\,\rm miss})>0.8$;
- $m_{\rm eff}=p_T(j_1)+p_T(j_2)+E_T^{\rm miss}>1600$ GeV.

For each of the three mass points compute the pass fractions $\epsilon_{\rm QCD}$ (P3-QCD) and $\epsilon_{\rm full}$ (P3-full at $\lambda=1.5$), and from them the pass fraction of the pure $\chi$-exchange-plus-interference part,
$$r_{\rm acc}=\frac{\epsilon_{\rm full}\,\sigma_{\text{P3-full}}-\epsilon_{\rm QCD}\,\sigma_{\text{P3-QCD}}}{\epsilon_{\rm QCD}\,(\sigma_{\text{P3-full}}-\sigma_{\text{P3-QCD}})} .$$
Report the three values. In the figures draw a second exclusion contour in which the $B$ and $C$ terms of Step 2 are multiplied by $\min(1, r_{\rm acc})$, with $r_{\rm acc}$ taken from the nearest of the three mass points.

### Step 5: relic density line and LZ requirement (closed forms)

- Relic-density coupling (LO $s$-wave annihilation $\chi\bar\chi\to u\bar u$, arXiv:2307.10367 App. A, equated to the canonical $2.2\times10^{-26}$ cm³/s = $1.885\times10^{-9}$ GeV⁻²):
$$\lambda_{\rm relic}(m_\chi,M_\varphi)=\Big[1.885\times10^{-9}\,\text{GeV}^{-2}\times\frac{64\pi\,(m_\chi^2+M_\varphi^2)^2}{3\,m_\chi^2}\Big]^{1/4}$$
(masses in GeV). Values: 0.93, 1.07, 1.33, 1.89, 2.46 for $m_\chi$ = 1000 GeV and $M_\varphi$ = 1200, 1500, 2000, 3000, 4000 GeV.
- Inelastic DM–nucleus scattering: $b_u=\dfrac{\lambda^2}{8(M_\varphi^2-m_\chi^2)}$, $f_p=2b_u$, $f_n=b_u$, $\sigma_p=\dfrac{\mu_p^2f_p^2}{\pi}\times3.894\times10^{-28}$ cm² GeV² with $\mu_p=m_\chi m_p/(m_\chi+m_p)$, $m_p=0.9383$ GeV, and the isoscalar-equivalent cross section on xenon $\sigma_{\rm eff}=0.498\,\sigma_p$.
- Required splitting $\delta_{\rm LZ}(m_\chi,\sigma_{\rm eff})$: import `research/lz_excess/tools/idm_rate.py` and solve `counts(m_chi, delta, sigma_eff)['roi'] = N_cal` for `delta` (keV) by bisection on [50, 450] keV (the function is monotonically decreasing in `delta`); `N_cal = 2.5` events is a **calibration constant declared here**, see Section 6. If `counts(m_chi, 50, sigma_eff)['roi'] < N_cal` there is no solution (cross section too small). Flag points where `counts(...)['lo'] / counts(...)['roi'] > 0.3` (more than 30% of the predicted events below 70 keV) as "low-energy leakage".
- Large-width region: $\lambda^2(1-m_\chi^2/M_\varphi^2)^2/(16\pi)>0.1$.
- HL-LHC event counts: $N_{\rm P1}=\sigma_{\rm P1}(14\text{ TeV})\times3000$ fb$^{-1}$ and $N_{\rm P2}=D(14\text{ TeV})\lambda^2\times3000$ fb$^{-1}$, before any selection.

## 4.3 Statistical analysis

A parameter point is excluded at 95% CL if $\mu\ge1$: the ATLAS upper limits are observed 95% CL (CL$_s$) limits on the cross section of exactly this topology, obtained with the signal region of best expected sensitivity at each mass point. No combination and no further likelihood is constructed. Uncertainty bands are not propagated; instead two variations are shown: $K_t=K_{\rm QCD}$ instead of 1 (Step 2) and the acceptance-corrected contour (Step 4).

## 4.4 Figure

**Figure 1** — two panels side by side, left $m_\chi$ = 1000 GeV, right $m_\chi$ = 500 GeV. Each contains:
1. **ATLAS-excluded region** — $\mu\ge1$ from 13 TeV coefficients, defined for $M_\varphi\le2400$ GeV; red fill (alpha 0.3) with solid red boundary. Red dashed: boundary for $K_t=K_{\rm QCD}$. Red dotted: acceptance-corrected boundary (Step 4).
2. **Relic-density line** — $\lambda_{\rm relic}(M_\varphi)$, black solid; black dots at the micrOMEGAs points of Section 5 lying in the panel, each annotated with its $\Omega h^2$.
3. **LZ requirement** — contours $\delta_{\rm LZ}$ = 200, 250, 300, 325 keV (blue solid, labelled). In the left panel additionally the contours $\sigma_{\rm eff}=\sigma_c(\delta)$ for $\delta$ = 200, 250, 300 keV from the LZ table of Section 4.1 (blue dotted) as a cross-check of the calibration.
4. **HL-LHC event counts** — contours $N_{\rm P1}$ = 10 and 100 (green dashed) and $N_{\rm P2}$ = 10 and 100 (green dotted), from 14 TeV coefficients.
5. **Large-width region** — grey hatching; and a horizontal grey line at $\lambda=\sqrt{4\pi}$.
6. Left panel only: a star at the benchmark (2000 GeV, 1.33).

Plot styles: aspect ratio 2:1 for the two-panel figure; x-axis $M_\varphi$ [GeV], range [1200, 4000] (left) and [600, 4000] (right), linear; y-axis $\lambda$, range [0, 3.6], linear; legend in the upper left of the left panel.

**Figure 2** — single panel:
1. **Signal strength on the relic line** — colour map of $\log_{10}\mu$ evaluated at $\lambda=\lambda_{\rm relic}(m_\chi,M_\varphi)$ on the 61 group-A mass points (triangulated), colour range [−2, 1]; solid black contour at $\mu=1$; dashed black for $K_t=K_{\rm QCD}$.
2. **ATLAS single-squark observed contour** (file `ins1827025_obs_contour_2.csv`), grey dash-dotted — the QCD-only reference.
3. **Required splitting** — contours $\delta_{\rm LZ}$ = 250, 300, 325 keV at $\sigma_{\rm eff}(\lambda_{\rm relic})$ (blue); points flagged for low-energy leakage or without solution marked with grey crosses.
4. Diagonal grey line $M_\varphi=m_\chi$.

Plot styles: aspect ratio 4:3; x-axis $M_\varphi$ [GeV], [600, 2400], linear; y-axis $m_\chi$ [GeV], [100, 1100], linear; colour bar labelled $\log_{10}(\sigma_{\rm pred}/\sigma_{\rm UL})$.

---

# 5. Dark Matter Observables

Computed with micrOMEGAs from the CalcHEP output of the same model (not part of the collider pipeline).
- $Z_2$-odd particles: `chiD`, `phiU` (dark matter candidate: `chiD`, a Dirac fermion — particle and antiparticle both contribute).
- observables: relic density $\Omega h^2$; elastic spin-independent cross sections on proton and neutron; elastic spin-dependent cross sections on proton and neutron.
- parameter points ($m_\chi$, $M_\varphi$, $\lambda$) in GeV: (1000, 1200, 0.93), (1000, 1500, 1.07), (1000, 2000, 1.33), (1000, 3000, 1.89), (500, 1000, 0.94), (500, 1500, 1.33), (300, 1000, 1.14), (2000, 3000, 1.52) — eight points, $\lambda=\lambda_{\rm relic}$ of Section 4.2.
- use in figures: annotate $\Omega h^2$ in Figure 1; write all values to `output/data/t1_benchmarks.csv` next to the analytic $\sigma_p$ of Section 4.2 Step 5, the analytic $\sigma^{p}_{\rm SD}=3\mu_p^2(0.842\,b_u)^2/\pi$ and $\sigma^{n}_{\rm SD}=3\mu_n^2(0.427\,b_u)^2/\pi$, and $\mu$.
- Interpretation: for a Dirac $\chi$ micrOMEGAs returns the *elastic* vector-current cross section. In the pseudo-Dirac model this elastic process is absent; the same number is the $\sigma_p$ that normalises the *inelastic* rate. It is therefore a check of the closed form, not a quantity to compare with elastic limits. The spin-dependent cross sections are physical in both cases and are to be compared with the LZ SD-neutron limit of Section 4.1.

---

# 6. Validation

Before interpreting the results, validate the analysis chain:
- **Exclusion prescription against ATLAS's own result** (no simulation needed; already done in this session, see Appendix): with $\sigma_{\rm pred}=\sigma_{\rm NNLL}(M)$ of the reference table and $m_\chi\to0$, the $\mu=1$ crossing must reproduce ATLAS's observed single-squark limit of 1220 GeV within ±50 GeV.
- **LO normalisation**: $K_{\rm QCD}=\sigma_{\rm NNLL}/A$ is expected between 1.2 and 2.5 at all ten masses [estimate]; report the values; if any lies outside, stop and report.
- **Scaling law**: at one mass point, (2000, 1000) GeV at 13 TeV, run P1-full additionally at $\lambda=1.5$ and check $\sigma=A+2.25B+5.0625C$ within 3 Monte Carlo standard deviations.
- **Width**: MadGraph's automatic $\Gamma_\varphi$ in the group-C runs must agree with the closed form of Section 2.2 within 2%.
- **micrOMEGAs vs closed forms**: $\sigma^p_{\rm SI}$ within 20% of $\mu_p^2(2b_u)^2/\pi$ and $\sigma^n_{\rm SI}/\sigma^p_{\rm SI}=0.25$ within 10%; $\Omega h^2=0.12$ within ±30% for the points with $M_\varphi\ge1.5\,m_\chi$ (for $M_\varphi=1.2\,m_\chi$ coannihilation with $\varphi$ is expected to lower $\Omega h^2$ — report, do not tune).
- **Calibration of the rate code** (declared here, before running): `N_cal = 2.5` is fixed so that at $m_\chi$ = 1 TeV the code reproduces LZ's central cross sections $\sigma_c$ at $\delta$ = 200, 250, 300 keV (the code gives 2.5, 2.8, 2.2 events there). It is tested at $\delta$ = 150 and 350 keV, where the code gives 2.4 and 4.0 events. Re-compute these five numbers as the first step; the blue dotted and blue solid contours of Figure 1 (left) must agree within 10 keV in $\delta$.

If validation fails, report the discrepancy with the results instead of tuning the analysis to match.

---

# Appendix: Rationale and References

- **Why this study**: target report `research/lz_excess/targets.md`, target T1. Thermal $t$-channel models with Dirac dark matter are excluded by elastic direct detection and were therefore not confronted with LHC data in arXiv:2307.10367; a keV-scale Majorana splitting removes that exclusion and turns the model into an explanation of the LZ event, so its LHC status is an open question. It is also the first plan for a new model: cheap, it validates the model files, and its coefficient table fixes the scan ranges of the proposed HL-LHC projection (plan_02).
- **Design choices**: (i) *limit reinterpretation instead of a recast* — the topology is identical to the experiment's squark simplified model and ATLAS publishes cross-section limits on the full mass grid, so re-implementing a multi-bin jets + $E_T^{\rm miss}$ analysis with a fast simulation would add uncertainty, not information; the one assumption this makes (equal acceptance of $\chi$-exchange events) is tested in Step 4. (ii) *Dirac UFO for a pseudo-Dirac model* — $\delta/m_\chi\sim3\times10^{-7}$; same-sign $uu\to\varphi\varphi$ is suppressed by $(\delta/m_\chi)^2$ in the rate [estimate]. (iii) *Exact λ-scaling* reduces a three-dimensional scan to two reference couplings. (iv) P2 is left out of the limit: conservative. (v) LO with reference K-factors; the dominant theory uncertainty is $K_t$, shown as a variation. (vi) 13 TeV limits only; no 13.6 TeV Run-3 result is used.
- **Statistical prescription tested in this session**: feeding the prescription the reference NNLL cross section of a single scalar colour triplet and ATLAS's limits at $m_{\rm LSP}=0$ gives $\mu$ = 1.11, 1.04, 0.97 at $M$ = 1200, 1220, 1240 GeV, i.e. a crossing at 1232 GeV against ATLAS's published 1220 GeV (12 GeV, 1%).
- **Expected outcome** [estimate]: at the benchmark (2000, 1000) GeV ATLAS allows 0.57 fb while QCD production gives 0.020 fb; the $\lambda^4$ term would have to supply a factor ~29, which is not expected for $\lambda=1.33$ — the benchmark should be open. For $m_\chi\lesssim500$ GeV the QCD term alone excludes $M_\varphi\lesssim1.2$ TeV (1.9 fb predicted at 1200 GeV against limits of 2–6 fb for $m_\chi$ = 100–500 GeV), and the $\chi$-exchange term with $\lambda_{\rm relic}\approx1$–1.3 should push this to roughly 1.4–1.8 TeV. At the HL-LHC, a few hundred to a few thousand P1+P2 events are expected at the benchmark before cuts. A result in which the benchmark *is* excluded would mean $C$ is an order of magnitude larger than estimated — check the process definition (same-sign production must be absent) before believing it.
- **References** (all verified in this session):
  - [1] LZ Collaboration (Akerib et al.), "Search for dark matter particle interactions in an extended nuclear recoil energy window with the LUX-ZEPLIN (LZ) experiment", arXiv:2609.02823 — used for: event, exposure, efficiency window, Fig. S7 interval (by eye)
  - [2] Arina, Fuks, Heisig, Krämer, Mantani, Panizzi, "Comprehensive exploration of t-channel simplified models of dark matter", arXiv:2307.10367 — used for: Lagrangian convention, annihilation cross section (App. A; note the misprinted definition of $r$ there), K-factor prescription for the interference term, status of Dirac-DM models
  - [3] ATLAS Collaboration, "Search for squarks and gluinos in final states with jets and missing transverse momentum using 139 fb$^{-1}$ of $\sqrt s$ = 13 TeV $pp$ collision data with the ATLAS detector", arXiv:2010.14293, HEPData ins1827025 — used for: cross-section upper limits, single-squark contour
  - [4] LHC SUSY Cross Section Working Group, stop/sbottom pair production at 13 TeV, NNLO$_{\rm approx}$+NNLL (twiki page `LHCPhysics/SUSYCrossSections13TeVstopsbottom`, raw page read 2026-09-21) — used for: reference cross sections
  - [5] LZ Collaboration (Aalbers et al.), "Dark Matter Search Results from 4.2 Tonne-Years of Exposure of the LUX-ZEPLIN (LZ) Experiment", arXiv:2410.17036, HEPData ins2841863 — used for: SD-neutron limit
  - [6] Steigman, Dasgupta, Beacom, "Precise Relic WIMP Abundance and its Impact on Searches for Dark Matter Annihilation", arXiv:1204.3622 — used for: canonical thermal cross section (value $2.2\times10^{-26}$ cm³/s quoted from memory of the abstract: [unverified])
  - Inputs of `tools/idm_rate.py` (Standard Halo Model parameters, Helm form-factor parameters) and the spin fractions 0.842 / −0.427 are recalled values: [unverified].
