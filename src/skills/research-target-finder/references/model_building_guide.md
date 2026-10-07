# Model Building Guide

How to go from an anomaly or a purpose to a consistent, testable, pipeline-ready BSM model. The tables in this guide are for **orientation** — they tell you what to look for, not what is currently viable. Viability always comes from the literature search (see [literature_search.md](literature_search.md)). The first decision is the **regime** (Section 1.0): whether the new physics is heavy enough for an effective-operator description, or whether a light mediator, a new light state, or a collider resonance makes the explicit particle the only valid language — the rest of the guide branches on it.

Conventions: $Q = T_3 + Y$; representations are $(SU(3)_C, SU(2)_L, U(1)_Y)$; $v = 246$ GeV.

SM fields: $Q_L\,(3,2,\tfrac16)$, $u_R\,(3,1,\tfrac23)$, $d_R\,(3,1,-\tfrac13)$, $L_L\,(1,2,-\tfrac12)$, $e_R\,(1,1,-1)$, $H\,(1,2,\tfrac12)$.

## 1. From Anomaly to Model-Independent Requirement

Before choosing particles, establish what the data demand — and in which **language** the data can be expressed. An effective operator among SM fields is the right language only when every new state is far heavier than the momentum flowing through the anomalous process. Decide that first.

### 1.0 Decide the regime: is an EFT description valid?

Compare the characteristic momentum transfer $q$ of the anomalous process with the masses $M$ of the new states the data allow. Do this **twice** — once for the anomaly, once for the collider process that will test the explanation — because the two can fall into different regimes: a 2 TeV leptoquark is a contact interaction in $B$ decays and an explicit $t$-channel mediator in the LHC $\tau\nu$ tail.

| Regime | Condition | Language for "what the data require" | Mediator enumeration | Sections |
|---|---|---|---|---|
| **Heavy** | every new state has $M\gg q$ | SMEFT / LEFT operators among SM fields; Wilson coefficients | tree-level dictionary, then loops | 1.1, 2.1–2.2 |
| **Heavy mediator, light new state** | the mediator has $M\gg q$ but a new light state ($\chi$, $N$, $a$, ...) is produced | EFT whose operators contain the light state as a field | open the operator with the light state at a vertex | 1.1 (enlarged field content), 1.2, 2.1, 2.3 |
| **Light mediator** | $M\lesssim q$: produced on shell (below the kinematic limit) or exchanged at $q^2\sim M^2$ | mass, spin, couplings, width, lifetime, decay modes, and the $q^2$ or energy spectrum; a fit with the full propagator or the full loop function — no single Wilson coefficient exists | portal catalogue | 1.2, 2.3 |
| **Resonance / high-energy tail** | the collider reaches $\sqrt{\hat s}\sim M$: a bump, or a tail whose signal events have $\sqrt{\hat s}$ not $\ll M$ | mass, width, spin/CP, $\sigma\times$BR; or the explicit-mediator simplified model whose propagator shapes the tail | quantum numbers from production and decay | 1.3, 2.1, 2.4 |

Characteristic momentum transfers (kinematic limits follow from PDG masses):

| Anomalous process | $q$ | Heavy regime requires | Light regime is possible for |
|---|---|---|---|
| $(g-2)_\mu$, $(g-2)_e$ | $m_\ell$ | $M\gg m_\ell$ — loop function in its heavy limit | $M\lesssim$ GeV: full mass dependence of the loop function (Section 7) |
| $B$ decays ($b\to s\nu\bar\nu$, $b\to s\ell\ell$, $b\to c\tau\nu$) | $\sqrt{q^2}$ up to $m_B-m_K\approx4.8$ GeV ($m_B-m_{K^*}\approx4.4$ GeV; $m_B-m_{D^{(*)}}$ for $b\to c$) | $M\gg5$ GeV | $M<m_B-m_K$: on-shell $B\to K^{(*)}X$ (two-body, monochromatic kaon); $M\sim$ GeV off shell: $q^2$-shaped three-body decay |
| Kaon decays ($K\to\pi\nu\bar\nu$, $K\to\pi\ell\ell$) | $\lesssim m_K-m_\pi\approx0.35$ GeV | $M\gg0.4$ GeV | $M<0.35$ GeV on shell |
| Neutrino scattering (trident, CE$\nu$NS, short-baseline) | 10 MeV – few GeV | $M\gg$ GeV | $M\lesssim$ GeV |
| Dark-matter direct detection | 10–100 MeV | $M\gg100$ MeV (contact interaction) | $M\lesssim q$: long-range $1/(q^2+M^2)^2$ |
| Electroweak precision, $m_W$, Higgs rates | $m_Z$, $m_h$ | $M\gg v$ | light states appear as exotic $Z$ / $h$ decays |
| LHC high-$p_T$ tails (dilepton, mono-$X$, $t\bar t$) | $\sqrt{\hat s}$ of the signal region, 1–5 TeV | $M\gg$ several TeV | otherwise the explicit mediator (resonance regime) |
| LHC bump | $\sqrt{\hat s}=M$ | never | always the explicit resonance |

Rules:
- **Enumerate every regime the data allow.** One anomaly usually has candidates in several: for $B\to K+\text{invisible}$ there are a heavy leptoquark or $Z'$, a heavy mediator producing a light dark-matter pair, a light $Z'$, scalar or ALP on shell, and a light mediator off shell. A report that covers one regime is incomplete — state which regimes were considered and why the others were dropped
- **The EFT is an interpretation tool, not the pipeline's Lagrangian.** Whatever the regime of the anomaly, the Lagrangian handed to the pipeline (Section 4) contains the explicit mediator unless the validity check of Section 7 passes for the simulated process
- **One state can sit in two regimes at once**: a few-GeV $Z'$ is a light mediator in $B$ decays and a low-mass Drell–Yan resonance at LHCb — treat each observable in its own regime

### 1.1 Heavy new physics: the EFT route

Work EFT-first in this regime.

1. **Identify the transition** at the quark/lepton level (e.g. $b \to c\tau\nu$, the $\mu \to \mu\gamma$ dipole; a collider resonance belongs to Section 1.3) and the relevant scale
2. **Write the effective Lagrangian** — low-energy EFT below the electroweak scale, SMEFT (Warsaw basis, arXiv:1008.4884; review arXiv:1706.08945) above it
3. **Extract from the data** (take fit results from a recent global fit in the literature, do not fit by eye):
   - size of the Wilson coefficient(s)
   - sign — constructive or destructive interference with the SM
   - Lorentz and chirality structure (V−A, scalar, tensor, dipole)
   - flavour structure (which generations; what must be suppressed)
4. **Convert to a scale**: $C/\Lambda^2$. For tree-level exchange with couplings $g_1, g_2$: $C/\Lambda^2 \sim g_1 g_2/M^2$. For a loop: $C/\Lambda^2 \sim g^4/(16\pi^2 M^2)$ — so loop explanations need light or strongly coupled states
5. **Read off the collider implication**: a large required $C/\Lambda^2$ means light mediators or large couplings, i.e. large production rates or broad resonances. This is what makes anomalies collider-testable

