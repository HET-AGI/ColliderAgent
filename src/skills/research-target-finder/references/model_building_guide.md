# Model Building Guide

How to go from an anomaly or a purpose to a consistent, testable, pipeline-ready BSM model. The tables in this guide are for **orientation** — they tell you what to look for, not what is currently viable. Viability always comes from the literature search (see [literature_search.md](literature_search.md)).

Conventions: $Q = T_3 + Y$; representations are $(SU(3)_C, SU(2)_L, U(1)_Y)$; $v = 246$ GeV.

SM fields: $Q_L\,(3,2,\tfrac16)$, $u_R\,(3,1,\tfrac23)$, $d_R\,(3,1,-\tfrac13)$, $L_L\,(1,2,-\tfrac12)$, $e_R\,(1,1,-1)$, $H\,(1,2,\tfrac12)$.

## 1. From Anomaly to Operator

Work EFT-first. Before choosing particles, establish what the data demand.

1. **Identify the transition** at the quark/lepton level (e.g. $b \to c\tau\nu$, $\mu \to \mu\gamma$ dipole, $pp \to \gamma\gamma$ resonance at mass $m$) and the relevant scale
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

### When the anomaly is a dark-matter direct-detection signal

The same logic applies, with a non-relativistic EFT in place of SMEFT (operator basis: arXiv:1203.3542, 1308.6288; reporting conventions and halo parameters: arXiv:2105.00599). Establish, before choosing particles:

1. **Kinematics.** For a nucleus of mass $m_N$ and reduced mass $\mu$: momentum transfer $q=\sqrt{2m_NE_R}$; elastic scattering needs $v_\text{min}=q/(2\mu)$, i.e. $E_R^\text{max}=2\mu^2v^2/m_N$; for $\chi_1N\to\chi_2N$ with splitting $\delta=m_2-m_1$ (inelastic dark matter, hep-ph/0101138): $v_\text{min}=\dfrac{|m_NE_R/\mu+\delta|}{\sqrt{2m_NE_R}}$, with threshold $v>\sqrt{2\delta/\mu}$ for $\delta>0$ (endothermic) and none for $\delta<0$ (exothermic). Compare with the fastest halo particles in the lab frame (≈ 750–800 km/s; take the halo parameters from arXiv:2105.00599)
2. **What the spectrum excludes.** Ordinary spin-independent scattering is coherent ($\propto A^2F^2(q)$) and falls steeply with $E_R$ — for xenon the form factor has its first zero near 100 keV. A signal at high recoil energy with nothing at low energy therefore rules out the standard interaction and requires a mechanism that removes low-energy recoils: endothermic or exothermic inelastic scattering, momentum- or velocity-dependent operators, or a non-halo (boosted) flux. Check what the experiment itself tested (operators, splittings, local significances) — read its paper at source depth
3. **Required rate**, as a cross-section band versus the mechanism's parameter ($\delta$, mass), from the experiment's own fit
4. **Target dependence and companions**: what the same model predicts in other targets (Ar, Ge, NaI, CaWO$_4$, F), in the experiment's other energy windows and sidebands, and in annual modulation

Useful exact statements: a quark vector-current operator $b_q\,\bar\chi\gamma^\mu\chi\,\bar q\gamma_\mu q$ gives nucleon couplings $b_p=2b_u+b_d$, $b_n=b_u+2b_d$ (no hadronic uncertainty) and, for a Dirac fermion, $\sigma_p=\mu_p^2b_p^2/\pi$. Self-conjugate dark matter (Majorana fermion, real scalar) has **no** vector current; when a Dirac fermion or complex scalar is split into two self-conjugate states, the vector current becomes purely off-diagonal — this is what makes a model inelastic, while its axial-current part stays diagonal and gives a correlated elastic spin-dependent signal. For spin-dependent and scalar-operator cross sections, take the formula and its Dirac/Majorana normalization from a cited source and state the convention — factors of 4 differ between papers.

The direct-detection rate itself (velocity integral × form factor × detector efficiency) is not computed by the pipeline's tools (Section 5 of the capability reference): it has to be supplied as a closed-form or scripted overlay, **calibrated against the experiment's published band** and used for shapes and scalings rather than absolute normalization unless that calibration succeeds.

