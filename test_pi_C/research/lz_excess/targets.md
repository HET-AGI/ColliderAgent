# Research Targets: New models for the LZ 248 keV nuclear-recoil event

- **Study label**: `lz_excess`
- **Date**: 2026-09-21
- **Mode**: A. Model building (new constructions requested by the user), with a brief map of the existing explanations (B) to position them
- **Literature access**: partial — INSPIRE, arXiv and HEPData APIs worked; the HEPData data release of the LZ paper itself (doi:10.17182/hepdata.182472.v1, announced in the arXiv comment of [1]) did **not resolve** on 2026-09-21 (DOI: HTTP 404; `record/182472`: HTTP 403; `record/ins3199115`: HTTP 404). All LZ confidence intervals below are therefore read off the paper's figures by eye and are marked as such.

<!-- Evidence labels used in this report:
     (untagged)    backed by a reference in Section 7, verified in this session
     [estimate]    own estimate; formula given
     [assumed]     a choice made where no source fixes the value
     [unverified]  a fact from memory or from a source that could not be checked -->

## 1. Problem Statement

### 1.1 User goal (verbatim)

> Please also test it by considering the recent LZ expreiment results on dark matter. At least, construct two new models which have never been considered to expain the LZ excess.

### 1.2 Interpretation

- **Physics question**: LZ reported (arXiv 2026-09-02) one nuclear-recoil-like event at $E_R = 248$ keV in an extended-energy search, 2.6σ global. Which particle-physics models that have *not yet been proposed for this event* can produce it, without being excluded by what LZ and others did **not** see — and which of them can the collider pipeline test?
- **Success criterion**: a model counts as a target if (i) it predicts $\mathcal O(1)$ event at $E_R\sim 200$–270 keV in 2.84 t yr of xenon with $\lesssim$ few events at lower energies, i.e. it falls inside LZ's own two-sided 90% CL interval for a tested signal class; (ii) it is theoretically consistent; (iii) it survives the constraints that matter for it (LZ low-energy limits, solar capture/IceCube, indirect detection, LHC); (iv) it is absent from the literature on the event as of 2026-09-21.
- **Boundary conditions**: at least two new constructions (user); exactly one plan, for the top-ranked new model (main agent); ~35–45 lookups, 3 source downloads (main agent). No collider preference given by the user.
- **Assumptions made on the user's behalf**:
  1. "The LZ excess" = the single 248 keV event of arXiv:2609.02823 [1]. (The other recent LZ result, the 5.7 t yr low-mass search of arXiv:2512.08065, reports no dark-matter excess — its abstract says the $^8$B CEνNS signal is "consistent with expectation".)
  2. "Never been considered to explain the LZ excess" is read as: *not proposed as an interpretation of this event* in any paper found by the searches logged in the Appendix. It is **not** read as "every ingredient is unknown to physics" — that would be impossible to satisfy honestly: both new constructions below are built from known simplified-model building blocks, and this is stated in each Origin line.
  3. Since the pipeline is a collider pipeline, new models with an LHC-testable mediator are preferred over purely dark-sector ones.
  4. Dark matter is assumed to make up the full local density; the Standard Halo Model is used for all rates.

### 1.3 Current status

Excess in a search (bump, tail, or event count):

| Search (experiment, channel, exposure) | Location | Local (global) significance | Observed (expected) / fitted signal | Source (paper, HEPData) | As of |
|---|---|---|---|---|---|
| LZ, single-scatter nuclear recoils, extended window S1$c$ 3–600 phd (NR efficiency > 50% for 5.4–269.9 keV, 96% on average for 14–250 keV); 220 live days × 4.71 t = 2.84 t yr; data 2023-03-27 to 2024-04-01 | one event, $E_R = 248 \pm 23\,(\text{stat}) \pm 23\,(\text{sys})$ keV (S1$c$ = 540.1 phd, S2$c$ = 9268 phd), recorded 2023-06-16 21:22:39 UTC; 1.5σ below the NR-band median, 6.7σ below the ER-band median; 26.9 cm from the true TPC wall | max. local 3.4σ over the models tested (2.6σ global) | background in the event's S1$c$ slice: $0.0106 \pm 0.0008$ counts (Fig. 5, bottom panel); fitted signal $1.0^{+1.4}_{-0.7}$ events for $\mathcal L_{10}^s$ at 1 TeV (Table I); total 1710 observed vs $1713 \pm 39$ fitted (ER-dominated) | [1] (depth: source). HEPData: announced, **not accessible** (see header) | 2026-09-02 |

How solid is it? One event. LZ itself calls the analysis **non-blind**: the salting did not cover the high-energy signal region [1]. The event came 25 minutes after a $^{57}$Co calibration source was withdrawn (opposite side of the detector), the radon tag could not be applied (mixed-flow state), and the S1 pulse shape "does not allow for conclusive ER–NR discrimination" [1]. LZ examined accidentals, atmospheric neutrinos, MSSI events and neutrons and found none likely: each would come with a larger population that is not seen [1]. No independent confirmation exists: XENONnT's 2.1 t yr search for inelastic dark matter (a nuclear recoil followed by a delayed de-excitation photon — a different topology) found data consistent with background [3]; no extended-window nuclear-recoil result from XENONnT or PandaX-4T was found (INSPIRE query #18 of the Appendix, 2026-09-21). What will settle it: LZ's remaining exposure (the 1000-live-day goal is quoted in [12]), and extended-window analyses of existing XENONnT/PandaX-4T data [12].

