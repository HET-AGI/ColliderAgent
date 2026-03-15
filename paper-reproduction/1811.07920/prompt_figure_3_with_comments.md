# 1. Target

Considering the $U_1$ Leptoquark Model described in this document, plot the 2σ exclusion contour for the $U_1$ Leptoquark in the $(\sqrt{|g_c^* g_b|},\, M_{U_1})$ plane, with some other lines and bands.


---

# 2. $U_1$ Leptoquark Model

In this section, $U_1$ Leptoquark Model is introduced.

## 2.1 Lagrangian

$$\mathcal{L}_{U_1} = -(D_\mu U_{1\nu} - D_\nu U_{1\mu})^\dagger(D^\mu U_1^\nu - D^\nu U_1^\mu) + M_{U_1}^2\,U_{1\mu}^\dagger U_1^\mu + \bigl[g_{c}\,(\bar{c}\gamma^\mu P_L\nu_\tau)\,U_{1\mu}^\dagger + g_{b}\,(\bar{b}\gamma^\mu P_L\tau)\,U_{1\mu}^\dagger + \text{h.c.}\bigr]$$

Here, 
- $U_1$ is a vector leptoquark beyond the SM. It is a new gauge boson, carrying color triplet, SU(2)_L singlet, and electric charge $Q = 2/3$.
- $P_L$ is the left-handed projection operator.
- $D_\mu$ is the covariant derivative of the SM gauge fields.
- $\nu_\tau$ is the tau neutrino.
- $\tau$ is the tau lepton.
- $c$ is the charm quark.
- $b$ is the bottom quark.

## 2.2 Parameters

The free parameters are:
- $M_{U_1}$ is the mass of $U_1$.
- $g_{c}$ and $g_{b}$ are the couplings of $U_1$ to $c$ and $b$ quarks, respectively. Bothe of them are real.

---

# 3. Collider Simulation


## 3.1 Process

$$ p p \to \tau \nu$$

which is mediated by the $U_1$ vector leptoquark. Since the $U_1$ leptoquark couples to $b$ and $c$ quarks, the initial-state $b$ and $c$ partons from the proton PDF must be included.

## 3.2 Collider simulation settings

We have two runs. For each run,
- collider: 13 TeV LHC
- event number: 10000
- parton shower: Pythia8
- perform mass scan for $M_{U_1}$ masses: 750, 1000, 1250, 1500, 2000, 2500, 3000, 4000, 5000 GeV
- Output format for reconstructed events: LHCO
  - comment: Enable LHCO output from Delphes by uncommenting the `root2lhco` section in `bin/internal/run_delphes3` (lines 48–58). LHCO files are ~470 KB vs ~615 MB ROOT — essential for efficient event-level analysis.
- comment: decay width of LQ is not relevant, since only the t-channel contribution exists.

Run 1 (with ATLAS detector simulation):
- detector simulation: Delphes ATLAS card

Run 2 (with CMS detector simulation):
- detector simulation: Delphes CMS card

---


# 3 Numerical Analysis

## 3.1 Experimental data

Binned $m_T$ distribution from ATLAS and CMS are given below:

**ATLAS**:
- Stored as `analysis/hepdata/table1.yaml`
- 22 bins from 250 to 3200 GeV (log-spaced)
- Columns: observed events $n_i$, SM background $b_i$, symmetric error $\delta b_i$
- comment
   - from HEPData record of arXiv:1801.06992 in the link https://www.hepdata.net/record/80812
   - skill version: please search on HEPData website to find the data for arXiv:1801.06992, which should be used in this analysis.

**CMS**:
The experimental data is given below:

| $m_T$ bin (GeV) | $n_\text{obs}$ | $b_\text{SM}$ | $\delta b$ |
|---|---|---|---|
| 320–500 | 1203 | 1243 | 160 |
| 500–1000 | 452 | 485 | 77 |
| 1000–3200 | 15 | 23.4 | 6.2 |

- extracted from CMS paper (1807.11421)'s Table 1 manually.
- comment: Since CMS did not directly release data on the HEPData website, only this coarse data was manually extracted from the paper (more detailed numbers in the paper would have to be digitized from the plots).


## 3.2 Simulated signal events

In this section, the expected signal events in each bin are calcualted.


### step 1: event selection

Read the reconstructed events from the simulation output and apply experiment-specific selection for the two runs:
- comment
  - Read LHCO files event-by-event (for LQ runs) or Delphes ROOT files via `uproot` (for EFT jet-matched runs which lack LHCO). The `find_event_file()` function searches for LHCO first, then falls back to ROOT.
  - Particle identification — **LHCO format**: 1=electron, 2=muon, 3=tau, 4=jet, 6=MET. **Delphes ROOT**: `Jet.TauTag=1` for taus, separate `Electron`/`Muon`/`MissingET` branches.
  - comment:`MT(particle)` in MA5 returns the jet mass from LHCO, NOT the ATLAS-style transverse mass. Must compute $m_T = \sqrt{2 p_T^\tau E_T^\text{miss}(1-\cos\Delta\phi)}$ directly from event-level data.