## 2. From Operator to Mediator

### Tree-level mediators

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

### Loop-level realizations

Needed when the operator is a dipole (always loop-induced in a renormalizable theory) or when all tree-level mediators are excluded. Typical structure: a new scalar + a new fermion running in the loop. Look for **chirality enhancement** (e.g. $m_t/m_\mu$ for $S_1$/$R_2$ leptoquarks, or a heavy vector-like lepton mass insertion in $(g-2)_\mu$) and for a **dark matter connection** (loop particles odd under a $Z_2$).

### UV considerations

A massive vector mediator is either a gauge boson of an extended gauge group (then its couplings are constrained by gauge invariance and anomaly cancellation, and a symmetry-breaking sector exists) or a composite state. For the collider study a simplified model suffices, but state the intended UV origin and what it implies (e.g. "$U_1$ as a gauge boson of $SU(4)$ is accompanied by a $Z'$ and a coloron, which are typically more constrained").

## 3. Building Blocks by Purpose (Orientation)

| Purpose / anomaly class | Low-energy structure | Typical candidates | Typical collider handles | Entry point |
|---|---|---|---|---|
| $b\to c\tau\nu$ ($R_{D^{(*)}}$) | $(\bar c\Gamma b)(\bar\tau\Gamma\nu)$ | LQs $U_1$, $S_1$, $R_2$, $V_2$; historically also $W'$ and charged Higgs (strongly constrained — check current status) | $pp\to\tau\nu(+b)$, $pp\to\tau\tau$ high-mass tails; LQ pair/single production → $b\tau$, $t\nu$ | 1706.07808, 1603.04993; fit: 2405.06062 |
| $b\to s\ell\ell$ | $(\bar s\gamma_\mu P_Lb)(\bar\ell\gamma^\mu\ell)$ | $Z'$ (e.g. $L_\mu-L_\tau$); LQs $S_3$, $U_1$, $U_3$; loop models | $pp\to\ell\ell$ tails, $Z'\to\mu\mu$ (+$b$), LQ → $b\mu$ | 1706.07808, 1603.04993 |
| $(g-2)_\mu$ | dipole $\bar\mu\sigma^{\mu\nu}\mu F_{\mu\nu}$ (chirality flip) | light $Z'$, ALP, 2HDM, LQs with top-mass enhancement, vector-like leptons, scalar+fermion loops with DM | multi-muon final states, VLL pair production, muon collider | 2104.03691 (SM: 2006.04822, 2505.21476) |
| Neutrino mass | Weinberg operator $(LH)(LH)/\Lambda$ | seesaw type I $N$, type II $\Delta(1,3,1)$, type III $\Sigma$; inverse seesaw; radiative (Zee, scotogenic) | same-sign dileptons + jets, $H^{\pm\pm}\to\ell^\pm\ell^\pm$, heavy-lepton pairs, $W_R\to\ell N$ | 1711.02180, hep-ph/0601225 |
| Dark matter | — | scalar singlet (Higgs portal), inert doublet, electroweak multiplets, $s$-channel mediator simplified models (vector/axial/scalar/pseudoscalar), $t$-channel (quark- or lepton-portal) mediators, dark photon; inelastic variants (pseudo-Dirac fermion, split complex scalar) of any of these | mono-$X$ + $E_T^\text{miss}$, mediator dijet/dilepton resonances, jets + $E_T^\text{miss}$ from coloured partners, disappearing tracks, invisible Higgs decays; plus relic density and direct detection | 1506.03116, 1306.4710, hep-ph/0603188, 2005.01515; $t$-channel: 2001.05024, 2307.10367, 2504.10597; inelastic: hep-ph/0101138 |
| New scalar resonance (e.g. $\gamma\gamma$, $\tau\tau$, $b\bar b$ excess) | coupling modifiers of a new spin-0 state (Section 7) | singlet-like state of a 2HDM + singlet (N2HDM, NMSSM-like); type-I 2HDM (fermiophobic-leaning state); CP-odd state; triplets / Georgi–Machacek (charged-scalar loops); singlet + vector-like fermions (dilaton-like). Pure singlet–Higgs mixing rescales all rates by $\sin^2\theta$ and rarely suffices | $gg\to S\to\gamma\gamma/\tau\tau/VV$ (needs effective $SGG$, $S\gamma\gamma$ vertices), VBF/$VS$, production with companions ($H^\pm$, $H^{\pm\pm}$, vector-like quarks), $e^+e^-\to ZS$ | 1106.0034, 1612.01309; SM-like reference rates: 1610.07922 |
| Heavy resonance ($\ell\ell$, $\ell\nu$, $jj$, $VV$, $t\bar t$) | — | $Z'$ (sequential, $B-L$, $E_6$), $W'$, heavy vector triplet, KK graviton, coloron | Drell–Yan $\ell\ell$/$\ell\nu$, dijet, diboson | 0801.1345, 1402.4431 |
| Electroweak precision shift (e.g. $m_W$) | oblique $T$ (or $S$) | real triplet with vev, $Z'$ mixing, vector-like fermions, 2HDM mass splitting | pair production of the new electroweak states | 1711.10391 |
| Top / Higgs sector | — | vector-like quarks; top-philic scalars/vectors; FCNC $tqH$, $tqZ$ | single and pair VLQ production, $t\bar t+X$, four tops, $t\to qH$ | 1306.0572 |
| Light / feebly coupled states | — | ALP ($aG\tilde G$, $aF\tilde F$, $aW\tilde W$), dark photon, heavy neutral leptons | $pp\to a\to\gamma\gamma$, mono-$X$, exotic $Z$/$h$ decays, displaced vertices (limited pipeline support) | 1708.00443, 2005.01515, 1903.04497 |

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
- Loop-induced couplings must be written as effective operators with explicit coefficients, e.g. $\frac{c_g\,\alpha_s}{12\pi v}S\,G^a_{\mu\nu}G^{a\mu\nu}$ — the pipeline generates tree-level models only. State the origin and validity range of the coefficient
- EFT operators: define $\Lambda$ and state the validity condition ($\sqrt{\hat s}\ll\Lambda$)