The theory response has been extremely fast: 77 INSPIRE citations and ≥ 83 arXiv papers on the event in 19 days (Appendix #5, #10, #11). This is what makes "never considered" a demanding claim, and why the novelty check below is built on the full citing list rather than on keyword searches.

### 1.4 What the data require

Model-independent requirements, before any model is chosen:

1. **Kinematics.** $q = \sqrt{2 m_{\rm Xe} E_R} \simeq 246$ MeV [estimate; $m_{\rm Xe} = 131\times0.9315$ GeV]. Elastic halo scattering needs $v_{\min} = q/(2\mu_{\chi \rm Xe}) < v_{\rm esc}+v_E \approx 800$ km/s, i.e. $m_\chi \gtrsim 80$–100 GeV [estimate]; LZ's table confirms: all local significances are 0.0–0.1σ for $m_\chi \le 50$ GeV [1, Table S-II].
2. **The ordinary SI interaction fails**: $\mathcal L_1^s$ and $\mathcal L_5^s$ have 0.0σ at every mass [1]. Reason: the coherent form factor. Helm $F^2$ for $^{131}$Xe is 0.056 at 50 keV, $1.8\times10^{-4}$ at 100 keV (first zero ≈ 94 keV), $1.6\times10^{-3}$ at 200 keV (second lobe) and $1.7\times10^{-4}$ at 248 keV [estimate, `tools/idm_rate.py`] — an SI signal normalised to one event at 248 keV would give hundreds at low energy. Any explanation must remove the low-energy recoils.
3. **Generic ways of doing so** (all tested by LZ, local significance at $m_\chi = 1$ TeV from [1], Tables S-II/S-III):
   - *endothermic* (inelastic up-scattering, splitting $\delta$): $\mathcal O_1^s$: 0.8σ (δ = 100 keV), 2.2σ (150), 2.7σ (200), 2.9σ (250), 3.0σ (300), 3.3σ (350); $\mathcal O_1^v$ and $\mathcal O_4$ are at 2.6–3.4σ already for δ ≥ 100 keV;
   - *elastic spin-dependent or momentum-dependent* operators with a heavy WIMP: $\mathcal O_4$ 2.7σ, $\mathcal L_4$ (pseudoscalar–pseudoscalar) 3.1σ, $\mathcal L_6^v$ 3.3σ, $\mathcal L_{10}$ (dipole–dipole) 3.4σ;
   - not tested by LZ but proposed since: *exothermic* down-scattering, boosted (non-halo) fluxes, exotic nuclear processes (Section 2).
4. **Required rate for the coherent endothermic case.** LZ's two-sided 90% CL interval on the DM–nucleon cross section for inelastic $\mathcal O_1^s$ ([1], Fig. S7; the mass is not restated in the caption — taken to be the 1 TeV of Fig. 6 [assumed]), **read off by eye, ±30%**:

| δ [keV] | 150 | 200 | 250 | 300 | 350 |
|---|---|---|---|---|---|
| lower edge [cm²] | $1.3\times10^{-45}$ | $1.2\times10^{-44}$ | $8\times10^{-44}$ | $3.5\times10^{-43}$ | $4\times10^{-41}$ |
| upper edge [cm²] | $2.0\times10^{-44}$ | $1.7\times10^{-43}$ | $1.1\times10^{-42}$ | $7.5\times10^{-42}$ | $6.5\times10^{-40}$ |

   Cross-check with an independent box-efficiency rate code (`tools/idm_rate.py`, Helm form factor, SHM): the lower edges correspond to 0.5–1.0 and the upper edges to 9–16 events in the full window [estimate] — the code reproduces the δ-dependence of LZ's band over five orders of magnitude; its absolute normalisation is a factor ~2–4 above what a one-event Poisson interval would give, as expected from the missing detector response and the Helm approximation in the second lobe. The code is used below only for *shapes* and for mass scaling; LZ's band sets the normalisation.
5. **Spectral shape to keep in mind** [estimate, same code, $m_\chi$ = 1 TeV]: for δ = 300 keV only 23% of the window events fall at 200–270 keV and 77% at 70–200 keV (the second Helm lobe peaks near 170 keV); for δ = 350 keV the split is 67%/33% but 0.9 events are predicted *above* the window per event inside — the origin of the "empty high-energy sideband" tension of [9].
6. **Constraints every endothermic explanation faces**: (a) solar capture — the Sun accelerates DM to ~1400 km/s, so up-scattering on heavy solar elements is open; for a thermal Higgsino annihilating to $WW/ZZ$ IceCube requires δ > 566 keV, excluding the LZ interpretation [8] (confirmed by other groups, e.g. δ ≳ 557 keV with Super-K + IceCube, arXiv:2609.07807, and [28]); the bound is on *that* model — it weakens with the cross section, with soft annihilation channels [41] and when the captured population cannot thermalise [28]; (b) the empty sideband above the window [9, 12]; (c) exponential sensitivity to the halo tail — the predicted count changes from 0 to 143× its central value as $v_{\rm esc}$ runs from 500 to 600 km/s for splittings near the kinematic ceiling [14]; (d) a large annual modulation peaking in early June [11] (the event date, 16 June, is compatible).

**Shared inputs for estimates**: SHM with $\rho = 0.3$ GeV/cm³, $v_0 = 238$ km/s, $v_{\rm esc} = 544$ km/s, $v_E = 254$ km/s (267 in June) — values recalled from the conventions paper [38] that LZ cites; **[unverified]** numerically (only the title of [38] was checked). Helm form factor with $s = 0.9$ fm, $a = 0.52$ fm, $c = 1.23A^{1/3}-0.6$ fm [39] **[unverified]** numerically. Exposure 2.84 t yr, efficiency box 0.96 on 5.4–269.9 keV [1] (box shape [assumed]). Canonical thermal cross section $2.2\times10^{-26}$ cm³/s [37] (the number is in the part of the abstract of [37] beyond what was printed in this session — **[unverified]**). LZ 4.2 t yr limits at $m_\chi$ = 1 TeV: $\sigma_{\rm SI} < 3.0\times10^{-47}$ cm², $\sigma_{\rm SD}^n < 5.0\times10^{-42}$ cm² (500 GeV: $1.5\times10^{-47}$, $2.6\times10^{-42}$) — log-log interpolation of the HEPData tables of [2], files `data/ins2841863_SI_cross_section.csv`, `data/ins2841863_SDn_cross_section.csv`. Nucleon spin fractions $\Delta u^p = 0.842$, $\Delta d^p = -0.427$, $\Delta s = -0.085$ (micrOMEGAs defaults, from memory) **[unverified]**. Conversions: 1 GeV⁻² = $3.894\times10^{-28}$ cm² = $1.167\times10^{-17}$ cm³/s.

## 2. Model Landscape

A brief map of the explanations already in the literature, to position the new constructions. All entries were read at abstract depth unless stated; the variant lists are by arXiv ID.

| Class | New state(s) | Mechanism | Addresses goal via | Status | Characteristic collider signature | Key refs | Variants (by reference) |
|---|---|---|---|---|---|---|---|
| Higgsino / electroweak-doublet inelastic DM | pseudo-Dirac doublet fermion $(1,2,\tfrac12)$, $m\approx1.1$ TeV, δ ≈ 350–490 keV | tree-level off-diagonal $Z$ exchange, $\sigma_n^Z\simeq1.9\times10^{-39}$ cm² fixed | endothermic, halo tail | **excluded as a thermal relic** by solar capture (δ > 566 keV needed) [8]; tension with empty sideband [9] | disappearing tracks / soft tracklets | [6], [7], [8], [9] | 2609.01590, 2609.01892, 2609.04163, 2609.09385, 2609.07811, 2609.08712, 2609.06750, 2609.02807, 2609.11241, 2609.15321, 2609.07807, 2609.11833, 2609.09830 |
| Other electroweak multiplets with off-diagonal $Z$ | inert doublet, singlet–doublet scalar/fermion, scotogenic, sneutrino, Higgs-coupled minimal DM, mixing-suppressed singlet–doublet, asymmetric singlet–doublet | off-diagonal $Z$, rate reduced by mixing | endothermic | constrained (solar capture model by model [28]; 2609.19174) | electroweak pair production, compressed spectra | [25], [26] | 2609.06571, 2609.07451, 2609.07800, 2609.13038, 2609.15027, 2609.15742, 2609.02505, 2609.18564, 2609.08808 |
| $Z'$ / dark-photon mediated inelastic DM | pseudo-Dirac fermion or split scalar + $s$-channel vector: $U(1)_B$, $B-L$, chiral $B-L$, $B-3L_\tau$, $B_i-B_j$, $q_1-q_2$, hidden $U(1)$, dark photon, KK $Z'$ | tree-level off-diagonal vector current | endothermic (several also exothermic) | viable / constrained | dijet and dilepton resonances | [15], [16] | 2609.09015, 2609.15600, 2609.10827, 2609.10636, 2609.06171, 2609.15714, 2609.13130, 2609.09136, 2609.07138, 2609.06640, 2609.02868 |
| Generic endothermic fits | — | EFT | fits of $(m_\chi,\delta)$, modulation, isotope effects | — | — | [10], [11], [27] | 2609.01475, 2609.10491, 2609.15634, 2609.14799 |
| Exothermic DM | metastable excited state, δ ≈ 0.3–1 MeV, GeV-scale dark mediator | down-scattering, no velocity threshold | recoil peak set by δ | viable; needs a cosmologically stable excited state and a leptophobic mediator [12] | dark-photon searches; argon predicts a line [14] | [12], [13], [14] | 2609.15782, 2609.17935, 2609.17412 |
| Axion / pseudoscalar portal | Dirac DM + light pseudoscalar $a$ (1–10 GeV) | elastic $\mathcal L_4$, rate ∝ $q^4$ | momentum dependence | viable | $a$ production, 2HDM+$a$ searches | [18] | 2609.17196, 2609.08893, 2609.17412 |
| Dipole interactions | transition magnetic dipole; magnetic inelastic dark baryons | photon exchange, spin-dependent response | endothermic + delayed photon | constrained (γ-ray lines [20]) | dark mesons | [19], [20] | — |
| Elastic spin-dependent | singlet–doublet Majorana on the Higgs blind spot | diagonal axial $Z$ coupling → $\mathcal O_4$ | hard SD response | constrained: LZ SD-$n$ limit and IceCube each remove part of the region (source-level reading of [17]) | soft leptons + $E_T^{\rm miss}$ | [17] | — |
| Boosted / non-halo dark particles | light DM + boost mechanism | elastic, often momentum-dependent | flux not tied to the halo tail | viable | — | [21] | 2609.07742, 2609.06756, 2609.11600, 2609.14799 |
| Exotic nuclear processes | neutron (pair) disappearance, fermionic DM absorption, neutrino up-scattering | — | line or threshold spectra | absorption benchmark excluded by KamLAND [24]; elastic-neutrino origins excluded (2609.10504) | — | [22], [23], [24] | 2609.12045, 2609.15933 |
| **Quark-portal ($t$-channel, coloured-mediator) dark matter** | DM singlet + coloured $Z_2$-odd partner | tree-level exchange of the coloured partner | endothermic (T1), exothermic (T2), elastic SD (T3) | **not found in the literature on the event** → Section 3 | jets + $E_T^{\rm miss}$ | [29] | — |
| No new physics | — | — | rare background topology (MSSI, neutron, accidental), unmodelled detector effect, or fluctuation in a non-blind analysis | open | more LZ exposure; extended-window analyses by XENONnT/PandaX-4T | [1] | — |

**Coverage statement**: the map is built from (i) the complete INSPIRE citing list of [1] (77 records, all abstracts read via one arXiv batch call), (ii) two arXiv listing searches on the abstract text (53 and 77 hits), which surfaced six further papers not yet linked on INSPIRE (2609.13130, 2609.11241, 2609.10662, 2609.02994, 2609.01592 and the LZ paper). The newest arXiv entry returned by either search is dated 2026-09-16; papers submitted on 17–21 September may exist and were **not** seen. There is no review yet; the closest to a cross-check is the model-independent inference of [27], whose classification (tuned endothermic, exothermic, momentum-suppressed/spin-dependent elastic) matches rows 1–8. Everything is read at abstract depth except [1], [17] and [29] (source).

## 3. Candidate Targets

**The gap.** Going through the tree-level ways of generating an off-diagonal vector current with a coherent coupling to nuclei — $s$-channel $Z$ (done), $s$-channel $Z'$/dark photon (done many times), dipole (done), $t$-channel coloured partner — the last one is absent from all ≥ 83 papers: no abstract contains "$t$-channel", "squark", "colo(u)red mediator" (the only "vector-like quarks" are those generating flavour mixing in 2609.06171, not a DM mediator), and two INSPIRE full-text queries returned nothing relevant (Appendix #19, #20). The class comes in two spin assignments, which turn out to behave very differently for this event; a third member realises a different detection mechanism. T1–T3 share the field content of the standard $t$-channel simplified models [29]: the UFO models differ only in the spin of the two new fields.

There is a physics reason to look here beyond novelty. [29] finds that thermal $t$-channel models with *complex* (non-self-conjugate) dark matter are "excluded by cosmology and astrophysics alone", the killer being the tree-level vector interaction with nuclei. A Majorana (or soft $U(1)_D$-breaking) mass of a few hundred keV — a $3\times10^{-7}$ perturbation — makes exactly that interaction inelastic: the models are resurrected, and the *one* place where they must show up is a high-energy recoil search in a heavy target.

### T1: Quark-portal pseudo-Dirac dark matter (coloured scalar mediator, $u_R$-philic)

- **Origin**: new construction as an interpretation of the LZ event — no prior work found with the queries of Appendix #5, #6, #10, #11, #12, #14, #19, #20, #33 (as of 2026-09-21). Structurally it is a **variant** of the Dirac $t$-channel simplified model `S3D_uR` [29, 30]; what changed: a Majorana mass splits the Dirac state by δ ≈ 230–340 keV. Pseudo-Dirac dark matter exchanging squark-like scalars is itself old (pseudo-Dirac bino [31, 32]); there the splitting is large and inelastic scattering is the *absence* of a signal, here it is the signal.
- **Status**: viable (region given below); inherits the halo-tail sensitivity common to all endothermic explanations.
- **One-line idea**: a TeV-scale singlet pseudo-Dirac fermion couples to right-handed up quarks through a squark-like scalar; the Fierzed vector current is purely off-diagonal, so nuclei see only $\chi_1 N\to\chi_2 N$; the coupling fixed by thermal freeze-out predicts a cross section inside LZ's band, today's annihilation is $p$-wave into light quarks, and the mediator is an LHC jets + $E_T^{\rm miss}$ target.

#### Field content

| Field | Spin / type | $SU(3)_C$ | $SU(2)_L$ | $Y$ | $Q$ | Self-conj. | Mass | Decays? | $Z_2$ |
|---|---|---|---|---|---|---|---|---|---|
| `chiD` ($\chi$) | Dirac fermion (pseudo-Dirac: two Majorana states $\chi_{1,2}$, $m_{1,2} = m_\chi \mp \delta/2$) | 1 | 1 | 0 | 0 | no | $m_\chi$ | $\chi_1$ stable; $\chi_2\to\chi_1\gamma$ with τ ≈ 0.1 s [estimate] — not modelled | odd |
| `phiU` ($\varphi$) | complex scalar | 3 | 1 | 2/3 | +2/3 | no | $M_\varphi$ | yes, $\varphi\to u\chi$ (auto width) | odd |

#### Lagrangian (BSM part, pipeline-ready)

$$\mathcal{L}_\text{BSM} = \bar\chi\,(i\slashed\partial - m_\chi)\,\chi + (D_\mu\varphi)^\dagger(D^\mu\varphi) - M_\varphi^2\,\varphi^\dagger\varphi + \big[\lambda\,\bar\chi\,P_R\,u\,\varphi^\dagger + \text{h.c.}\big] \;-\; \frac{\delta}{4}\big[\overline{\chi^c}\chi + \text{h.c.}\big]$$

where
- $D_\mu\varphi = (\partial_\mu - i g_s T^a G^a_\mu - i g' Y B_\mu)\varphi$ with $Y = 2/3$ (FeynRules sign convention); $P_R = \tfrac12(1+\gamma^5)$; $u$ is the up quark; $\chi^c = C\bar\chi^T$.
- $\lambda$: real, dimensionless. $\delta$: real, in GeV ($\sim 3\times10^{-4}$); it splits the Dirac state into Majorana eigenstates $m_{1,2} = m_\chi\mp\delta/2$ with maximal mixing.
- Bookkeeping of the Yukawa term: colour $1\otimes3\otimes\bar3\ni1$; charge $0+\tfrac23-\tfrac23=0$; hypercharge $0+\tfrac23-\tfrac23$; dimension $\tfrac32+\tfrac32+1=4$; its h.c. is $\lambda\,\varphi\,\bar u P_L\chi$. With $\varphi$ instead of $\varphi^\dagger$ it would be neither neutral nor a colour singlet.
- **For the pipeline the last term is dropped**: $\delta/m_\chi\sim3\times10^{-7}$ is irrelevant for collider kinematics and for freeze-out ($T_f\sim40$ GeV ≫ δ), where $\chi$ behaves as a Dirac fermion. δ enters only the analytic direct-detection overlay. Same-sign production $uu\to\varphi\varphi$, which drives the strongest LHC bounds for Majorana DM [29], is suppressed by $(\delta/m_\chi)^2\sim10^{-13}$ [estimate: the two Majorana exchanges cancel up to $\delta/m_\chi$ in the amplitude] — so the Dirac UFO is also the right collider model.
- Not included: the portal $\varphi^\dagger\varphi H^\dagger H$ (set to zero [assumed], irrelevant here); couplings to other quark flavours (flavour alignment [assumed]; a UV completion would make $\varphi$ a flavour triplet).
- Provenance: Yukawa term **from source** [29], unnumbered display in Sec. II A defining $\mathcal L_{XY}$ for `S3D_uR` ($\lambda\,\bar\chi u_R\varphi^\dagger$ + H.c.); convention changes: none. Majorana term: own addition.

#### Parameters

| Parameter | Meaning | Type | Benchmark | Allowed / interesting range | Basis for the range |
|---|---|---|---|---|---|
| $m_\chi$ | DM mass | real, GeV | 1000 | 300–2000 | lower: kinematics of a 248 keV endothermic recoil; upper: along the relic line $\sigma\propto1/m_\chi^2$ drops out of LZ's band unless $M_\varphi/m_\chi\lesssim1.5$ [estimate] |
| $M_\varphi$ | mediator mass | real, GeV | 2000 | $1.2\,m_\chi$ – 4000 | below $1.2\,m_\chi$: coannihilation and loop-induced elastic SI become important [29, 34]; above 4 TeV $\lambda>2.5$, $\Gamma/M>0.1$ [estimate] |
| $\lambda$ | Yukawa coupling | real | 1.33 | 0.9–2.5 (relic line) | $\langle\sigma v\rangle = 3\lambda^4 m_\chi^2/[64\pi(m_\chi^2+M_\varphi^2)^2]$ [29, App. A] $=2.2\times10^{-26}$ cm³/s |
| $\delta$ | splitting | real, keV | 280 | 230–340 | LZ band (table below); not a UFO parameter |

Note on [29], App. A: the text defines $r = M_X/M_Y$, but the functions given there ($\log\frac{r^2-1}{r^2+1}$, $\arcsin\frac1r$) require $r>1$, and the formula only decouples for $r = M_Y/M_X$. It is used here with $r = M_\varphi/m_\chi$ — a misprint in the source, not propagated.

#### How it addresses the goal

Integrating out $\varphi$ and Fierzing, $\mathcal L_{\rm eff} = \dfrac{\lambda^2}{8(M_\varphi^2-m_\chi^2)}\,[\bar\chi\gamma^\mu(1-\gamma^5)\chi]\,[\bar u\gamma_\mu(1+\gamma^5)u]$ [own derivation]. In terms of the mass eigenstates $\bar\chi\gamma^\mu\chi = i\,\bar\chi_2\gamma^\mu\chi_1$ (purely off-diagonal) and $\bar\chi\gamma^\mu\gamma^5\chi = \tfrac12\sum_i\bar\chi_i\gamma^\mu\gamma^5\chi_i$ (diagonal). Hence:

- coherent **inelastic** scattering with $f_p = 2b_u$, $f_n = b_u$, $b_u = \lambda^2/[8(M_\varphi^2-m_\chi^2)]$, $\sigma_p = \mu_p^2 f_p^2/\pi$, and an isoscalar-equivalent cross section on xenon $\sigma_{\rm eff} = \sigma_p\,[(Zf_p+(A-Z)f_n)/(Af_p)]^2 = 0.498\,\sigma_p$ [estimate; Helm form factor taken equal for protons and neutrons];
- a correlated **elastic spin-dependent** signal, $\sigma^{N}_{\rm SD} = 3\mu_N^2(b_u\Delta u^N)^2/\pi$ [estimate].

Along the relic line, for $m_\chi$ = 1 TeV (all [estimate], `tools/tchannel_estimates.py`; δ-window = where $\sigma_{\rm eff}$ lies inside the LZ band of Section 1.4):

| $M_\varphi$ [GeV] | $\lambda_{\rm relic}$ | $\Gamma_\varphi/M_\varphi$ | $\sigma_p$ [cm²] | $\sigma_{\rm eff}$ [cm²] | δ-window [keV] | $\sigma_{\rm SD}^p$ / $\sigma_{\rm SD}^n$ [cm²] |
|---|---|---|---|---|---|---|
| 1200 | 0.93 | 0.002 | $2.6\times10^{-41}$ | $1.3\times10^{-41}$ | 306–338 | $1.4\times10^{-41}$ / $3.6\times10^{-42}$ |
| 1500 | 1.07 | 0.007 | $5.8\times10^{-42}$ | $2.9\times10^{-42}$ | 275–322 | $3.1\times10^{-42}$ / $7.9\times10^{-43}$ |
| **2000** | **1.33** | 0.020 | $2.4\times10^{-42}$ | $1.2\times10^{-42}$ | 252–313 | $1.3\times10^{-42}$ / $3.3\times10^{-43}$ |
| 3000 | 1.89 | 0.056 | $1.3\times10^{-42}$ | $6.7\times10^{-43}$ | 237–307 | $7.1\times10^{-43}$ / $1.8\times10^{-43}$ |
| 4000 | 2.46 | 0.106 | $1.1\times10^{-42}$ | $5.5\times10^{-43}$ | 232–305 | $5.9\times10^{-43}$ / $1.5\times10^{-43}$ |

Since $\langle\sigma v\rangle$ and $\sigma_p$ both scale as $\lambda^4/M_\varphi^4$ for $M_\varphi\gg m_\chi$, the thermal relic *predicts* $\sigma_{\rm eff}\to5\times10^{-43}$ cm² × (1 TeV/$m_\chi$)² — three orders of magnitude below the Higgsino's fixed $1.9\times10^{-39}$ cm², and therefore a splitting of 230–340 keV instead of 350–490 keV: further from the kinematic ceiling ($\sqrt{2\delta/\mu}$ = 643–739 km/s for δ = 250–330 keV against ≈ 800 km/s [estimate]). LZ's local significance for this signal class at these splittings is 2.9–3.3σ [1]. For comparison, [10] quotes $\sigma_N\simeq6.5\times10^{-43}$ cm² at δ ≃ 297 keV for a generic thermal pseudo-Dirac fermion at 1 TeV — the same ballpark, reached here with no free normalisation once $M_\varphi$ is given.

#### Constraints

| Constraint | Bound / impact | Source | Verdict |
|---|---|---|---|
| Elastic SI, tree level | absent: a Majorana eigenstate has no vector current (this is what excludes the Dirac model) | [29], [32] | ok |
| Elastic SI, one loop | not computed here; grows as $1/(M_\varphi^2-m_\chi^2)^4$ towards degeneracy; own twist-2 estimate: $\sim10^{-51}$ cm² at $M_\varphi=2m_\chi$, $\sim7\times10^{-47}$ cm² at $M_\varphi=1.1\,m_\chi$ (λ = 1) [estimate, crude] against $3.0\times10^{-47}$ cm² | [2], [34] (abstract: the full one-loop matching exists) | ok for $M_\varphi\gtrsim1.2\,m_\chi$; compressed region needs [34] |
| Elastic SD (correlated signal) | $\sigma_{\rm SD}^n$ = $3.3\times10^{-43}$ cm² at the benchmark vs limit $5.0\times10^{-42}$ cm²; $3.6\times10^{-42}$ at $M_\varphi=1.2$ TeV | [2] HEPData | ok; marginal only for $M_\varphi\le1.2\,m_\chi$ |
| Indirect detection | the Dirac model has $s$-wave $\chi\bar\chi\to u\bar u$ and is constrained by dwarf-galaxy γ rays and antiprotons [29]; here only $\chi_1$ survives ($\chi_2$ decays in ~0.1 s) and $\chi_1\chi_1\to u\bar u$ is helicity/$p$-wave suppressed as in the Majorana model [29] | [29] + [estimate] | ok |
| Solar capture / IceCube | the Higgsino bound [8] assumes $\sigma_n\simeq1.9\times10^{-39}$ cm² and $WW/ZZ$ final states. Here σ is $10^2$–$10^3$ times smaller, annihilation in the Sun is $p$-wave, and the final state is light quarks, whose hadrons stop in the Sun before decaying [41] | [8], [41], [28] | expected ok [estimate]; **not computed** — open issue |
| $\chi_2$ lifetime | $\mu_{12}\sim N_cQ_u e\lambda^2m_\chi/(32\pi^2M_\varphi^2) = 8.5\times10^{-7}$ GeV⁻¹, $\Gamma = \mu_{12}^2\delta^3/\pi$ → τ ≈ 0.11 s, decay length ≈ 74 km at 700 km/s [estimate; loop function set to 1] | own | single-scatter topology preserved; no relic $\chi_2$, hence no exothermic component; XENONnT's recoil + delayed-photon search [3] does not apply |
| LHC jets + $E_T^{\rm miss}$ | not available for Dirac DM: [29] skips it because direct detection already excluded that model. QCD-only production bounds $M_\varphi\gtrsim800$ GeV and vanishes for $m_\chi\gtrsim500$–700 GeV [29]. At ($M_\varphi,m_\chi$) = (2000, 1000) GeV ATLAS allows 0.57 fb [35, HEPData] while QCD alone gives 0.0196 fb [40]; whether $u\bar u\to\varphi\varphi^*$ through $\chi$ exchange (∝ λ⁴) closes the factor 29 is unknown | [29], [35], [40] | **open → plan_01** |
| Flavour | a single flavour coupling requires alignment with the quark mass basis, else $D^0$–$\bar D^0$ mixing | — | [assumed] aligned |
| Perturbativity, width | λ < 2.5 and Γ/M < 0.11 for $M_\varphi\le4$ TeV | [estimate] | ok |
| Halo tail, sideband | rate exponentially sensitive to $v_{\rm esc}$ (general statement in [14]); 0.45–0.6 events above the window per event at 200–270 keV for δ = 250–300 keV [estimate] | [9], [14] | acceptable; shared with all endothermic models |

#### Collider signatures

| Process | Collider | Final state | Rate driver | Existing search (HEPData?) | Untested region |
|---|---|---|---|---|---|
| $pp\to\varphi\varphi^*$, $\varphi\to u\chi$ | LHC 13/13.6/14 TeV | 2 hard jets + $E_T^{\rm miss}$ | QCD + $t$-channel $\chi$ exchange from valence $u\bar u$ (∝ λ⁴) + interference | ATLAS 139 fb⁻¹ [35], ins1827025: cross-section upper limits on the $(m_{\tilde q}, m_{\rm LSP})$ grid (table "X-section U.L. 1"), acceptances/efficiencies of SR 2j-1600/2200/2800, cut-flows | everything with $m_\chi\gtrsim700$ GeV |
| $pp\to\varphi\bar\chi + \varphi^*\chi$ | same | 1 hard jet + $E_T^{\rm miss}$ | $ug$ initial state, ∝ λ² | mono-jet searches (not retrieved) | $M_\varphi+m_\chi\gtrsim2$ TeV |
| $pp\to\chi\bar\chi+j$ | same | mono-jet | ∝ λ⁴, $t$-channel $\varphi$ | mono-jet searches | subleading [29] |

#### Pipeline feasibility

- Tree-level UFO possible: yes — two new fields, one Yukawa coupling; this is the structure of the public DMSimpt models [30].
- Special requirements: CalcHEP output for micrOMEGAs (relic density; its *elastic* Dirac $\sigma_{\rm SI}^p$ is precisely the $\sigma_p$ that enters the inelastic rate — a free cross-check); $Z_2$-odd fields `chiD`, `phiU`.
- Not executable with the current pipeline: the inelastic recoil rate (micrOMEGAs does elastic scattering only) — supplied as a closed-form overlay plus `tools/idm_rate.py`; NLO-QCD and jet merging (LO + reference $K$-factors instead); the solar-capture calculation.

#### Open issues

- Solar capture and thermalisation for this specific model (capture through the inelastic SI channel, cooling through the elastic SD channel on hydrogen).
- One-loop elastic SI in the compressed region; QCD corrections to $\lambda_{\rm relic}$.
- The nuclear form factor in the second lobe (150–270 keV) is the largest hidden uncertainty of *every* coherent interpretation: LZ uses shell-model responses, the estimates here Helm.
- UV origin of δ (a Majorana mass for a singlet is technically natural — it is the only source of $U(1)_\chi$ breaking — but its size is unexplained).

### T2: Quark-portal split-scalar dark matter (vector-like quark mediator): automatically exothermic

- **Origin**: new construction as an interpretation of the LZ event — no prior work found with the queries of Appendix #5, #6, #10, #11, #20, #28 (as of 2026-09-21). Structurally a **variant** of the complex-scalar $t$-channel model `F3C_uR` [29]; what changed: a soft $U(1)_D$-breaking mass splits $S$ into two real scalars. The field content (complex scalar DM + vector-like quark) also appears in [36] (posted 2026-09-08), with a $Z_3$ symmetry, a down-type quark partner and *elastic* scattering — it does not address the event.
- **Status**: constrained — it works, but not in the way first expected, and only with a relic abundance set by coannihilation (or non-thermally).
- **One-line idea**: the same portal with the spins exchanged. A scalar $0\to0$ transition cannot emit a single photon and δ < 2$m_e$ closes $e^+e^-$, so $S_2$ is cosmologically stable; $S_2\leftrightarrow S_1$ conversions decouple at $T\gg\delta$, so half of the dark matter *is* $S_2$ today. The model is therefore exothermic whether one wants it or not — which turns the two assumptions that exothermic interpretations must make (a stable excited state with a sizeable abundance, a leptophobic mediator [12]) into predictions, and ties them to an LHC-accessible coloured fermion.

#### Field content

| Field | Spin / type | $SU(3)_C$ | $SU(2)_L$ | $Y$ | $Q$ | Self-conj. | Mass | Decays? | $Z_2$ |
|---|---|---|---|---|---|---|---|---|---|
| `Sdm` ($S = (S_1+iS_2)/\sqrt2$) | complex scalar (two real states, $m_2-m_1=\delta$) | 1 | 1 | 0 | 0 | no | $m_S$ | $S_1$ stable; $S_2$ stable on cosmological time scales [estimate] | odd |
| `psiU` ($\psi$) | Dirac fermion, vector-like | 3 | 1 | 2/3 | +2/3 | no | $M_\psi$ | yes, $\psi\to uS$ (auto width) | odd |

#### Lagrangian (BSM part, pipeline-ready)

$$\mathcal{L}_\text{BSM} = |\partial_\mu S|^2 - m_S^2|S|^2 + \bar\psi\,(i\slashed D - M_\psi)\,\psi + \big[y\,\bar\psi\,P_R\,u\,S + \text{h.c.}\big] - \frac{m_S\delta}{2}\big(S^2+S^{*2}\big) - \lambda_{HS}|S|^2H^\dagger H$$

where
- $D_\mu\psi = (\partial_\mu - ig_sT^aG^a_\mu - ig'YB_\mu)\psi$, $Y=2/3$; $y$ real, dimensionless; the soft term gives $m^2_{1,2} = m_S^2\pm m_S\delta$, i.e. a splitting δ to first order in $\delta/m_S$ (which state is lighter is a convention).
- Bookkeeping of the Yukawa term: colour $\bar3\otimes3\otimes1\ni1$; charge $-\tfrac23+\tfrac23+0$; dimension 4. Dark charges: $U(1)_D$ with $D(S)=-D(\psi)$ … the soft term breaks it to the $Z_2$ under which $S,\psi$ are odd.
- $\lambda_{HS}$ cannot be forbidden; it must satisfy $\lambda_{HS}<0.058$ at $m_S$ = 1 TeV [estimate: $\sigma_{\rm SI} = \lambda_{HS}^2f_N^2\mu^2m_N^2/(4\pi m_h^4m_S^2)$, $f_N = 0.3$ [assumed], against [2]] and is set to zero in the simplified model [assumed].
- **For the pipeline the soft term is dropped** (complex $S$), for the same reason as in T1.
- Provenance: Yukawa term **from source** [29], same display, model `F3C_uR` ($\lambda\,\bar\psi u_RS^\dagger$ + H.c.; here $S\to S^\dagger$ relabelled, coupling called $y$). Soft term and portal: own addition.

#### Parameters

| Parameter | Meaning | Type | Benchmark | Allowed / interesting range | Basis for the range |
|---|---|---|---|---|---|
| $m_S$ | DM mass | real, GeV | 1000 | 200–1500 | exothermic kinematics work for any mass ≳ 100 GeV [estimate]; upper end: coannihilation relic [unverified] |
| $M_\psi$ | mediator mass | real, GeV | 1080 | (1.03–1.15) $m_S$ | coannihilation strip; exact width **not computed** — "requires a micrOMEGAs scan" |
| $y$ | Yukawa | real | 0.05–0.07 (at $M_\psi$ = 1080 GeV); 0.21–0.31 at 2000 GeV | fixed by the LZ rate | $b_u = y^2/[4(M_\psi^2-m_S^2)]$, $\sigma_{\rm eff} = (0.3$–$1.4)\times10^{-44}$ cm² [estimate] |
| $|\delta|$ | splitting | real, keV | 320 | 300–450 (< 2$m_e$ = 1022 keV) | below 250–300 keV the spectrum leaks to low energy: 2.6 events at 5–70 keV per event at 200–270 keV for δ = 250 keV, 0.4 for 300 keV [estimate, `tools/exo_rate.py`] |

#### How it addresses the goal

$\varphi\to\psi$ exchange gives $\mathcal L_{\rm eff} = \dfrac{y^2}{2(M_\psi^2-m_S^2)}(S^\dagger i\overleftrightarrow{\partial_\mu}S)(\bar u\gamma^\mu P_Ru)$ [own derivation], and $S^\dagger i\overleftrightarrow\partial S = S_1\partial S_2 - S_2\partial S_1$ is purely off-diagonal; $b_u = y^2/[4(M_\psi^2-m_S^2)]$, $\sigma_p = \mu_p^2(2b_u)^2/\pi$. There is no spin, hence no elastic SD companion signal (a clean discriminator against T1).

Why exothermic: (i) $S_2\to S_1\gamma$ is forbidden (0→0), $S_2\to S_1e^+e^-$ is closed, $S_2\to S_1\gamma\gamma$ proceeds through the axial part of the quark current and an off-shell $\pi^0$: $\Gamma\sim b_u^2\alpha^2\delta^7/(64\pi^5m_\pi^4)$ → τ ~ $10^{22}$ s [estimate, dimensional, uncertain by ≥ 10×]; (ii) $S_2q\leftrightarrow S_1q$ keeps $n_2/n_1 = e^{-\delta/T}$ until it decouples at $T\sim50$–100 MeV ≫ δ (rate on pions at $T$ = 20 MeV ≈ $10^{-3}H$ [estimate]), and $S_2S_2\to S_1S_1$ is never efficient for TeV masses ($\Gamma/H\sim10^{-4}$ at 1 GeV [estimate]) → $f_2 = 0.5$ [assumed from these estimates]. With $f_2 = 0.5$, one event at 200–270 keV needs $\sigma_{\rm eff} = 1.4\times10^{-44}$ cm² at 1 TeV (δ = 300–350 keV), accompanied by 4–5 events at 70–200 keV and 0.6–0.8 above the window; normalising instead to ~1–2 events in the whole 70–270 keV range gives $3\times10^{-45}$ cm² [estimate; Helm second lobe]. No velocity threshold: halo-insensitive, percent-level modulation, and a signal in argon at higher energies (the test proposed for exothermic models in general [14]).

**What does not work** (kept because it is the instructive dead end): fixing $y$ by $t$-channel freeze-out. The annihilation is $p$-wave [29]; with $\sigma v = y^4m_S^2v^2/[16\pi(m_S^2+M_\psi^2)^2]$ [own derivation] the relic density needs $y$ = 1.8–2.5, i.e. $\sigma_{\rm eff} = 6\times10^{-41}$–$7\times10^{-40}$ cm² — $10^3$–$10^5$ times above the exothermic requirement, which with $f_2 = 0.5$ means thousands of events. The thermal $t$-channel version of T2 is **excluded by LZ's own window**.

#### Constraints

| Constraint | Bound / impact | Source | Verdict |
|---|---|---|---|
| Relic density | cannot come from the $t$-channel (above) nor from the Higgs portal ($\lambda_{HS}<0.058$). Coannihilation with $\psi$ (QCD-driven, independent of $y$) or a non-thermal history is required | [29] for the mechanism | viable only on the coannihilation strip [unverified: strip not computed] |
| Elastic SI | tree level absent; loops ∝ $y^4$ with $y\lesssim0.3$: negligible [estimate]; Higgs portal as above | [2] | ok |
| $S_2\to S_1\gamma\gamma$ | τ ~ $10^{22}$ s with a ~150 keV photon pair, number density suppressed by $m_S$; hard X-ray line/continuum limits rescaled to this density sit around $10^{21}$–$10^{22}$ s [unverified, from memory] | own | **borderline — needs a real calculation** |
| Empty sideband | 0.6–0.8 events above the window per event at 200–270 keV for δ = 300–350 keV; broadly peaked exothermic spectra are disfavoured by the sideband [12] | [12] + [estimate] | mild tension; prefers δ ≈ 300 keV |
| Solar capture | exothermic and elastic capture with σ ~ $10^{-44}$ cm² — five orders below the Higgsino case | [8] | ok [estimate] |
| LHC | compressed $\psi\bar\psi$ → soft jets + $E_T^{\rm miss}$; QCD-only bound for a fermionic mediator is 1.5 TeV at small DM mass and vanishes for DM masses above 500–700 GeV [29] | [29] | benchmark untested; mono-jet reach to be determined |

#### Collider signatures

| Process | Collider | Final state | Rate driver | Existing search (HEPData?) | Untested region |
|---|---|---|---|---|---|
| $pp\to\psi\bar\psi$, $\psi\to uS$, $M_\psi-m_S$ = 30–150 GeV | LHC / HL-LHC | mono-jet (ISR) + soft jets + $E_T^{\rm miss}$ | QCD only ($y$ is small); fermion pair rates ≈ 5–10× a scalar's at equal mass [unverified] | compressed-squark regions of [35] ("MB-C" rows of the HEPData table, up to $m_{\tilde q}$ = 1200 GeV) | $m_S\gtrsim700$ GeV |

#### Pipeline feasibility

- Tree-level UFO possible: yes (the `F3C` structure of [30]).
- Special requirements: CalcHEP + micrOMEGAs with coannihilation (slow: coloured coannihilation channels, keep the scan coarse); Sommerfeld and bound-state effects are *not* in micrOMEGAs and matter on this strip [29].
- Not executable: a mono-jet analysis needs the ISR jet at matrix-element level and no jet merging — feasible only as the stated approximation of the capability reference; the exothermic rate is an analytic overlay.

#### Open issues

- The coannihilation strip and its upper mass end; the $S_2$ lifetime and the X-ray bound; the precise $f_2$.

### T3: Majorana quark-portal dark matter, $d_R$-philic — elastic spin-dependent (short form)

- **Origin**: new as an interpretation of the event (same queries as T1); the model itself is the standard Majorana $t$-channel model [29, 42] with the mediator coupled to $d_R$ instead of $u_R$.
- **Status**: constrained — marginal; **not assessed quantitatively**.
- **One-line idea**: a Majorana singlet has only the axial current, so the quark portal gives pure elastic $\mathcal O_4$ scattering, and coupling to $d_R$ makes it neutron-dominated ($a_n/a_p = \Delta d^n/\Delta d^p\approx-2$ [unverified inputs]) — what an odd-neutron target like xenon wants. No halo-tail tuning, no modulation. Lagrangian: that of T1 with $\chi\to$ Majorana and $u\to d$, $\varphi\sim(3,1,-\tfrac13)$; not pipeline-ready as written only in the sense that no benchmark was fixed.

Why marginal. The elastic-SD route was worked out in [17] for a $Z$-mediated model; read at source level, it needs 0.5–2 events at 100–270 keV, and its own benchmark ($Y_n$ = 0.1, $m_0$ = 500 GeV, 1.27 events) corresponds to $\sigma_{\rm SD}^n\approx6.8\times10^{-42}$ cm² [estimate from the couplings of [17], Eqs. for $g_{ZNN}$] — against LZ's own 4.2 t yr limit of $2.6\times10^{-42}$ cm² at 500 GeV [2]. [17] says the same in words: the LZ low-energy SD limit "excludes the upper end of our signal region". Only the ≈ 0.5-event end survives, for any mediator. For the quark portal, $\sigma_{\rm SD}^n = 12\mu_n^2(\lambda^2\Delta d^n/[8(M^2-m^2)])^2/\pi$ reaches $10^{-41}$ cm² for (λ, $M_\varphi$, $m_\chi$) = (1, 1.5 TeV, 1 TeV) or (2, 2.4 TeV, 1 TeV) [estimate], couplings of the size a $p$-wave thermal relic needs anyway — but for such couplings [29] finds LHC limits of 2.2–3.7 TeV on the mediator of the $u_R$ version, driven by same-sign $uu\to\varphi\varphi$. The $d_R$ version is weaker-constrained ("the numerical relevance … would be smaller" [29]) but has not been computed. LZ's local significance for elastic $\mathcal O_4$ is also lower (2.7σ) than for the inelastic classes [1]. T3 would become interesting if LZ released the $\mathcal O_4$ interval; it is kept as a proposed plan because its LHC signature — same-sign mediator pairs — is qualitatively different from T1's.

## 4. Comparison and Ranking

| Rank | Target | Addresses goal | Viability | Collider testability | Minimality | Pipeline feasibility | Novelty |
|---|---|---|---|---|---|---|---|
| 1 | T1 pseudo-Dirac + coloured scalar | inside LZ's band with **no free normalisation** on the relic line; 2.9–3.3σ class | viable; solar capture expected harmless but uncomputed; halo-tail sensitive | jets + $E_T^{\rm miss}$ with λ⁴-enhanced production; untested for $m_\chi\gtrsim700$ GeV | 2 fields, 3 parameters + δ | full (UFO + CalcHEP); DD as overlay | new for the event; variant of `S3D_uR` |
| 2 | T2 split scalar + vector-like quark | exothermic; halo-independent; stability and abundance of the excited state predicted | constrained: relic only via coannihilation; $S_2\to S_1\gamma\gamma$ bound borderline | compressed mono-jet | 2 fields, 3 parameters + δ (+ unavoidable $\lambda_{HS}$) | UFO fine; relic needs effects beyond micrOMEGAs | new for the event; new observation that the scalar portal is automatically exothermic |
| 3 | T3 Majorana, $d_R$-philic | elastic SD, 2.7σ class | marginal against LZ's own SD-$n$ limit | same-sign mediator pairs | 2 fields, 3 parameters | full | new for the event; standard model otherwise |

T1 is first because it is the only one of the three where a second, independent requirement (the relic density) lands the prediction inside the experimental band, and because the question "is the preferred region already excluded by the LHC?" has no answer in the literature — [29] stopped studying the Dirac model at colliders precisely because direct detection had killed it. T2 is physically the more surprising construction, but every one of its viability questions (coannihilation strip with Sommerfeld effects, $\gamma\gamma$ lifetime) lies outside what the pipeline computes well. T3 is an honest "probably not".

## 5. Recommended Research Program

| Plan | Status | Target(s) | Physics question | Deliverable (figure/table) | Strategy | Depends on |
|---|---|---|---|---|---|---|
| `plans/plan_01_t1_quarkportal_lhc_reinterpretation.md` | **written** | T1 | Which part of the ($M_\varphi$, λ) and ($M_\varphi$, $m_\chi$) space that gives the LZ event and the relic density is excluded by ATLAS Run-2 squark limits, and what are the HL-LHC rates? | exclusion map with relic line and LZ δ-band; table of cross-section coefficients in powers of λ | signal characterization + limit reinterpretation + DM complementarity | — |
| `plans/plan_02_t1_hllhc_projection.md` | proposed | T1 | HL-LHC (3 ab⁻¹) reach in jets + $E_T^{\rm miss}$ and mono-jet for the region left open by plan_01 | expected 95% CL reach in ($M_\varphi$, $m_\chi$) on the relic line | sensitivity projection ($Z(\nu\nu)$+jets, $W$+jets, $t\bar t$ backgrounds with generator-level cuts) | plan_01 (UFO, scan ranges) |
| `plans/plan_03_t2_compressed_vlq.md` | proposed | T2 | Where is the coannihilation strip, and does the mono-jet channel reach it? | $\Omega h^2$ = 0.12 strip in ($m_S$, $M_\psi-m_S$) with mono-jet limits | DM complementarity + recast | — |
| `plans/plan_04_t3_samesign_mediators.md` | proposed | T3 | Does same-sign $dd\to\varphi\varphi$ exclude the couplings an elastic-SD explanation needs? | exclusion in ($M_\varphi$, λ) against the $\sigma_{\rm SD}^n$ band | recast | plan_01 (method) |

## 6. Decisions for the User

1. **Meaning of "new".** Both constructions are new *as interpretations of the event* (search basis: Appendix; date 2026-09-21; nothing after 2026-09-16 was visible), but are variants of known simplified models. If the user wants field content that exists nowhere in the literature, say so — my recommendation is against it: the known building blocks are what make T1 predictive and executable.
2. **A deeper pass is needed before any of this is written up**: (a) solar capture for T1; (b) the $S_2\to S_1\gamma\gamma$ rate and X-ray limits for T2; (c) LZ's data release, once it resolves, to replace the by-eye band and to obtain the $\mathcal O_1^v$, $\mathcal O_4$ intervals and the 0.3–2 TeV mass dependence; (d) a re-run of the arXiv listing search — this literature grows by ~4 papers per day.
3. **$u_R$ or $d_R$ for T1.** The plan uses $u_R$ (largest LHC rates; [29] conventions). The $d_R$ version has $\sigma_{\rm eff} = 0.631\,\sigma_n$, a four times larger correlated SD-neutron signal ($1.3\times10^{-42}$ cm² at the benchmark [estimate], a factor 4 below LZ's limit — a second handle in xenon) and weaker LHC limits. Recommendation: run plan_01 for $u_R$, add $d_R$ only if the $u_R$ region turns out excluded.
4. **How much to invest at 2.6σ, non-blind, one event.** plan_01 is parton-level and cheap (~330 short runs); plan_02 is not. Recommendation: run plan_01 now, decide on plan_02 after LZ's next exposure update.

## 7. References

[1] LZ Collaboration (Akerib et al.), "Search for dark matter particle interactions in an extended nuclear recoil energy window with the LUX-ZEPLIN (LZ) experiment", arXiv:2609.02823 (depth: source) — used for: event, exposure, efficiency, background table, significances (Tables S-II, S-III), intervals (Figs. 6, S7, by eye), caveats of the analysis
[2] LZ Collaboration (Aalbers et al.), "Dark Matter Search Results from 4.2 Tonne-Years of Exposure of the LUX-ZEPLIN (LZ) Experiment", arXiv:2410.17036 (depth: abstract + HEPData ins2841863 tables) — used for: SI and SD-neutron limits
[3] XENON Collaboration (Aprile et al.), "Search for Magnetic and Spin-Independent Inelastic Dark Matter with XENONnT", arXiv:2608.15149 (depth: abstract) — used for: null result, topology searched
[4] Tucker-Smith, Weiner, "Inelastic dark matter", arXiv:hep-ph/0101138 (depth: title) — used for: the mechanism
[5] Bramante, Fox, Kribs, Martin, "The Inelastic Frontier: Discovering Dark Matter at High Recoil Energy", arXiv:1608.02662 (depth: abstract) — used for: pre-LZ bounds up to δ ≈ 550 keV, target-mass dependence
[6] Freese, Theodosopoulos, "Higgsino Dark Matter Interpretation of the LUX-ZEPLIN 248 keV Nuclear-Recoil Event", arXiv:2609.01583 (depth: abstract) — used for: Higgsino class
[7] Fan, Reece, "Higgsino Above the Sea of Fog", arXiv:2609.01504 (depth: abstract) — used for: Higgsino class, halo dependence
[8] Pospelov, Ramani, "Strong Constraints on Higgsino Dark Matter from Solar Capture", arXiv:2609.02775 (depth: abstract) — used for: δ > 566 keV, 1400 km/s
[9] Rodd, Safdi, Slatyer, Xu, "Confronting the Higgsino Interpretation of the LZ Event with the High-Energy Sideband", arXiv:2609.04175 (depth: abstract) — used for: sideband tension
[10] Di Mauro, "Dark Matter at the Kinematic Edge: Interpreting the 248 keV LZ Nuclear-Recoil Candidate", arXiv:2609.02608 (depth: abstract) — used for: $\sigma_N\simeq6.5\times10^{-43}$ cm² at δ ≃ 297 keV
[11] McCabe, "Seasonal dark matter from the LUX-ZEPLIN high-energy event", arXiv:2609.04181 (depth: abstract) — used for: modulation
[12] Dent, Newstead, "Exothermic and Endothermic Inelastic Dark Matter Interpretations at LZ: Sideband Constraints and Future Prospects", arXiv:2609.04673 (depth: abstract) — used for: requirements of exothermic models, sideband, 1000-live-day projection
[13] de Lima, "Exothermic Dark Matter at LZ", arXiv:2609.05204 (depth: abstract) — used for: exothermic class
[14] Baer, Barger, "Exothermic dark matter and the 248 keV nuclear recoil in LUX-ZEPLIN", arXiv:2609.06153 (depth: abstract) — used for: escape-speed sensitivity (0 to 143×), argon test
[15] Du, Huang, Xie, "Pseudo-Dirac Inelastic Dark Matter in the Leptophobic $U(1)_B$ Model: Confronting the LUX-ZEPLIN High-Recoil Event with Collider Searches", arXiv:2609.07225 (depth: abstract) — used for: $Z'$ class, collider link
[16] Okada, Seto, "Inelastic $B-L$ scalar dark matter and the LUX-ZEPLIN event", arXiv:2609.06909 (depth: abstract) — used for: $Z'$ class
[17] Elahi, Schwaller, "A Vector-Like Lepton Interpretation of the High-Energy Nuclear Recoil Candidate in LUX-ZEPLIN", arXiv:2609.08993 (depth: source) — used for: elastic-SD requirement, benchmark couplings, tension with LZ SD limit and IceCube
[18] Unwin, "Axion Portal Dark Matter and the LUX-ZEPLIN High-Recoil Event", arXiv:2609.04186 (depth: abstract) — used for: pseudoscalar class
[19] Asadi, Batz, Fox, Homiller, "For Whom the Xenon Recoils: Magnetic Inelastic Dark Baryons", arXiv:2609.09107 (depth: abstract) — used for: dipole class
[20] He, "Transition magnetic-dipole dark matter and the LZ230616 high-recoil candidate", arXiv:2609.10453 (depth: abstract) — used for: dipole class
[21] Alhazmi, Kim, Kong, Park, "High-Energy Nuclear Recoils from Boosted Dark Matter for the LZ 248-keV Event", arXiv:2609.06890 (depth: abstract) — used for: boosted class
[22] Aghaie, Strumia, "Neutron disappearance and the LZ nuclear recoil event", arXiv:2609.09037 (depth: abstract) — used for: exotic nuclear class
[23] Jeesun, Majumdar, "Atmospheric neutrino up-scattering explanation of LZ 2026 excess", arXiv:2609.04185 (depth: abstract) — used for: exotic class
[24] Lou, Lu, "Fermionic Dark Matter Absorption and the High-Energy Event in LUX-ZEPLIN", arXiv:2609.01592 (depth: abstract) — used for: absorption, KamLAND exclusion
[25] Lee, Youn, "Mixing-suppressed inelastic dark matter: a minimal model for the LZ 248 keV event", arXiv:2609.09138 (depth: abstract) — used for: mixing-suppressed class
[26] Smirnov, Griffith, Beacom, "Inelastic Signatures of Electroweak Dark Matter", arXiv:2609.04144 (depth: abstract) — used for: electroweak multiplets
[27] Palmisano, Tammaro, Tesi, "Inferring dark matter masses and interactions from high recoil energy events in LUX-ZEPLIN", arXiv:2609.15985 (depth: abstract) — used for: classification cross-check
[28] Di Mauro, Shaikh, "Solar Capture Tests of Inelastic Dark Matter after the LZ High-Recoil Event", arXiv:2609.06760 (depth: abstract) — used for: solar bounds are model-specific
[29] Arina, Fuks, Heisig, Krämer, Mantani, Panizzi, "Comprehensive exploration of t-channel simplified models of dark matter", arXiv:2307.10367 (depth: source) — used for: Lagrangians, $\langle\sigma v\rangle$ (App. A), exclusion of complex-DM models, LHC bounds and their origin
[30] Arina, Fuks, Mantani, "A universal framework for t-channel dark matter models", arXiv:2001.05024 (depth: abstract) — used for: existence of the DMSimpt FeynRules implementation
[31] Hsieh, "Pseudo-Dirac bino dark matter", arXiv:0708.3970 (depth: abstract) — used for: prior art
[32] De Simone, Sanz, Sato, "Pseudo-Dirac Dark Matter Leaves a Trace", arXiv:1004.1567 (depth: abstract) — used for: prior art; Dirac-like relic, Majorana-like detection
[33] Bai, Berger, "Fermion Portal Dark Matter", arXiv:1308.0612 (depth: abstract) — used for: prior art on the portal
[34] Arcadi, Cabo-Almeida, Mescia, et al., "Dark Matter Direct Detection in t-channel mediator models", arXiv:2309.07896 (depth: abstract) — used for: existence of the one-loop elastic computation
[35] ATLAS Collaboration, "Search for squarks and gluinos in final states with jets and missing transverse momentum using 139 fb$^{-1}$ of $\sqrt s$ = 13 TeV $pp$ collision data with the ATLAS detector", arXiv:2010.14293 (depth: abstract + HEPData ins1827025 tables) — used for: cross-section upper limits, single-squark contour
[36] Kolay, Mandal, Mitra, "Complex Scalar Dark Matter with a Vector-Like Quark and Lepton: Precision, Flavor, and HL-LHC", arXiv:2609.09120 (depth: abstract) — used for: nearest prior work to T2
[37] Steigman, Dasgupta, Beacom, "Precise Relic WIMP Abundance and its Impact on Searches for Dark Matter Annihilation", arXiv:1204.3622 (depth: abstract, partially) — used for: canonical cross section
[38] Baxter et al., "Recommended conventions for reporting results from direct dark matter searches", arXiv:2105.00599 (depth: title) — used for: existence of the halo conventions LZ adopts
[39] Lewin, Smith, "Review of mathematics, numerical factors, and corrections for dark matter experiments based on elastic nuclear recoil", INSPIRE 405551 (depth: title) — used for: Helm form factor
[40] LHC SUSY Cross Section Working Group, stop/sbottom pair production at 13 TeV, NNLO$_{\rm approx}$+NNLL, `twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVstopsbottom` (depth: raw page, retrieved 2026-09-21; extract in `data/stop_xsec_13TeV_nnll.csv`) — used for: reference cross sections
[41] Nussinov, Wang, Yavin, "Capture of Inelastic Dark Matter in the Sun", arXiv:0905.1333 (depth: abstract) — used for: light hadronic channels unconstrained
[42] Garny, Ibarra, Vogl, "Signatures of Majorana dark matter with t-channel mediators", arXiv:1503.01500 (depth: abstract) — used for: Majorana portal
[43] LZ-event papers cited by ID only in Section 2 — all resolved and read at abstract depth in this session: 2609.01475, 2609.01590, 2609.01892, 2609.02505, 2609.02807, 2609.02868, 2609.02994, 2609.04163, 2609.06171, 2609.06571, 2609.06640, 2609.06750, 2609.06756, 2609.07138, 2609.07451, 2609.07742, 2609.07800, 2609.07807, 2609.07811, 2609.08712, 2609.08808, 2609.08893, 2609.09015, 2609.09136, 2609.09385, 2609.09830, 2609.10491, 2609.10504, 2609.10636, 2609.10662, 2609.10827, 2609.11241, 2609.11600, 2609.11833, 2609.12045, 2609.13038, 2609.13130, 2609.14799, 2609.15027, 2609.15321, 2609.15600, 2609.15634, 2609.15714, 2609.15742, 2609.15782, 2609.15933, 2609.17196, 2609.17412, 2609.17935, 2609.18564, 2609.19174 (abstracts stored in `tools/citing_abstracts.txt`)

## Appendix: Search Log

Machine log: `tools/search_log.tsv`. 35 lookups, 3 source downloads.

| # | Service | Query | Yield |
|---|---|---|---|
| 1 | INSPIRE | `cn LZ and de > 2024` | 14 hits; found [1] (posted 2026-09-02, already 77 citations) and the 2512.08065 low-mass result |
| 2–3 | INSPIRE, arXiv | `arxiv:2609.02823 or arxiv:2512.08065`; `id_list=2609.02823` | abstracts; HEPData DOI in the arXiv comment |
| 4 | arXiv e-print | 2609.02823 | **download 1/3**; read results, theory, analysis, discussion, tables, Figs. 6 and S7 |
| 5 | INSPIRE | `refersto:recid:3199115` | 77 hits = citation count (sanity check passed); full list in `tools/citing_titles.txt` |
| 6 | arXiv | `id_list=` 77 IDs | all abstracts, `tools/citing_abstracts.txt` |
| 7–9 | HEPData | `record/ins3199115`, `record/182472`, DOI | 404 / 403 / 404 — data release not accessible |
| 10 | arXiv | `abs:"LUX-ZEPLIN" AND abs:recoil`, 2026-09-01…21, newest first | 53 hits; 5 papers not on the INSPIRE list |
| 11 | arXiv | `(abs:LZ OR abs:"LUX-ZEPLIN") AND (abs:"248" OR abs:"high-recoil" OR abs:"high-energy" OR abs:inelastic OR abs:excess)`, 2026-08-20…09-21 | 77 hits, none new; newest dated 2026-09-16; grep for t-channel/squark/colo(u)red: 0 |
| 12 | INSPIRE | `t inelastic and t "dark matter" and (t "t-channel" or t colored or t coloured or t squark or t "quark partner" or t "vector-like quark")` | 0 hits |
| 13 | INSPIRE | `t "pseudo-Dirac" and t "dark matter"` | 19 hits; prior art [31], [32] |
| 14 | INSPIRE | `abstracts.value:"inelastic" and abstracts.value:"t-channel" and abstracts.value:"dark matter" and abstracts.value:"direct detection" and de > 2015` | 1 hit (a thesis), irrelevant |
| 15 | INSPIRE | batch of 24 arXiv IDs | all 24 resolve and match |
| 16 | arXiv | `id_list=` 17 IDs | abstracts of prior art and constraints |
| 17 | arXiv e-print | 2307.10367 | **download 2/3**; Lagrangians, App. A, cosmology and collider sections |
| 18 | INSPIRE | `(cn XENON or cn PandaX or … or cn CRESST) and de > 2026-05` | 8 hits; found [3]; no extended-window NR result |
| 19 | INSPIRE | `ft "inelastic dark matter" and ft "t-channel mediator" and de > 2026-08` | 0 hits |
| 20 | INSPIRE | `ft "LUX-ZEPLIN" and (ft "colored mediator" or ft "coloured mediator" or ft "squark exchange" or ft "vector-like quark mediator" or ft "t-channel mediator") and de > 2026-08` | 2 hits: [36] and 2609.16156, neither about the event |
| 21 | arXiv | `id_list=2608.15149,2609.09120,2609.16156` | abstracts |
| 22–23 | HEPData | `record/ins1827025`; table "X-section U.L. 1" | 75 tables; `data/ins1827025_xsec_ul_1.csv` |
| 24 | arXiv e-print | 2609.08993 | **download 3/3**; elastic-SD requirement |
| 25–27 | HEPData | `record/ins2841863`; SI and SDn tables | `data/ins2841863_*.csv` |
| 28 | INSPIRE | `(ft "exothermic" or ft "inelastic dark matter") and (ft "vector-like quark" or ft "fermion portal" or ft "t-channel mediator" or ft "colored mediator") and ft "mass splitting" and de > 2009 and t "dark matter"` | 26 hits; none builds T1 or T2 for the event; surfaced the $t$-channel whitepaper 2504.10597 |
| 29 | HEPData | table "Obs.Contour 2" | `data/ins1827025_obs_contour_2.csv`; single-squark limit 1220 GeV |
| 30 | Web (WebFetch + raw `curl`) | LHC SUSY XS WG twiki, stop pairs 13 TeV | [40]; numbers re-read from the raw page |
| 31 | arXiv | `id_list=2504.10597,1204.3622,1708.09698` | abstracts |
| 32 | INSPIRE | `a Lewin and a Smith and t "numerical factors"` | [39] |
| 33 | WebSearch | `LZ 248 keV nuclear recoil event dark matter "t-channel" OR "colored mediator" OR "squark" OR "vector-like quark" mediator inelastic interpretation` | no coloured-mediator interpretation; surfaced [34] |
| 34 | INSPIRE | `arxiv:2309.07896 or arxiv:1204.3622 or arxiv:2504.10597 or arxiv:2608.15149` | verification |