**ATLAS selection:**
- Lepton veto: no electrons or muons
- ≥1 hadronic tau with $p_T > 80$ GeV, $|\eta| < 2.3$
- $E_T^\text{miss} > 150$ GeV
- Compute $m_T = \sqrt{2\,p_T^\tau\,E_T^\text{miss}\,(1-\cos\Delta\phi)}$
- Require $m_T > 250$ GeV

**CMS selection:**
- Lepton veto: no electrons or muons
- ≥1 hadronic tau with $p_T > 80$ GeV, $|\eta| < 2.1$
- $E_T^\text{miss} > 200$ GeV
- $0.7 < p_T^\tau / E_T^\text{miss} < 1.3$
- $\Delta\phi(\tau, E_T^\text{miss}) > 2.4$ rad
- Require $m_T > 320$ GeV

### step 2: signal template construction

For events passing selection, histogram $m_T$ into the ATLAS (22 bins) or CMS (3 bins) bin edges. The signal template at coupling $g=1$ in each bin is:
$$s_i^{(g=1)} = \frac{N_i^\text{pass}}{N_\text{gen}} \times \sigma(g=1) \times \mathcal{L}$$
where
- $N_\text{gen}$ is the number of reconstructed events.
- $\sigma(g=1)$ is the cross section at coupling $g=1$
- $\mathcal{L}$ is the luminosity (36.1 fb⁻¹ for ATLAS, 35.9 fb⁻¹ for CMS).

At arbitrary coupling $g$, the signal scales as: $s_i(g) = g^4 \times s_i^{(g=1)}$.

## 3.3 Profile likelihood analysis

In this section, the standard profile likelihood analysis is performed to find the 2σ exclusion contour for the $U_1$ leptoquark.

For each experiment, the negative log-likelihood per bin is defined as:
$$-\ln L_i(\theta_i) = -\bigl[n_i \ln\mu_i - \mu_i\bigr] + \frac{1}{2}\frac{\theta_i^2}{(\delta_i/b_i)^2}$$
where:
- $n_i$: observed events in bin $i$ (from ATLAS/CMS data)
- $b_i$: expected SM background in bin $i$ (from ATLAS/CMS data)
- $\delta_i$: absolute systematic uncertainty on $b_i$ (from ATLAS/CMS data)
- $\theta_i$: nuisance parameter (independent per bin, profiled out)
- $s_i(g) = g^4 \times s_i^{(g=1)}$: signal expectation
- $\mu_i = b_i(1+\theta_i) + s_i$, with constraint $\mu_i > 0$.

### procedure to find the 2σ exclusion contour

For each leptoquark mass point, the exclusion contour can be obtained by performing the following steps.

**setp 1: profiling**

For each bin $i$ and coupling $g$, numerically minimize the negative log-likelihood $-\ln L_i(\theta_i)$ over $\theta_i$ to get the profile log-likelihood for each bin and coupling $g$. Then, sum the profile log-likelihoods for all bins to get the total profile log-likelihood. The profile log-likelihood is a function of the coupling $g$.
- comment: e.g., using bounded scalar minimization (scipy `minimize_scalar`) with constraint $\mu_i > 0$.

**step 2: combine ATLAS+CMS:**
Sum the profile log-likelihoods:
$$\ln\mathcal{L}_\text{comb}(g) = \ln\mathcal{L}_\text{ATLAS}(g) + \ln\mathcal{L}_\text{CMS}(g)$$

**step 3: extract exclusion region (2σ):**
1. Find best-fit coupling $\hat{g}$ that maximizes $\ln\mathcal{L}_\text{comb}(g)$
2. Find $g_\text{excl}$ such that $-2\bigl[\ln\mathcal{L}(g_\text{excl}) - \ln\mathcal{L}(\hat{g})\bigr] = 4.0$.
3. The exclusion region is the region satisfying the condition $-2\bigl[\ln\mathcal{L}(g) - \ln\mathcal{L}(\hat{g})\bigr] > 4.0$.

## 3.4 Plot Figure

The figure contains the following elements:

1. **Exclusion curve**
- style: solid black line
- exclusion curve obtained from section 3.3.
- The excluded region (above the curve up,  gray shading) should also be plotted.

2. **LH $R_{D^{(*)}}$ band**
- style: blue dashed line and light blue band
- The left-handed coupling values as a function of the leptoquark mass.
- The left-handed coupling is defined as $g_\text{LH}(M) = \frac{M}{v}\sqrt{2 V_{cb}\,\epsilon_L}$, with $\epsilon_L = 0.11 \pm 0.02$ and $v = 246$ GeV.

3. **RH $R_{D^{(*)}}$ band**
- style: red dashed line and light red band
- The right-handed coupling values as a function of the leptoquark mass.
- The right-handed coupling is defined as $g_\text{RH}(M) = \frac{M}{v}\sqrt{2 V_{cb}\,\tilde\epsilon_R}$, with $\tilde\epsilon_R = 0.48 \pm 0.06$ and $v = 246$ GeV.

### plot styles
- aspect ratio: 4:3
- x-axis
  - $M_{U_1}$ [TeV]
  - range: [0.8, 5.0]
- y-axis
  - range [0, 4.0]