Worked example ($b \to c\tau\nu$, left-handed vector operator):

$$\mathcal{L}_\text{eff} = -\frac{4G_F}{\sqrt2} V_{cb}\,(1+\epsilon_L)\,(\bar c\gamma_\mu P_L b)(\bar\tau\gamma^\mu P_L\nu_\tau) + \text{h.c.}$$

A vector leptoquark $U_1\sim(3,1,\tfrac23)$ with couplings $\big[g_c(\bar c\gamma^\mu P_L\nu_\tau) + g_b(\bar b\gamma^\mu P_L\tau)\big]U_{1\mu} + \text{h.c.}$ gives, after a Fierz rearrangement, $\epsilon_L = \dfrac{g_c g_b^*\,v^2}{2V_{cb}M_{U_1}^2}$ at tree level, i.e. the anomaly fixes $\sqrt{|g_c g_b|}/M_{U_1}$ — a line in the coupling–mass plane that a collider search can cut. (Check of the term: $\bar c\,\nu\,U_1$ has charge $-\tfrac23+0+\tfrac23=0$ and colour $\bar3\otimes3\ni1$; with $U_1^\dagger$ instead it would be neither neutral nor a colour singlet — an easy slip, so always do this bookkeeping.) Always re-derive or look up such matching relations for the model at hand, check sign conventions against the source, and take running/QCD corrections to the matching (typically $\mathcal O(10\%)$) from a recent fit paper rather than ignoring them silently.

**Heavy mediator, light new final state.** The same procedure applies when a new light state appears in the final state while the mediator is heavy: write the operator with the light state as an explicit field — e.g. $\frac{C}{\Lambda^2}(\bar s\gamma_\mu P_Lb)(\bar\chi\gamma^\mu\chi)$ for $B\to K\chi\bar\chi$, or $\frac{c_{sb}}{f_a}\,\partial_\mu a\,(\bar s\gamma^\mu P_Lb)$ for $B\to Ka$ — taking the operator basis from that state's EFT literature (ALPs: arXiv:2012.12272, their flavour probes: arXiv:2110.10698). The data now fix $C/\Lambda^2$ **and** the light state's mass: read the mass off the kinematic spectrum (Section 1.2, point 1), not only off the rate. Opening the operator (Section 2.1) then puts the light state at one vertex of the mediator.

### 1.2 Light mediators and new light states: the light-state route

Here the new state is part of the kinematics, so the model-independent requirement is a **spectrum plus a coupling structure**, not a coefficient. Establish, before choosing a model:

1. **Kinematic window.** Which masses are allowed? On-shell production in a decay $P\to D\,X$ needs $M_X<m_P-m_D$ and gives a two-body final state: a monochromatic daughter, i.e. a peak at $q^2=M_X^2$. An excess localized in the daughter energy therefore points to a two-body decay, a broad excess to a three-body decay through an off-shell mediator or a contact operator. Thresholds matter: $X\to\chi\bar\chi$ needs $M_X>2m_\chi$; below it $X$ is off shell and the three-body spectrum is shaped by its propagator (formulas in Section 7)
2. **What the experiment actually fitted.** Signal strengths are extracted assuming a kinematic shape (the SM's, or a heavy-NP one). A light-state hypothesis has a different shape and a different efficiency, so the number to use is a **refit** of the binned data with the hypothesis' own spectrum — from the literature, or from the published bins and efficiency maps (HEPData). Quote both the refitted significance and the shape it assumes
3. **Spin, parity and coupling structure** from angular distributions, helicity suppression, and the pattern across related channels (e.g. $B\to KX$ versus $B\to K^*X$ separates vector from axial couplings to $\bar sb$)
4. **Required coupling versus mass**, from the on-shell rate (two-body), the full propagator (off shell), or the full one-loop function (a light state in a loop, Section 7). Present it as a band in the $(M,g)$ plane — this band, not a scale $\Lambda$, is what a search cuts into. For any other loop observable (meson mixing, EDMs, $K\to\pi\pi$, loop-induced kinetic mixing) take the full loop function from the portal literature, never the heavy-limit matching
5. **Fate of the state**: decay modes (visible, invisible, into a dark sector), width, and lifetime. A state explaining a missing-energy anomaly must decay invisibly or leave the detector; one explaining a visible anomaly must decay promptly enough to be seen. This decides the signature and whether the pipeline can simulate it (displaced decays cannot be — see the capability reference)
6. **Companion observables**: the portal that gives the state its couplings (Section 2.3) couples it to other SM currents too. Enumerate the rare decays ($K\to\pi X$, $B\to K^*X$, $Z\to\gamma X$, $h\to XX$), the fixed-target and $e^+e^-$ production modes, and the cosmological consequences ($N_\text{eff}$, BBN, supernova cooling) that a sub-GeV state entails — these are usually the decisive constraints (Section 6)

Worked example ($B^+\to K^+\nu\bar\nu$, where Belle II reported evidence above the SM in 2023, arXiv:2311.14647 — re-check the status before use): the heavy-regime reading is a shift of the operator $(\bar s\gamma_\mu P_Lb)(\bar\nu\gamma^\mu\nu)$. Because the excess is localized in the kaon energy, the data also admit the two-body reading $B\to KX$ with an invisible $X$, for which fits to the binned data prefer $M_X\approx2$ GeV (arXiv:2311.14629), and the three-body reading $B\to K\chi\bar\chi$ through a vector current, which fits prefer with $m_\chi\approx0.6$ GeV (arXiv:2312.12507) — both fits as of late 2023. For a light vector with $\mathcal L\supset Z'_\mu\,\bar s\gamma^\mu(g_LP_L+g_RP_R)\,b+\text{h.c.}$ the two-body rate is

$$\Gamma(B\to KZ')=\frac{|g_V|^2}{64\pi}\,\frac{m_B^3}{M_{Z'}^2}\,\lambda^{3/2}\,f_+^2(M_{Z'}^2),\qquad g_V=g_L+g_R,\quad\lambda=\lambda(1,\,m_K^2/m_B^2,\,M_{Z'}^2/m_B^2)\ \text{(Källén function, Section 7)},$$