**Dark matter models** — mark every $Z_2$-odd field explicitly. Downstream (CalcHEP/micrOmegas) identifies the dark sector by a `~` prefix on particle names; you only flag which fields are odd (and suggest plain alphanumeric names as above) — applying the `~` convention is the model builder's job. If a tiny parameter is irrelevant for the pipeline (e.g. a keV-scale mass splitting at a collider or at freeze-out), say explicitly that it is dropped from the UFO model and where it enters instead (e.g. only the analytic direct-detection overlay), and that one field then stands for two nearly degenerate mass eigenstates.

## 5. Theory Consistency Checklist

- [ ] Every term gauge invariant under $SU(3)_C\times SU(2)_L\times U(1)_Y$ (hypercharges sum to zero) — or, for a mass-basis simplified model, invariant under $SU(3)_C\times U(1)_\text{em}$ with a stated gauge-invariant origin
- [ ] Lorentz invariant; hermitian
- [ ] Renormalizable, or explicitly an EFT with stated cutoff and validity range
- [ ] Gauge anomalies cancel (new chiral fermions; new $U(1)'$ charges — e.g. $B-L$ needs three $\nu_R$; $L_\mu-L_\tau$ is anomaly-free; vector-like fermions are safe)
- [ ] Massive vectors have a stated origin (broken gauge symmetry / composite)
- [ ] Couplings perturbative ($g\lesssim\sqrt{4\pi}$) and total width sensible ($\Gamma/M\lesssim 0.3$; narrow-width treatment needs $\Gamma/M\lesssim0.1$)
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
- **EFT validity**: if the study uses an EFT, the events populating the signal region must satisfy $\sqrt{\hat s}<\Lambda$; otherwise use the explicit mediator

### Loop-induced couplings of a neutral spin-0 state

The pipeline is tree-level, so $Sgg$ and $S\gamma\gamma$ couplings must be supplied as effective operators. Fix the normalization as follows ($v=246$ GeV; $\tilde X^{\mu\nu}=\tfrac12\epsilon^{\mu\nu\rho\sigma}X_{\rho\sigma}$):

$$\mathcal{L}_\text{eff}^{S} = c_g\frac{\alpha_s}{12\pi v}\,S\,G^a_{\mu\nu}G^{a\mu\nu} + c_\gamma\frac{\alpha}{8\pi v}\,S\,F_{\mu\nu}F^{\mu\nu},\qquad \mathcal{L}_\text{eff}^{A} = \tilde c_g\frac{\alpha_s}{8\pi v}\,A\,G^a_{\mu\nu}\tilde G^{a\mu\nu} + \tilde c_\gamma\frac{\alpha}{8\pi v}\,A\,F_{\mu\nu}\tilde F^{\mu\nu}$$

- Widths at LO: $\Gamma(S\to\gamma\gamma)=\dfrac{\alpha^2m^3|c_\gamma|^2}{256\pi^3v^2}$ (same for $A$ with $\tilde c_\gamma$); $\Gamma(S\to gg)=\dfrac{\alpha_s^2m^3|c_g|^2}{72\pi^3v^2}$; $\Gamma(A\to gg)=\dfrac{\alpha_s^2m^3|\tilde c_g|^2}{32\pi^3v^2}$
- Coefficients from SM particles in the loop, with coupling modifiers $\kappa_i$ relative to an SM Higgs and $\tau_i=m^2/(4m_i^2)$:
  $c_g=\tfrac34\sum_q\kappa_qA_{1/2}(\tau_q)$, $\quad c_\gamma=\sum_fN_cQ_f^2\kappa_fA_{1/2}(\tau_f)+\kappa_VA_1(\tau_W)$, $\quad\tilde c_g=\tfrac12\sum_q\tilde\kappa_qA^A_{1/2}(\tau_q)$, $\quad\tilde c_\gamma=\sum_fN_cQ_f^2\tilde\kappa_fA^A_{1/2}(\tau_f)$
- Loop functions (conventions of hep-ph/0503172, hep-ph/0503173), with $f(\tau)=\arcsin^2\sqrt\tau$ for $\tau\le1$ and $f(\tau)=-\tfrac14\big[\ln\tfrac{1+\sqrt{1-1/\tau}}{1-\sqrt{1-1/\tau}}-i\pi\big]^2$ for $\tau>1$:
  $A_{1/2}=2[\tau+(\tau-1)f]/\tau^2$, $\;A_1=-[2\tau^2+3\tau+3(2\tau-1)f]/\tau^2$, $\;A_0=-[\tau-f]/\tau^2$, $\;A^A_{1/2}=2f/\tau$.
  Heavy-loop limits ($\tau\to0$): $A_{1/2}\to\tfrac43$, $A_1\to-7$, $A_0\to\tfrac13$, $A^A_{1/2}\to2$. So a heavy top gives $c_g=\kappa_t$, $\tilde c_g=\tilde\kappa_t$; and the $W$ and top loops interfere destructively in $c_\gamma$ (SM Higgs at 125 GeV: $c_\gamma\approx-6.5$)
- New heavy particles ($m\ll2M$): a vector-like fermion with coupling $-y_FS\bar FF$, mass $M_F$, charge $Q$, colour multiplicity $N_c$ adds $\delta c_\gamma=\tfrac43N_cQ^2\,y_Fv/M_F$, and $\delta c_g=y_Fv/M_F$ if it is a colour triplet; a charged scalar with coupling $-g\,S\,H^+H^-$ ($g$ in GeV) adds $\delta c_\gamma=\dfrac{g\,v}{2m_{H^\pm}^2}A_0(\tau_{H^\pm})$
- Evaluate the loop functions numerically at the mass in question and quote the result as an `[estimate]`; check the normalization against the source when a paper uses a different operator basis

Caveats for light scalars produced through these operators:
- LO gluon fusion through the effective vertex underestimates the rate by a factor of roughly 2–3. Do not quote LO cross sections: normalize to the SM-like reference cross section at that mass (LHC Higgs Working Group, arXiv:1610.07922) times $|c_g/c_g^\text{SM-like}|^2$, or to the experiment's own reference rate
- A $2\to1$ process has no transverse momentum at matrix-element level; observables that depend on the resonance $p_T$ or on recoil jets are unreliable without jet matching
- Automatically computed widths are LO and contain only the channels present in the model (light-quark Yukawas may be absent). For rates, prefer $\sigma\times\text{BR}$ built from reference branching ratios rescaled by the coupling modifiers