with the $B\to K$ form factor $f_+$ from lattice QCD (arXiv:2311.14629, equation for $\Gamma^{(4)}_{B\to KZ'}$, which prints $f_+$ where the squared amplitude requires $f_+^2$ — re-derive before use; the check: only the vector current contributes to a $0^-\to0^-$ transition, and only the longitudinal $Z'$ polarization survives, which is the origin of the $1/M_{Z'}^2$). The axial combination $g_A=g_R-g_L$ dominates $B\to K^*Z'$ for a light $Z'$ (through its longitudinal, $1/M_{Z'}^2$-enhanced piece), and the $B\to K^*\nu\bar\nu$ bound then forces dominantly vectorial couplings (same source). The required $|g_V|$ is of order $10^{-8}$ (same source) — and a 2 GeV $Z'$ cannot decay through its $\bar sb$ coupling at all: every hadronic final state with that flavour content ($BK$, $\bar B_s\pi\pi$) lies above 5.5 GeV. It needs another coupling, to neutrinos or to a dark sector, to decay. That coupling, not $g_V$, fixes its width, lifetime and visibility, and is what other experiments probe. None of this is a Wilson coefficient: the rate scales as $1/M_{Z'}^2$ (longitudinal enhancement) and switches off at $M_{Z'}=m_B-m_K$.

### 1.3 Resonances and high-energy collider excesses: the explicit-mediator route

When the collider reaches the mass of the new state, the data *are* the state. Establish: mass and width (or an upper limit on the width — narrow versus broad), spin and CP from the production mode and angular distributions, the required $\sigma\times\text{BR}$ with the experiment's acceptance assumptions, and the pattern across channels (which final states show the excess, which exclude it). Write a **master simplified model** — the resonance with generic couplings to the initial and final states (loop-induced $gg$ and $\gamma\gamma$ couplings: [loop_induced_couplings.md](loop_induced_couplings.md)) — and list the distinct ways of obtaining the rate (production through gluons, quarks, vector bosons, or in association). If the state is broad ($\Gamma/M\gtrsim0.3$), drop the narrow-width approximation: simulate the full propagator with SM interference and scan the width as a parameter of its own — it is then an independent handle on the sum of the couplings. For a non-resonant tail, the explicit mediator is needed whenever a non-negligible fraction of the signal events has $\sqrt{\hat s}$ comparable to $M$: $s$-channel and $t$-channel exchange with the same low-energy operator give different tail shapes and interference patterns (arXiv:1704.09015 for dilepton tails; arXiv:1307.2253 for mono-jet dark-matter searches; arXiv:1604.06444 for the general argument), so the collider data select among mediators that the anomaly alone cannot distinguish.

### 1.4 When the anomaly is a dark-matter direct-detection signal

The EFT route of Section 1.1 applies, with a non-relativistic EFT in place of SMEFT (operator basis: arXiv:1203.3542, 1308.6288; reporting conventions and halo parameters: arXiv:2105.00599). Establish, before choosing particles:

1. **Kinematics.** For a nucleus of mass $m_N$ and reduced mass $\mu$: momentum transfer $q=\sqrt{2m_NE_R}$; elastic scattering needs $v_\text{min}=q/(2\mu)$, i.e. $E_R^\text{max}=2\mu^2v^2/m_N$; for $\chi_1N\to\chi_2N$ with splitting $\delta=m_2-m_1$ (inelastic dark matter, hep-ph/0101138): $v_\text{min}=\dfrac{|m_NE_R/\mu+\delta|}{\sqrt{2m_NE_R}}$, with threshold $v>\sqrt{2\delta/\mu}$ for $\delta>0$ (endothermic) and none for $\delta<0$ (exothermic). Compare with the fastest halo particles in the lab frame (≈ 750–800 km/s; take the halo parameters from arXiv:2105.00599)
2. **What the spectrum excludes.** Ordinary spin-independent scattering is coherent ($\propto A^2F^2(q)$) and falls steeply with $E_R$ — for xenon the form factor has its first zero near 100 keV. A signal at high recoil energy with nothing at low energy therefore rules out the standard interaction and requires a mechanism that removes low-energy recoils: endothermic or exothermic inelastic scattering, momentum- or velocity-dependent operators, or a non-halo (boosted) flux. Check what the experiment itself tested (operators, splittings, local significances) — read its paper at source depth
3. **Required rate**, as a cross-section band versus the mechanism's parameter ($\delta$, mass), from the experiment's own fit
4. **Target dependence and companions**: what the same model predicts in other targets (Ar, Ge, NaI, CaWO$_4$, F), in the experiment's other energy windows and sidebands, and in annual modulation
5. **Mediator mass versus momentum transfer**: if the mediator is lighter than $q$ (tens of MeV), the amplitude carries the propagator $1/(q^2+M^2)$, the recoil spectrum is pushed to low energies, and published contact-operator limits do not apply — recompute the rate with the full propagator (light-mediator regime, Section 1.2)

Useful exact statements: a quark vector-current operator $b_q\,\bar\chi\gamma^\mu\chi\,\bar q\gamma_\mu q$ gives nucleon couplings $b_p=2b_u+b_d$, $b_n=b_u+2b_d$ (no hadronic uncertainty) and, for a Dirac fermion, $\sigma_p=\mu_p^2b_p^2/\pi$. Self-conjugate dark matter (Majorana fermion, real scalar) has **no** vector current; when a Dirac fermion or complex scalar is split into two self-conjugate states, the vector current becomes purely off-diagonal — this is what makes a model inelastic, while its axial-current part stays diagonal and gives a correlated elastic spin-dependent signal. For spin-dependent and scalar-operator cross sections, take the formula and its Dirac/Majorana normalization from a cited source and state the convention — factors of 4 differ between papers.

The direct-detection rate itself (velocity integral × form factor × detector efficiency) is not computed by the pipeline's tools (Section 5 of the capability reference): it has to be supplied as a closed-form or scripted overlay, **calibrated against the experiment's published band** and used for shapes and scalings rather than absolute normalization unless that calibration succeeds.

## 2. From Requirement to Mediator

### 2.1 Tree-level mediators (heavy regime)

"Open" the operator: split its fields into two vertices in every possible way ($s$-, $t$-, $u$-channel pairings, including Fierz-related ones). The product of the SM representations at one vertex fixes the mediator's quantum numbers; the Lorentz structure of the bilinear fixes its spin.

Example: the bilinear $\bar Q_L\gamma^\mu L_L$ transforms as $(\bar 3, 1\oplus3, -\tfrac23)$, so it couples to a vector in $(3,1,\tfrac23)$ ($U_1$) or $(3,3,\tfrac23)$ ($U_3$).

The complete list of fields that contribute to dimension-6 operators at tree level is the "tree-level dictionary", arXiv:1711.10391. The most used entries:

**Colour singlets**

| Spin | Representations | Common names |
|------|-----------------|--------------|
| Scalar | $(1,1,0)$, $(1,1,1)$, $(1,1,2)$ | real singlet; singly / doubly charged singlet |
| Scalar | $(1,2,\tfrac12)$ | second Higgs doublet (2HDM, inert doublet) |
| Scalar | $(1,3,0)$, $(1,3,1)$ | real triplet; complex triplet (type-II seesaw) |
| Fermion | $(1,1,0)$, $(1,3,0)$ | sterile neutrino $N$ (type-I); triplet $\Sigma$ (type-III) |
| Fermion (vector-like) | $(1,1,-1)$, $(1,2,-\tfrac12)$, $(1,2,-\tfrac32)$, $(1,3,-1)$ | vector-like leptons |
| Vector | $(1,1,0)$, $(1,1,1)$, $(1,3,0)$ | $Z'$; $W'_R$-like singlet; $W'$ triplet (HVT) |

**Coloured**

| Spin | Representations | Common names |
|------|-----------------|--------------|
| Fermion (vector-like) | $(3,1,\tfrac23)$, $(3,1,-\tfrac13)$, $(3,2,\tfrac16)$, $(3,2,\tfrac76)$, $(3,2,-\tfrac56)$, $(3,3,\tfrac23)$, $(3,3,-\tfrac13)$ | vector-like quarks $T$, $B$, $(T,B)$, $(X,T)$, $(B,Y)$, triplets |
| Vector | $(8,1,0)$ | coloron / axigluon / KK gluon |
| Scalar LQ | $S_1(\bar3,1,\tfrac13)$, $\tilde S_1(\bar3,1,\tfrac43)$, $R_2(3,2,\tfrac76)$, $\tilde R_2(3,2,\tfrac16)$, $S_3(\bar3,3,\tfrac13)$ | scalar leptoquarks |
| Vector LQ | $U_1(3,1,\tfrac23)$, $\tilde U_1(3,1,\tfrac53)$, $V_2(\bar3,2,\tfrac56)$, $\tilde V_2(\bar3,2,-\tfrac16)$, $U_3(3,3,\tfrac23)$ | vector leptoquarks |

Leptoquark nomenclature follows arXiv:1603.04993. Several LQs ($S_1$, $\tilde S_1$, $S_3$, $V_2$, $\tilde V_2$) also admit diquark couplings that mediate proton decay — these must be forbidden by a symmetry (state it).

The same opening works for an operator that contains a new light field (heavy mediator, light new state): a vertex then joins a SM field to the light state. $(\bar s\gamma_\mu P_Lb)(\bar\chi\gamma^\mu\chi)$ opens into a heavy $s$-channel $Z'$ coupled to both currents, or into a $t$-channel colour-triplet scalar or fermion coupling $b\chi$ and $s\chi$ — the quark-portal ($t$-channel) mediators of the dark-matter literature (Section 3). The mediator's quantum numbers follow from the SM field and the light state at the vertex exactly as before.

### 2.2 Loop-level realizations

Needed when the operator is a dipole (always loop-induced in a renormalizable theory) or when all tree-level mediators are excluded. Typical structure: a new scalar + a new fermion running in the loop. Look for **chirality enhancement** (e.g. $m_t/m_\mu$ for $S_1$/$R_2$ leptoquarks, or a heavy vector-like lepton mass insertion in $(g-2)_\mu$) and for a **dark matter connection** (loop particles odd under a $Z_2$).

### 2.3 Light mediators and light new states: the portal catalogue

A state below the electroweak scale couples to the SM through one of a few **portals** — the renormalizable or lowest-dimension gauge-invariant operators that connect a SM-singlet state to SM fields. The portal fixes the coupling pattern across *all* SM currents, which is what makes these models predictive and heavily constrained. Enumerate by portal × spin × decay mode (visible / invisible / long-lived):

| Portal | Light state | Interaction | Couples to | Where it shows up | Entry points |
|---|---|---|---|---|---|
| Vector, kinetic mixing | dark photon $A'$ | $-\frac{\epsilon}{2\cos\theta_W}B_{\mu\nu}F'^{\mu\nu}$ | the electromagnetic current, $\epsilon eQ_f$; no tree-level flavour violation | $\pi^0/\eta\to\gamma A'$, $e^+e^-\to\gamma A'$, bremsstrahlung, low-mass Drell–Yan ($A'\to\ell\ell$), beam dumps | 2005.01515 (review), 0811.1030, 1801.04847 (translating limits between vector models) |
| Vector, gauged $U(1)'$ | $Z'$ of $L_\mu-L_\tau$, $B-L$, $B$, $L_i-L_j$, $B_3-L_3$, ... | $g'Z'_\mu J^\mu_X$, plus loop-induced kinetic mixing | the charges of the chosen current — $L_\mu-L_\tau$: $\mu,\tau,\nu_\mu,\nu_\tau$ only; $B-L$: all fermions; a flavour-violating $\bar sbZ'$ coupling needs extra ingredients (vector-like quarks that mix, or flavour-dependent charges) | $Z\to4\mu$, $e^+e^-\to\mu\mu Z'$, neutrino trident, $B\to K^{(*)}Z'$, $B_s$ mixing, invisible-$Z'$ searches | 1403.1269 (quark flavour), 1406.2332 (trident), 1808.03684 (CMS $Z\to4\mu$), 1705.06726 (anomalous currents) |
| Scalar (Higgs portal) | light scalar $\phi$ mixing with $h$ by $\sin\theta$ | $\mu\,\phi H^\dagger H$, $\lambda\,\phi^2H^\dagger H$ | all SM fermions $\propto m_f\sin\theta/v$; $b\to s\phi$ and $s\to d\phi$ at one loop through the top | $B\to K^{(*)}\phi$, $K\to\pi\phi$, $h\to\phi\phi$, beam dumps; $\phi\to\ell\ell/\pi\pi$, often displaced | 0911.4938, 1809.01876 |
| Pseudoscalar / ALP | $a$ | $\frac{c_{GG}\alpha_s}{4\pi f_a}aG\tilde G$, $\frac{c_{\gamma\gamma}\alpha}{4\pi f_a}aF\tilde F$, $\frac{c_{WW}\alpha_2}{4\pi f_a}aW\tilde W$, $\frac{\partial_\mu a}{f_a}\sum_f c_f\bar f\gamma^\mu\gamma_5f$ | gauge bosons and/or fermions; $b\to sa$ at one loop from $c_{WW}$ or $c_{tt}$ | $B\to K^{(*)}a$, $K\to\pi a$, $a\to\gamma\gamma/\ell\ell$, $h\to aa$, $Z\to\gamma a$, $pp\to a\to\gamma\gamma$ | 2012.12272 (EFT), 2110.10698 (flavour), 1708.00443 (colliders) |
| Neutrino portal | heavy neutral lepton $N$ | $y\,\bar L\tilde HN$, giving mixing $U_{\ell N}$ with $\nu_\ell$ | the weak currents, suppressed by $U_{\ell N}$ | meson decays $M\to\ell N$, $W/Z\to\ell N$, peak searches, displaced $N$ decays | 1805.08567 |
| Light dark matter through any of the above | $\chi$ (fermion or scalar) plus its mediator | $g_\chi$ to the mediator | via the mediator only | invisible final states: $B\to K\chi\bar\chi$, $e^+e^-\to\gamma\chi\bar\chi$, missing-energy beam dumps; relic density | 1901.09966 (benchmark portals BC1–BC11), 2305.01715, 2102.12143 |

Two things the portal fixes that a simplified model hides — check them before building: (i) **the coupling to every other SM current**, which carries the bulk of the constraints (a $Z'$ coupled to quarks for $B\to K$ also appears in $K\to\pi$, in $B_s$ mixing, and in low-mass Drell–Yan); (ii) **the mass origin** — a Stückelberg mass is available for a $U(1)'$ but not for a non-abelian group, and a dark Higgs brings its own states and its mixing with $h$. An **anomalous** $U(1)'$ (gauged $B$, a single $L_\ell$) is only consistent with spectator fermions that cancel the anomaly; their loops give the longitudinal $Z'$ enhanced couplings to $Z\gamma$ and $WW$, and hence strong flavour and $Z$-decay bounds (arXiv:1705.06726) — state the anomaly-cancelling sector.

Collider handles for light states, in the pipeline's reach: production in decays of heavy SM particles ($Z\to\mu\mu Z'$, $h\to XX$, $Z\to\gamma a$), final-state radiation off Drell–Yan leptons ($pp\to\mu\mu Z'$), low-mass Drell–Yan ($pp\to A'\to\mu\mu$ — LHCb, arXiv:1910.06926, which normalizes the signal to the observed $\gamma^*\to\mu\mu$ rate rather than to a parton-level cross section), and $e^+e^-\to\mu\mu Z'$ or $\gamma X$ at Belle II energies. The anomalous hadron decay itself ($B\to KX$) is never simulated — it enters as a closed-form overlay (Section 4).

Non-perturbative dark sectors (hidden valleys, dark showers, dark pions from $B$ or $Z$ decays) have no entry in this catalogue: they are outside the pipeline's reach — say so in the report instead of forcing a perturbative stand-in.

### 2.4 Resonances

For a state the collider produces directly, the quantum numbers follow from how it is produced and how it decays: gluon fusion favours colour-singlet spin-0 or spin-2 states coupled to gluons (through loops — [loop_induced_couplings.md](loop_induced_couplings.md)), $q\bar q$ annihilation a spin-1 colour singlet (or a spin-0 state with sizeable light-quark couplings), vector-boson fusion and $VX$ associated production a state with electroweak couplings, $b\bar b$- or $t\bar t$-associated production a heavy-flavour-philic scalar; Landau–Yang forbids a spin-1 state decaying to two photons. The UV origin supplies companions that a survey must list ($Z'$ with $W'$ in a left-right model, a singlet scalar inside a 2HDM + singlet, vector-like fermions that generate the loop couplings), and those companions are often more constrained than the resonance itself.

### 2.5 UV considerations

A massive vector mediator is either a gauge boson of an extended gauge group (then its couplings are constrained by gauge invariance and anomaly cancellation, and a symmetry-breaking sector exists) or a composite state. For the collider study a simplified model suffices, but state the intended UV origin and what it implies (e.g. "$U_1$ as a gauge boson of $SU(4)$ is accompanied by a $Z'$ and a coloron, which are typically more constrained").

## 3. Building Blocks by Purpose (Orientation)

| Purpose / anomaly class | Low-energy structure | Typical candidates | Typical collider handles | Entry point |
|---|---|---|---|---|
| $b\to c\tau\nu$ ($R_{D^{(*)}}$) | $(\bar c\Gamma b)(\bar\tau\Gamma\nu)$ | LQs $U_1$, $S_1$, $R_2$, $V_2$; historically also $W'$ and charged Higgs (strongly constrained — check current status) | $pp\to\tau\nu(+b)$, $pp\to\tau\tau$ high-mass tails; LQ pair/single production → $b\tau$, $t\nu$ | 1706.07808, 1603.04993; fit: 2405.06062 |
| $b\to s\ell\ell$ | $(\bar s\gamma_\mu P_Lb)(\bar\ell\gamma^\mu\ell)$ | $Z'$ (e.g. $L_\mu-L_\tau$); LQs $S_3$, $U_1$, $U_3$; loop models | $pp\to\ell\ell$ tails, $Z'\to\mu\mu$ (+$b$), LQ → $b\mu$ | 1706.07808, 1603.04993 |
| $(g-2)_\mu$ | dipole $\bar\mu\sigma^{\mu\nu}\mu F_{\mu\nu}$ (chirality flip); heavy regime: matching $\propto g^2m_\mu/(16\pi^2M^2)$; light regime ($M\lesssim$ GeV): full one-loop function (Section 7) | light $Z'$ ($L_\mu-L_\tau$, roughly $M\sim10$–200 MeV, decaying to neutrinos — re-check the surviving window), ALP, 2HDM, LQs with top-mass enhancement, vector-like leptons, scalar+fermion loops with DM | multi-muon final states ($Z\to4\mu$, $e^+e^-\to\mu\mu Z'$ at Belle II), neutrino trident, VLL pair production, muon collider | 2104.03691 (SM: 2006.04822, 2505.21476); light $Z'$: 0811.1030, 1406.2332, 1808.03684 |
| $B\to K^{(*)}+\text{invisible}$ ($B\to K\nu\bar\nu$ excess) | heavy: $(\bar s\gamma_\mu P_Lb)(\bar\nu\gamma^\mu\nu)$; heavy mediator + light DM: $(\bar s\Gamma b)(\bar\chi\Gamma\chi)$; light: $B\to KX$ (two-body, $M_X<m_B-m_K$) or $B\to K\chi\bar\chi$ through a light mediator ($q^2$-shaped) — the spectrum discriminates (Section 1.2) | leptoquarks with a $d\nu$ coupling ($S_1$, $S_3$, $\tilde R_2$, $V_2$, $U_3$ — not $U_1$ at tree level), heavy $Z'$; light $Z'$ (e.g. gauged $B_3-L_3$), light scalar, ALP, light DM pair | $B\to K^*+$inv (vector vs axial), $K\to\pi\nu\bar\nu$; LQ pair production → $b\nu b\nu$, $t\nu$; dedicated $B\to K^{(*)}X$ searches at Belle II; low-mass dimuon and missing-energy searches for the light mediator | 2311.14647 (Belle II), 2311.14629, 2312.12507 |
| Neutrino mass | Weinberg operator $(LH)(LH)/\Lambda$ | seesaw type I $N$, type II $\Delta(1,3,1)$, type III $\Sigma$; inverse seesaw; radiative (Zee, scotogenic) | same-sign dileptons + jets, $H^{\pm\pm}\to\ell^\pm\ell^\pm$, heavy-lepton pairs, $W_R\to\ell N$ | 1711.02180, hep-ph/0601225 |
| Dark matter | — | scalar singlet (Higgs portal), inert doublet, electroweak multiplets, $s$-channel mediator simplified models (vector/axial/scalar/pseudoscalar), $t$-channel (quark- or lepton-portal) mediators, dark photon; inelastic variants (pseudo-Dirac fermion, split complex scalar) of any of these | mono-$X$ + $E_T^\text{miss}$, mediator dijet/dilepton resonances, jets + $E_T^\text{miss}$ from coloured partners, disappearing tracks, invisible Higgs decays; plus relic density and direct detection | 1506.03116, 1306.4710, hep-ph/0603188, 2005.01515; $t$-channel: 2001.05024, 2307.10367, 2504.10597; inelastic: hep-ph/0101138 |
| New scalar resonance (e.g. $\gamma\gamma$, $\tau\tau$, $b\bar b$ excess) | coupling modifiers of a new spin-0 state ([loop_induced_couplings.md](loop_induced_couplings.md)) | singlet-like state of a 2HDM + singlet (N2HDM, NMSSM-like); type-I 2HDM (fermiophobic-leaning state); CP-odd state; triplets / Georgi–Machacek (charged-scalar loops); singlet + vector-like fermions (dilaton-like). Pure singlet–Higgs mixing rescales all rates by $\sin^2\theta$ and rarely suffices | $gg\to S\to\gamma\gamma/\tau\tau/VV$ (needs effective $SGG$, $S\gamma\gamma$ vertices), VBF/$VS$, production with companions ($H^\pm$, $H^{\pm\pm}$, vector-like quarks), $e^+e^-\to ZS$ | 1106.0034, 1612.01309; SM-like reference rates: 1610.07922 |
| Heavy resonance ($\ell\ell$, $\ell\nu$, $jj$, $VV$, $t\bar t$) | — | $Z'$ (sequential, $B-L$, $E_6$), $W'$, heavy vector triplet, KK graviton, coloron | Drell–Yan $\ell\ell$/$\ell\nu$, dijet, diboson | 0801.1345, 1402.4431 |
| Electroweak precision shift (e.g. $m_W$) | oblique $T$ (or $S$) | real triplet with vev, $Z'$ mixing, vector-like fermions, 2HDM mass splitting | pair production of the new electroweak states | 1711.10391 |
| Top / Higgs sector | — | vector-like quarks; top-philic scalars/vectors; FCNC $tqH$, $tqZ$ | single and pair VLQ production, $t\bar t+X$, four tops, $t\to qH$ | 1306.0572 |
| Light / feebly coupled states | the portals of Section 2.3 — no EFT among SM fields: the state is in the spectrum | ALP ($aG\tilde G$, $aF\tilde F$, $aW\tilde W$), dark photon, gauged-$U(1)'$ $Z'$, dark scalar, heavy neutral leptons, light DM | $pp\to a\to\gamma\gamma$, mono-$X$, exotic $Z$/$h$ decays, low-mass Drell–Yan, $e^+e^-$ at Belle II, displaced vertices (limited pipeline support) | 1901.09966 (benchmark portals), 2305.01715, 1708.00443, 2005.01515, 1805.08567, 1903.04497 |

Purposes with no direct collider handle (baryogenesis, strong CP, inflation, ...) need a collider-facing sector: identify which new states are light enough to be produced, and target those.

## 4. Writing a Pipeline-Ready Lagrangian

The Lagrangian you write is consumed by the feynrules-model-generator skill, which converts LaTeX into a FeynRules `.fr` file. It needs the following — ambiguity here is the main cause of downstream failures.

**Scope**
- Write **only the BSM part**; the SM is built into FeynRules
- Include kinetic and mass terms of new fields, and define the covariant derivative explicitly, including its sign convention — FeynRules uses $D_\mu=\partial_\mu-ig_sT^aG^a_\mu-\ldots$ — and which gauge fields act on the new field ("$U_1$ is a colour triplet with $Y=2/3$"). Gauge interactions from kinetic terms drive pair production
- For coloured vectors, write the non-minimal gluon coupling **as an explicit operator with its coefficient**, e.g. $-ig_s\,U_{1\mu}^\dagger T^aU_{1\nu}G^{a\mu\nu}$ for a gauge-boson-like (Yang–Mills) $U_1$, or state that it is absent (minimal coupling). Do not specify it through a "$\kappa$" value alone: papers use opposite conventions ($-ig_s\kappa$ with $\kappa=1$ for Yang–Mills, or $-ig_s(1-\kappa)$ with $\kappa=0$ for Yang–Mills), and its sign is tied to the sign convention of $D_\mu$

**Fields** — for each new field give: symbol; spin and type (real/complex scalar, Dirac/Majorana fermion, real/complex vector); $SU(3)_C$ representation; $SU(2)_L$ representation; $Y$; electric charge(s); whether it is self-conjugate; mass symbol and benchmark value; whether it decays (width computed automatically) or is stable
- Names: at least 2 characters, alphanumeric (e.g. `Zp`, `U1`, `N1`, `Snew`) — they become FeynRules class names
- $SU(2)_L$ multiplets: list each component as a separate field with its charge, and give the mass relation between components

**Basis**
- Preferred: a **simplified model in the mass basis after electroweak symmetry breaking**, written with SM mass eigenstates ($u,d,c,s,t,b,e,\mu,\tau,\nu_i$; $W^\pm, Z, A, G$; $h$), explicit flavour and explicit chirality projectors. This is the form of all shipped example prompts
- If you start from a gauge-invariant form, also give the expanded component form, and state the flavour basis (down-aligned / up-aligned) and where CKM elements appear
- **$SU(2)_L$ partners and CKM rotations are physics, not decoration.** A coupling to a left-handed doublet implies couplings of its partner components ($\bar b\tau$ comes with $\bar t\nu$), and the CKM rotation feeds a coupling into other generations ($\bar c\nu$, $\bar u\nu$ from $\bar s\nu$-type couplings). These open additional production and decay channels — valence-quark-initiated ones can dominate at colliders. Include them, or drop them explicitly with an estimate of the effect
- The pipeline builds the SM with a **diagonal CKM matrix** and massless light fermions by default (see the research-plan-generator skill's `references/pipeline_capabilities.md`). CKM factors that matter must therefore appear inside the BSM couplings as explicit numerical constants (with source)
- Mixing (e.g. singlet–Higgs, $Z$–$Z'$, heavy–light neutrino): write the interactions of the mass eigenstates with the mixing angle as an explicit parameter

**Couplings and structure**
- Declare every coupling real or complex, dimensionless or dimensionful (GeV), with a benchmark value
- Distinguish **free (external) parameters**, which will be scanned, from **derived (internal) parameters**, given as formulas of the free ones (e.g. $c_{c\nu}=V_{cs}\beta_{23}+V_{cb}$). Scans are set up on external parameters only
- Write "$+\,\text{h.c.}$" explicitly where needed — and only there (hermitian terms must not get it)
- Every term must be a Lorentz scalar, a colour singlet, and electrically neutral: check each monomial
- Loop-induced couplings must be written as effective operators with explicit coefficients, e.g. $\frac{c_g\,\alpha_s}{12\pi v}S\,G^a_{\mu\nu}G^{a\mu\nu}$ — the pipeline generates tree-level models only. State the origin and validity range of the coefficient; normalization, loop functions and caveats for a neutral spin-0 state: [loop_induced_couplings.md](loop_induced_couplings.md)
- EFT operators are a last resort for the pipeline, not a convenience: hand one over only when the explicit mediator is unknown or deliberately unspecified **and** the validity check of Section 7 passes for the simulated process. Then define $\Lambda$, state the mediator mass and couplings it stands for, and give the validity condition the plan must enforce. In every other case write the explicit mediator — a heavy-regime anomaly does not make the EFT valid at the collider, where $\sqrt{\hat s}$ can reach $M$

**Dark matter models** — mark every $Z_2$-odd field explicitly. Downstream (CalcHEP/micrOmegas) identifies the dark sector by a `~` prefix on particle names; you only flag which fields are odd (and suggest plain alphanumeric names as above) — applying the `~` convention is the model builder's job. If a tiny parameter is irrelevant for the pipeline (e.g. a keV-scale mass splitting at a collider or at freeze-out), say explicitly that it is dropped from the UFO model and where it enters instead (e.g. only the analytic direct-detection overlay), and that one field then stands for two nearly degenerate mass eigenstates.

**Light mediators and light new states** (masses below a few GeV) — the fields are declared like any other, with three additions:
- **Widths are fixed by hand**, with their source. MadGraph's automatic width is partonic and meaningless for a state below ~2 GeV that decays to hadrons (it decays to $\pi\pi$, $KK$, ..., with branching ratios from the $R$-ratio / vector-meson-dominance treatment of arXiv:1801.04847 or the model's own literature), and it is blind to invisible or dark-sector channels unless they are in the Lagrangian. Give the total width, the branching ratios used, and $\beta\gamma c\tau$ at the benchmarks (Section 7) together with the statement that decays are prompt
- **The anomalous process itself is usually not simulable.** Decays of $B$, $K$ and $\Upsilon$ mesons are hadronic: their rates enter as closed-form overlays with form factors from a cited source, validated against a published number (the helper-script rule in the skill's Output Paths section: assumptions in the script header, validation in the plan). What the pipeline simulates is the perturbative production of the same state (Section 2.3), so the Lagrangian must contain the couplings those processes need, with the portal relation to the anomalous coupling written out explicitly
- **Soft objects**: the pipeline's detector cards reconstruct no electrons or muons below $p_T=10$ GeV (capability reference, Section 3). Say how the decay products of a light state are to be analysed — at truth level with an assumed efficiency, or with a user-supplied card

## 5. Theory Consistency Checklist

- [ ] Every term gauge invariant under $SU(3)_C\times SU(2)_L\times U(1)_Y$ (hypercharges sum to zero) — or, for a mass-basis simplified model, invariant under $SU(3)_C\times U(1)_\text{em}$ with a stated gauge-invariant origin
- [ ] Lorentz invariant; hermitian
- [ ] Renormalizable, or explicitly an EFT with stated cutoff and validity range
- [ ] Gauge anomalies cancel (new chiral fermions; new $U(1)'$ charges — e.g. $B-L$ needs three $\nu_R$; $L_\mu-L_\tau$ is anomaly-free; vector-like fermions are safe)
- [ ] Massive vectors have a stated origin (broken gauge symmetry / composite)
- [ ] Regime consistent: the pipeline Lagrangian contains the explicit mediator, or the EFT's validity for the simulated process is demonstrated (Section 7)
- [ ] Light $U(1)'$: the gauged current is anomaly-free with the stated fermion content ($L_\mu-L_\tau$ is; $B-L$ with three $\nu_R$ is; gauged $B$ or a single $L_\ell$ is not — it needs spectator fermions, whose loops enhance the longitudinal $Z'$ couplings, arXiv:1705.06726); loop-induced kinetic mixing with the photon accounted for; mass origin stated (Stückelberg, or a dark Higgs with its own states and $h$ mixing)
- [ ] Couplings perturbative ($g\lesssim\sqrt{4\pi}$) and total width sensible ($\Gamma/M\lesssim 0.3$; narrow-width treatment needs $\Gamma/M\lesssim0.1$; a broader state is simulated with its full propagator and SM interference, never with the narrow-width approximation)
- [ ] Scalar potential bounded from below where a potential is part of the model
- [ ] Accidental symmetries respected: no proton decay (LQ diquark couplings), lepton/baryon number violation only where intended
- [ ] DM candidate neutral, colourless, and stabilized by a symmetry
- [ ] **Fate of every new state settled**: stable or decaying, through which channel, with what lifetime, and with what abundance today? A metastable partner can change the mechanism itself (an excited state that survives makes an "endothermic" model exothermic) or be excluded by late-decay limits — ask this before computing rates
- [ ] Free parameters counted; redundant ones removed

## 6. Experimental Constraint Checklist

Check each category that applies; quote bound, source, and date. A model that explains an anomaly but violates a precise measurement elsewhere is not a target.

| Category | Typical observables |
|----------|---------------------|
| Direct collider searches | resonance, pair-production, and non-resonant (high-$p_T$ tail) searches at ATLAS/CMS; LEP limits on light charged states |
| Flavour | meson mixing ($B_s$, $K$, $D$), $B\to K^{(*)}\nu\nu$, $B_c\to\tau\nu$, $\tau$ and $\mu$ LFV decays, $\mu\to e\gamma$, rare kaon decays — especially those generated by the *same* couplings that explain the anomaly |
| Electroweak precision | $S$, $T$; $Z$-pole couplings ($Z\to\ell\ell,\nu\nu,b\bar b$); $m_W$; lepton-flavour universality in $W$, $Z$, $\tau$ decays |
| Higgs | signal strengths, invisible width, exotic decays |
| Low energy | $(g-2)_{e,\mu}$, EDMs, atomic parity violation, neutrino trident production, neutrino scattering |
| Cosmology / astrophysics (light or stable states) | relic density, direct and indirect detection, $N_\text{eff}$, BBN, stellar cooling, supernova bounds |
| Light states (keV – few GeV), in detail | beam dumps and fixed-target experiments (electron and proton beams; kaon factories for $K\to\pi X$), $e^+e^-$ factories ($\gamma X$, $\mu\mu X$, invisible $X$ at BaBar / Belle II / KLOE), LHCb low-mass dimuon resonances (arXiv:1910.06926, prompt and displaced), $Z\to4\mu$ (arXiv:1808.03684), neutrino trident and CE$\nu$NS, exotic $h$ / $Z$ / meson decays; cosmology and astrophysics — $N_\text{eff}$ and BBN for states in thermal contact at $T\sim$ MeV, supernova (SN1987A) and stellar cooling. Dark-photon limits translate to other vector couplings only with the proper rescaling (arXiv:1801.04847) — never apply them blindly to a $Z'$ with different charges |
| Dark matter, in detail | what sets the relic density (and whether that coupling is compatible with the signal); elastic SI and SD limits, including loop-induced elastic scattering of inelastic models; the experiment's own other energy windows and sidebands; other targets; annual modulation; solar capture → neutrino telescopes (IceCube, Super-Kamiokande); indirect detection (dwarf galaxies, antiprotons, CMB energy injection; $s$- vs $p$-wave today); late decays of partner states (BBN, CMB, X-/γ-ray lines); collider limits on the mediator |
| Radiative effects | constraints generated at one loop by the required couplings (e.g. LQ contributions to $Z\to\tau\tau$, $\tau\to\mu\gamma$) |

## 7. Quick Estimates

Use these to choose benchmark points and scan ranges; label results `[estimate]`.

- **Two-body widths** (massless final-state fermions, coupling to one chirality):
  - vector $\to f\bar f'$ with coupling $g$: $\Gamma = C\,g^2M/(24\pi)$
  - scalar $\to f\bar f'$ with coupling $y$: $\Gamma = C\,y^2M/(16\pi)$
  - colour factor $C$ = (number of final-state colour combinations) / (dimension of the decaying particle's colour representation): $C=3$ for a colour singlet $\to q\bar q$ ($Z'$, $W'$), $C=1$ for a colour singlet $\to$ leptons **and for a leptoquark $\to q\ell$** (its colour fixes the quark's)
  - one massive daughter of mass $m$ (e.g. a mediator decaying to a quark and the dark matter particle): multiply by $(1-m^2/M^2)^2$
  - sum over open channels; check $\Gamma/M$ against Section 5
- **Dark matter**: unit conversions $1\,\text{GeV}^{-2}=3.894\times10^{-28}\,\text{cm}^2$, and $\times c$: $1.167\times10^{-17}\,\text{cm}^3/\text{s}$. Thermal freeze-out needs $\langle\sigma v\rangle\approx2.2\times10^{-26}$ cm³/s for self-conjugate dark matter above ~10 GeV (arXiv:1204.3622); for Dirac or complex dark matter the particle–antiparticle cross section must be twice that. $p$-wave annihilation ($\sigma v=bv^2$) is suppressed by $\langle v^2\rangle\approx6/x_f\approx0.25$ at freeze-out and by $\sim10^{-6}$ today — relic density from a larger coupling, indirect detection evaded. Coannihilation with a partner matters for mass gaps below roughly 10%. A splitting $\delta\ll T_f\approx m/25$ does not affect freeze-out
- **Narrow-width approximation**: $\sigma(pp\to X\to f)\simeq\sigma(pp\to X)\times\text{BR}(X\to f)$, valid for $\Gamma/M\lesssim0.1$ and away from thresholds
- **Coupling scaling**: resonant single production $\propto g^2$; $t$-channel exchange contributions to $pp\to f f'$ $\propto g^4$ (pure BSM) and $\propto g^2$ (interference); QCD pair production is coupling-independent. Knowing the scaling lets one simulation at a reference coupling cover a coupling scan
- **Event yield**: $N=\sigma\times\mathcal{L}\times A\times\epsilon$. Reference luminosities: LHC Run 2 ≈ 140 fb$^{-1}$ per experiment at 13 TeV; HL-LHC target 3 ab$^{-1}$ at 14 TeV. A target with $N\ll10$ signal events before cuts is not testable there
- **Initial-state flavour**: processes initiated by $b$, $c$, $s$ quarks are PDF-suppressed and need the heavy flavours included in the proton definition — flag this in the plan
- **EFT validity at a collider**: with the operator normalized as $\mathcal O/\Lambda^2$ (couplings absorbed into $\Lambda$), the physical cutoff of a tree-level-generated operator is the mediator mass $M=\Lambda\sqrt{g_1g_2}$, which lies *below* $\Lambda$ for $g_1g_2<1$ — so $\sqrt{\hat s}<\Lambda$ is not enough. The EFT reproduces the explicit mediator only for $\sqrt{\hat s}\ll M$: estimate, from the parton-level invariant-mass distribution of the final state, the fraction of signal events in the signal region with $\sqrt{\hat s}>M$ (arXiv:1307.2253 defines such a ratio for mono-jet searches; for $t$-channel exchange the expansion parameter is $|t|/M^2$, so $\sqrt{\hat s}$ is the conservative proxy); if it is not negligible, or the search's bins extend to $m\sim M$, simulate the explicit mediator. Mediators sharing one low-energy operator then differ — $s$-channel versus $t$-channel exchange gives different tail shapes and interference (arXiv:1704.09015, arXiv:1604.06444) — which is information, not a nuisance
- **Light vector in a loop** ($(g-2)_\ell$), for $\mathcal L\supset g'\,V_\mu\bar\ell\gamma^\mu\ell$:
  $$\Delta a_\ell=\frac{g'^2}{8\pi^2}\int_0^1dz\,\frac{2m_\ell^2\,z(1-z)^2}{m_\ell^2(1-z)^2+M_V^2\,z}\;\longrightarrow\;\begin{cases}g'^2/(8\pi^2) & M_V\ll m_\ell\\ g'^2m_\ell^2/(12\pi^2M_V^2) & M_V\gg m_\ell\end{cases}$$
  (arXiv:0811.1030, equation for $a_\ell^V$, with $\alpha\kappa^2\to g'^2/4\pi$ for a general coupling). The heavy limit is the EFT matching; the light limit saturates — the effect of a light mediator is set by its coupling alone, which is why the $(g-2)_\mu$ band in the $(M_V,g')$ plane turns flat below $M_V\sim m_\mu$. Scalar, pseudoscalar and axial-vector loop functions: arXiv:0902.3360 (one-loop signs for a neutral boson with flavour-diagonal couplings: scalar and vector positive, pseudoscalar and axial-vector negative; chirality-flipping or flavour-changing couplings can change them)
- **On-shell production in a decay** $P\to D\,X$ needs $M_X<m_P-m_D$ and gives $|\vec p_X|=\lambda^{1/2}(m_P^2,m_D^2,M_X^2)/(2m_P)$ in the parent's rest frame, with the Källén function $\lambda(a,b,c)=a^2+b^2+c^2-2ab-2ac-2bc$; a narrow $X$ populates a single $q^2$ bin, so the experiment's resolution and efficiency in that bin set the sensitivity. Off shell ($M_X$ above the kinematic limit, or $X\to\chi\bar\chi$ with $M_X<2m_\chi$) the three-body spectrum carries the factor $1/[(q^2-M_X^2)^2+M_X^2\Gamma_X^2]$
- **Decay length**: $c\tau=\hbar c/\Gamma=1.973\times10^{-16}\,\text{GeV·m}/\Gamma$; lab-frame length $L=\beta\gamma\,c\tau$ with $\beta\gamma=|\vec p\,|/M$. For a vector with vector coupling $g$ to one massless lepton flavour, $\Gamma(V\to\ell^+\ell^-)=g^2M/(12\pi)$ (both chiralities in the width formula above). Example `[estimate]`: $M_V=1$ GeV, $g=10^{-5}$ gives $\Gamma=2.7\times10^{-12}$ GeV and $c\tau=74\,\mu$m — prompt at rest, but $L\approx0.7$ mm at $\beta\gamma=10$, comparable to the impact-parameter cuts that define prompt leptons in LHC analyses; Delphes applies no displacement criterion, so the pipeline can neither reproduce such a selection nor model its efficiency loss. Quote $L$ at every benchmark of a weakly coupled state
